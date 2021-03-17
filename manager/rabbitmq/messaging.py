from rabbitmq.adaptor import Messaging
import json
from threading import Thread
from manager import VSMF

class MessageReceiver(Thread):

    def __init__(self):
        super().__init__()
        self.messaging=Messaging()
        self.messaging.createExchange("vsLCM_Management")
        self.messaging.consumeExchange("vsLCM_Management",self.callback)

    def callback(self, channel, method_frame, header_frame, body):
        print(" [x] Received %r" % body)
        data=json.loads(body)
        vsmf=VSMF(data["vsiId"], data)
        vsmf.start()

    def run(self):
        print(' [*] Waiting for messages. To exit press CTRL+C')
        self.messaging.startConsuming()