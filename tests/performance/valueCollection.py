from flask import Flask, request, make_response, jsonify
from flask_cors import CORS, cross_origin
import json
from secrets import token_urlsafe
import csv
import time

app = Flask(__name__)
cors = CORS(app, support_credentials=True)

requestCounter=0
timestamps=[]
with open('values.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Request", 'Step', 'DeltaTime'])

@app.route("/startTimer/<stage>", methods=["POST"])
@cross_origin(supports_credentials=True)
def startTimer(stage):
    global requestCounter
    global timestamps

    requestCounter+=1

    # timestamp=request.form["timestamp"]
    timestamp=time.time()*1000
    timestamps.append(timestamp)
    return ""

@app.route("/stopTimer/<stage>", methods=["POST"])
@cross_origin(supports_credentials=True)
def stopTimer(stage):
    global requestCounter
    global timestamps
    if len(timestamps)==0:
        return ""
    # timestamp=request.form["timestamp"]
    timestamp=time.time()*1000
    final=float(timestamp)-float(timestamps[0])
    del timestamps[0]
    print(stage+": "+str(final))
    with open('values.csv', 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([str(requestCounter), stage, final])

    return ""

if __name__ == '__main__':
    #firefox modo headless
    app.run(host="0.0.0.0", port=9999)
