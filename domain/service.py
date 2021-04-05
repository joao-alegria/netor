import db.persistance as persistance
from flask import jsonify
import db.schemas as schemas

def createDomain():
    return ""

def getAllDomains():
    schema=schemas.DomainSchema()
    domains=persistance.session.query(persistance.Domain).all()
    domainsDict=[]
    for domain in domains:
        domainsDict.append(schema.dump(domain))
    return domainsDict

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