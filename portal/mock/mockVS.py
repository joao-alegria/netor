from flask import Flask, request, make_response, jsonify
from flask_cors import CORS, cross_origin
import json
from secrets import token_urlsafe
import csv

app = Flask(__name__)
cors = CORS(app, support_credentials=True)


# new tenant endpoint: /portal/catalogue/vsblueprint
#new: remoteTenantInfos
groups = [{
    "name": "user",
    "tenants": [{
        "remoteTenantInfos": [{
            "host": "string",
            "remoteTenantName": "string",
            "remoteTenantPwd": "string"
        }],
        "username": "vertical",
        "password": "vertical",
        "sla": [{
            "id": 1,
            "slaConstraints": [{
                "scope": "GLOBAL_VIRTUAL_RESOURCE",
                "maxResourceLimit": {
                    "diskStorage": 100,
                    "vCPU": 100,
                    "memoryRAM": 100
                },
                "location": "teste"
            }],
            "slaStatus": "ENABLED"
        }],
        "vsdId": [1],
        "vsiId":[1],
        "allocatedResources":{"diskStorage": 100, "vCPU": 100, "memoryRAM": 100}
    }, {
        "remoteTenantInfos": [],
        "username": "user",
        "password": "user",
        "sla": [{
            "slaConstraints": [{
                "scope": "GLOBAL_VIRTUAL_RESOURCE",
                "maxResourceLimit": {
                    "diskStorage": 100,
                    "vCPU": 100,
                    "memoryRAM": 100
                },
                "location": "teste"
            }],
            "slaStatus": "ENABLE"
        }],
        "vsdId": [1],
        "vsiId": [1],
        "allocatedResources": {
            "diskStorage": 100,
            "vCPU": 100,
            "memoryRAM": 100
        },
    }]
}, {
    "name": "admin",
    "tenants": [{
        "remoteTenantInfos": [],
        "username": "operator",
        "password": "operator",
        "sla": [{
            "slaConstraints": [{
                "scope": "GLOBAL_VIRTUAL_RESOURCE",
                "maxResourceLimit": {
                    "diskStorage": 100,
                    "vCPU": 100,
                    "memoryRAM": 100
                },
                "location": "ITAV"
            }],
            "slaStatus": "ENABLED"
        }],
        "vsdId": [1],
        "vsiId": [1],
        "allocatedResources": {"diskStorage": 100, "vCPU": 100, "memoryRAM": 100},
    }]
}]


domains=[{'domainId': 'SONATA', 'name': 'SONATA', 'description': 'SONATA', 'owner': 'operator', 'admin': 'SONATA', 'domainStatus': 'ACTIVE', 'domainInterface': {'url': 'localhost', 'port': 1234, 'auth': False, 'interfaceType': 'HTTP'}, 'ownedLayers': [{'domainLayerId': 'SONATA', 'domainLayerType': 'NETWORK_SLICE_PROVIDER', 'type': 'SONATA_NSP', 'username': 'SONATA', 'password': 'SONATA'}]}]

