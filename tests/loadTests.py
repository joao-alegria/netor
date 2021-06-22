from locust import HttpUser, TaskSet, between, task, events
import os
import json
import requests
#import time

# Change these variables if you wish to personalize the script

# These variables hold the codes of the errors that occur and their frequencies
# getFailures = {}
# postFailures = {}


# class UserBehavior(TaskSet):
    
#     def __init__(self):
#         super().__init__() 

#         self.host = "http://localhost"

#         self.totalUsers = 0
#         # maxUsers = int(os.environ["USERS"])
#         self.maxUsers = 10

#         parameters={'response_type': 'code','grant_type': 'password', 'client_id': 'portal', 'client_secret': 'portal', 'username': 'admin', 'password': 'admin'}
#         response = self.client.post(host+"/tenant/oauth/token", headers={"Content-Type": "application/json"}, data=parameters)

#         self.adminToken=response.json["access_token"]

#     @task
#     def get(self):
        
#         if self.totalUsers == self.maxUsers:
#             return
        
#         self.totalUsers+=1
#         #print("Total Purchase Attempts: "+str(UserBehavior.totalPurchaseAttempts))

#         #create user
#         createUser={"group": "user","username": "user"+self.totalUsers,"password": "test","role": "TENANT","storage": 100,"memory": 100,"vcpu": 100}

#         response = self.client.post(host+"/lcm/vs", headers={"Authorization": "Bearer " + self.adminToken, "Content-Type": "application/json"}, data=json.dumps(createUser))

#         #login user
#         parameters={'response_type': 'code','grant_type': 'password', 'client_id': 'portal', 'client_secret': 'portal', 'username': 'user'+self.totalUsers, 'password': 'test'}

#         response = self.client.post(host+"/tenant/oauth/token", headers={"Content-Type": "application/json"}, data=parameters)
#         token=response.json["access_token"]
#         #create VSI
#         vsiData={"name":"test","vsdId":"60ca601412002d67ff294e67","domainId":"ITAV","vsiId":self.totalUsers}
        
#         response = self.client.post(host+"/lcm/vs", headers={"Authorization": "Bearer " + token, "Content-Type": "application/json"}, data=json.dumps(vsiData))

        # response_code = int(str(response).split("[")[1].split("]")[0])
        # while response_code == 409: #"201" not in str(response):
        #     attempts = attempts-1
        #     if attempts == 0:
        #         #raise InterruptedError
        #         if response_code in postFailures.keys():
        #             postFailures[response_code] = postFailures[response_code] + 1
        #         else:
        #             postFailures[response_code] = 1
        #         print(postFailures)
        #         break
        #     response = self.client.post(r[len(r)-1][0], headers={"Authorization": "Token " + token, "Content-Type": "application/json"}, data=body)
        #     response_code = int(str(response).split("[")[1].split("]")[0])
        # if response_code > 299:
        #     if response_code in postFailures.keys():
        #         postFailures[response_code] = postFailures[response_code] + 1
        #     else:
        #         postFailures[response_code] = 1
        #     print(postFailures)
        
        # response = self.client.get(r[i][j], headers={"Authorization": "Token " + token})
        # response_code = int(str(response).split("[")[1].split("]")[0])
        # while response_code == 409: #"200" not in str(response):
        #     attempts = attempts-1
        #     if attempts == 0:
        #         #raise InterruptedError
        #         if response_code in getFailures.keys():
        #             getFailures[response_code] = getFailures[response_code] + 1
        #         else:
        #             getFailures[response_code] = 1
        #         print(getFailures)
        #         break
        #     response = self.client.get(r[i][j], headers={"Authorization": "Token " + token})
        #     response_code = int(str(response).split("[")[1].split("]")[0])
        # if response_code > 299:
        #     if response_code in getFailures.keys():
        #         getFailures[response_code] = getFailures[response_code] + 1
        #     else:
        #         getFailures[response_code] = 1
        #     print(getFailures)

ids=[i for i in range(1000,0,-1)]

parameters={'response_type': 'code','grant_type': 'password', 'client_id': 'portal', 'client_secret': 'portal', 'username': 'admin', 'password': 'admin'}
response = requests.post("http://localhost/tenant/oauth/token", params=parameters)

adminToken=response.json()["access_token"]


class WebsiteUser(HttpUser):
    wait_time = between(1,2)

    def on_start(self):
        self.identifier=ids.pop()
        print(self.identifier)
    
        createUser={"role":"TENANT","group": "user","username": "user_"+str(self.identifier),"password": "test","role": "TENANT","storage": 100,"memory": 100,"vcpu": 100}

        response = self.client.post("/tenant/tenant", headers={"Authorization": "Bearer " + adminToken, "Content-Type": "application/json"}, data=json.dumps(createUser))
        if response.status_code!=200:
            print(response.text)

        #login user
        parameters={'response_type': 'code','grant_type': 'password', 'client_id': 'portal', 'client_secret': 'portal', 'username': 'user_'+str(self.identifier), 'password': 'test'}

        response = self.client.post("/tenant/oauth/token", headers={"Content-Type": "application/json"}, params=parameters)
        if response.status_code!=200:
            print(response.text)

        self.token=response.json()["access_token"]
        #create VSI
        vsiData={"name":"test","description":"test","vsdId":"60ca601412002d67ff294e67","domainId":"ITAV","vsiId":str(self.identifier)}
        
        response = self.client.post("/lcm/vs", headers={"Authorization": "Bearer " + self.token, "Content-Type": "application/json"}, data=json.dumps(vsiData))
        if response.status_code!=200:
            print(response.text)
        

    def on_stop(self):
        print(self.token)
        parameters={'force': True}
        response = requests.delete("http://localhost/lcm/vs/"+str(self.identifier), headers={"Authorization": "Bearer " + self.token, "Content-Type": "application/json"}, params=parameters)
        if response.status_code!=200:
            print(response.text)

        response = requests.delete("http://localhost/tenant/tenant/user_"+str(self.identifier), headers={"Authorization": "Bearer " + adminToken, "Content-Type": "application/json"})
        if response.status_code!=200:
            print(response.text)


    @task
    def get(self):
        # if self.token:
        #     response = self.client.get("/lcm/vs", headers={"Authorization": "Bearer " + self.token, "Content-Type": "application/json"})
        #     if response.status_code!=200:
        #         print(response.text)
        return
        