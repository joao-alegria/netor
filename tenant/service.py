import db.schemas as schemas
import db.persistance as persistance
from hashlib import blake2b
import logging
from rabbitmq.adaptor import Messaging
from datetime import datetime, timedelta
import json
from api.exception import CustomException
def getAllGroups():
    schema=schemas.GroupSchema()
    groups=persistance.DB.session.query(persistance.Group).all()
    groupsDict=[]
    for group in groups:
        groupsDict.append(schema.dump(group))
    return groupsDict


def has_valid_role(tenantName, check_admin=False):
    tenant = getTenantById(tenantName)
    if tenant == {}:
        return False    
    role = tenant['role']
    if check_admin:
        return role == 'ADMIN'
    return role == 'ADMIN' or role == 'TENANT'
    

def createGroup(tenantName, groupData):
    if not has_valid_role(tenantName):
        raise CustomException("Invalid user. No permissions to create a new Group.", status_code=401)
    schema=schemas.GroupSchema()
    if getGroupById(groupData['name']):
        raise CustomException(message=f"Invalid Group. There is already a group with the name {groupData['name']}",status_code=409)
    group=schema.load(groupData, session=persistance.DB.session)
    persistance.DB.persist(group)
    return schema.dump(group)

def getGroupById(groupName):
    schema=schemas.GroupSchema()
    group=persistance.DB.session.query(persistance.Group).filter(persistance.Group.name==groupName).first()
    if not group:
        return None
    return schema.dump(group)


def modifyGroup(groupName):
    schema=schemas.GroupSchema()
    group=persistance.DB.session.query(persistance.Group).filter(persistance.Group.name==groupName).first()

    return schema.dump(group)

def removeGroup(groupName):
    group=persistance.DB.session.query(persistance.Group).filter(persistance.Group.name==groupName).first()
    #TODO: add deletion verification
    persistance.DB.delete(group)

def getAllTenants(tenantName):
    if not has_valid_role(tenantName,check_admin=True):
         raise CustomException("Invalid User. Can not obtains Tenants Informations.", status_code=401)
    schema=schemas.TenantSchema()
    tenants=persistance.DB.session.query(persistance.Tenant).all()
    tenantsDict=[schema.dump(tenant) for tenant in tenants]
    return tenantsDict

def createTenant(tenantName, tenantData):
    if tenantName != "admin":
        raise Exception("Invalid user. No permissions to create a new Tenant.")
    schema=schemas.TenantSchema()

    groups=getAllGroups()
    groupNames=[group["name"] for group in groups]
    if tenantData["group"] not in groupNames:
        raise Exception("Group "+tenantData["group"]+" does not exist.")

    tenants=getAllTenants()
    tenantNames=[tenant["username"] for tenant in tenants]
    if tenantData["username"] in tenantNames:
        raise Exception("Tenant "+tenantData["username"]+" already exists.")

    tenantData["password"]=blake2b(tenantData["password"].encode("utf-8")).hexdigest()

    tenant=schema.load(tenantData, session=persistance.DB.session)
    persistance.DB.persist(tenant)

def getTenantById(tenantName):
    schema=schemas.TenantSchema()
    tenant=persistance.DB.session.query(persistance.Tenant).filter(persistance.Tenant.username==tenantName).first()
    return schema.dump(tenant)


def addVsiToTenant(tenantName, vsiId):
    vsi=persistance.VSI(id=vsiId, tenantUsername=tenantName)
    persistance.DB.persist(vsi)

def modifyTenant(tenantName):
    schema=schemas.TenantSchema()
    tenant=persistance.DB.session.query(persistance.Tenant).filter(persistance.Tenant.username==tenantName).first()
    return schema.dump(tenant)

def removeTenant(tenantName):
    messaging=Messaging()
    tenant=persistance.DB.session.query(persistance.Tenant).filter(persistance.Tenant.username==tenantName).first()
    #TODO: add deletion verification
    if tenant==None:
        return {"message":"Tenant doesn't exist"}
    for vsi in tenant.vsis:
        persistance.DB.delete(vsi)
        message={"msgType":"removeVSI", "vsiId":str(vsi.id), "tenantId":tenantName, "force":True}
        messaging.publish2Exchange('vsLCM_Management',json.dumps(message))
    persistance.DB.delete(tenant)
    return {"message":"Success"}

def deleteVsiFromTenant(tenantName, vsiId):
    vsi=persistance.DB.session.query(persistance.VSI).filter(persistance.VSI.tenantUsername==tenantName, persistance.VSI.id==vsiId).first()
    if vsi!=None:
        persistance.DB.delete(vsi)
    else:
        logging.info("Error while deleting VSI from Tenant: VSI " + str(vsiId) + " not found in Tenant "+tenantName)