# new blueprint endpoint: /portal/catalogue/vsblueprint
#new: applicationMetrics | compatibleContextBlueprint | compatibleSites
#changed: serviceSequence
blueprints = [{
    "vsBlueprintId": 1,
    "vsBlueprintVersion": "1.0",
    "name": "railCrossing",
    "vsBlueprint": {
        "applicationMetrics": [{
            "interval": "string",
            "metricCollectionType": "CUMULATIVE",
            "metricId": "string",
            "name": "string",
            "topic": "string",
            "unit": "string"
        }],
        "compatibleContextBlueprint": ["1"],
        "compatibleSites": [
            "AVEIRO_ITAV"
        ],
        "vsBlueprintId": 1,
        "version": "1.0",
        "name": "railCrossing",
        "description": "Blueprint for Rail Road Crossing",
        "imgUrl": "www.teste.com",
        "parameters": [{
            "parameterId": "1",
            "parameterName": "availability",
            "parameterType": "integer",
            "parameterDescription": "System Availability",
            "applicabilityField": "PortoAveiro"
        },{
            "parameterId": "2",
            "parameterName": "activityFactor",
            "parameterType": "integer",
            "parameterDescription": "System Availability",
            "applicabilityField": "PortoAveiro"
        },{
            "parameterId": "3",
            "parameterName": "coverage",
            "parameterType": "string",
            "parameterDescription": "System Availability",
            "applicabilityField": "PortoAveiro"
        }],
        "atomicComponents": [{
            "componentId": 1,
            "serversNumber": 1,
            "imagesUrls": ["teste1"],
            "endPointsIds":["teste1"],
            "lifecycleOperations":{"teste": "teste"}
        }],
        "serviceSequence": [{
            "hopEndPoints": [{
                "endPointId": "1",
                "vsComponentId": "1"
            }]
        }],
        "endPoints": [{
            "endPointId": "1",
            "external": True,
            "management": True,
            "ranConnection": True
        }],
        "connectivityServices": [{
            "endPointIds": [1],
            "external":True,
            "connectivityProperties":["teste1"]
        }],
        "configurableParameters": ["teste1"],
        "service_category":"string",
        "service_type":"string"
    },
    "onBoardedNsdInfoId": ["1"],
    "onBoardedVnfPackageInfoId": ["1"],
    "onBoardedMecAppPackageInfoId": ["1"],
    "activeVsdId": ["1"]
}]


# new descriptor endpoint: /portal/catalogue/vsdescriptor
descriptors = [{
    "vsDescriptorId": 1,
    "name": "railCrossing-PortoAveiro",
    "version": "1.0",
    "vsBlueprintId": 1,
    "sst": "NONE",
    "managementType": "PROVIDER_MANAGED",
    "qosParameters": {"availability": 100, "activityFactor":20,"coverage":"FULL"},
    "serviceConstraints": [{
        "sharable": True,
        "canIncludeSharedElements": True,
        "priority": "LOW",
        "preferredProviders": ["providerA"],
        "nonPreferredProviders":["providerB"],
        "prohibitedProviders":["providerC"],
        "atomicComponentId":"1"
    }],
    "sla": {
        "serviceCreationTime": "SERVICE_CREATION_TIME_LOW",
        "availabilityCoverage": "AVAILABILITY_COVERAGE_HIGH",
        "lowCostRequired": True
    }
}]

# netslices = [{
#     "name": "PortoAveiro-Net",
#     "description": "Porto Aveiro Network Slice",
#     "nsiId": 1,
#     "nsdId": 1,
#     "nsdVersion": "1.0",
#     "dfId": "1",
#     "instantiationLevelId": "1",
#     "nfvNsId": 1,
#     "soManaged": "true",
#     "networkSliceSubnetInstances": ["1"],
#     "tenantId": 1,
#     "status": "ONLINE",
#     "errorMessage": "NONE",
#     "nfvNsUrl": "www.test.com"
# }]

netslices = [{
    "name": "PortoAveiro-Net",
    "description": "Porto Aveiro Network Slice",
    "nstId": 1,
    "nsiId":1,
    "status":"ONLINE"
}]

