from rabbitmq.messaging import MessageReceiver
import logging

if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)

    messageReceiver=MessageReceiver()
    messageReceiver.start()