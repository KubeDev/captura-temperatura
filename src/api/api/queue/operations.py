import pika, os
from flask import jsonify
from api.traccing import tracing, opentracing_tracer
import opentracing

queue_host = os.getenv("QUEUE_HOST", "localhost")
queue = os.getenv("QUEUE", "evento")
routing_key = os.getenv("ROUTING_KEY", "evento")
exchange = os.getenv("EXCHANGE", "")


def send_to_queue(data):
    
    span = tracing.get_span()

    with opentracing_tracer.start_span(operation_name="evento-no-rabbitmq",child_of=span) as spanrb:
        spanrb.set_tag("teste-rb", "teste")

        text_carrier = {}
        opentracing_tracer.inject(span, opentracing.Format.TEXT_MAP, text_carrier)

        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=queue_host,credentials=pika.credentials.PlainCredentials(username='logUser', password='logPwd',erase_on_connect=False)))
        channel = connection.channel()
        channel.queue_declare(queue=queue,durable=True)
        channel.basic_publish(exchange=exchange, routing_key=routing_key, body=data.toJSON(),properties=pika.BasicProperties(headers=text_carrier))
        connection.close()

