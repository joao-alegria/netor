from osmclient import client
from osmclient.common.exceptions import ClientException
import io
from contextlib import redirect_stdout

def getNS(domainIp, nsId):
    return

def instantiateNS(domainIp, nsName, nsdName, account, additionalConf=None):
    tmpClient = client.Client(host=domainIp)
    return tmpClient.ns.create(nsd_name=nsdName, nsr_name=nsName, account=account, config=additionalConf)

def sendActionNS(domainIp, nsId, additionalConf=None):
    # {'member_vnf_index': '2', 'primitive': 'addpeer', 'primitive_params': {'peer_endpoint': '192.168.222.9','peer_key' : 'NkdhJEf/ExUiDbQA38h/sn7wjScr3tbCeFLNb2W2cVQ=','peer_network': '10.0.0.1/32'}}
    tmpClient = client.Client(host=domainIp)
    return tmpClient.ns.exec_op(nsId, "action", op_data=additionalConf)

def modifyNS(domainIp):
    return

def terminateNS(domainIp, nsName):
    tmpClient = client.Client(host=domainIp)
    return tmpClient.ns.delete(nsName)

def queryNS(domainIp):
    return 

def getNSI(domainIp, nsiId):
    tmpClient = client.Client(host=domainIp)
    return tmpClient.nsi.get(nsiId)

def instantiateNSI(domainIp,nsiName,nstName,account, additionalConf=None):
    tmpClient = client.Client(host=domainIp)
    f = io.StringIO()
    with redirect_stdout(f):
        tmpClient.nsi.create(nst_name=nstName,nsi_name=nsiName,account=account,config=additionalConf)
    nsiId = f.getvalue()
    return nsiId.strip()

def sendActionNSI(domainIp, nsiId, additionalConf):
    # {'member_vnf_index': '2', 'primitive': 'addpeer', 'primitive_params': {'peer_endpoint': '192.168.222.9','peer_key' : 'NkdhJEf/ExUiDbQA38h/sn7wjScr3tbCeFLNb2W2cVQ=','peer_network': '10.0.0.1/32'}}
    tmpClient = client.Client(host=domainIp)
    return tmpClient.nsi.exec_op(nsiId, "action", op_data=additionalConf)

def modifyNSI(domainIp):
    return 

def terminateNSI(domainIp,nsiName):
    tmpClient = client.Client(host=domainIp)
    return tmpClient.nsi.delete(nsiName)

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