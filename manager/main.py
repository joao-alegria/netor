from rabbitmq.messaging import MessageReceiver

if __name__ == '__main__':
    messageReceiver=MessageReceiver()
    messageReceiver.start()