import requests
import time

TOKEN="64XBY7CsHFwDTfn9qmFbXU1iFkuIMb"

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
    time.sleep(0.5)


# cookie={"JSESSIONID":"EF3700199EEF2FBDF9558292C6E6F6A1"}

# data={
# 	"name":"t0",
# 	"description":"t0",
# 	"vsdId":"19",
# 	"tenantId":"5growth",
# 	"userData": {},
# 	"locationConstraints":{}
# }

# for i in range(1,100):
#     print(requests.post("http://localhost:9999/startTimer/1", data={"timestamp":str(round(time.time()*1000))}))
#     print(requests.post("http://localhost:8082/vs/basic/vslcm/vs", json=data, cookies=cookie).text)
#     time.sleep(0.5)