nstemplates = [{
    "nstInfoId":"49c1af90-e3e3-4af1-ade4-35015f83fdb9",
    "nsTemplateId":"string",
    "name":"string",
    "nsTemplateVersion":"string",
    "designer":"string",
    "operationalState":None,
    "usageState":None,
    "deletionPending":False,
    "sst":None,
    "userDefinedData":{},
    "nst":{
        "nstId":"string",
        "nstName":"string",
        "nstVersion":"string",
        "nstProvider":"string",
        "geographicalAreaInfoList":[],
        "nsstIds":["string"],
        "nsst":[],
        "nsdId":"string",
        "nsdVersion":"string",
        "nstServiceProfile":{
            "serviceProfileId":"string",
            "pLMNIdList":["string"],
            "eMBBPerfReq":[{
                "expDataRateDL":0,
                "expDataRateUL":0,
                "areaTrafficCapDL":0,
                "areaTrafficCapUL":0,
                "userDensity":0,
                "activityFactor":0,
                "uESpeed":0,
                "coverage":"string"
            }],
            "uRLLCPerfReq":[{
                "e2eLatency":0,
                "jitter":0,
                "survivalTime":0,
                "cSAvailability":0,
                "reliability":0,
                "expDataRate":0,
                "payloadSize":"string",
                "trafficDensity":0,
                "connDensity":0,
                "serviceAreaDimension":"string"
            }],
            "maxNumberofUEs":0,
            "coverageAreaTAList":["string"],
            "latency":0,
            "uEMobilityLevel":"STATIONARY",
            "resourceSharingLevel":True,
            "sST":"EMBB",
            "availability":0
        },
        "nsstType":None
    }
},
    {"nstInfoId":"49c1af90-e3e3-4af1-ade4-35015f83fdb9",
    "nsTemplateId":"string",
    "name":"string",
    "nsTemplateVersion":"string",
    "designer":"string",
    "operationalState":None,
    "usageState":None,
    "deletionPending":False,
    "sst":None,
    "userDefinedData":{},
    "nst":{
        "nsdId": "1",
        "nsdVersion": "1.0",
        "nsstIds": [
            "1"
        ],
        "nstId": "9",
        "nstName": "Airplane Connectivity",
        "nstProvider": "string",
        "nstServiceProfile": {
            "availability": 100,
            "coverageAreaTAList": [
                "ITAV"
            ],
            "eMBBPerfReq": [
                {
                    "activityFactor": 20,
                    "areaTrafficCapDL": 1.2,
                    "areaTrafficCapUL": 0.6,
                    "coverage": "FULL",
                    "expDataRateDL": 15,
                    "expDataRateUL": 7.5,
                    "uESpeed": 1000,
                    "userDensity": 400
                }
            ],
            "latency": 2,
            "maxNumberofUEs": 10,
            "pLMNIdList": [
                "string"
            ],
            "resourceSharingLevel": True,
            "sST": "EMBB",
            "serviceProfileId": "string",
            "uEMobilityLevel": "STATIONARY"
        },
        "nstVersion": "1.0"
    }
},
    {"nstInfoId":"49c1af90-e3e3-4af1-ade4-35015f83fdb9",
    "nsTemplateId":"string",
    "name":"string",
    "nsTemplateVersion":"string",
    "designer":"string",
    "operationalState":None,
    "usageState":None,
    "deletionPending":False,
    "sst":None,
    "userDefinedData":{},
    "nst":{
        "nsdId": "1",
        "nsdVersion": "1.0",
        "nsstIds": [
            "1"
        ],
        "nstId": "5",
        "nstName": "Dense Urban",
        "nstProvider": "string",
        "nstServiceProfile": {
            "availability": 100,
            "coverageAreaTAList": [
                "ITAV"
            ],
            "eMBBPerfReq": [
                {
                    "activityFactor": 10,
                    "areaTrafficCapDL": 750,
                    "areaTrafficCapUL": 125,
                    "coverage": "DOWNTOWN",
                    "expDataRateDL": 300,
                    "expDataRateUL": 50,
                    "uESpeed": 60,
                    "userDensity": 25000
                }
            ],
            "latency": 2,
            "maxNumberofUEs": 10,
            "pLMNIdList": [
                "string"
            ],
            "resourceSharingLevel": True,
            "sST": "EMBB",
            "serviceProfileId": "string",
            "uEMobilityLevel": "STATIONARY"
        },
        "nstVersion": "1.0"
    }
},
    {"nstInfoId":"49c1af90-e3e3-4af1-ade4-35015f83fdb9",
    "nsTemplateId":"string",
    "name":"string",
    "nsTemplateVersion":"string",
    "designer":"string",
    "operationalState":None,
    "usageState":None,
    "deletionPending":False,
    "sst":None,
    "userDefinedData":{},
    "nst":{
        "nsdId": "1",
        "nsdVersion": "1.0",
        "nsstIds": [
            "1"
        ],
        "nstId": "10",
        "nstName": "Discrete Automation",
        "nstProvider": "string",
        "nstServiceProfile": {
            "availability": 100,
            "coverageAreaTAList": [
                "ITAV"
            ],
            "latency": 2,
            "maxNumberofUEs": 10,
            "pLMNIdList": [
                "string"
            ],
            "resourceSharingLevel": True,
            "sST": "URLLC",
            "serviceProfileId": "string",
            "uEMobilityLevel": "STATIONARY",
            "uRLLCPerfReq": [
                {
                    "cSAvailability": 99.99,
                    "connDensity": 100000,
                    "e2eLatency": 10,
                    "expDataRate": 10,
                    "jitter": 0,
                    "payloadSize": "BIG",
                    "reliability": 99.99,
                    "serviceAreaDimension": "1000x1000x30",
                    "survivalTime": 0,
                    "trafficDensity": 1000
                }
            ]
        },
        "nstVersion": "1.0"
    }
},
    {"nstInfoId":"49c1af90-e3e3-4af1-ade4-35015f83fdb9",
    "nsTemplateId":"string",
    "name":"string",
    "nsTemplateVersion":"string",
    "designer":"string",
    "operationalState":None,
    "usageState":None,
    "deletionPending":False,
    "sst":None,
    "userDefinedData":{},
    "nst":{
        "nsdId": "1",
        "nsdVersion": "1.0",
        "nsstIds": [
            "1"
        ],
        "nstId": "14",
        "nstName": "Eletricity Distribution(High)",
        "nstProvider": "string",
        "nstServiceProfile": {
            "availability": 100,
            "coverageAreaTAList": [
                "ITAV"
            ],
            "latency": 2,
            "maxNumberofUEs": 10,
            "pLMNIdList": [
                "string"
            ],
            "resourceSharingLevel": True,
            "sST": "URLLC",
            "serviceProfileId": "string",
            "uEMobilityLevel": "STATIONARY",
            "uRLLCPerfReq": [
                {
                    "cSAvailability": 99.9999,
                    "connDensity": 1000,
                    "e2eLatency": 5,
                    "expDataRate": 10,
                    "jitter": 0,
                    "payloadSize": "SMALL",
                    "reliability": 99.999,
                    "serviceAreaDimension": "200000x1x1",
                    "survivalTime": 10,
                    "trafficDensity": 100
                }
            ]
        },
        "nstVersion": "1.0"
    }
}
]


