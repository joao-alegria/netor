from threading import Thread
from rabbitmq.messaging import Messaging
import json
import logging
import redisHandler as redis

class Arbitrator(Thread):

    def __init__(self, vsiId, info):
        super().__init__()
        self.vsiId=vsiId
        self.info=info
        # self.createVSI=True
        # self.received={}
        redis.setKeyValue("createVSI",vsiId, "create")
        self.messaging=Messaging()
        self.messaging.consumeQueue("placementQueue-vsLCM_"+str(vsiId), self.vsCallback, ack=False)

    def vsCallback(self, channel, method_frame, header_frame, body):
        logging.info("Received Message {}".format(body))
        data=json.loads(body)
        th=Thread(target=self.processAction, args=[data])
        th.start()

    def processAction(self, data):
        if data["msgType"]=="modifyVSI":
            return
        else:
            # self.received[data["msgType"]]=data
            # if self.createVSI and "catalogueInfo" in self.received.keys() and "domainInfo" in self.received.keys() and "tenantInfo" in self.received.keys():
            #     self.processEntitiesPlacement()
            redis.setKeyValue(self.vsiId, data["msgType"],json.dumps(data))

            receivedData=[]
            for key in redis.getHashKeys(self.vsiId):
                receivedData.append(key.decode("UTF-8"))

            createVsi=redis.getHashValue("createVSI",self.vsiId).decode("UTF-8")

            if createVsi=="create" and set(["catalogueInfo","domainInfo","tenantInfo"]).issubset(receivedData):
                redis.setKeyValue("createVSI", self.vsiId, "alreadyCreated")
                self.processEntitiesPlacement()
            return

    def translateVSD(self, catalogueInfo):
        qosParamsInfo=catalogueInfo["vs_blueprint_info"]["vs_blueprint"]["parameters"]
        qosParams={}
        for parameter in qosParamsInfo:
            if parameter["parameter_type"]!="number":
                logging.error("Parameter type unsupported: "+parameter["parameter_type"])
                return None
            qosParams[parameter["parameter_id"]]=parameter["parameter_type"]

        translationRules=catalogueInfo["vs_blueprint_info"]["vs_blueprint"]["translation_rules"]
        qosValues=catalogueInfo["vsd"]["qos_parameters"]

        translation=[]
        domainId=catalogueInfo["vsd"]["domain_id"]
        for rule in translationRules:
            validRule=True
            for inputRange in rule["input"]:
                if not validRule:
                    break
                if qosParams[inputRange["parameter_id"]] == "number":
                    if not (inputRange["max_value"]>int(qosValues[inputRange["parameter_id"]]) and inputRange["min_value"]<int(qosValues[inputRange["parameter_id"]])):
                        validRule=False
            if validRule:
                if "nst_id" in rule and rule["nst_id"]!="":
                    nstId=rule["nst_id"]

                    externalNST=True
                    for nst in catalogueInfo["nsts"]:
                        if nst["nst_id"]==nstId:
                            externalNST=False
                            if len(nst["nsst"])>0:
                                for nsstId in nst["nsst_ids"]:
                                    externalNSST=True
                                    for nsst in nst["nsst"]:
                                        if nsst["nst_id"]==nsstId:
                                            externalNSST=False
                                            translation.append({"domainId":domainId,"sliceEnabled":False,"nsdId":nsst["nsd_id"]})
                                            break
                                    if externalNSST:
                                        translation.append({"domainId":domainId,"sliceEnabled":True,"nstId":nstId})
                            else:
                                translation.append({"domainId":domainId,"sliceEnabled":True,"nsdId":nst["nsd_id"]})
                    if externalNST:
                        translation.append({"domainId":domainId,"sliceEnabled":True,"nstId":nstId})

                elif "nsd_id" in rule and rule["nsd_id"]!="":
                    translation.append({"domainId":domainId,"sliceEnabled":False,"nsdId":rule["nsd_id"]})
        
        return translation


    def processEntitiesPlacement(self):
        allVsiData={}
        for key,value in redis.getEntireHash(self.vsiId).items():
            allVsiData[key.decode("UTF-8")]=json.loads(value)

        domainInfo=allVsiData["domainInfo"]
        tenantInfo=allVsiData["tenantInfo"]
        catalogueInfo=allVsiData["catalogueInfo"]

        if domainInfo["error"] or tenantInfo["error"] or catalogueInfo["error"]:
            message={"vsiId":domainInfo["vsiId"],"msgType":"placementInfo","error":True, "message":"Invalid Necessary Information. Error: " + "\nDomain error: "+domainInfo["message"] if domainInfo["error"] else "" + "\nTenant error: "+tenantInfo["message"] if tenantInfo["error"] else "" + "\nCatalogue error: "+catalogueInfo["message"] if catalogueInfo["error"] else "" }
            self.messaging.publish2Exchange("vsLCM_"+str(self.vsiId), json.dumps(message))
            return

        translation=self.translateVSD(catalogueInfo["data"])
        for component in translation:
            if component["domainId"] not in domainInfo["data"]:
                message={"msgType":"placementInfo","error":True, "message":"Invalid Domain Id. Identifier "+component["domainId"]+" not present in the onboarded domains" }
                self.messaging.publish2Exchange("vsLCM_"+str(self.vsiId), json.dumps(message))
                return

        #user defined domains in instantiation

        message={"vsiId":self.vsiId,"msgType":"placementInfo", "error":False, "message":"Success", "data":translation}
        self.messaging.publish2Exchange("vsLCM_"+str(self.vsiId), json.dumps(message))
        return

    # def newMessage(self, data):
    #     self.received[data["msgType"]]=data
    #     if self.createVSI and "catalogueInfo" in self.received.keys() and "domainInfo" in self.received.keys() and "tenantInfo" in self.received.keys():
    #         self.processEntitiesPlacement()
    #     return

    def tearDown(self):
        logging.info("Tearing down Arbitrator of VSI "+str(self.vsiId))
        redis.deleteKey(self.vsiId)
        redis.deleteHash("createVSI",self.vsiId)
        self.stop()

    def stop(self):
        try:
            self.messaging.stopConsuming()
        except Exception as e:
            logging.error("Pika exception: "+str(e))

    def run(self):
        try:
            logging.info('Started Consuming RabbitMQ Topics')
            self.messaging.startConsuming()
        except Exception as e:
            logging.info("VSI "+str(self.vsiId)+" Arbitrator Ended")
            logging.error("Pika exception: "+str(e))

arbitrators={}

def newArbitrator(data):
    arbitrator=Arbitrator(data["vsiId"], data)
    arbitrators[data["vsiId"]]=arbitrator
    arbitrator.start()

def tearDownArbitrator(data):
    vsiId=str(data["vsiId"])
    if vsiId in arbitrators:
        arbitrators[vsiId].tearDown()
        del arbitrators[vsiId]
    else:
        logging.info("VSI Id not found during tearDown: "+str(vsiId))