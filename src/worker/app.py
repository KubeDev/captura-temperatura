import pika
import os
from pymongo import MongoClient
import json
import opentracing
import logging
from jaeger_client import Config

queue_host = os.getenv("QUEUE_HOST", "localhost")
queue = os.getenv("QUEUE", "evento")
routing_key = os.getenv("ROUTING_KEY", "evento")
exchange = os.getenv("EXCHANGE", "")
queue_user = os.getenv("RABBITMQ_USER", "queueUser")
queue_pwd = os.getenv("RABBITMQ_USER", "queuePwd")

mongodb_db = os.getenv("MONGODB_DB", "admin")
mongodb_host = os.getenv("MONGODB_HOST", "localhost")
mongodb_port = int(os.getenv("MONGODB_PORT", "27017"))
mongodb_username = os.getenv("MONGODB_USERNAME", "mongouser")
mongodb_password = os.getenv("MONGODB_PASSWORD", "mongopwd")


def init_tracer(service):
    logging.getLogger('').handlers = []
    logging.basicConfig(format='%(message)s', level=logging.DEBUG)

    config = Config(
        config={
            'sampler': {
                'type': 'const',
                'param': 1,
            },
            'logging': True,
        },
        service_name=service,
    )

    return config.initialize_tracer()

opentracing_tracer = init_tracer("worker")

client = MongoClient("mongodb://" + mongodb_username + ":" + mongodb_password +"@" + mongodb_host + ":" + str(mongodb_port) + "/" + mongodb_db)
db = client[mongodb_db]

collection = db["evento"]

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host=queue_host,credentials=pika.credentials.PlainCredentials(username=queue_user, password=queue_pwd,erase_on_connect=False)))
channel = connection.channel()

channel.queue_declare(queue=queue, durable=True)

def callback(ch, method, properties, body):
    
    span_context = opentracing_tracer.extract(
        format=opentracing.Format.TEXT_MAP,
        carrier=properties.headers,
    )

    with opentracing_tracer.start_span(
        operation_name="evento-mongodb",
        child_of=span_context) as span:
        span.set_tag("teste", "teste")

        collection.insert_one(eval(body.decode()))
        ch.basic_ack(delivery_tag=method.delivery_tag)

channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue=queue, on_message_callback=callback)

channel.start_consuming()