vsis = [{
        "vsiId": 1,
        "name": "PortoAveiro",
        "description": "Porto Aveiro Vertical Service",
        "vsdId": 1,
        "status": "LIVE",
        "errorMessage": "NONE",
        "externalInterconnections": ["teste"],
        "monitoringUrl": "www.test.com",
        "internalInterconnections": {"teste": "teste"}
        }]


cookies = {}


@app.route('/login', methods=['POST'])
@cross_origin(supports_credentials=True)
def login():
    if request.form.get("username") in [y["username"] for x in groups for y in x["tenants"] if x["name"] == "admin"]:
        resp = make_response("")
        token = token_urlsafe(64)
        cookies[token] = request.form.get("username")
        resp.set_cookie('JSESSION', token)
    else:
        resp = make_response("")
        token = token_urlsafe(64)
        cookies[token] = request.form.get("username")
        resp.set_cookie('JSESSION', token)
    return resp


@app.route('/vs/whoami')
@cross_origin(supports_credentials=True)
def whoami():
    username = cookies[request.cookies.get("JSESSION")]

    for group in groups:
        for tenant in group["tenants"]:
            if tenant["username"] == username:
                t = tenant.copy()
                t["role"] = "TENANT" if group["name"] != "admin" else "ADMIN"
                return t


# -----------------Groups and Tenants------------------


@app.route('/vs/admin/group')
@cross_origin(supports_credentials=True)
def getGroups():
    return jsonify(groups)


@app.route('/vs/admin/groups/tenants')
@cross_origin(supports_credentials=True)
def getTenants():
    tenants = [y for x in groups for y in x["tenants"]]
    return jsonify(tenants)


@app.route('/vs/admin/group/<groupName>/tenant')
@cross_origin(supports_credentials=True)
def getGroupTenants(groupName):
    tenants = [x["tenants"] for x in groups if x["name"] == groupName][0]
    return jsonify(tenants)


@app.route("/vs/admin/group/<groupName>", methods=["POST"])
@cross_origin(supports_credentials=True)
def insertGroup(groupName):
    existing = [x["name"] for x in groups]
    if groupName in existing:
        return "", 400
    groups.append({"name": groupName, "tenants": []})
    return ""


