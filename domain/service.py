import db.persistance as persistance
from flask import jsonify
import db.schemas as schemas
from threading import Thread
import driver.osm as osm
import json
from rabbitmq.adaptor import Messaging
import logging


def createDomain(data):
    schema=schemas.DomainSchema()
    if "domainAgreement" in data:
        agreements=data["domainAgreement"]
    if "ownedLayers" in data:
        layers=data["ownedLayers"]
        for layer in layers:
            if layer["domainLayerType"]=="OSM_NSP":
                osmSchema=schemas.OsmDomainLayerSchema()
                domainLayer=osmSchema.load(layer, session=persistance.DB.session)
                persistance.DB.persist(domainLayer)

    domain=schema.load(data, session=persistance.DB.session)
    persistance.DB.persist(domain)
    return

def getAllDomains():
    schema=schemas.DomainSchema()
    domains=persistance.DB.session.query(persistance.Domain).all()
    domainsDict=[]
    for domain in domains:
        domainsDict.append(schema.dump(domain))
    return domainsDict

def getDomainsIds():
    domains=[domainId for domainId, in persistance.DB.session.query(persistance.Domain.domainId).all()]
    return domains

def getDomain(domainId):
    schema=schemas.DomainSchema()
    domain=persistance.DB.session.query(persistance.Domain).filter(persistance.Domain.domainId==domainId).first()
    return schema.dump(domain)

def getOsmDomain(domainLayerId):
    schema=schemas.OsmDomainLayerSchema()
    osm_domain=persistance.DB.session.query(persistance.OsmDomainLayer).filter(persistance.OsmDomainLayer.domainLayerId==domainLayerId).first()
    return schema.dump(osm_domain)

def updateDomain(domainId):
    domain=persistance.DB.session.query(persistance.Domain).filter(persistance.Domain.domainId==domainId).first()
    #update Domain
    return

def removeDomain(domainId):
    domain=persistance.DB.session.query(persistance.Domain).filter(persistance.Domain.domainId==domainId).first()
    persistance.DB.delete(domain)
    return



