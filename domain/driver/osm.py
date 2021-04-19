from osmclient import client
from osmclient.common.exceptions import ClientException
import io

def getNS(domainIp, nsId):
    tmpClient = client.Client(host=domainIp)
    return tmpClient.ns.get(nsId)

def instantiateNS(domainIp, nsName, nsdName, account, additionalConf=None):
    tmpClient = client.Client(host=domainIp)
    return tmpClient.ns.create(nsd_name=nsdName, nsr_name=nsName, account=account, config=additionalConf)

def sendActionNS(domainIp, nsId, additionalConf=None):
    tmpClient = client.Client(host=domainIp)
    return tmpClient.ns.exec_op(nsId, "action", op_data=additionalConf)

def modifyNS(domainIp):
    return

def terminateNS(domainIp, nsName):
    tmpClient = client.Client(host=domainIp)
    return tmpClient.ns.delete(nsName)

def getNSI(domainIp, nsiId):
    tmpClient = client.Client(host=domainIp)
    return tmpClient.nsi.get(nsiId)

def instantiateNSI(domainIp,nsiName,nstName,account, additionalConf=None):
    tmpClient = client.Client(host=domainIp)
    tmpClient.nsi.create(nst_name=nstName,nsi_name=nsiName,account=account,config=additionalConf)

    nsiId=tmpClient.nsi.get(nsiName)["id"]
    return nsiId

def sendActionNSI(domainIp, nsiId, additionalConf):
    tmpClient = client.Client(host=domainIp)
    return tmpClient.nsi.exec_op(nsiId, "action", op_data=additionalConf)

def modifyNSI(domainIp):
    return 

def terminateNSI(domainIp,nsiName):
    tmpClient = client.Client(host=domainIp)
    return tmpClient.nsi.delete(nsiName)

# def instantiateNSSI(domainIp):
#     return 

# def modifyNSSI(domainIp):
#     return 

# def terminateNSSI(domainIp):
#     return 
