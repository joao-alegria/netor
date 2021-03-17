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
    return jsonify(domainsDict),200

def getDomain(domainId):
    schema=schemas.DomainSchema()
    domain=persistance.session.query(persistance.Domain).filter(persistance.Domain.domainId==domainId).first()
    return jsonify(schema.dump(domain)),200


def updateDomain(domainId):
    domain=persistance.session.query(persistance.Domain).filter(persistance.Domain.domainId==domainId).first()
    #update Domain
    message={"msg":"Success"}
    return jsonify(message),200

def removeDomain(domainId):
    domain=persistance.session.query(persistance.Domain).filter(persistance.Domain.domainId==domainId).first()
    persistance.delete(domain)
    message={"msg":"Success"}
    return jsonify(message),200