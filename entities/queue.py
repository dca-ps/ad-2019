class Queue:
    def __init__(self):
        self.array = []

    def __str__(self):
        string = ''
        for element in self.array:
            string += str(element) + ' '
        return string

    #IMPORTANTE!!!!!!
    #A chegada não tem prioridade, o que tem prioridade é a fila, por isso aqui não tem sort do tipo de evento.
    #Uma pessoa que não chegou ainda não tem prioridade sobre quem esta em atendimento.
    def push(self, element):
        self.array.append(element)
        self.array = sorted(self.array, key = lambda e :  e.event_start_time, reverse = True)
        #print("Fila de eventos futuros ")
        #print(*self.array)
        #print('\n*********************************************************\n')
        
    #Push com organização por prioridade.
    def push_queue(self, element):
        self.array.append(element)
        self.array = sorted(self.array, key = lambda e : (e.event_type, e.event_start_time,), reverse = True)
        #print("Fila de pessoas aguardando ")
        #print(*self.array)
        #print('\n*********************************************************\n')

    def pop(self):
        return self.array.pop()
    
    def nextEvent(self):
        return next(iter(self.array))

    def is_queue_empty(self):
        return len(self.array) == 0