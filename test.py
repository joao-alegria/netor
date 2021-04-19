# import redis
# import json

# r=redis.Redis(password="netorRedisPassword")
# # r.hset(10, "createVsi", 0)
# # print(r.hgetall(10))

# allVsiData={}
# for key,value in r.hgetall(11).items():
#     allVsiData[key.decode("UTF-8")]=json.loads(value)

# print(allVsiData)

from osmclient import client 

c = client.Client(host="10.0.12.118")
# c.nsi.create(nst_name="interdomain_nst",nsi_name="test",account="microstack",config=additionalConf)

nsiInfo=c.ns.get("test1.interdomain-ns_2")
print(nsiInfo)