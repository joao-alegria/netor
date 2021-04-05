from api.controller import app
from rabbitmq.messaging import MessageReceiver
import db.persistance as persistance

if __name__ == '__main__':
    persistance.initDB()

    messageReceiver=MessageReceiver()
    messageReceiver.start()

    app.debug = True
    app.secret_key = 'tenantManager'
    app.run(port=5001)