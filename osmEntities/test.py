from osmclient import client
from osmclient.common.exceptions import ClientException

myClient = client.Client(host="10.0.12.118")
print(myClient.ns.exec_op("53d397bf-7a02-4ba2-958a-1708af349231", "action", op_data={'member_vnf_index': '1', 'primitive': 'addpeer', 'primitive_params': {'peer_endpoint': '192.168.222.146','peer_key': 'fBfSKYXGlLfnYSto1AC3CPvpoMNTWPkPY7xAxexNJWw=','peer_network': '10.0.0.2/32'}}))

print(myClient.ns.exec_op("53d397bf-7a02-4ba2-958a-1708af349231", "action", op_data={'member_vnf_index': '2', 'primitive': 'addpeer', 'primitive_params': {'peer_endpoint': '192.168.222.9','peer_key' : 'NkdhJEf/ExUiDbQA38h/sn7wjScr3tbCeFLNb2W2cVQ=','peer_network': '10.0.0.1/32'}}))

# print(myClient.ns.exec_op("1166000b-34b1-4973-b4d7-f0ecd9a32e36", "action", op_data={'member_vnf_index': '1', 'primitive': 'touch', 'primitive_params': {}}))