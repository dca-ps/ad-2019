class Queue:
    def __init__(self):
        self.array = []

    def __str__(self):
        string = ''
        for element in self.array:
            string += str(element) + ' '
        return string

    def push(self, element):
        self.array.append(element)
        self.array = sorted(self.array, key = lambda e : (e.event_class, e.event_start_time,), reverse = True)
        print(*self.array)
        print('\n*********************************************************\n')

    def pop(self):
        return self.array.pop()
    
    def nextEvent(self):
        return next(iter(self.array))

    def is_queue_empty(self):
        return len(self.array) == 0