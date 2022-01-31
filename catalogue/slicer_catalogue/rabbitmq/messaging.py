from rabbitmq.adaptor import Messaging
from rabbitmq.api_wrapper import get_info
from threading import Thread
import json


class MessageReceiver(Thread):

    def __init__(self):
        super().__init__()
        self.messaging = Messaging()
        self.messaging.consumeExchange("vsLCM_Management", self.callback)

    def callback(self, ch, method, properties, body):
        # print(" [x] Received status update %r" % body)
        content = json.loads(body)

        data = get_info(content)
        if data is not None:
            # self.messaging.publish2Exchange("vsLCM_"+str(content["vsiId"]), json.dumps(data))
            self.messaging.publish2Exchange("vsLCM_Management", json.dumps(data))

    def run(self):
        print(' [*] Waiting for messages. To exit press CTRL+C')
        self.messaging.startConsuming()
