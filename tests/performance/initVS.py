import requests
import time

TOKEN="o8rAy7MQKCNU4Td9wZ2zE43iGyIUQn"

data={
    "name":"testNST",
    "description":"test",
    "vsdId":"60ca601412002d67ff294e67",
    "vsiId":"1",
    "domainPlacements":[
        {
            "domainId":"ITAV",
            "componentName":"1_1-testNST"
        },
        {
            "domainId":"DETI",
            "componentName":"1_2-testNST"
        }
    ],
    "additionalConf":[
        {
            "componentName":"1_1-testNST",
            "conf":"{\"netslice-subnet\": [{\"id\": \"interdomain-tunnel-peer\", \"additionalParamsForVnf\": [{\"member-vnf-index\": \"1\", \"additionalParams\": {\"use_data_interfaces\": \"false\"}}]}]}"
        },{
            "componentName":"1_2-testNST",
            "conf":"{\"netslice-subnet\": [{\"id\": \"interdomain-tunnel-peer\", \"additionalParamsForVnf\": [{\"member-vnf-index\": \"1\", \"additionalParams\": {\"use_data_interfaces\": \"false\"}}]}]}"
        }
    ]
}

for i in range(1,2):
    data["vsiId"]=str(i)
    print(requests.post("http://localhost:9999/startTimer/1", data={"timestamp":str(round(time.time()*1000))}))
    print(requests.post("http://localhost/lcm/vs", headers={"Authorization":"Bearer "+TOKEN}, json=data).text)
    time.sleep(1)
    # print(requests.post("http://localhost:9999/startTimer/2", data={"timestamp":str(round(time.time()*1000))}))
    # print(requests.delete("http://localhost/lcm/vs/"+str(i), headers={"Authorization":"Bearer "+TOKEN}, json=data).text)
    # time.sleep(1)


# cookie={"JSESSIONID":"EE7139F74575A3CE9C3F554DA7A60D45"}

# data={
# 	"name":"t0",
# 	"description":"t0",
# 	"vsdId":"19",
# 	"tenantId":"itav",
# 	"userData": {},
# 	"locationConstraints":{}
# }

# for i in range(2,102):
#     print(requests.post("http://localhost:9999/startTimer/1", data={"timestamp":str(round(time.time()*1000))}))
#     vsiId=requests.post("http://localhost:8082/vs/basic/vslcm/vs", json=data, cookies=cookie).text
#     print(vsiId)
#     time.sleep(1)
#     print(requests.post("http://localhost:9999/startTimer/2", data={"timestamp":str(round(time.time()*1000))}))
#     print(requests.post("http://localhost:8082/vs/basic/vslcm/vs/"+vsiId+"/terminate", json=data, cookies=cookie).text)
#     time.sleep(1)