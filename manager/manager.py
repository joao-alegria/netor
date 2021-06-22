import json
from rabbitmq.messaging import Messaging
from threading import Thread
import logging
import yaml
import time
import requests
import redisHandler as redis

class Polling(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.runControl=True
        # self.vsiId=vsiId
        # self.composition=composition
        self.messaging=Messaging()
        self.vs={}

    def addVSI(self, vsiId, composition):
        print(vsiId)
        print(composition)
        self.vs[vsiId]=composition

    def removeVSI(self, vsiId):
        if vsiId in self.vs:
            del self.vs[vsiId]

    def stop(self):
        self.runControl=False

    def run(self):
        while self.runControl:
            time.sleep(60)
            if self.runControl:
                if len(self.vs)>0:
                    for vsiId, composition in self.vs.items():
                        for component, componentData in composition.items():
                            if componentData["sliceEnabled"]:
                                message={"vsiId":vsiId,"msgType":"getNsiInfo", "data":{"domainId":componentData["domainId"], "nsiId":component}}
                            else:
                                message={"vsiId":vsiId,"msgType":"getNsInfo", "data":{"domainId":componentData["domainId"], "nsId":component}}
                            logging.info("Polling action: {}".format(message))
                            self.messaging.publish2Queue("vsDomain", json.dumps(message))
        pass

class CSMF():
    def __init__(self, vsiId, vsiRequest, pollingThread):
        super().__init__()
        self.vsiId=vsiId
        self.interdomain=False
        redis.setKeyValue(vsiId,"vsiRequest",json.dumps(vsiRequest))
        self.pollingThread=pollingThread

        redis.setKeyValue("createVSI", vsiId, "create")
        redis.setKeyValue("interdomainTunnel", vsiId, "off")
        self.messaging=Messaging()
        # self.messaging.consumeQueue("managementQueue-vsLCM_"+str(vsiId), self.vsCallback, ack=False)

        statusUpdate={"msgType":"statusUpdate","data":{"vsiId":self.vsiId, "status":"creating", "message":"Created Management Function, waiting to receive all necessary information"}}
        self.messaging.publish2Queue("vsCoordinator", json.dumps(statusUpdate))

    # def vsCallback(self, channel, method_frame, header_frame, body):
    #     logging.info("Received Message {}".format(body))
    #     print(method_frame.exchange)
    #     data=json.loads(body)
    #     th=Thread(target=self.processAction, args=[data])
    #     th.start()

    def processAction(self, data):
        serviceComposition={}
        tmp=redis.getHashValue("serviceComposition", self.vsiId)
        if tmp!=None:
            serviceComposition=json.loads(tmp)


        if data["msgType"]=="nsInfo":
            statusUpdate={"msgType":"statusUpdate", "data":{"vsiId":self.vsiId, "status":data["data"]["nsInfo"]["operational-status"], "message":data["data"]["nsId"]+": "+data["data"]["nsInfo"]["detailed-status"]}}
            self.messaging.publish2Queue("vsCoordinator", json.dumps(statusUpdate))
            if "running" in data["data"]["nsInfo"]["operational-status"].lower():
                if serviceComposition=={}:
                    redis.setKeyValue("serviceComposition", self.vsiId,json.dumps({data["data"]["nsId"]:{"status":"instantiated"}}))
                else:
                    serviceComposition[data["data"]["nsId"]]["status"]="instantiated"
                    redis.setKeyValue("serviceComposition", self.vsiId,json.dumps(serviceComposition))

                tunnelActive=redis.getHashValue("interdomainTunnel",self.vsiId).decode("UTF-8")
                if self.interdomain and tunnelActive=="off":
                    primitiveData={"data":{"primitiveName":"getvnfinfo", "primitiveTarget":data["data"]["nsId"], "primitiveInternalTarget":"1"}}
                    self.processVsiPrimitive(primitiveData)
            elif "terminated" in data["data"]["nsiInfo"]["operational-status"].lower():
                self.tearDown(data["data"]["nsId"])
            return
        elif data["msgType"]=="nsiInfo":
            statusUpdate={"msgType":"statusUpdate", "data":{"vsiId":self.vsiId, "status":data["data"]["nsiInfo"]["operational-status"], "message":data["data"]["nsiId"]+": "+data["data"]["nsiInfo"]["detailed-status"]}}
            self.messaging.publish2Queue("vsCoordinator", json.dumps(statusUpdate))
            if "running" in data["data"]["nsiInfo"]["operational-status"].lower():
                if serviceComposition=={}:
                    redis.setKeyValue("serviceComposition", self.vsiId,json.dumps({data["data"]["nsiId"]:{"status":"instantiated"}}))
                else:
                    serviceComposition[data["data"]["nsiId"]]["status"]="instantiated"
                    redis.setKeyValue("serviceComposition", self.vsiId,json.dumps(serviceComposition))

                tunnelActive=redis.getHashValue("interdomainTunnel",self.vsiId).decode("UTF-8")
                if self.interdomain and tunnelActive=="off":
                    primitiveData={"data":{"primitiveName":"getvnfinfo", "primitiveTarget":data["data"]["nsiId"], "primitiveInternalTarget":"1"}}
                    self.processVsiPrimitive(primitiveData)
            elif "terminated" in data["data"]["nsiInfo"]["operational-status"].lower():
                self.tearDown(data["data"]["nsiId"])
            return
        elif data["msgType"]=="updateResourcesNfvoIds":
            nfvoData=data["data"]

            if serviceComposition=={}:
                redis.setKeyValue("serviceComposition", self.vsiId,json.dumps({nfvoData["componentName"]:{"nfvoId":nfvoData["componentId"]}}))
            else:
                serviceComposition[nfvoData["componentName"]]["nfvoId"]=nfvoData["componentId"]
                redis.setKeyValue("serviceComposition", self.vsiId,json.dumps(serviceComposition))

            return
        elif data["msgType"]=="primitive":
            self.processVsiPrimitive(data)
            return
        elif data["msgType"]=="terminate":
            return
        elif data["msgType"]=="modify":
            return
        elif data["msgType"]=="actionResponse":
            if data["data"]["primitiveName"]=="getvnfinfo":
                try:
                    vnfInfo=json.loads(data["data"]["output"])
                    self.interdomainHandler(vnfInfo)
                except Exception as e:
                    logging.error("Error after fetching Tunnel VNF info: "+str(e))
            return
        else:
            redis.setKeyValue(self.vsiId, data["msgType"],json.dumps(data))

            receivedData=[]
            for key in redis.getHashKeys(self.vsiId):
                receivedData.append(key.decode("UTF-8"))

            createVsi=redis.getHashValue("createVSI",self.vsiId).decode("UTF-8")

            if createVsi=="create" and set(["catalogueInfo","domainInfo","tenantInfo","placementInfo"]).issubset(receivedData):
                redis.setKeyValue("createVSI", self.vsiId, "alreadyCreated")
                self.instantiateVSI()
            return

    def instantiateVSI(self):
        print("INSTANTIATING")
        messaging=Messaging()

        allVsiData={}
        for key,value in redis.getEntireHash(self.vsiId).items():
            allVsiData[key.decode("UTF-8")]=json.loads(value)

        vsiRequest=allVsiData["vsiRequest"]
        domainInfo=allVsiData["domainInfo"]
        tenantInfo=allVsiData["tenantInfo"]
        catalogueInfo=allVsiData["catalogueInfo"]
        placementInfo=allVsiData["placementInfo"]

        #verify all information was received and there was no error
        if domainInfo["error"] or tenantInfo["error"] or catalogueInfo["error"] or placementInfo["error"]:
            statusUpdate={"msgType":"statusUpdate","data":{"vsiId":self.vsiId, "status":"failed","message":"Invalid Necessary Information. Error: " + "\nDomain error: "+domainInfo["message"] if domainInfo["error"] else "" + "\nTenant error: "+tenantInfo["message"] if tenantInfo["error"] else "" + "\nCatalogue error: "+catalogueInfo["message"] if catalogueInfo["error"] else "" + "\nPlacement error: "+placementInfo["message"] if placementInfo["error"] else "" }}
            messaging.publish2Queue("vsCoordinator", json.dumps(statusUpdate))
            return

        placementData=placementInfo["data"]

        domainPlacements={}
        if "domainPlacements" in vsiRequest["data"]:
            for placement in vsiRequest["data"]["domainPlacements"]:
                if placement["domainId"] in domainInfo["data"]:
                    domainPlacements[placement["componentName"]]=placement["domainId"]
        
        composingComponentId=1
        for creationData in placementData:
            #compute unique component id
            componentName=str(self.vsiId)+"_"+str(composingComponentId)+"-"+vsiRequest["data"]["name"]

            #in case the component is a slice
            if creationData["sliceEnabled"] and creationData["nstId"]!=None:
                domainId=creationData["domainId"]
                if componentName in domainPlacements:
                    domainId=domainPlacements[componentName]
                message={"msgType":"instantiateNsi", "data":{"name":componentName, "description":vsiRequest["data"]["description"],"domainId":domainId,"nstId":creationData["nstId"]}}
                if "additionalConf" in vsiRequest["data"] and vsiRequest["data"]["additionalConf"]!="":
                    componentConfigs=vsiRequest["data"]["additionalConf"]
                    if catalogueInfo["data"]["vs_blueprint_info"]["vs_blueprint"]["inter_site"]:
                        self.interdomain=True
                        config={}
                        for componentConf in componentConfigs:
                            if componentConf["componentName"]==componentName:
                                config=json.loads(componentConf["conf"])
                                break
                        if "netslice-subnet" in config:
                            configured=False
                            for subnet in config["netslice-subnet"]:
                                if subnet["id"]=="interdomain-tunnel-peer":
                                    if "additionalParamsForVnf" in subnet:
                                        internalConfigured=False
                                        for member in subnet['additionalParamsForVnf']:
                                            if member["member-vnf-index"]=="1":
                                                if 'additionalParams' in member:
                                                    member['additionalParams'].update({'vsi_id':str(self.vsiId),'tunnel_address': '10.100.100.'+str(composingComponentId)+'/24', 'tunnel_id': componentName})
                                                else:
                                                    member['additionalParams']={'vsi_id':str(self.vsiId),'tunnel_address': '10.100.100.'+str(composingComponentId)+'/24', 'tunnel_id': componentName}
                                                internalConfigured=True
                                                configured=True
                                                break
                                        if not internalConfigured:
                                            subnet['additionalParamsForVnf'].append({'member-vnf-index': '1', 'additionalParams': {'vsi_id':str(self.vsiId),'tunnel_address': '10.100.100.'+str(composingComponentId)+'/24', 'tunnel_id': componentName}})
                                            configured=True
                                    else:
                                        subnet['additionalParamsForVnf']=[{'member-vnf-index': '1', 'additionalParams': {'vsi_id':str(self.vsiId),'tunnel_address': '10.100.100.'+str(composingComponentId)+'/24', 'tunnel_id': componentName}}]
                                        configured=True
                                        break
                            if not configured:
                                config["netslice-subnet"].append({'id':'interdomain-tunnel-peer','additionalParamsForVnf':[{'member-vnf-index': '1', 'additionalParams': {'vsi_id':str(self.vsiId),'tunnel_address': '10.100.100.'+str(composingComponentId)+'/24', 'tunnel_id': componentName}}]})
                        else:
                            config["netslice-subnet"]=[{'id':'interdomain-tunnel-peer','additionalParamsForVnf':[{'member-vnf-index': '1', 'additionalParams': {'vsi_id':str(self.vsiId),'tunnel_address': '10.100.100.'+str(composingComponentId)+'/24', 'tunnel_id': componentName}}]}]
                        confStr=yaml.safe_dump(config)
                    message["data"]["additionalConf"]=confStr
                else:
                    if catalogueInfo["data"]["vs_blueprint_info"]["vs_blueprint"]["inter_site"]:
                        self.interdomain=True
                        config={"netslice-subnet":[{'id':'interdomain-tunnel-peer','additionalParamsForVnf':[{'member-vnf-index': '1', 'additionalParams': {'vsi_id':str(self.vsiId),'tunnel_address': '10.100.100.'+str(composingComponentId)+'/24', 'tunnel_id': componentName}}]}]}
                        confStr=yaml.safe_dump(config)
                        message["data"]["additionalConf"]=confStr

            #in case the component is a simple service
            elif not creationData["sliceEnabled"] and creationData["nsdId"]!=None:
                domainId=creationData["domainId"]
                if componentName in domainPlacements:
                    domainId=domainPlacements[componentName]
                message={"msgType":"instantiateNs", "data":{"name":componentName,"domainId":domainId,"nsdId":creationData["nsdId"]}}
                if "additionalConf" in vsiRequest["data"] and vsiRequest["data"]["additionalConf"]!="":
                    confStr=vsiRequest["data"]["additionalConf"]
                    if catalogueInfo["data"]["vs_blueprint_info"]["vs_blueprint"]["inter_site"]:
                        self.interdomain=True
                        config=yaml.safe_load(confStr)
                        if "additionalParamsForVnf" in config:
                            config["additionalParamsForVnf"].append({'member-vnf-index': '1', 'additionalParams': {'vsi_id':str(self.vsiId),'tunnel_address': '10.100.100.'+str(composingComponentId)+'/24', 'tunnel_id': componentName}})
                        else:
                            config["additionalParamsForVnf"]=[{'member-vnf-index': '1', 'additionalParams': {'vsi_id':str(self.vsiId),'tunnel_address': '10.100.100.'+str(composingComponentId)+'/24', 'tunnel_id': componentName}}]
                        confStr=yaml.safe_dump(config)
                    message["data"]["additionalConf"]=confStr
                else:
                    if catalogueInfo["data"]["vs_blueprint_info"]["vs_blueprint"]["inter_site"]:
                        self.interdomain=True
                        config={"additionalParamsForVnf":[{'member-vnf-index': '1', 'additionalParams': {'vsi_id':str(self.vsiId),'tunnel_address': '10.100.100.'+str(composingComponentId)+'/24', 'tunnel_id': componentName}}]}
                        confStr=yaml.safe_dump(config)
                        message["data"]["additionalConf"]=confStr

            serviceComposition=redis.getHashValue("serviceComposition", self.vsiId)
            if serviceComposition==None:
                serviceComposition={componentName:{"sliceEnabled":creationData["sliceEnabled"],"domainId":domainId, "status":"instantiating"}}
                redis.setKeyValue("serviceComposition", self.vsiId,json.dumps(serviceComposition))
            else:
                serviceComposition=json.loads(serviceComposition)
                serviceComposition[componentName]={"sliceEnabled":creationData["sliceEnabled"],"domainId":domainId,"status":"instantiating"}
                redis.setKeyValue("serviceComposition", self.vsiId,json.dumps(serviceComposition))
                
            message["vsiId"]=str(self.vsiId)
            messaging.publish2Queue("vsDomain", json.dumps(message))
            composingComponentId+=1

        
        statusUpdate={"msgType":"statusUpdate","data":{"vsiId":self.vsiId, "status":"deploying", "message":"Sent all instantiation requests to the appropriate domains"}}
        messaging.publish2Queue("vsCoordinator", json.dumps(statusUpdate))
        

        # self.pollingThread=Polling(self.vsiId, serviceComposition)
        # self.pollingThread.start()
        self.pollingThread.addVSI(self.vsiId, serviceComposition)
        return

    def processVsiPrimitive(self, data):
        createVsi=redis.getHashValue("createVSI",self.vsiId).decode("UTF-8")
        if createVsi=="alreadyCreated":

            allVsiData={}
            for key,value in redis.getEntireHash(self.vsiId).items():
                allVsiData[key.decode("UTF-8")]=json.loads(value)

            serviceComposition={}
            tmp=redis.getHashValue("serviceComposition", self.vsiId)
            if tmp!=None:
                serviceComposition=json.loads(tmp)

            catalogueInfo=allVsiData["catalogueInfo"]
            tmpActions=catalogueInfo["data"]["vsb_actions"]
            actions={}
            for action in tmpActions:
                actions[action["action_id"]]=action["parameters"]

            if data["data"]["primitiveName"] not in actions:
                statusUpdate={"msgType":"statusUpdate","data":{"vsiId":self.vsiId, "status":"Invalid Primitive", "message":"Primitive "+data["data"]["primitiveName"]+" is not defined in the VSB."}}
                self.messaging.publish2Queue("vsCoordinator", json.dumps(statusUpdate))
                return

            if data["data"]["primitiveTarget"] in serviceComposition:
                if serviceComposition[data["data"]["primitiveTarget"]]["sliceEnabled"]:
                    conf={"member_vnf_index":data["data"]["primitiveInternalTarget"],"primitive":data["data"]["primitiveName"],"primitive_params":{}}

                    for param in actions[data["data"]["primitiveName"]]:
                        if "parameter_default_value" in param:
                            if param["parameter_default_value"]!=None and param["parameter_default_value"]!="":
                                conf["primitive_params"][param["parameter_id"]]=param["parameter_default_value"]

                    if "primitiveParams" in data["data"]:
                        for param in data["data"]["primitiveParams"]:
                            conf["primitive_params"][param]=data["data"]["primitiveParams"][param]
                    
                    # message={"msgType":"actionNsi","vsiId":self.vsiId, "data":{"domainId":serviceComposition[data["data"]["primitiveTarget"]]["domainId"],"nsiId":data["data"]["primitiveTarget"], "additionalConf":conf}}

                    #TODO: processing with the Subnet NS Id because OSM currently doesn't support NSI actions
                    message={"msgType":"actionNs","vsiId":self.vsiId, "data":{"domainId":serviceComposition[data["data"]["primitiveTarget"]]["domainId"],"nsId":serviceComposition[data["data"]["primitiveTarget"]]["nfvoId"], "additionalConf":conf}}
                else:
                    conf={"member_vnf_index":data["data"]["primitiveInternalTarget"],"primitive":data["data"]["primitiveName"],"primitive_params":{}}

                    for param in actions[data["data"]["primitiveName"]]:
                        if "parameter_default_value" in param:
                            if param["parameter_default_value"]!=None and param["parameter_default_value"]!="":
                                conf["primitive_params"][param["parameter_id"]]=param["parameter_default_value"]

                    if "primitiveParams" in data["data"]:
                        for param in data["data"]["primitiveParams"]:
                            conf["primitive_params"][param]=data["data"]["primitiveParams"][param]
                        
                    message={"msgType":"actionNs","vsiId":self.vsiId, "data":{"domainId":serviceComposition[data["data"]["primitiveTarget"]]["domainId"],"nsId":data["data"]["primitiveTarget"], "additionalConf":conf}}
            message["data"]["primitiveName"]=data["data"]["primitiveName"]
            self.messaging.publish2Queue("vsDomain", json.dumps(message))
        else:
            statusUpdate={"msgType":"statusUpdate","data":{"vsiId":self.vsiId, "status":"Invalid Primitive Trigger", "message":"Triggered primitive before VSI deployment finalized."}}
            self.messaging.publish2Queue("vsCoordinator", json.dumps(statusUpdate))

    def interdomainHandler(self,data):
        logging.info("Processing interdomain info: {}".format(data))

        serviceComposition={}
        tmp=redis.getHashValue("serviceComposition", self.vsiId)
        if tmp!=None:
            serviceComposition=json.loads(tmp)

        interdomainInfo=redis.getHashValue("interdomainInfo", self.vsiId)
        if interdomainInfo==None:
            interdomainInfo={data["tunnelId"]:data}
            redis.setKeyValue("interdomainInfo", self.vsiId,json.dumps(interdomainInfo))
        else:
            interdomainInfo=json.loads(interdomainInfo)
            interdomainInfo[data["tunnelId"]]=data
            redis.setKeyValue("interdomainInfo", self.vsiId,json.dumps(interdomainInfo))

        interdomainInfo[data["tunnelId"]]=data
        if len(interdomainInfo)==len(serviceComposition):
            tunnelActive=redis.getHashValue("interdomainTunnel",self.vsiId).decode("UTF-8")
            if tunnelActive=="off":

                redis.setKeyValue("interdomainTunnel", self.vsiId, "on")

                allVsiData={}
                for key,value in redis.getEntireHash(self.vsiId).items():
                    allVsiData[key.decode("UTF-8")]=json.loads(value)

                catalogueInfo=allVsiData["catalogueInfo"]
                tmpActions=catalogueInfo["data"]["vsb_actions"]
                actions={}
                for action in tmpActions:
                    actions[action["action_id"]]=action["parameters"]

                if "addpeer" not in actions:
                    statusUpdate={"msgType":"statusUpdate","data":{"vsiId":self.vsiId, "status":"Invalid Primitive", "message":"addpeer primitive not present in the blueprint."}}
                    self.messaging.publish2Queue("vsCoordinator", json.dumps(statusUpdate))
                    return

                for componentSend, infoSend in interdomainInfo.items():
                    for componentReceive, infoReceive in interdomainInfo.items():
                        if componentSend!=componentReceive:
                            if serviceComposition[componentReceive]["sliceEnabled"]:
                                #processed like a NS because OSM currently doesn't support NSI actions
                                conf={"member_vnf_index":"1","primitive":"addpeer","primitive_params":{'peer_endpoint': infoSend["vnfIp"],'peer_key' : infoSend["publicKey"]}}
                                for param in actions["addpeer"]:
                                    if "parameter_default_value" in param:
                                        if param["parameter_default_value"]!=None and param["parameter_default_value"]!="":
                                            conf["primitive_params"][param["parameter_id"]]=param["parameter_default_value"]

                                message={"msgType":"actionNs", "data":{"primitiveName":"addpeer","domainId":serviceComposition[componentReceive]["domainId"], "nsId":serviceComposition[componentReceive]["nfvoId"], "additionalConf":conf}}
                            else:
                                conf={"member_vnf_index":"1","primitive":"addpeer","primitive_params":{'peer_endpoint': infoSend["vnfIp"],'peer_key' : infoSend["publicKey"]}}
                                for param in actions["addpeer"]:
                                    if "parameter_default_value" in param:
                                        if param["parameter_default_value"]!=None and param["parameter_default_value"]!="":
                                            conf["primitive_params"][param["parameter_id"]]=param["parameter_default_value"]

                                message={"msgType":"actionNs", "data":{"primitiveName":"addpeer","domainId":serviceComposition[componentReceive]["domainId"], "nsId":serviceComposition[componentReceive]["nfvoId"], "additionalConf":conf}}

                            logging.info("Sending interdomain addpeer action: {}".format(message))
                            self.messaging.publish2Queue("vsDomain", json.dumps(message))


                requests.post("http://192.168.0.100:9999/stopTimer/1", data={"timestamp":str(round(time.time()*1000))})

    def deleteVsi(self, force=False):
        serviceComposition={}
        tmp=redis.getHashValue("serviceComposition", self.vsiId)
        if tmp!=None:
            serviceComposition=json.loads(tmp)

        for component, componentData in serviceComposition.items():
            serviceComposition[component]["status"]="terminating"
            if componentData["sliceEnabled"]:
                message={"vsiId":self.vsiId,"msgType":"deleteNsi", "data":{"domainId":componentData["domainId"], "nsiId":component}}
            else:
                message={"vsiId":self.vsiId,"msgType":"deleteNs", "data":{"domainId":componentData["domainId"], "nsId":component}}
            self.messaging.publish2Queue("vsDomain", json.dumps(message))

        redis.setKeyValue("serviceComposition", self.vsiId,json.dumps(serviceComposition))

        statusUpdate={"msgType":"statusUpdate","data":{"vsiId":self.vsiId, "status":"terminating", "message":"Terminating Vertical Service Instance."}}
        self.messaging.publish2Queue("vsCoordinator", json.dumps(statusUpdate))

        if serviceComposition=={} or force:
            if force:
                self.tearDown(None, force=force)
            else:
                self.tearDown(None)


    def tearDown(self, componentName, force=False):
        serviceComposition={}
        tmp=redis.getHashValue("serviceComposition", self.vsiId)
        if tmp!=None:
            serviceComposition=json.loads(tmp)

        if componentName in serviceComposition:
            serviceComposition[componentName]["status"]="terminated"
            redis.setKeyValue("serviceComposition", self.vsiId,json.dumps(serviceComposition))

        terminated=True
        for component in serviceComposition:
            terminated = terminated and serviceComposition[component]["status"]=="terminated"

        if terminated or force:
            logging.info("Tearing down CSMF of VSI "+str(self.vsiId))
            self.pollingThread.removeVSI(self.vsiId)
            redis.deleteKey(self.vsiId)
            redis.deleteHash("serviceComposition",self.vsiId)
            redis.deleteHash("interdomainInfo",self.vsiId)
            redis.deleteHash("createVSI",self.vsiId)
            redis.deleteHash("interdomainTunnel",self.vsiId)

            statusUpdate={"msgType":"statusUpdate","data":{"vsiId":self.vsiId, "status":"terminated","message":"Vertical Service Instance Terminated."}}
            self.messaging.publish2Queue("vsCoordinator", json.dumps(statusUpdate))

            # requests.post("http://192.168.0.100:9999/stopTimer/2", data={"timestamp":str(round(time.time()*1000))})
        
        # self.stop()


    # def stop(self):
    #     try:
    #         self.messaging.stopConsuming()
    #     except Exception as e:
    #         logging.error("Pika exception: "+str(e))

    # def run(self):
    #     try:
    #         logging.info('Started Consuming RabbitMQ Topics')
    #         self.messaging.startConsuming()
    #     except Exception as e:
    #         logging.info("VSI "+str(self.vsiId)+" CSMF Ended")
    #         logging.error("Pika exception: "+str(e))    