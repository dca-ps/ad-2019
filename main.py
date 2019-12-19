import math
import numpy


class Queue:
    def __init__(self):
        self.array = []

    def __str__(self):
        string = ''
        for element in self.array:
            string += str(element) + ' '
        return string

    def sortEvents(self, event):
        return event.eventStartTime

    def push(self, element):
        self.array.append(element)
        self.array.sort(key=self.sortEvents)

    def pop(self):
        return self.array.pop()

    def emptyQueue(self):
        return not self.array


class Event:
    def __init__(self, eventType, eventStartTime):
        self.eventType = eventType
        self.eventStartTime = eventStartTime
    def __str__(self):
        return '{' + self.eventType + ', ' + str(self.eventStartTime) + '}'


class Interval:
    def __init__(self, lowEndPoint, highEndPoint):
        self.lowEndPoint = lowEndPoint
        self.highEndPoint = highEndPoint
    def __str__(self):
        return '{' + str(self.lowEndPoint) + ', ' + str(self.highEndPoint) + '}'



def littleLaw(lmbd, mu):
    rho = lmbd/mu
    return rho/(1-rho)


def confidenceInterval(standardDeviation,sampleMean,sampleSize):
    return Interval(sampleMean - 1.96*(standardDeviation/math.sqrt(sampleSize)), sampleMean + 1.96*(standardDeviation/math.sqrt(sampleSize)))

def runQueue(step):
    print("{0:.5f}".format(step))

def simulate(lmbd, mu):
    for step in numpy.arange(lmbd, 0.9, 0.05):
        runQueue(step)





simulate(0.1, 2)