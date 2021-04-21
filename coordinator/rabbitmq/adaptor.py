import pika
import config

class Messaging:

    def __init__(self):
        credentials = pika.PlainCredentials(config.RABBIT_USER, config.RABBIT_PASS)
        self.parameters = pika.ConnectionParameters(host=config.RABBIT_IP,port=config.RABBIT_PORT,credentials=credentials,connection_attempts=10,retry_delay=5,socket_timeout=None)
        self.connection = pika.BlockingConnection(self.parameters)
        self.channel=self.connection.channel()

    def createQueue(self, name, durable=False, auto_delete=True):
        connection = pika.BlockingConnection(self.parameters)
        channel = connection.channel()
        channel.queue_declare(queue=name, durable=durable, auto_delete=auto_delete)
        channel.close()
        connection.close()

    def createExchange(self, name):
        connection = pika.BlockingConnection(self.parameters)
        channel = connection.channel()
        channel.exchange_declare(name, exchange_type='fanout')
        channel.close()
        connection.close()

    def consumeQueue(self, name, callback, ack=True):
        self.channel.basic_consume(queue=name, on_message_callback=callback, auto_ack=ack)

    def bindQueue2Exchange(self, exchange, queue ,durable=False, auto_delete=True, ack=True):
        connection = pika.BlockingConnection(self.parameters)
        channel = connection.channel()
        channel.queue_bind(exchange=exchange, queue=queue)
        channel.close()
        connection.close()

    def consumeExchange(self, name, callback, queue='',durable=False, auto_delete=True, ack=True):
        result = self.channel.queue_declare(queue=queue, exclusive=False, durable=durable, auto_delete=auto_delete)
        queue_name = result.method.queue
        self.channel.queue_bind(exchange=name, queue=queue_name)
        self.channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=ack)

    def publish2Queue(self, queue, message):
        connection = pika.BlockingConnection(self.parameters)
        channel = connection.channel()
        channel.basic_publish(exchange='', routing_key=queue, body=message)
        channel.close()
        connection.close()

    def publish2Exchange(self, exchange, message):
        connection = pika.BlockingConnection(self.parameters)
        channel = connection.channel()
        channel.basic_publish(exchange=exchange, routing_key='', body=message)
        channel.close()
        connection.close()

    def startConsuming(self):
        self.channel.start_consuming()

    def stopConsuming(self):
        self.channel.stop_consuming()
        self.channel.close()
        self.connection.close()
