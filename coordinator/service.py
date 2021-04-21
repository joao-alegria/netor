from db.persistance import VerticalServiceInstance, persist, session, delete
from flask import jsonify
import db.schemas as schemas
from rabbitmq.adaptor import Messaging
import json

messaging=Messaging()

def createNewVS(tenantName,request):
    vsis=getAllVSIs(tenantName)
    vsiIds=[vsi["vsiId"] for vsi in vsis]
    if request["vsiId"] in vsiIds:
        raise Exception("VSI Id "+request["vsiId"]+" already exists")

    schema = schemas.VerticalServiceInstanceSchema()
    vsInstance = schema.load(request,session=session)

    vsInstance.status="creating"
    vsInstance.statusMessage="Creating Vertical Service Instance"

    vsInstance.tenantId=tenantName
    persist(vsInstance)
    #create vsi queue
    messaging.createExchange("vsLCM_"+str(vsInstance.vsiId))
    messaging.createQueue("managementQueue-vsLCM_"+str(vsInstance.vsiId))
    messaging.createQueue("placementQueue-vsLCM_"+str(vsInstance.vsiId))
    messaging.bindQueue2Exchange("vsLCM_"+str(vsInstance.vsiId), "managementQueue-vsLCM_"+str(vsInstance.vsiId))
    messaging.bindQueue2Exchange("vsLCM_"+str(vsInstance.vsiId), "placementQueue-vsLCM_"+str(vsInstance.vsiId))
    
    message={"msgType":"createVSI","vsiId": vsInstance.vsiId, "tenantId":tenantName, "data": request}
    #send needed info
    messaging.publish2Exchange('vsLCM_Management',json.dumps(message))
    return vsInstance.vsiId

def getAllVSIs(tenantName):
    schema = schemas.VerticalServiceInstanceSchema()
    vsis=session.query(VerticalServiceInstance).filter(VerticalServiceInstance.tenantId==tenantName).all()
    vsisDict=[]
    for vsi in vsis:
        vsisDict.append(schema.dump(vsi))
    return vsisDict

def getVSI(tenantName, vsiId):
    schema = schemas.VerticalServiceInstanceSchema()
    vsi=session.query(VerticalServiceInstance).filter(VerticalServiceInstance.tenantId==tenantName,VerticalServiceInstance.vsiId==vsiId).first()
    return schema.dump(vsi)

def modifyVSI(tenantName, vsiId, request):
    vsi=session.query(VerticalServiceInstance).filter(VerticalServiceInstance.tenantId==tenantName,VerticalServiceInstance.vsiId==vsiId).first()
    #send message to manager
    if request["action"]=="primitive":
        message={"msgType":"primitive", "vsiId":vsiId, "data":{"primitiveName":request["primitiveName"],"primitiveTarget":request["primitiveTarget"],"primitiveInternalTarget":request["primitiveInternalTarget"],"primitiveParams":request["primitiveParams"]}}
    elif request["action"]=="terminate":
        message={"msgType":"terminate", "vsiId":vsiId}
    elif request["action"]=="modify":
        message={"msgType":"modifyVSI", "vsiId":vsiId}
    messaging.publish2Exchange('vsLCM_'+str(vsiId),json.dumps(message))

def removeVSI(tenantName, vsiId):
    vsi=session.query(VerticalServiceInstance).filter(VerticalServiceInstance.tenantId==tenantName,VerticalServiceInstance.vsiId==vsiId).first()
    #send message to manager
    message={"msgType":"removeVSI", "vsiId":vsiId, "tenantId":tenantName}
    messaging.publish2Exchange('vsLCM_Management',json.dumps(message))
    delete(vsi)

def changeStatusVSI(data):
    vsiId=data["data"]["vsiId"]
    vsi=session.query(VerticalServiceInstance).filter(VerticalServiceInstance.vsiId==vsiId).first()
    if "fail" not in vsi.status.lower():
        if "status" in data["data"]:
            vsi.status=data["data"]["status"]
        vsi.statusMessage=data["data"]["message"]
        persist(vsi)