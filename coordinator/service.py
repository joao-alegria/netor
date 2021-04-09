from db.persistance import VerticalServiceInstance, persist, session
from flask import jsonify
import db.schemas as schemas
from rabbitmq.adaptor import Messaging
import json

messaging=Messaging()

def createNewVS(tenantName,request):
    #TODO validate tenant and vsd
    schema = schemas.VerticalServiceInstanceSchema()
    vsInstance = schema.load(request,session=session)
    vsInstance.tenantId=tenantName
    persist(vsInstance)
    #create vsi queue
    # messaging.createQueue("vsLCM_"+str(vsInstance.vsiId))
    message={"msgType":"createVSI","vsiId": vsInstance.vsiId, "tenantId":tenantName, "data": request}
    #send needed info
    messaging.publish2Exchange('vsLCM_Management',json.dumps(message))

    return {"msg": "Acknowledge"}

def getAllVSIs(tenantName):
    schema = schemas.VerticalServiceInstanceSchema()
    vsis=session.query(VerticalServiceInstance).filter(VerticalServiceInstance.tenantId==tenantName).all()
    vsisDict=[]
    for vsi in vsis:
        vsisDict.append(schema.dump(vsi))
    return vsisDict

def getVSI(tenantName, vsiId):
    vsi=session.query(VerticalServiceInstance).filter(VerticalServiceInstance.tenantId==tenantName,VerticalServiceInstance.vsiId==vsiId).first()
    data=vsi.__dict__
    del data["_sa_instance_state"]
    return data

def modifyVSI(tenantName, vsiId):
    vsi=session.query(VerticalServiceInstance).filter(VerticalServiceInstance.tenantId==tenantName,VerticalServiceInstance.vsiId==vsiId).first()
    #send message to manager
    message={"msgType":"modifyVSI", "vsiId":vsiId}
    messaging.publish2Queue('vsLCM_'+str(vsiId),json.dumps(message))
    return {"msg":"Acknowledge"}

def removeVSI(tenantName, vsiId):
    vsi=session.query(VerticalServiceInstance).filter(VerticalServiceInstance.tenantId==tenantName,VerticalServiceInstance.vsiId==vsiId).first()
    #send message to manager
    message={"msgType":"removeVSI", "vsiId":vsiId}
    messaging.publish2Queue('vsLCM_'+str(vsiId),json.dumps(message))
    return {"msg":"Acknowledge"}

def changeStatusVSI(vsiId, status):
    vsi=session.query(VerticalServiceInstance).filter(VerticalServiceInstance.vsiId==vsiId).first()
    vsi.status=status