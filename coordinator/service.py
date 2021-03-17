from db.persistance import VerticalServiceInstance, persist, session
from flask import jsonify
import db.schemas as schemas
from rabbitmq.adaptor import Messaging

messaging=Messaging()

def createNewVS(tenantName,request):
    #TODO validate tenant and vsd
    schema = schemas.VerticalServiceInstanceSchema()
    vsInstance = schema.load(request,session=session)
    vsInstance.tenantId=tenantName
    persist(vsInstance)
    #create vsi queue
    messaging.createQueue("vsLCM_"+str(vsInstance.vsiId))
    message={"msgType":"createVSI","vsiId": vsInstance.vsiId, "data": request}
    #send needed info
    messaging.publish2Exchange('vsLCM_Management',json.dumps(message))

    return {"msg": "Acknowledge"}

def getAllVSIs(tenantName):
    vsis=session.query(VerticalServiceInstance).filter(VerticalServiceInstance.tenantId==tenantName).all()
    vsisDict=[]
    for vsi in vsis:
        data=vsi.__dict__
        del data["_sa_instance_state"]
        vsisDict.append(data)
    return jsonify(vsisDict),200

def getVSI(tenantName, vsiId):
    vsi=session.query(VerticalServiceInstance).filter(VerticalServiceInstance.tenantId==tenantName,VerticalServiceInstance.vsiId==vsiId).first()
    data=vsi.__dict__
    del data["_sa_instance_state"]
    return jsonify(data),200

def modifyVSI(tenantName, vsiId):
    vsi=session.query(VerticalServiceInstance).filter(VerticalServiceInstance.tenantId==tenantName,VerticalServiceInstance.vsiId==vsiId).first()
    #send message to manager
    message={"msgType":"modifyVSI", "vsiId":vsiId}
    messaging.publish2Queue('vsLCM_'+str(vsiId),json.dumps(message))
    return jsonify({"msg":"Acknowledge"}),200

def removeVSI(tenantName, vsiId):
    vsi=session.query(VerticalServiceInstance).filter(VerticalServiceInstance.tenantId==tenantName,VerticalServiceInstance.vsiId==vsiId).first()
    #send message to manager
    message={"msgType":"removeVSI", "vsiId":vsiId}
    messaging.publish2Queue('vsLCM_'+str(vsiId),json.dumps(message))
    return jsonify({"msg":"Acknowledge"}),200

def changeStatusVSI(vsiId, status):
    vsi=session.query(VerticalServiceInstance).filter(VerticalServiceInstance.vsiId==vsiId).first()
    vsi.status=status