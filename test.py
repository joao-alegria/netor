import redis
import json

# r=redis.Redis(password="netorRedisPassword", db=1)
# r.delete("3")
# print(r.hgetall(10))

# allVsiData={}
# for key,value in r.hgetall(11).items():
#     allVsiData[key.decode("UTF-8")]=json.loads(value)

# print(allVsiData)

from osmclient import client 

c = client.Client(host="10.0.12.118")
info=c.nst.list()
# # c.nsi.create(nst_name="interdomain_nst",nsi_name="test",account="microstack",config=additionalConf)

# info=c.ns.exec_op("63311c3b-7598-4406-a42b-f692a6982022", "action", op_data={'member_vnf_index': '1', 'primitive': 'getvnfinfo', 'primitive_params': {}}, wait=True)
# info=c.ns.get_op(info)
print(info)