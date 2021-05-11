import pytest
from api.loginConfig import Tenant
from api.controller import app
from db.persistance import DB
import flask_login
import rabbitmq.adaptor

@pytest.fixture
def client(rabbit):
    DB.createDB()
    app.testing=True
    yield app.test_client()
    DB.removeDB()

@pytest.fixture
def rabbit(monkeypatch, mocker):
    def mock_messaging(*args, **kwargs):
        return None
    monkeypatch.setattr(rabbitmq.adaptor.Messaging, "__init__", mock_messaging)

    def mock_messagingConsume(*args, **kwargs):
        return None
    monkeypatch.setattr(rabbitmq.adaptor.Messaging, "consumeQueue", mock_messagingConsume)

    def mock_messagingCreateQueue(*args, **kwargs):
        return None
    monkeypatch.setattr(rabbitmq.adaptor.Messaging, "createQueue", mock_messagingCreateQueue)

    def mock_messagingCreateExchange(*args, **kwargs):
        return None
    monkeypatch.setattr(rabbitmq.adaptor.Messaging, "createExchange", mock_messagingCreateExchange)

    def mock_messagingBind(*args, **kwargs):
        return None
    monkeypatch.setattr(rabbitmq.adaptor.Messaging, "bindQueue2Exchange", mock_messagingBind)

    # def mock_messagingPublish(*args, **kwargs):
    #     assert args==[]
    #     return None
    # monkeypatch.setattr(rabbitmq.adaptor.Messaging, "publish2Exchange", mock_messagingConsume)
    mocker.patch('rabbitmq.adaptor.Messaging.publish2Exchange')


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
    response=client.get("/vs")
    assert response.status_code==401

def test_getVSI(client,tenantUser):
    response=client.get("/vs")
    dataFetched=response.json
    assert response.status_code==200
    assert len(dataFetched["data"])==0

def test_getDomainById(client,tenantUser):
    test_createNewVSI(client,tenantUser)
    response=client.get("/vs/2")
    dataFetched=response.json
    assert dataFetched["data"]["vsiId"]=="2"
    assert dataFetched["data"]["status"]=="creating"

def test_getVSIAfterPost(client,tenantUser):
    test_createNewVSI(client,tenantUser)
    response=client.get("/vs")
    assert response.status_code==200
    dataFetched=response.json
    assert len(dataFetched["data"])==1
    assert [(vsi["vsiId"], vsi["status"]) for vsi in dataFetched["data"]]==[("2","creating")]

def test_createNewVSI(client,tenantUser):
    test_getVSI(client,tenantUser)
    vsiData={"name":"test","vsdId":"608ae08e063c52ff4d88f32f","domainId":"ITAV","vsiId":"2","domainPlacements":[{"domainId":"DETI","componentName":"test_VSI-1_1"},{"domainId":"DETI","componentName":"test_VSI-1_2"}]}
    response=client.post("/vs", json=vsiData)
    assert response.status_code==200
    assert response.json["message"]=="Success"

def test_deleteExistingVSI(client,tenantUser):
    test_getVSIAfterPost(client,tenantUser)
    response=client.delete("/vs/2")
    assert response.status_code==200
    test_getVSI(client,tenantUser)