import pytest
import requests
from api.loginConfig import Tenant
from api.controller import app
from db.persistance import DB
import flask_login

@pytest.fixture
def client():
    DB.createDB()
    DB.initDB()
    app.testing=True
    yield app.test_client()
    DB.removeDB()

@pytest.fixture
def adminUser(monkeypatch):
    def mock_requestLoader(*args, **kwargs):
        return Tenant("admin", "ADMIN")
    monkeypatch.setattr(flask_login.utils, "_get_user", mock_requestLoader)

@pytest.fixture
def tenantUser(monkeypatch):
    def mock_requestLoader(*args, **kwargs):
        return Tenant("user", "TENANT")
    monkeypatch.setattr(flask_login.utils, "_get_user", mock_requestLoader)

def test_requestWithoutAuthorization(client):
    response=client.get("/domain")
    assert response.status_code==401

def test_getDomains(client,adminUser):
    response=client.get("/domain")
    dataFetched=response.json
    assert response.status_code==200
    assert len(dataFetched["data"])==1
    assert [domain["domainId"] for domain in dataFetched["data"]]==["ITAV"]

def test_getDomainById(client,adminUser):
    response=client.get("/domain/ITAV")
    dataFetched=response.json
    assert response.status_code==200
    assert dataFetched["data"]["domainId"]=="ITAV"

def test_getDomainsAfterPost(client,adminUser):
    test_createNewDomain(client,adminUser)
    response=client.get("/domain")
    assert response.status_code==200
    dataFetched=response.json
    assert len(dataFetched["data"])==2
    assert [domain["domainId"] for domain in dataFetched["data"]]==["ITAV", "DETI"]

def test_createNewDomain(client,adminUser):
    test_getDomains(client,adminUser)
    domainData={"domainId":"DETI","admin":"DETI","description":"DETI domain","auth":False,"interfaceType":"HTTP","url":"10.0.12.118","name":"DETI","owner":"Joao Alegria","ownedLayers":[{"domainLayerId":"DETI_OSM","domainLayerType":"OsmDomainLayer","username":"admin","password":"admin","project":"admin","vimAccount":"microstack"}]}
    response=client.post("/domain", json=domainData)
    assert response.status_code==200
    assert response.json["message"]=="Success"

def test_deleteExistingDomain(client,adminUser):
    test_getDomainsAfterPost(client,adminUser)
    response=client.delete("/domain/DETI")
    assert response.status_code==200
    test_getDomains(client,adminUser)