class DomainActionHandler(Thread):
    def __init__(self, data):
        Thread.__init__(self)
        self.data=data
        self.messaging=Messaging()

    def getDomainInfo(self, domainId):
        domain=persistance.DB.session.query(persistance.Domain).filter(persistance.Domain.domainId==self.data["data"]["domainId"]).first()
        domainLayer=domain.ownedLayers[0]

        driver=None
        if domainLayer.domainLayerType=="OSM_NSP":
            driver=osm
        return domain, domainLayer, driver


    def run(self):
        messaging=Messaging()
        try:
            if self.data["msgType"] == "instantiateNs":
                domain, domainLayer, driver=self.getDomainInfo(self.data["data"]["domainId"])
                nsId=driver.instantiateNS(domain.url, self.data["data"]["name"], self.data["data"]["nsdId"], domainLayer.vimAccount,self.data["data"]["additionalConf"] if "additionalConf" in self.data["data"] else None)
                # messaging.publish2Exchange("vsLCM_"+str(self.data["vsiId"]), json.dumps({"msgType":"updateResourcesNfvoIds","vsiId":self.data["vsiId"],"error":False, "message":"Sending Resource's Components Ids", "data":{"componentName":self.data["data"]["name"],"componentId":nsId}}))
                messaging.publish2Exchange("vsLCM_Management", json.dumps({"msgType":"updateResourcesNfvoIds","vsiId":self.data["vsiId"],"error":False, "message":"Sending Resource's Components Ids", "data":{"componentName":self.data["data"]["name"],"componentId":nsId}}))
                return
            elif self.data["msgType"] == "instantiateNsi":
                domain, domainLayer, driver=self.getDomainInfo(self.data["data"]["domainId"])
                nsiId=driver.instantiateNSI(domain.url, self.data["data"]["name"], self.data["data"]["nstId"], domainLayer.vimAccount,self.data["data"]["additionalConf"] if "additionalConf" in self.data["data"] else None)
                nsiInfo=osm.getNSI(domain.url, self.data["data"]["name"])["_admin"]["nsrs-detailed-list"]

                nssNsrId={}
                tunnelServiceId=None
                for nss in nsiInfo:
                    if nss["nss-id"]=="interdomain-tunnel-peer":
                        tunnelServiceId=nss["nsrId"]
                    nssNsrId[nss["nss-id"]]=nss["nsrId"]

                # messaging.publish2Exchange("vsLCM_"+str(self.data["vsiId"]), json.dumps({"msgType":"updateResourcesNfvoIds","vsiId":self.data["vsiId"],"error":False, "message":"Sending Resource's Components Ids", "data":{"componentName":self.data["data"]["name"],"componentId":tunnelServiceId, "additionalData":nssNsrId}}))
                messaging.publish2Exchange("vsLCM_Management", json.dumps({"msgType":"updateResourcesNfvoIds","vsiId":self.data["vsiId"],"error":False, "message":"Sending Resource's Components Ids", "data":{"componentName":self.data["data"]["name"],"componentId":tunnelServiceId, "additionalData":nssNsrId}}))
                return
            elif self.data["msgType"] == "deleteNs":
                domain, domainLayer, driver=self.getDomainInfo(self.data["data"]["domainId"])
                driver.terminateNS(domain.url, self.data["data"]["nsId"])
                return
            elif self.data["msgType"] == "deleteNsi":
                domain, domainLayer, driver=self.getDomainInfo(self.data["data"]["domainId"])
                driver.terminateNSI(domain.url, self.data["data"]["nsiId"])
                return
            elif self.data["msgType"] == "actionNs":
                domain, domainLayer, driver=self.getDomainInfo(self.data["data"]["domainId"])
                result=driver.sendActionNS(domain.url, self.data["data"]["nsId"], additionalConf=self.data["data"]["additionalConf"])
                actionResult={"msgType": "actionResponse", "message":"Returning NS action result","vsiId":self.data["vsiId"], "data":{"primitiveName":self.data["data"]["primitiveName"],"status":result["operationState"], "output":result["detailed-status"]["output"]}}
                # messaging.publish2Exchange("vsLCM_"+str(self.data["vsiId"]), json.dumps(actionResult))
                messaging.publish2Exchange("vsLCM_Management", json.dumps(actionResult))
                return
            elif self.data["msgType"] == "actionNsi":
                domain, domainLayer, driver=self.getDomainInfo(self.data["data"]["domainId"])
                result=driver.sendActionNSI(domain.url, self.data["data"]["nsiId"], additionalConf=self.data["data"]["additionalConf"])
                actionResult={"msgType": "actionResponse", "message":"Returning NSI action result","vsiId":self.data["vsiId"], "data":{"primitiveName":self.data["data"]["primitiveName"],"status":result["operationState"], "output":result["detailed-status"]["output"]}}
                # messaging.publish2Exchange("vsLCM_"+str(self.data["vsiId"]), json.dumps(actionResult))
                messaging.publish2Exchange("vsLCM_Management", json.dumps(actionResult))
                return
            elif self.data["msgType"] == "getNsInfo":
                domain, domainLayer, driver=self.getDomainInfo(self.data["data"]["domainId"])
                nsInfo=driver.getNS(domain.url, self.data["data"]["nsId"])
                messaging.publish2Exchange("vsLCM_"+str(self.data["vsiId"]), json.dumps({"msgType":"nsInfo","vsiId":self.data["vsiId"],"error":False, "message":"Sending NS "+self.data["data"]["nsId"]+" Info", "data":{"nsId":self.data["data"]["nsId"],"nsInfo":nsInfo}}))
                return
            elif self.data["msgType"] == "getNsiInfo":
                domain, domainLayer, driver=self.getDomainInfo(self.data["data"]["domainId"])
                nsiInfo=driver.getNSI(domain.url, self.data["data"]["nsiId"])
                # messaging.publish2Exchange("vsLCM_"+str(self.data["vsiId"]), json.dumps({"msgType":"nsiInfo","vsiId":self.data["vsiId"],"vsiId":self.data["vsiId"],"error":False, "message":"Sending NSI "+self.data["data"]["nsiId"]+" Info", "data":{"nsiId":self.data["data"]["nsiId"],"nsiInfo":nsiInfo}}))
                messaging.publish2Exchange("vsLCM_Management", json.dumps({"msgType":"nsiInfo","vsiId":self.data["vsiId"],"vsiId":self.data["vsiId"],"error":False, "message":"Sending NSI "+self.data["data"]["nsiId"]+" Info", "data":{"nsiId":self.data["data"]["nsiId"],"nsiInfo":nsiInfo}}))
                return
        except Exception as e:
            logging.info("Error while performing action '"+self.data["msgType"]+"' in domain '"+str(self.data["data"]["domainId"])+"': "+str(e))
            return