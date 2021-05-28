from flask import request, jsonify
from flask_restplus import Resource, fields
from api.restplus import api
from api.models.evento import Evento
from api.queue.operations import send_to_queue
from opentracing.ext import tags
from opentracing.propagation import Format
from api.traccing import tracing, opentracing_tracer

ns_evento = api.namespace('Evento', '')

evento_model = ns_evento.model('EventoPostModel', {
                    'dataHora': fields.DateTime(required=True),
                    'sensor': fields.String(required=True),
                    'valor': fields.Float(required=True)
                })

@ns_evento.route('/')
class EventoItem(Resource):
    
    @api.response(204, 'Evento inserido.')
    @ns_evento.doc(body=evento_model)    
    @tracing.trace()
    def post(self):

        evento = Evento(request.json['dataHora'], request.json['sensor'],request.json['valor'])
        send_to_queue(evento)
        return None, 204    
