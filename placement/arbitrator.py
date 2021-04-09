from threading import Thread
from rabbitmq.messaging import Messaging
import json
import logging

class Arbitrator(Thread):

    def __init__(self, vsiId, info):
        super().__init__()
        self.vsiId=vsiId
        self.info=info
        self.createVSI=True
        self.received={}
        self.messaging=Messaging()
        # self.messaging.consumeQueue("vsLCM_"+str(vsiId),self.vsCallback, ack=False)

    def vsCallback(self, channel, method_frame, header_frame, body):
        logging.info("Received Message {}".format(body))
        data=json.loads(body)
        th=Thread(target=self.processAction, args=[data])
        th.start()

    def processAction(self, data):
        if data["msgType"]=="modifyVSI":
            return
        # else:
        #     self.received[data["msgType"]]=data
        #     if self.createVSI and "catalogueInfo" in self.received.keys() and "domainInfo" in self.received.keys() and "tenantInfo" in self.received.keys():
        #         self.processEntitiesPlacement()
        #     return

    def translateVSD(self):
        catalogueInfo=self.received["catalogueInfo"]["data"]
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
                            if len(nst["nsst_ids"])>0:
                                for nsstId in nst["nsst_ids"]:
                                    externalNSST=True
                                    for nsst in catalogueInfo["nsts"]:
                                        if nsst["nst_id"]==nsstId:
                                            externalNSST=False
                                            translation.append({"domainId":domainId,"sliceEnabled":False,"nsdId":nsst["nsd_id"]})
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
        # message={"msgType":"placementInfo", "data":{"nsId":"72f9e7d3-41d1-4dab-b6ae-bd1ee514bd93", "domainId":"osm"}}
        # messaging.publish2Queue("vsLCM_"+str(self.vsiId), json.dumps(message))
        self.createVSI=False
        domainInfo=self.received["domainInfo"]
        tenantInfo=self.received["tenantInfo"]
        catalogueInfo=self.received["catalogueInfo"]

        if domainInfo["error"] or tenantInfo["error"] or catalogueInfo["error"]:
            message={"vsiId":domainInfo["vsiId"],"msgType":"placementInfo","error":True, "message":"Invalid Necessary Information. Error: " + "\nDomain error: "+domainInfo["message"] if domainInfo["error"] else "" + "\nTenant error: "+tenantInfo["message"] if tenantInfo["error"] else "" + "\nCatalogue error: "+catalogueInfo["message"] if catalogueInfo["error"] else "" }
            self.messaging.publish2Exchange("vsLCM_Management", json.dumps(message))
            return

        translation=self.translateVSD()
        for component in translation:
            if component["domainId"] not in domainInfo["data"]:
                message={"msgType":"placementInfo","error":True, "message":"Invalid Domain Id. Identifier "+component["domainId"]+" not present in the onboarded domains" }
                self.messaging.publish2Exchange("vsLCM_Management", json.dumps(message))
                return

        #arbitrate the domains (see if user defined domains in instantiation)

        message={"vsiId":self.vsiId,"msgType":"placementInfo", "error":False, "message":"Success", "data":translation}
        self.messaging.publish2Exchange("vsLCM_Management", json.dumps(message))
        return

    def newMessage(self, data):
        self.received[data["msgType"]]=data
        if self.createVSI and "catalogueInfo" in self.received.keys() and "domainInfo" in self.received.keys() and "tenantInfo" in self.received.keys():
            self.processEntitiesPlacement()
        return

    def run(self):
        logging.info('Started Consuming RabbitMQ Topics')
        self.messaging.startConsuming()