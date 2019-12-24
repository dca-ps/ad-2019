from enums.event_type import EventType
from enums.client_type import ClientType

class Event:
    def __init__(self, event_type : EventType, event_start_time, client_type : ClientType):
        self.event_type = event_type
        self.event_start_time = event_start_time
        self.client_type = client_type

    def __str__(self):
        return '{' + str(self.event_type) + ', ' + str(self.event_start_time) + ', ' + str(self.client_type) + '}'