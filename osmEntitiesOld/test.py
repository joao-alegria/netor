from osmclient import client
from osmclient.common.exceptions import ClientException
import io
from contextlib import redirect_stdout

myClient = client.Client(host="10.0.12.118")
# print(myClient.ns.exec_op("77aef1ca-f419-4de0-855a-e5a1996e6989", "action", op_data={'member_vnf_index': '1', 'primitive': 'getvnfinfo', 'primitive_params': {}}, wait=True))

print(myClient.ns.exec_op("77aef1ca-f419-4de0-855a-e5a1996e6989", "action", op_data={'member_vnf_index': '1', 'primitive': 'modifytunnel', 'primitive_params': {"bandwidth":"15"}}, wait=True))

# print(myClient.ns.exec_op("53d397bf-7a02-4ba2-958a-1708af349231", "action", op_data={'member_vnf_index': '2', 'primitive': 'addpeer', 'primitive_params': {'peer_endpoint': '192.168.222.9','peer_key' : 'NkdhJEf/ExUiDbQA38h/sn7wjScr3tbCeFLNb2W2cVQ=','peer_network': '10.0.0.1/32'}}))

# print(myClient.nsi.delete("45fb6beb-2327-4436-b0c5-52d923a21f4e"))

# f = io.StringIO()
# with redirect_stdout(f):
#     myClient.nsi.create(nst_name="interdomain_nst",nsi_name="test",account="microstack",config="{netslice-subnet: [{id: interdomain-ns_1, additionalParamsForVnf: [{member-vnf-index: '1', additionalParams: {tunnel_address: 10.0.0.1/24, tunnel_id: '1', ns_id: interdomain-ns_1, vnf_id: '1'}}]}, {id: interdomain-ns_2, additionalParamsForVnf: [{member-vnf-index: '1', additionalParams: {tunnel_address: 10.0.0.2/24, tunnel_id: '2', ns_id: interdomain-ns_2, vnf_id: '1'}}]}]}")
# out = f.getvalue()
# print(out.strip())
# from threading import Thread

# class test(Thread):
#     def run(self):
#          print(myClient.ns.get("80991eec-91a9-41e9-b53e-848c92f64684"))

# try:
#     for a in range(10):
#         t=test()
#         t.start()
#         print(a)
# except:
#     print("aqui")
# print("banana")
