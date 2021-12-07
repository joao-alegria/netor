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
    if not tenant:
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
         raise CustomException("Invalid User. Can not obtains Tenants Information.", status_code=401)
    schema=schemas.TenantSchema()
    tenants=persistance.DB.session.query(persistance.Tenant).all()
    tenantsDict = []
    for tenant in tenants:
        tenant_dict = schema.dump(tenant)
        del tenant_dict['password']
        tenantsDict.append(tenant_dict)
    return tenantsDict

def createTenant(tenantName, tenantData):
    if not has_valid_role(tenantName,check_admin=True):
        raise CustomException("Invalid User. Can not obtains Tenants Information.", status_code=401)
    schema=schemas.TenantSchema()
    group_name = tenantData['group']
    db_group = getGroupById(group_name)
    groups=getAllGroups()
    #groupNames=[group["name"] for group in groups]
    #if tenantData["group"] not in groupNames:
    if not db_group:
        raise CustomException(message=f"Group {group_name} does not exist.", status_code=404)

    db_tenant = getTenantById(tenantData['username'])
    #tenantNames=[tenant["username"] for tenant in tenants]
    #if tenantData["username"] in tenantNames:
    if db_tenant:
        username = tenantData["username"]
        raise CustomException(message=f"Tenant {username} already exists.")

    tenantData["password"]=blake2b(tenantData["password"].encode("utf-8")).hexdigest()

    tenant=schema.load(tenantData, session=persistance.DB.session)
    persistance.DB.persist(tenant)
    return schema.dump(tenant)


def getTenant(current_user, tenantName):
    
    if not has_valid_role(current_user,check_admin=True) and current_user != tenantName :
        raise CustomException(message="Can not obtains this Tenant Information.", status_code=401)
    return getTenantById(tenantName)


def getTenantById(tenantName):
    schema=schemas.TenantSchema()
    tenant=persistance.DB.session.query(persistance.Tenant).filter(persistance.Tenant.username==tenantName).first()
    tenant_dict = schema.dump(tenant)
    tenant_dict.pop('password',None)
    return tenant_dict


def addVsiToTenant(tenantName, vsiId):
    vsi=persistance.VSI(id=vsiId, tenantUsername=tenantName)
    persistance.DB.persist(vsi)

def modifyTenant(tenantName):
    schema=schemas.TenantSchema()
    tenant=persistance.DB.session.query(persistance.Tenant).filter(persistance.Tenant.username==tenantName).first()
    return schema.dump(tenant)

def removeTenant(current_user, tenantName):
    #Only Admins should be able to remove Tenants
    if not has_valid_role(current_user,check_admin=True):
        raise CustomException(message="No permission to delete this Tenant Information", status_code=401)
    messaging=Messaging()
    tenant=persistance.DB.session.query(persistance.Tenant).filter(persistance.Tenant.username==tenantName).first()
    #TODO: add deletion verification
    if not tenant:
        return None
    for vsi in tenant.vsis:
        persistance.DB.delete(vsi)
        message={"msgType":"removeVSI", "vsiId":str(vsi.id), "tenantId":tenantName, "force":True}
        messaging.publish2Exchange('vsLCM_Management',json.dumps(message))
    persistance.DB.delete(tenant)
    return tenant

def deleteVsiFromTenant(tenantName, vsiId):
    vsi=persistance.DB.session.query(persistance.VSI).filter(persistance.VSI.tenantUsername==tenantName, persistance.VSI.id==vsiId).first()
    if vsi!=None:
        persistance.DB.delete(vsi)
    else:
        logging.info("Error while deleting VSI from Tenant: VSI " + str(vsiId) + " not found in Tenant "+tenantName)