@app.route("/vs/admin/group/<groupName>", methods=["DELETE"])
@cross_origin(supports_credentials=True)
def deleteGroup(groupName):
    group = [x for x in groups if x["name"] == groupName][0]
    groups.remove(group)
    return ""


@app.route("/vs/admin/group/<groupName>/tenant", methods=["POST"])
@cross_origin(supports_credentials=True)
def insertTenantInGroup(groupName):
    data = json.loads(request.data)
    data["allocatedResources"] = {"diskStorage": 0, "vCPU": 0, "memoryRAM": 0}
    data["sla"] = []
    group = [x for x in groups if x["name"] == groupName][0]
    group["tenants"].append(data)
    return ""


@app.route("/vs/admin/group/<groupName>/tenant/<tenantName>", methods=["DELETE"])
@cross_origin(supports_credentials=True)
def deleteTenantInGroup(groupName, tenantName):
    group = [x for x in groups if x["name"] == groupName][0]
    tenant = [x for x in group["tenants"] if x["username"] == tenantName][0]
    group["tenants"].remove(tenant)
    return ""


@app.route("/vs/admin/group/<groupName>/tenant/<tenantName>/sla", methods=["POST"])
@cross_origin(supports_credentials=True)
def createSLA(groupName, tenantName):
    sla = json.loads(request.data)
    group = [x for x in groups if x["name"] == groupName][0]
    tenant = [x for x in group["tenants"] if x["username"] == tenantName][0]
    del sla["tenant"]
    sla["id"] = tenant["sla"][-1]["id"]+1 if len(tenant["sla"]) > 0 else 1
    tenant["sla"].append(sla)
    return ""


@app.route("/vs/admin/group/<groupName>/tenant/<tenantName>/sla")
@cross_origin(supports_credentials=True)
def getSLA(groupName, tenantName):
    group = [x for x in groups if x["name"] == groupName][0]
    tenant = [x for x in group["tenants"] if x["username"] == tenantName][0]
    return jsonify(tenant["sla"])


@app.route("/vs/admin/group/<groupName>/tenant/<tenantName>/sla/<slaId>", methods=["DELETE"])
@cross_origin(supports_credentials=True)
def deleteSLA(groupName, tenantName, slaId):
    group = [x for x in groups if x["name"] == groupName][0]
    tenant = [x for x in group["tenants"] if x["username"] == tenantName][0]
    sla = [x for x in tenant["sla"] if x["id"] == int(slaId)][0]
    tenant["sla"].remove(sla)
    return ""


# ---------------Domains------------------
@app.route("/domainLayer/catalogue")
@cross_origin(supports_credentials=True)
def getDomains():
    return jsonify(domains)


@app.route("/domainLayer/catalogue", methods=["POST"])
@cross_origin(supports_credentials=True)
def newDomain():
    data=json.loads(request.data)
    domainIds=[x["domainId"] for x in domains]
    if data["domainId"] in domainIds:
        return "Invalid Domain Id", 500
    domains.append(data)
    return ""

@app.route("/domainLayer/catalogue/<domainId>",methods=["DELETE"])
@cross_origin(supports_credentials=True)
def deleteDomain(domainId):
    domain=[x for x in domains if x["domainId"]==domainId][0]
    domains.remove(domain)
    return ""

# --------------Blueprints----------------


@app.route('/vs/catalogue/vsblueprint')
@cross_origin(supports_credentials=True)
def blueprint():
    return jsonify(blueprints)


@app.route("/vs/catalogue/vsblueprint", methods=["POST"])
@cross_origin(supports_credentials=True)
def addBlueprint():
    data = json.loads(request.data)
    blueprint = data["vsBlueprint"]
    out = {"vsBlueprintId": blueprints[-1]["vsBlueprintId"]+1, "name": blueprint["name"],
           "vsBlueprintVersion": blueprint["version"], "vsBlueprint": blueprint}
    out["onBoardedNsdInfoId"] = []
    out["onBoardedNstInfoId"] = []
    out["onBoardedVnfPackageInfoId"] = []
    out["onBoardedMecAppPackageInfoId"] = []
    out["activeVsdId"] = []
    blueprints.append(out)
    return str(out["vsBlueprintId"])


