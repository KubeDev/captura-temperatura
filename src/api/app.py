from flask import Flask, Blueprint 
from api.endpoints.evento import ns_evento
from api.restplus import api
from prometheus_flask_exporter import PrometheusMetrics

app = Flask(__name__)
metrics = PrometheusMetrics(app)

blueprint = Blueprint('api', __name__, url_prefix='/api')
api.init_app(blueprint)
api.add_namespace(ns_evento)
app.register_blueprint(blueprint)          

if __name__ == '__main__':
    app.run()