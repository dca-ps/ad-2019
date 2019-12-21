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
        self.array.sort(key = lambda e : e.event_start_time, reverse = True)

    def pop(self):
        return self.array.pop()

    def is_queue_empty(self):
        return len(self.array) == 0