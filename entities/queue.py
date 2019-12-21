class Queue:
    def __init__(self):
        self.array = []

    def __str__(self):
        string = ''
        for element in self.array:
            string += str(element) + ' '
        return string

    def sortEvents(self, event):
        return event.event_start_time

    def push(self, element):
        self.array.append(element)
        self.array.sort(key=self.sortEvents)

    def pop(self):
        return self.array.pop()

    def emptyQueue(self):
        return not self.array