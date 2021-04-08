import pika
import config

class Messaging:

    def __init__(self):
        super().__init__()
        credentials = pika.PlainCredentials(config.RABBIT_USER, config.RABBIT_PASS)
        self.parameters = pika.ConnectionParameters(host=config.RABBIT_IP,port=config.RABBIT_PORT,credentials=credentials,connection_attempts=10,retry_delay=5,socket_timeout=None)

    def createQueue(self, name):
        connection = pika.BlockingConnection(self.parameters)
        channel = connection.channel()
        channel.queue_declare(queue=name, durable=True)

    def createExchange(self, name):
        connection = pika.BlockingConnection(self.parameters)
        channel = connection.channel()
        channel.exchange_declare(name, exchange_type='fanout')

    def consumeQueue(self, name, callback, ack=True):
        connection = pika.BlockingConnection(self.parameters)
        channel = connection.channel()
        channel.basic_consume(queue=name, on_message_callback=callback, auto_ack=ack)

    def consumeExchange(self, name, callback, ack=True):
        connection = pika.BlockingConnection(self.parameters)
        channel = connection.channel()
        result = channel.queue_declare(queue='', exclusive=True)
        queue_name = result.method.queue
        channel.queue_bind(exchange=name, queue=queue_name)
        channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=ack)

    def publish2Queue(self, queue, message):
        connection = pika.BlockingConnection(self.parameters)
        channel = connection.channel()
        channel.basic_publish(exchange='', routing_key=queue, body=message)

    def publish2Exchange(self, exchange, message):
        connection = pika.BlockingConnection(self.parameters)
        channel = connection.channel()
        channel.basic_publish(exchange=exchange, routing_key='', body=message)

    def startConsuming(self):
        connection = pika.BlockingConnection(self.parameters)
        channel = connection.channel()
        channel.start_consuming()

    def stopConsuming(self):
        connection = pika.BlockingConnection(self.parameters)
        channel = connection.channel()
        channel.stop_consuming()
