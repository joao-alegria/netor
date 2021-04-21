import db.schemas as schemas
import db.persistance as persistance
from hashlib import blake2b

def getAllGroups():
    schema=schemas.GroupSchema()
    groups=persistance.session.query(persistance.Group).all()
    groupsDict=[]
    for group in groups:
        groupsDict.append(schema.dump(group))
    return groupsDict

def createGroup(tenantName, groupData):
    if tenantName != "admin":
        raise Exception("Invalid user. No permissions to create a new Group.")
    schema=schemas.GroupSchema()
    group=schema.load(groupData, session=persistance.session)
    persistance.persist(group)
    #TODO verifications

def getGroupById(groupName):
    schema=schemas.GroupSchema()
    group=persistance.session.query(persistance.Group).filter(persistance.Group.name==groupName).first()
    return schema.dump(group)

def modifyGroup(groupName):
    schema=schemas.GroupSchema()
    group=persistance.session.query(persistance.Group).filter(persistance.Group.name==groupName).first()
    return schema.dump(group)

def removeGroup(groupName):
    group=persistance.session.query(persistance.Group).filter(persistance.Group.name==groupName).first()
    #TODO: add deletion verification
    persistance.delete(group)

def getAllTenants():
    schema=schemas.TenantSchema()
    tenants=persistance.session.query(persistance.Tenant).all()
    tenantsDict=[]
    for tenant in tenants:
        tenantsDict.append(schema.dump(tenant))
    return tenantsDict

def createTenant(tenantName, tenantData):
    if tenantName != "admin":
        raise Exception("Invalid user. No permissions to create a new Tenant.")
    schema=schemas.TenantSchema()

    groups=getAllGroups()
    groupNames=[group["name"] for group in groups]
    if tenantData["group"] not in groupNames:
        raise Exception("Group "+tenantData["group"]+" does not exist.")

    tenantData["password"]=blake2b(tenantData["password"].encode("utf-8")).hexdigest()

    tenant=schema.load(tenantData, session=persistance.session)
    persistance.persist(tenant)
    #TODO verifications

def getTenantById(tenantName):
    schema=schemas.TenantSchema()
    tenant=persistance.session.query(persistance.Tenant).filter(persistance.Tenant.username==tenantName).first()
    return schema.dump(tenant)

def addVsiToTenant(tenantName, vsiId):
    vsi=persistance.VSI(id=vsiId, tenantUsername=tenantName)
    persistance.persist(vsi)

def modifyTenant(tenantName):
    schema=schemas.TenantSchema()
    tenant=persistance.session.query(persistance.Tenant).filter(persistance.Tenant.username==tenantName).first()
    return schema.dump(tenant)

def removeTenant(tenantName):
    tenant=persistance.session.query(persistance.Tenant).filter(persistance.Tenant.username==tenantName).first()
    #TODO: add deletion verification
    persistance.delete(tenant)

def deleteVsiFromTenant(tenantName, vsiId):
    vsi=persistance.session.query(persistance.VSI).filter(persistance.VSI.tenantUsername==tenantName, persistance.VSI.id==vsiId).first()
    persistance.delete(vsi)