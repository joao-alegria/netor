import pytest
import requests
from api.controller import app
from db.persistance import DB

@pytest.fixture
def client():
    DB.createDB()
    DB.initDB()
    app.testing=True
    yield app.test_client()
    DB.removeDB()

@pytest.fixture
def token(client):
    parameters={'response_type': 'code','grant_type': 'password', 'client_id': 'portal', 'client_secret': 'portal', 'username': 'admin', 'password': 'admin'}
    authorization=client.post("/oauth/token", data=parameters)
    data=authorization.json
    return data["access_token"]

def test_requestWithoutAuthorization(client):
    response=client.get("/group")
    assert response.status_code==401

def test_getGroups(client,token):
    response=client.get("/group", headers={"Authorization": "Bearer "+token})
    assert response.status_code==200
    dataFetched=response.json
    assert len(dataFetched["data"])==2
    assert [group["name"] for group in dataFetched["data"]]==["admin", "user"]

def test_getGroupById(client,token):
    response=client.get("/group/user", headers={"Authorization": "Bearer "+token})
    assert response.status_code==200
    dataFetched=response.json
    assert dataFetched["data"]["name"]=="user"

def test_getGroupsAfterPost(client,token):
    test_createNewGroup(client,token)
    response=client.get("/group", headers={"Authorization": "Bearer "+token})
    assert response.status_code==200
    dataFetched=response.json
    assert len(dataFetched["data"])==3
    assert [group["name"] for group in dataFetched["data"]]==["admin", "user", "test"]

def test_createNewGroup(client,token):
    test_getGroups(client,token)
    groupData={"name":"test"}
    response=client.post("/group", json=groupData, headers={"Authorization": "Bearer "+token})
    assert response.status_code==200
    assert response.json["message"]=="Success"

def test_deleteExistingGroup(client,token):
    test_getGroupsAfterPost(client,token)
    response=client.delete("/group/test", headers={"Authorization": "Bearer "+token})
    assert response.status_code==200
    test_getGroups(client,token)

def test_getTenants(client,token):
    response=client.get("/tenant", headers={"Authorization": "Bearer "+token})
    assert response.status_code==200
    dataFetched=response.json
    assert len(dataFetched["data"])==2
    assert [tenant["username"] for tenant in dataFetched["data"]]==["admin", "user"]

def test_getTenantById(client,token):
    response=client.get("/tenant/user", headers={"Authorization": "Bearer "+token})
    assert response.status_code==200
    dataFetched=response.json
    assert dataFetched["data"]["username"]=="user"

def test_getTenantsAfterPost(client,token):
    test_createNewTenant(client,token)
    response=client.get("/tenant", headers={"Authorization": "Bearer "+token})
    assert response.status_code==200
    dataFetched=response.json
    assert len(dataFetched["data"])==3
    assert [tenant["username"] for tenant in dataFetched["data"]]==["admin", "user", "test"]

def test_createNewTenant(client,token):
    test_getTenants(client,token)
    tenantData={"group": "user","username": "test","password": "test","role": "TENANT","storage": 100,"memory": 100,"vcpu": 100}
    response=client.post("/tenant", json=tenantData, headers={"Authorization": "Bearer "+token})
    assert response.status_code==200
    assert response.json["message"]=="Success"

def test_deleteExistingTenant(client,token):
    test_getTenantsAfterPost(client,token)
    response=client.delete("/tenant/test", headers={"Authorization": "Bearer "+token})
    assert response.status_code==200
    test_getTenants(client,token)
