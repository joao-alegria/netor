from osmclient import client
from osmclient.common.exceptions import ClientException

def instantiateNS(domainIp, nsName, nsdName, account, additionalConf=None):
    tmpClient = client.Client(host=domainIp)
    tmpClient.ns.create(nsd_name=nsdName, nsr_name=nsName, account=account, config=additionalConf)
    return 

def sendActionNS(domainIp, nsId, additionalConf):
    # {'member_vnf_index': '2', 'primitive': 'addpeer', 'primitive_params': {'peer_endpoint': '192.168.222.9','peer_key' : 'NkdhJEf/ExUiDbQA38h/sn7wjScr3tbCeFLNb2W2cVQ=','peer_network': '10.0.0.1/32'}}
    tmpClient = client.Client(host=domainIp)
    tmpClient.ns.exec_op(nsId, "action", op_data=additionalConf)
    return

def modifyNS(domainIp):
    return

def terminateNS(domainIp, nsName):
    tmpClient = client.Client(host=domainIp)
    tmpClient.ns.delete(nsName)
    return 

def queryNS(domainIp):
    return 

def instantiateNSI(domainIp,nsiName,nstName,account, additionalConf):
    tmpClient = client.Client(host=domainIp)
    tmpClient.nsi.create(nst_name=nstName,nsi_name=nsiName,account=account,config=additionalConf)
    return 

def modifyNSI(domainIp):
    return 

def terminateNSI(domainIp,nsiName):
    tmpClient = client.Client(host=domainIp)
    tmpClient.nsi.delete(nsiName)
    return 

def queryNSI(domainIp):
    return 

def instantiateNSSI(domainIp):
    return 

def modifyNSSI(domainIp):
    return 

def terminateNSSI(domainIp):
    return 

def queryNSSI(domainIp):
    return 