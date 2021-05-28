import json

class Evento:
    def __init__(self, data_hora,sensor, valor):
        self.data_hora = data_hora
        self.sensor = sensor
        self.valor = valor

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)        