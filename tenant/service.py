import db.schemas as schemas
import db.persistance as persistance

def getAllGroups():
    schema=schemas.GroupSchema()
    groups=persistance.session.query(persistance.Group).all()
    groupsDict=[]
    for group in groups:
        groupsDict.append(schema.dump(groups))
    return groupsDict

def createGroup(tenantName, groupData):
    if tenantName != "admin":
        message={"msg":"Invalid user. No permissions to create a new Group."}
        return message
    schema=schemas.GroupSchema()
    group=schema.load(groupData, session=persistance.session)
    persistance.persist(group)
    message={"msg":"Acknowledge"}
    #TODO verifications
    return message

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
    message={"msg":"Acknowledge"}
    return message

def getAllTenants():
    schema=schemas.TenantSchema()
    tenants=persistance.session.query(persistance.Tenant).all()
    tenantsDict=[]
    for tenant in tenants:
        tenantsDict.append(schema.dump(tenant))
    return tenantsDict

def createTenant(tenantName, tenantData):
    if tenantName != "admin":
        message={"msg":"Invalid user. No permissions to create a new Tenant."}
        return jsonify(message)
    schema=schemas.TenantSchema()
    tenant=schema.load(tenantData, session=persistance.session)
    persistance.persist(tenant)
    message={"msg":"Acknowledge"}
    #TODO verifications
    return message

def getTenantById(tenantName):
    schema=schemas.TenantSchema()
    tenant=persistance.session.query(persistance.Tenant).filter(persistance.Tenant.username==tenantName).first()
    return schema.dump(tenant)

def addVsiToTenant(tenantName, vsiId):
    vsi=persistance.VSI(id=vsiId, tenantUsername=tenantName)
    persistance.persist(vsi)
    return

def modifyTenant(tenantName):
    schema=schemas.TenantSchema()
    tenant=persistance.session.query(persistance.Tenant).filter(persistance.Tenant.username==tenantName).first()
    return schema.dump(tenant)

def removeTenant(tenantName):
    tenant=persistance.session.query(persistance.Tenant).filter(persistance.Tenant.username==tenantName).first()
    #TODO: add deletion verification
    persistance.delete(tenant)
    message={"msg":"Acknowledge"}
    return message
