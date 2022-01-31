from datetime import datetime
from db.persistance import VerticalServiceInstance, DB, VSIStatus
from flask import jsonify
import db.schemas as schemas
from rabbitmq.adaptor import Messaging
import json
import logging
import config
import requests
from api.exception import CustomException


def getCatalogueVSdInfo(token, vsd_id):
    VSD_ENDPOINT=f"http://{config.CATALOGUE_IP}:{config.CATALOGUE_PORT}/vsdescriptor?vsd_id={vsd_id}"
    print(VSD_ENDPOINT)
    try:
        r = requests.get(VSD_ENDPOINT,
        headers={'Authorization': f"{token}"},
         timeout=15)
        r.raise_for_status()
    except requests.exceptions.ConnectionError as e:
        raise CustomException(message="Could not connect to the Catalogue", status_code=404)
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 404:
            raise CustomException(message=f"Could not find any vs descriptor with id {vsd_id}")
        raise CustomException(message="Something went wrong", status_code=e.response.status_code)
    return r.status_code
    

def getDomainInfo(token, domain_id):
    DOMAIN_ENDPOINT = f"http://{config.DOMAIN_IP}:{config.DOMAIN_PORT}/domain/{domain_id}"
    try:
        r = requests.get(DOMAIN_ENDPOINT,
        headers={'Authorization': f"{token}"},
         timeout=15)
        r.raise_for_status()
    except requests.exceptions.ConnectionError as e:
        raise CustomException(message="Could not connect to the Domain Service", status_code=404)
    except requests.exceptions.HTTPError as e:
        raise CustomException(message=f"Could not find any domain with id {domain_id}")
    except Exception as e:
        raise CustomException(message="Something went wrong", status_code=e.response.status_code)
    return r.status_code


def createNewVS(token,tenantName,request):
    messaging=Messaging()
    vsi = getVSI(tenantName, request['vsiId'])
    if vsi:
        vsiId = request["vsiId"]
        message = f"VS with  with VSiId {vsiId} already exists"
        raise CustomException(message=message, status_code=400)

    #Verify if vsd exists
    getCatalogueVSdInfo(token,request['vsdId'])
    

    # Verify if both Domains exist
    all_domains = request['domainPlacements']
    for domain in all_domains:
        domain_id = domain['domainId']
        getDomainInfo(token,domain_id)
    
    schema = schemas.VerticalServiceInstanceSchema()
    vsInstance = schema.load(request,session=DB.session)
    status_table = VSIStatus(status='Creating',statusMessage="Creating Vertical Service Instance", timestamp=datetime.utcnow())
    vsInstance.status="creating"
    vsInstance.statusMessage="Creating Vertical Service Instance"
    
    vsInstance.tenantId=tenantName
    vsInstance.all_status=[status_table]
    DB.persist(vsInstance)
    DB.persist(status_table)
    #create vsi queue

    # messaging.createExchange("vsLCM_"+str(vsInstance.vsiId))
    # messaging.createQueue("managementQueue-vsLCM_"+str(vsInstance.vsiId))
    # messaging.createQueue("placementQueue-vsLCM_"+str(vsInstance.vsiId))
    # messaging.bindQueue2Exchange("vsLCM_"+str(vsInstance.vsiId), "managementQueue-vsLCM_"+str(vsInstance.vsiId))
    # messaging.bindQueue2Exchange("vsLCM_"+str(vsInstance.vsiId), "placementQueue-vsLCM_"+str(vsInstance.vsiId))
    
    message={"msgType":"createVSI","vsiId": vsInstance.vsiId, "tenantId":tenantName, "data": request}
    #send needed info
    messaging.publish2Exchange('vsLCM_Management',json.dumps(message))
    return schema.dump(vsInstance)

def getAllVSIs(tenantName):
    schema = schemas.VerticalServiceInstanceSchema()
    vsis=DB.session.query(VerticalServiceInstance).filter(VerticalServiceInstance.tenantId==tenantName).all()
    vsisDict=[]
    for vsi in vsis:
        vsisDict.append(schema.dump(vsi))
    return vsisDict

def getVSI(tenantName, vsiId):
    schema = schemas.VerticalServiceInstanceSchema()
    vsi=DB.session.query(VerticalServiceInstance).filter(VerticalServiceInstance.tenantId==tenantName,VerticalServiceInstance.vsiId==vsiId).first()
    return schema.dump(vsi)

def modifyVSI(tenantName, vsiId, request):
    messaging=Messaging()
    vsi=DB.session.query(VerticalServiceInstance).filter(VerticalServiceInstance.tenantId==tenantName,VerticalServiceInstance.vsiId==vsiId).first()
    #send message to manager
    if request["action"]=="primitive":
        message={"msgType":"primitive", "vsiId":vsiId, "data":{"primitiveName":request["primitiveName"],"primitiveTarget":request["primitiveTarget"],"primitiveInternalTarget":request["primitiveInternalTarget"],"primitiveParams":request["primitiveParams"]}}
    elif request["action"]=="terminate":
        message={"msgType":"terminate", "vsiId":vsiId}
    elif request["action"]=="modify":
        message={"msgType":"modifyVSI", "vsiId":vsiId}
    # messaging.publish2Exchange('vsLCM_'+str(vsiId),json.dumps(message))
    messaging.publish2Exchange('vsLCM_Management',json.dumps(message))

def removeVSI(tenantName, vsiId, force=False):
    messaging=Messaging()
    # vsi=DB.session.query(VerticalServiceInstance).filter(VerticalServiceInstance.tenantId==tenantName,VerticalServiceInstance.vsiId==vsiId).first()
    # if vsi!=None:
        #send message to manager
    message={"msgType":"removeVSI", "vsiId":vsiId, "tenantId":tenantName, "force":force}
    messaging.publish2Exchange('vsLCM_Management',json.dumps(message))
    # DB.delete(vsi)
    return "Success"
    # return "VSI "+ str(vsiId)+ " not found"

def changeStatusVSI(data):
    vsiId=data["data"]["vsiId"]
    vsi=DB.session.query(VerticalServiceInstance).filter(VerticalServiceInstance.vsiId==vsiId).first()
    logging.info("changing status")
    logging.info(data)
    if "fail" not in vsi.status.lower():
        if "status" in data["data"]:
            vsi.status=data["data"]["status"]
            vsi.statusMessage=data["data"]["message"]
            status_table = VSIStatus(status=data["data"]["status"],statusMessage=data["data"]["message"], timestamp=datetime.utcnow())
            vsi.all_status.append(status_table)
            DB.persist(vsi)
            DB.persist(status_table)
    if "status" in data["data"] and "terminated" in data["data"]["status"]:
        vsi=DB.session.query(VerticalServiceInstance).filter(VerticalServiceInstance.vsiId==vsiId).first()
        DB.delete(vsi)

def getAllVSIStatus(tenantName,vsiId):
    vsi = getVSI(tenantName,vsiId)
    if not vsi:
        raise CustomException(f"Could not find vsiId with Id {vsiId}",status_code=400)
    schema = schemas.VSIStatusSchema()
    vsis_status=DB.session.query(VSIStatus).filter(VSIStatus.vsiId==vsiId).all()
    statusDict=[]
    for vsi in vsis_status:
        statusDict.append(schema.dump(vsi))
    return statusDict
    
