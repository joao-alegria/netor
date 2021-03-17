from api.controller import app
from rabbitmq.messaging import MessageReceiver

if __name__ == '__main__':
    messageReceiver=MessageReceiver()
    messageReceiver.start()

    app.debug = True
    app.secret_key = 'tenantManager'
    app.run(port=5000)