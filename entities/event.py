from enums.tipo_evento import TipoEvento

class Event:
    def __init__(self, event_type : TipoEvento, event_start_time):
        self.event_type = event_type
        self.event_start_time = event_start_time

    def __str__(self):
        return '{' + self.event_type + ', ' + str(self.event_start_time) + '}'