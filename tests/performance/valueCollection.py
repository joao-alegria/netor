from flask import Flask, request, make_response, jsonify
from flask_cors import CORS, cross_origin
import json
from secrets import token_urlsafe
import csv
import time

app = Flask(__name__)
cors = CORS(app, support_credentials=True)

# requestCounter=0
# timestamps={}

@app.route("/startTimer/<stage>", methods=["POST"])
@cross_origin(supports_credentials=True)
def startTimer(stage):
    # global requestCounter
    # global timestamps
    myfile = open('timestamps.txt', 'a')
    # requestCounter+=1

    timestamp=request.form["timestamp"]
    if stage=="1" or stage=="vsCreateId":
        myfile.write("New test\n")
    print(stage+": "+str(timestamp))
    myfile.write("startStage-"+stage+":"+str(timestamp)+"\n")
    # timestamp=time.time()*1000
    # if stage not in timestamps:
    #     timestamps[stage]=[]
    # timestamps[stage].append(timestamp)
    myfile.close()
    return ""

@app.route("/stopTimer/<stage>", methods=["POST"])
@cross_origin(supports_credentials=True)
def stopTimer(stage):
    myfile = open('timestamps.txt', 'a')
    # global requestCounter
    # global timestamps
    # if len(timestamps[stage])==0:
    #     return ""
    timestamp=request.form["timestamp"]
    print(stage+": "+str(timestamp))
    myfile.write("stopStage-"+stage+":"+str(timestamp)+"\n")
    # timestamp=time.time()*1000
    # final=float(timestamp)-float(timestamps[stage][0])
    # del timestamps[stage][0]
    # print(stage+": "+str(final))
    # with open('values.csv', 'a', newline='') as csvfile:
    #     writer = csv.writer(csvfile)
    #     writer.writerow([str(requestCounter), stage, final])
    myfile.close()
    return ""

if __name__ == '__main__':
    #firefox modo headless
    app.run(host="0.0.0.0", port=9999)
