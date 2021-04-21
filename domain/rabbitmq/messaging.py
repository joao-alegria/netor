from rabbitmq.adaptor import Messaging
import json
from threading import Thread
import db.persistance as persistance
import service
import logging

class MessageReceiver(Thread):

    def __init__(self):
        Thread.__init__(self)
        self.messaging=Messaging()
        self.messaging.createExchange("vsLCM_Management")
        self.messaging.createQueue("vsDomain")
        self.messaging.consumeExchange("vsLCM_Management",self.callback)
        self.messaging.consumeQueue("vsDomain",self.myCallback)

    def myCallback(self, channel, method, properties, body):
        logging.info("ActionHandler - Received {}".format(body))
        data=json.loads(body)
        handler=service.DomainActionHandler(data)
        handler.start()

    def callback(self, ch, method, properties, body):
        logging.info("Received Message {}".format(body))
        data=json.loads(body)
        # messaging.consumeQueue("vsLCM_"+str(data["vsiId"]),simplecallback)
        if data["msgType"] == "createVSI":
            try:
                domainsId=service.getDomainsIds()
                message={"vsiId":data["vsiId"],"msgType":"domainInfo", "data":domainsId, "error":False}
                self.messaging.publish2Exchange("vsLCM_"+str(data["vsiId"]), json.dumps(message))
                logging.info("sent message:" + str(message))
            except Exception as e:
                message={"vsiId":data["vsiId"],"msgType":"domainInfo", "error":True, "message":"Error when fetching domains ids: "+str(e)}
                self.messaging.publish2Exchange("vsLCM_"+str(data["vsiId"]), json.dumps(message))

    def stop(self):
        try:
            self.messaging.stopConsuming()
        except Exception as e:
            logging.error("Pika exception: "+str(e))

    def run(self):
        try:
            logging.info('Started Consuming RabbitMQ Topics')
            self.messaging.startConsuming()
        except Exception as e:
            logging.info("Stop consuming now!")
            logging.error("Pika exception: "+str(e))    