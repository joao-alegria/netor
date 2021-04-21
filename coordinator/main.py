from api.controller import app
from rabbitmq.messaging import MessageReceiver
import config
import logging

if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)
    logging.getLogger('pika').propagate=False

    messageReceiver=MessageReceiver()
    messageReceiver.start()

    # app.debug = True
    app.secret_key = config.APP_SECRET
    app.run(host="0.0.0.0",port=config.APP_PORT)