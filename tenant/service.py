import db.schemas as schemas
import db.persistance as persistance
from flask import jsonify

def getAllGroups():
    schema=schemas.GroupSchema()
    groups=persistance.session.query(persistance.Group).all()
    groupsDict=[]
    for group in groups:
        groupsDict.append(schema.dump(groups))
    return jsonify(groupsDict),200

def createGroup(tenantName, groupData):
    if tenantName != "admin":
        message={"msg":"Invalid user. No permissions to create a new Group."}
        return jsonify(message),500
    schema=schemas.GroupSchema()
    group=schema.load(groupData, session=persistance.session)
    persistance.persist(group)
    message={"msg":"Acknowledge"}
    #TODO verifications
    return jsonify(message),200

def getGroupById(groupName):
    schema=schemas.GroupSchema()
    group=persistance.session.query(persistance.Group).filter(persistance.Group.name==groupName).first()
    return jsonify(schema.dump(group)),200

def modifyGroup(groupName):
    schema=schemas.GroupSchema()
    group=persistance.session.query(persistance.Group).filter(persistance.Group.name==groupName).first()
    return jsonify(schema.dump(group)),200

def removeGroup(groupName):
    group=persistance.session.query(persistance.Group).filter(persistance.Group.name==groupName).first()
    #TODO: add deletion verification
    persistance.delete(group)
    message={"msg":"Acknowledge"}
    return jsonify(message),200

def getAllTenants():
    schema=schemas.TenantSchema()
    tenants=persistance.session.query(persistance.Tenant).all()
    tenantsDict=[]
    for tenant in tenants:
        tenantsDict.append(schema.dump(tenant))
    return jsonify(tenantsDict),200

def createTenant(tenantName, tenantData):
    if tenantName != "admin":
        message={"msg":"Invalid user. No permissions to create a new Tenant."}
        return jsonify(message),500
    schema=schemas.TenantSchema()
    tenant=schema.load(tenantData, session=persistance.session)
    persistance.persist(tenant)
    message={"msg":"Acknowledge"}
    #TODO verifications
    return jsonify(message),200

def getTenantById(tenantName):
    schema=schemas.TenantSchema()
    tenant=persistance.session.query(persistance.Tenant).query(persistance.Tenant.username==tenantName).first()
    return jsonify(schema.dump(tenant)),200

def modifyTenant(tenantName):
    schema=schemas.TenantSchema()
    tenant=persistance.session.query(persistance.Tenant).query(persistance.Tenant.username==tenantName).first()
    return jsonify(schema.dump(tenant)),200

def removeTenant(tenantName):
    tenant=persistance.session.query(persistance.Tenant).query(persistance.Tenant.username==tenantName).first()
    #TODO: add deletion verification
    persistance.delete(tenant)
    message={"msg":"Acknowledge"}
    return jsonify(message),200