@app.route("/vs/catalogue/vsblueprint/<blueprintId>", methods=["DELETE"])
@cross_origin(supports_credentials=True)
def deleteBlueprint(blueprintId):
    blueprintId = int(blueprintId)
    blueprint = [x for x in blueprints if x["vsBlueprintId"]
                 == blueprintId][0]
    blueprints.remove(blueprint)
    return ""


@app.route("/vs/catalogue/vsblueprint/<blueprintId>")
@cross_origin(supports_credentials=True)
def getBlueprint(blueprintId):
    blueprintId = int(blueprintId)
    blueprint = [x for x in blueprints if x["vsBlueprintId"] == blueprintId][0]
    return jsonify(blueprint)


# --------------descriptors------------------------


@app.route('/vs/catalogue/vsdescriptor')
@cross_origin(supports_credentials=True)
def getDescriptors():
    return jsonify(descriptors)


@app.route('/vs/catalogue/vsdescriptor/<descriptorId>')
@cross_origin(supports_credentials=True)
def getDescriptorInfo(descriptorId):
    descriptorId = int(descriptorId)
    descriptor = [
        x for x in descriptors if x["vsDescriptorId"] == descriptorId][0]
    return jsonify(descriptor)


@app.route("/vs/catalogue/vsdescriptor", methods=["POST"])
@cross_origin(supports_credentials=True)
def addDescriptor():
    vsd = json.loads(request.data)["vsd"]
    currentVsdIds = [x["vsDescriptorId"] for x in descriptors]
    currentVsdIds.sort()
    vsd["vsDescriptorId"] = currentVsdIds[-1]+1
    descriptors.append(vsd)
    return str(vsd["vsDescriptorId"] )


@app.route("/vs/catalogue/vsdescriptor/<descriptorId>", methods=["DELETE"])
@cross_origin(supports_credentials=True)
def deleteDescriptor(descriptorId):
    descriptorId = int(descriptorId)
    descriptor = [
        x for x in descriptors if x["vsDescriptorId"] == descriptorId][0]
    descriptors.remove(descriptor)
    return ""


# ---------------------netslices-----------------------


# @app.route('/vs/admin/nsmf/networksliceids')
# @cross_origin(supports_credentials=True)
# def networkslicesIDS():
#     return jsonify([x["nsiId"] for x in netslices])


# @app.route('/vs/admin/nsmf/networkslice/<nsiId>')
# @cross_origin(supports_credentials=True)
# def networksliceById(nsiId):
#     nsiId = int(nsiId)
#     nsi = [x for x in netslices if x["nsiId"] == nsiId][0]
#     return jsonify(nsi)


@app.route('/vs/basic/nslcm/ns')
@cross_origin(supports_credentials=True)
def networkslices():
    return jsonify(netslices)


@app.route('/vs/basic/nslcm/ns', methods=["POST"])
@cross_origin(supports_credentials=True)
def insertNS():
    ns = json.loads(request.data)
    nssID = [x["nsiId"] for x in netslices]
    nssID.sort()
    tmpNS = [x for x in netslices if x["nsiId"] == nssID[-1]][0].copy()
    tmpNS["nsiId"] = nssID[-1]+1
    tmpNS["name"] = ns["name"]
    tmpNS["description"] = ns["description"]
    tmpNS["status"] = "OFFLINE"
    netslices.append(tmpNS)
    return jsonify(netslices)


@app.route('/ns/catalogue/nstemplate')
@cross_origin(supports_credentials=True)
def getNSTemplates():
    return jsonify(nstemplates)


@app.route("/ns/catalogue/nstemplate", methods=["POST"])
@cross_origin(supports_credentials=True)
def addNst():
    nst = json.loads(request.data)["nst"]
    nstemplates.append(nst)
    return ""


@app.route("/ns/catalogue/nstemplate/<nstId>", methods=["DELETE"])
@cross_origin(supports_credentials=True)
def removeNst(nstId):
    nst = [x for x in nstemplates if x["nst"]["nstId"] == nstId][0]
    nstemplates.remove(nst)
    return ""

