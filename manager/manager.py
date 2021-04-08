import json
from rabbitmq.messaging import Messaging
from threading import Thread
import logging
import yaml

# class Polling(Thread):

class CSMF(Thread):
    def __init__(self, vsiId, vsiRequest):
        super().__init__()
        self.vsiId=vsiId
        # self.action=action
        self.vsiRequest=vsiRequest
        self.createVSI=True
        self.received={}
        self.messaging=Messaging()
        # self.messaging.consumeQueue("vsLCM_"+str(vsiId),self.vsCallback, ack=False)

        statusUpdate={"vsiId":self.vsiId, "status":"creating"}
        self.messaging.publish2Queue("vsCoordinator", json.dumps(statusUpdate))
        self.interdomainInfo={}

        #{uniqueComponentName:{sliceEnabled:true, domainId:ITAV, nfvoId:"ib234b2bib21"}}
        self.serviceComposition={}

    def vsCallback(self, channel, method_frame, header_frame, body):
        print(" [x] Received %r" % body)
        data=json.loads(body)
        th=Thread(target=self.processAction, args=[data])
        th.start()

    def processAction(self, data):
        if data["msgType"]=="modifyVSI":
            return
        elif data["msgType"]=="terminateVSI":
            return
        # else:
        #     self.received[data["msgType"]]=data
        #     if self.createVSI and "catalogueInfo" in self.received.keys() and "placementInfo" in self.received.keys() and "domainInfo" in self.received.keys() and "tenantInfo" in self.received.keys():
        #         self.createVSI()
        #     return

    def instantiateVSI(self):
        messaging=Messaging()

        domainInfo=self.received["domainInfo"]
        tenantInfo=self.received["tenantInfo"]
        catalogueInfo=self.received["catalogueInfo"]
        placementInfo=self.received["placementInfo"]

        if domainInfo["error"] or tenantInfo["error"] or catalogueInfo["error"] or placementInfo["error"]:
            statusUpdate={"vsiId":self.vsiId, "status":"failed","message":"Invalid Necessary Information. Error: " + "\nDomain error: "+domainInfo["message"] if domainInfo["error"] else "" + "\nTenant error: "+tenantInfo["message"] if tenantInfo["error"] else "" + "\nCatalogue error: "+catalogueInfo["message"] if catalogueInfo["error"] else "" + "\nPlacement error: "+placementInfo["message"] if placementInfo["error"] else "" }
            messaging.publish2Queue("vsCoordinator", json.dumps(statusUpdate))
            return

        placementData=placementInfo["data"]

        
        composingComponentId=1
        for creationData in placementData:
            componentName=self.vsiRequest["data"]["name"]+"_VSI-"+str(self.vsiId)+"_"+str(composingComponentId)
            if creationData["sliceEnabled"] and creationData["nstId"]!=None:
                message={"msgType":"instantiateNsi", "data":{"name":componentName,"domainId":creationData["domainId"],"nstId":creationData["nstId"]}}
                if "additionalConf" in self.vsiRequest["data"] and self.vsiRequest["data"]["additionalConf"]!="":
                    confStr=self.vsiRequest["data"]["additionalConf"]
                    if domainInfo["data"]["vs_blueprint_info"]["vs_blueprint"]["inter-site"]:
                        config=yaml.safe_load(confStr)
                        if "netslice-subnet" in config:
                            config["netslice-subnet"].append({'id':'interdomain-tunnel-peer','additionalParamsForVnf':[{'member-vnf-index': '1', 'additionalParams': {'vsi_id':str(self.vsiId),'tunnel_address': '10.0.0.'+str(composingComponentId)+'/24', 'tunnel_id': componentName}}]})
                        else:
                            config["netslice-subnet"]=[{'id':'interdomain-tunnel-peer','additionalParamsForVnf':[{'member-vnf-index': '1', 'additionalParams': {'vsi_id':str(self.vsiId),'tunnel_address': '10.0.0.'+str(composingComponentId)+'/24', 'tunnel_id': componentName}}]}]
                        confStr=yaml.safe_dump(config)
                    message["data"]["additionalConf"]=confStr
                else:
                    config={"netslice-subnet":[{'id':'interdomain-tunnel-peer','additionalParamsForVnf':[{'member-vnf-index': '1', 'additionalParams': {'vsi_id':str(self.vsiId),'tunnel_address': '10.0.0.'+str(composingComponentId)+'/24', 'tunnel_id': componentName}}]}]}
                    confStr=yaml.safe_dump(config)
                    message["data"]["additionalConf"]=confStr

            elif not creationData["sliceEnabled"] and creationData["nsdId"]!=None:
                message={"msgType":"instantiateNs", "data":{"name":componentName,"domainId":creationData["domainId"],"nsdId":creationData["nsdId"]}}
                if "additionalConf" in self.vsiRequest["data"] and self.vsiRequest["data"]["additionalConf"]!="":
                    confStr=self.vsiRequest["data"]["additionalConf"]
                    if domainInfo["data"]["vs_blueprint_info"]["vs_blueprint"]["inter-site"]:
                        config=yaml.safe_load(confStr)
                        if "additionalParamsForVnf" in config:
                            config["additionalParamsForVnf"].append({'member-vnf-index': '1', 'additionalParams': {'vsi_id':str(self.vsiId),'tunnel_address': '10.0.0.'+str(composingComponentId)+'/24', 'tunnel_id': componentName}})
                        else:
                            config["additionalParamsForVnf"]=[{'member-vnf-index': '1', 'additionalParams': {'vsi_id':str(self.vsiId),'tunnel_address': '10.0.0.'+str(composingComponentId)+'/24', 'tunnel_id': componentName}}]
                        confStr=yaml.safe_dump(config)
                    message["data"]["additionalConf"]=confStr
                else:
                    config={"additionalParamsForVnf":[{'member-vnf-index': '1', 'additionalParams': {'vsi_id':str(self.vsiId),'tunnel_address': '10.0.0.'+str(composingComponentId)+'/24', 'tunnel_id': componentName}}]}
                    confStr=yaml.safe_dump(config)
                    message["data"]["additionalConf"]=confStr
            self.serviceComposition[componentName]={"sliceEnabled":creationData["sliceEnabled"],"domainId":creationData["domainId"]}
            message["vsiId"]=str(self.vsiId)
            messaging.publish2Queue("vsDomain", json.dumps(message))
            composingComponentId+=1

        
        statusUpdate={"vsiId":self.vsiId, "status":"deploying"}
        messaging.publish2Queue("vsCoordinator", json.dumps(statusUpdate))

        self.createVSI=False
        return

    def newMessage(self, data):
        if data["msgType"]=="updateResourcesNfvoIds":
            nfvoId=data["data"]
            self.serviceComposition[nfvoId["componentName"]]["nfvoId"]=nfvoId["componentId"]
        else:
            self.received[data["msgType"]]=data
            if self.createVSI and "catalogueInfo" in self.received.keys() and "placementInfo" in self.received.keys() and "domainInfo" in self.received.keys() and "tenantInfo" in self.received.keys():
                self.instantiateVSI()

    def interdomainHandler(self,data):
        logging.info("Received interdomain info: {}".format(data))
        self.interdomainInfo[data["tunnelId"]]=data
        if len(self.interdomainInfo)==len(self.serviceComposition):
            for componentSend, infoSend in self.interdomainInfo.items():
                for componentReceive, infoReceive in self.interdomainInfo.items():
                    if componentSend!=componentReceive:
                        #TODO extend the actions option, standardize addpeer action
                        # if self.serviceComposition[componentReceive]["sliceEnabled"]:
                        #     message={"msgType":"actionNSI", "domainId":self.serviceComposition[componentReceive]["domainId"], "data":{"nsiId":self.serviceComposition[componentReceive]["nfvoId"], "vnfId":1,"action":"addpeer","params":{'peer_endpoint': infoSend["vnfIp"],'peer_key' : infoSend["publicKey"],'peer_network': "0.0.0.0/0"}}}
                        # else:
                        message={"msgType":"actionNs", "data":{"domainId":self.serviceComposition[componentReceive]["domainId"], "nsId":self.serviceComposition[componentReceive]["nfvoId"], "additionalConf":{"member_vnf_index":"1","primitive":"addpeer","primitive_params":{'peer_endpoint': infoSend["vnfIp"],'peer_key' : infoSend["publicKey"],'peer_network': "0.0.0.0/0"}}}}
                        logging.info("Sending interdomain addpeer action: {}".format(message))
                        self.messaging.publish2Queue("vsDomain", json.dumps(message))

    def run(self):
        print(' [*] Waiting for messages. To exit press CTRL+C')
        self.messaging.startConsuming()



csmfs={}

def newCSMF(data):
    csmf=CSMF(data["vsiId"], data)
    csmfs[data["vsiId"]]=csmf
    csmf.start()

def newCsmfMessage(data):
    vsiId=int(data["vsiId"])
    if vsiId in csmfs:
        csmfs[vsiId].newMessage(data)
    else:
        logging.warning("VSI Id not found: "+str(vsiId))

def newVnfInfo(data):
    vsiId=int(data["vsiId"])
    if vsiId in csmfs:
        csmfs[vsiId].interdomainHandler(data)
    else:
        logging.warning("VSI Id not found during newVnfInfo: "+str(vsiId))
        return {"error":True,"message": "Error: VSI Id not found during newVnfInfo: "+str(vsiId)}
    return {"error":False,"message": "Acknowledge"}