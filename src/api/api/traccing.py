import logging
from jaeger_client import Config
from flask_opentracing import FlaskTracing
from os import getenv

JAEGER_HOST = getenv('JAEGER_HOST', 'localhost')

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
            'local_agent': {'reporting_host': JAEGER_HOST}
        },
        service_name=service,
    )

    return config.initialize_tracer()

opentracing_tracer = init_tracer(__name__)
tracing = FlaskTracing(opentracing_tracer)