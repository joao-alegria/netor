from osmclient import client
from osmclient.common.exceptions import ClientException
import io
import requests
import time

def getNS(domainIp, nsId):
    tmpClient = client.Client(host=domainIp)
    return tmpClient.ns.get(nsId)

def instantiateNS(domainIp, nsName, nsdName, account, additionalConf=None):
    tmpClient = client.Client(host=domainIp)
    #valueExtraction
    # requests.post("http://192.168.0.100:9999/stopTimer/1", data={"timestamp":str(round(time.time()*1000))})
    return tmpClient.ns.create(nsd_name=nsdName, nsr_name=nsName, account=account, config=additionalConf)

def sendActionNS(domainIp, nsId, additionalConf=None):
    tmpClient = client.Client(host=domainIp)
    actionId=tmpClient.ns.exec_op(nsId, "action", op_data=additionalConf, wait=True)
    actionInfo=tmpClient.ns.get_op(actionId)
    return actionInfo

def modifyNS(domainIp):
    return

def terminateNS(domainIp, nsName):
    tmpClient = client.Client(host=domainIp)
    #valueExtraction
    # requests.post("http://192.168.0.100:9999/stopTimer/2", data={"timestamp":str(round(time.time()*1000))})
    return tmpClient.ns.delete(nsName)

def getNSI(domainIp, nsiId):
    tmpClient = client.Client(host=domainIp)
    return tmpClient.nsi.get(nsiId)

def instantiateNSI(domainIp,nsiName,nstName,account, additionalConf=None):
    tmpClient = client.Client(host=domainIp)
    #valueExtraction
    # requests.post("http://192.168.0.100:9999/stopTimer/1", data={"timestamp":str(round(time.time()*1000))})
    tmpClient.nsi.create(nst_name=nstName,nsi_name=nsiName,account=account,config=additionalConf)

    nsiId=tmpClient.nsi.get(nsiName)["id"]
    return nsiId

def sendActionNSI(domainIp, nsiId, additionalConf):
    tmpClient = client.Client(host=domainIp)
    actionId=tmpClient.nsi.exec_op(nsiId, "action", op_data=additionalConf)
    actionInfo=tmpClient.nsi.get_op(actionId)
    return actionInfo

def modifyNSI(domainIp):
    return 

def terminateNSI(domainIp,nsiName):
    tmpClient = client.Client(host=domainIp)
    #valueExtraction
    # requests.post("http://192.168.0.100:9999/stopTimer/2", data={"timestamp":str(round(time.time()*1000))})
    return tmpClient.nsi.delete(nsiName)
