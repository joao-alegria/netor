from rabbitmq.messaging import MessageReceiver
import logging

if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)
    logging.getLogger('pika').propagate=False

    messageReceiver=MessageReceiver()
    messageReceiver.setDaemon=False
    messageReceiver.start()