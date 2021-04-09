import requests
import time

cookie={"JSESSIONID":"A6D90A37CCFD26C35A65A04BBA7B67A3"}

data={
	"name":"t0",
	"description":"t0",
	"vsdId":"23",
	"tenantId":"user",
	"userData": {},
	"locationConstraints":{}
}

for i in range(1,100):
    print(requests.post("http://localhost:8082/startTimer/1", data={"timestamp":str(round(time.time()*1000))}))
    print(requests.post("http://10.0.12.121:8082/vs/basic/vslcm/vs", json=data, cookies=cookie).json())