import db.persistance as persistance
from flask import jsonify
import db.schemas as schemas
from threading import Thread
import driver.osm as osm
import json
from rabbitmq.adaptor import Messaging
import logging


def createDomain():
    return ""

def getAllDomains():
    schema=schemas.DomainSchema()
    domains=persistance.session.query(persistance.Domain).all()
    domainsDict=[]
    for domain in domains:
        domainsDict.append(schema.dump(domain))
    return domainsDict

def getDomainsIds():
    domains=[domainId for domainId, in persistance.session.query(persistance.Domain.domainId).all()]
    return domains

def getDomain(domainId):
    schema=schemas.DomainSchema()
    domain=persistance.session.query(persistance.Domain).filter(persistance.Domain.domainId==domainId).first()
    return schema.dump(domain)

def updateDomain(domainId):
    domain=persistance.session.query(persistance.Domain).filter(persistance.Domain.domainId==domainId).first()
    #update Domain
    message={"msg":"Success"}
    return message

def removeDomain(domainId):
    domain=persistance.session.query(persistance.Domain).filter(persistance.Domain.domainId==domainId).first()
    persistance.delete(domain)
    message={"msg":"Success"}
    return message



class DomainActionHandler(Thread):
    def __init__(self, data):
        Thread.__init__(self)
        self.data=data

    def run(self):
        messaging=Messaging()
        try:
            if self.data["msgType"] == "instantiateNs":
                domain=persistance.session.query(persistance.Domain).filter(persistance.Domain.domainId==self.data["data"]["domainId"]).first()
                domainLayer=domain.ownedLayers[0]
                nsId=osm.instantiateNS(domain.url, self.data["data"]["name"], self.data["data"]["nsdId"], domainLayer.vimAccount,self.data["data"]["additionalConf"] if "additionalConf" in self.data["data"] else None)
                messaging.publish2Exchange("vsLCM_Management", json.dumps({"msgType":"updateResourcesNfvoIds","vsiId":self.data["vsiId"],"error":False, "message":"Sending Resource's Components Ids", "data":{"componentName":self.data["data"]["name"],"componentId":nsId}}))
                return
            elif self.data["msgType"] == "instantiateNsi":
                domain=persistance.session.query(persistance.Domain).filter(persistance.Domain.domainId==self.data["data"]["domainId"]).first()
                domainLayer=domain.ownedLayers[0]
                nsiId=osm.instantiateNSI(domain.url, self.data["data"]["name"], self.data["data"]["nstId"], domainLayer.vimAccount,self.data["data"]["additionalConf"] if "additionalConf" in self.data["data"] else None)
                nsiInfo=osm.getNSI(domain.url, nsiId)["_admin"]["nsrs-detailed-list"]

                nssNsrId={}
                tunnelServiceId=None
                for nss in nsiInfo:
                    if nss["nss-id"]=="interdomain-tunnel-peer":
                        tunnelServiceId=nss["nsrId"]
                    nssNsrId[nss["nss-id"]]=nss["nsrId"]

                messaging.publish2Exchange("vsLCM_Management", json.dumps({"msgType":"updateResourcesNfvoIds","vsiId":self.data["vsiId"],"error":False, "message":"Sending Resource's Components Ids", "data":{"componentName":self.data["data"]["name"],"componentId":tunnelServiceId, "additionalData":nssNsrId}}))
                return
            elif self.data["msgType"] == "deleteNs":
                return
            elif self.data["msgType"] == "deleteNsi":
                return
            elif self.data["msgType"] == "actionNs":
                domain=persistance.session.query(persistance.Domain).filter(persistance.Domain.domainId==self.data["data"]["domainId"]).first()
                osm.sendActionNS(domain.url, self.data["data"]["nsId"], additionalConf=self.data["data"]["additionalConf"])
                return
            elif self.data["msgType"] == "actionNsi":
                return
        except Exception as e:
            logging.info("Error while performing action '"+self.data["msgType"]+"' in domain '"+str(self.data["data"]["domainId"])+"': "+str(e))
            return