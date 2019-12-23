from enums.tipo_evento import TipoEvento

class Event:
    def __init__(self, event_type : TipoEvento, event_start_time, event_class):
        self.event_type = event_type
        self.event_start_time = event_start_time
        self.event_class = event_class

    def __str__(self):
        return '{' + str(self.event_type) + ', ' + str(self.event_start_time) + ', ' + str(self.event_class) + '}'