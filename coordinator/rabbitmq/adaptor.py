import pika
import config

class Messaging:

    def __init__(self):
        super().__init__()
        credentials = pika.PlainCredentials(config.RABBIT_USER, config.RABBIT_PASS)
        parameters = pika.ConnectionParameters(host=config.RABBIT_IP,port=config.RABBIT_PORT,credentials=credentials,connection_attempts=10,retry_delay=5,socket_timeout=None)
        self.connection = pika.BlockingConnection(parameters)
        self.channel = self.connection.channel()

    def createQueue(self, name):
        self.channel.queue_declare(queue=name, durable=True)

    def createExchange(self, name):
        self.channel.exchange_declare(name, exchange_type='fanout')

    def consumeQueue(self, name, callback, ack=True):
        self.channel.basic_consume(queue=name, on_message_callback=callback, auto_ack=ack)

    def consumeExchange(self, name, callback, ack=True):
        result = self.channel.queue_declare(queue='', exclusive=True)
        queue_name = result.method.queue
        self.channel.queue_bind(exchange=name, queue=queue_name)
        self.channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=ack)

    def publish2Queue(self, queue, message):
        self.channel.basic_publish(exchange='', routing_key=queue, body=message)

    def publish2Exchange(self, exchange, message):
        self.channel.basic_publish(exchange=exchange, routing_key='', body=message)

    def startConsuming(self):
        self.channel.start_consuming()

    def stopConsuming(self):
        self.channel.stop_consuming()
