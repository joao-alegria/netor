from rabbitmq.adaptor import Messaging
import json
from threading import Thread
import logging
from manager import stopPollingThread, newCSMF, getCSMF, deleteVsi, csmfs
import redisHandler as redis


class MessageReceiver(Thread):

    def __init__(self):
        super().__init__()
        self.messaging=Messaging()
        self.messaging.createExchange("vsLCM_Management")
        self.messaging.consumeExchange("vsLCM_Management",self.callback)

    def callback(self, channel, method_frame, header_frame, body):
        logging.info("Received Message {}".format(body))
        # exchange = method_frame.exchange
        data=json.loads(body)
        # if exchange=="vsLCM_Management":
        if data["msgType"]=="createVSI":
            newCSMF(data)
        elif data["msgType"]=="removeVSI":
            deleteVsi(data)
        else:
            vsiId=data["vsiId"]
            csmf=getCSMF(vsiId)
            if csmf:
                th=Thread(target=csmfs[vsiId].processAction, args=[data])
                th.start()
            else:
                logging.warning("VSI Id not found: "+data["vsiId"])
                
        # else:
        #     newCsmfMessage(data)

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
        stopPollingThread()