@app.route("/vs/basic/nslcm/ns/<nsiId>/action/modify", methods=["PUT"])
@cross_origin(supports_credentials=True)
def modifyNS(nsiId):
    netslice = [x for x in netslices if x["nsiId"]==int(nsiId)][0]
    data = json.loads(request.data)
    for key in data:
        if data[key] != "":
            netslice[key]=data[key]
    return ""

@app.route("/vs/basic/nslcm/ns/<nsiId>/action/terminate", methods=["PUT"])
@cross_origin(supports_credentials=True)
def terminateNS(nsiId):
    netslice = [x for x in netslices if x["nsiId"]==int(nsiId)][0]
    netslice["status"]="OFFLINE"
    return ""

@app.route("/vs/basic/nslcm/ns/<nsiId>/action/instantiate", methods=["PUT"])
@cross_origin(supports_credentials=True)
def instantiateNS(nsiId):
    netslice = [x for x in netslices if x["nsiId"]==int(nsiId)][0]
    netslice["status"]="ONLINE"
    return ""


# ----------------vertical slices--------------------


@app.route('/vs/basic/vslcm/vsId')
@cross_origin(supports_credentials=True)
def verticalslices():
    return jsonify([x["vsiId"] for x in vsis])


@app.route('/vs/basic/vslcm/vs/<vsiId>')
@cross_origin(supports_credentials=True)
def verticalslicesID(vsiId):
    vsiId = int(vsiId)
    vsi = [x for x in vsis if x["vsiId"] == vsiId][0]
    return jsonify(vsi)


@app.route("/vs/basic/vslcm/vs", methods=["POST"])
@cross_origin(supports_credentials=True)
def instantiateVS():
    vsi = json.loads(request.data)
    print(vsi)
    currentVsiIds = [x["vsiId"] for x in vsis]
    currentVsiIds.sort()
    vsi["vsiId"] = currentVsiIds[-1]+1
    del vsi["userData"]
    del vsi["tenantId"]
    vsi["status"] = "LIVE"
    vsis.append(vsi)
    return ""


@app.route("/vs/basic/vslcm/vs/<vsiId>/terminate", methods=["POST"])
@cross_origin(supports_credentials=True)
def terminateVS(vsiId):
    vsiId = int(vsiId)
    vsi = [x for x in vsis if x["vsiId"] == vsiId][0]
    vsi["status"] = "OFFLINE"
    return ""


@app.route("/vs/basic/vslcm/vs/<vsiId>", methods=["DELETE"])
@cross_origin(supports_credentials=True)
def deleteVS(vsiId):
    vsiId = int(vsiId)
    vsi = [x for x in vsis if x["vsiId"] == vsiId][0]
    vsis.remove(vsi)
    return ""


@app.route("/vs/basic/vslcm/vs/<vsiId>", methods=["PUT"])
@cross_origin(supports_credentials=True)
def updateVS(vsiId):
    data = json.loads(request.data)
    vsiId = int(vsiId)
    vsi = [x for x in vsis if x["vsiId"] == vsiId][0]
    vsi["vsdId"] = data["vsdId"]
    return ""

requestCounter=0
timestamps={}
with open('values.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Request", 'Step', 'DeltaTime'])

@app.route("/startTimer/<stage>", methods=["POST"])
@cross_origin(supports_credentials=True)
def startTimer(stage):
    global requestCounter
    global timestamps
    timestamp=request.form["timestamp"]
    timestamps[str(requestCounter)+stage]=timestamp
    return ""

@app.route("/stopTimer/<stage>", methods=["POST"])
@cross_origin(supports_credentials=True)
def stopTimer(stage):
    global requestCounter
    global timestamps
    timestamp=request.form["timestamp"]
    final=float(timestamp)-float(timestamps[str(requestCounter)+stage])
    with open('values.csv', 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([str(requestCounter), stage, str(final)])

    if stage=="2":
        requestCounter+=1

    return ""

if __name__ == '__main__':
    #firefox modo headless
    app.run(host="0.0.0.0", port=8082)
