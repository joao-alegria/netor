import requests
import time

# TOKEN="K5vCTQ95aPhZg28QIxX3NSumJa2wth"

# data={
#     "name":"testNovelNST",
#     "description":"test",
#     "vsdId":"60d1b13065b67bdc757b66c3",
#     "vsiId":"1",
#     "domainPlacements":[
#         {
#             "domainId":"ITAV",
#             "componentName":"1_1-testNovelNST"
#         },
#         {
#             "domainId":"DETI",
#             "componentName":"1_2-testNovelNST"
#         }
#     ],
#     "additionalConf":[
#         {
#             "componentName":"1_1-testNovelNST",
#             "conf":"{\"netslice-subnet\": [{\"id\": \"interdomain-tunnel-peer\", \"additionalParamsForVnf\": [{\"member-vnf-index\": \"1\", \"additionalParams\": {\"use_data_interfaces\": \"false\", \"netorIp\": \"10.0.12.117/manager/interdomain\"}}]}]}"
#         },{
#             "componentName":"1_2-testNovelNST",
#             "conf":"{\"netslice-subnet\": [{\"id\": \"interdomain-tunnel-peer\", \"additionalParamsForVnf\": [{\"member-vnf-index\": \"1\", \"additionalParams\": {\"use_data_interfaces\": \"false\",\"netorIp\": \"10.0.12.117/manager/interdomain\"}}]}]}"
#         }
#     ]
# }

# for i in range(1,2):
#     data["vsiId"]=str(i)
#     # print(requests.post("http://10.0.12.117:9999/startTimer/1", data={"timestamp":str(round(time.time()*1000))}))
#     # print(requests.post("http://10.0.12.117/lcm/vs", headers={"Authorization":"Bearer "+TOKEN}, json=data).text)
#     # time.sleep(1)
#     print(requests.post("http://10.0.12.117:9999/startTimer/2", data={"timestamp":str(round(time.time()*1000))}))
#     print(requests.delete("http://10.0.12.117/lcm/vs/"+str(i), headers={"Authorization":"Bearer "+TOKEN}, json=data).text)
#     time.sleep(1)

ip="http://10.0.12.121"
cookie={"JSESSIONID":"7FC6067624FE4EFBD20141B7A199E25E"}
action=input("Action: ")

if not (action == "1" or action=="2"):
    exit()

data={
	"name":"a",
	"description":"a",
	"vsdId":"22",
	"tenantId":"itav",
	"userData": {
        "nsstId.20fd69b4-bbb3-44d5-87e5-5111b2609712.domain":"ITAV",
        "nsstId.0a56925a-3db4-4e76-b5b9-bf6a8fb6d8d1.domain":"DETI"
	},
	"locationConstraints":{}
}

if action=="1":
    m=int(input("Number of instances: "))
    for i in range(0,m):
        # currentTime=str(round(time.time()*1000))
        # print(requests.post(ip+":9999/startTimer/1", data={"timestamp":currentTime}))
        # print(requests.post(ip+":9999/startTimer/3", data={"timestamp":currentTime}))
        vsiId=requests.post(ip+":8082/vs/basic/vslcm/vs", json=data, cookies=cookie).text
        print(vsiId)
        time.sleep(1)

elif action=="2":
    vsis=[]
    vsi="a"
    while not vsi=="":
        vsi=input("VSI: ")
        if vsi!="":
            vsis.append(vsi)
    for vsiId in vsis:
        # currentTime=str(round(time.time()*1000))
        # print(requests.post(ip+":9999/startTimer/4", data={"timestamp":currentTime}))
        # print(requests.post(ip+":9999/startTimer/5", data={"timestamp":currentTime}))
        print(requests.post(ip+":8082/vs/basic/vslcm/vs/"+vsiId+"/terminate", cookies=cookie).text)
        time.sleep(1)


