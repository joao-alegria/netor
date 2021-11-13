import pika
import os


RABBIT_USERNAME = os.environ.get('RABBIT_USERNAME', 'admin')
RABBIT_PASSWORD = os.environ.get('RABBIT_PASSWORD', 'admin')
RABBIT_HOST = os.environ.get('RABBIT_HOST', 'localhost')


class Messaging:

    def __init__(self):
        super().__init__()
        self.credentials = pika.PlainCredentials(RABBIT_USERNAME, RABBIT_PASSWORD)
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=RABBIT_HOST, credentials=self.credentials))
        self.channel = self.connection.channel()

    def createQueue(self, name):
        self.channel.queue_declare(queue=name, durable=True)

    def createExchange(self, name):
        self.channel.exchange_declare(name, exchange_type='fanout')

    def consumeQueue(self, name, callback):
        self.channel.basic_consume(queue=name, on_message_callback=callback, auto_ack=True)

    def consumeExchange(self, name, callback):
        result = self.channel.queue_declare(queue='', exclusive=True)
        queue_name = result.method.queue
        self.channel.queue_bind(exchange=name, queue=queue_name)
        self.channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)

    def publish2Queue(self, queue, message):
        self.channel.basic_publish(exchange='', routing_key=queue, body=message)

    def publish2Exchange(self, exchange, message):
        self.channel.basic_publish(exchange=exchange, routing_key='', body=message)

    def startConsuming(self):
        self.channel.start_consuming()

    def stopConsuming(self):
        self.channel.stop_consuming()
