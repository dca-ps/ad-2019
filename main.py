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
    return Interval(sampleMean - 1.96*(standardDeviation/numpy.sqrt(sampleSize)), sampleMean + 1.96*(standardDeviation/numpy.sqrt(sampleSize)))

def runQueue(lmbd, mu, simulationTotalRounds, simulationTotalTime):
    meanPersonsOnSystem = 0
    meanPersonsPerRound = []

    for roundsCounter in range(1, simulationTotalRounds):
    
        simulationTime = 0
        simulationQueue = Queue()
        personsCounter = 0
        personsServed = 0
        lastEventTime = 0
        areaUnderPersonsChart = 0
        arrivalTime = numpy.random.exponential()
        serviceEndTime = simulationTotalTime

        arrivalTime = numpy.random.exponential()
        simulationQueue.push(Event("Arrival",arrivalTime))

        while simulationTime <= simulationTotalTime and (not simulationQueue.emptyQueue()):
            event = simulationQueue.pop()

            if event.eventType is 'Arrival':
                simulationTime = arrivalTime
                areaUnderPersonsChart += personsCounter * (simulationTime - lastEventTime)
                personsCounter += 1
                lastEventTime = simulationTime
                arrivalTime = simulationTime + numpy.random.exponential()
                simulationQueue.push(Event("Arrival", arrivalTime))

                if personsCounter == 1:
                    serviceEndTime = simulationTime + numpy.random.exponential()
                    simulationQueue.push(Event("Departure", serviceEndTime))
                
            elif event.eventType is 'Departure':
                simulationTime = serviceEndTime
                areaUnderPersonsChart += personsCounter * (simulationTime - lastEventTime)
                personsCounter -= 1
                lastEventTime = simulationTime
                personsServed += 1

                if personsCounter > 0:
                    serviceEndTime = simulationTime + numpy.random.exponential()
                    simulationQueue.push(Event("Departure", serviceEndTime))
        meanPersonsPerRound.append(areaUnderPersonsChart/simulationTotalTime)


    for i in range(0, len(meanPersonsPerRound)):
        meanPersonsOnSystem += (meanPersonsPerRound[i])/simulationTotalRounds
    analyticUtilisation = lmbd/mu
    personsOnSystemVariance = 0
    for i in range(0, len(meanPersonsPerRound)):
        personsOnSystemVariance += numpy.power(meanPersonsPerRound[i]-meanPersonsOnSystem,2)/numpy.maximum(len(meanPersonsPerRound)-1,1)

    personsOnSystemStandardDeviation = numpy.sqrt(personsOnSystemVariance)

    confidenceIntervalEndPoints = confidenceInterval(personsOnSystemStandardDeviation,meanPersonsOnSystem,len(meanPersonsPerRound))

    analyticMeanPersonsOnSystem = littleLaw(lmbd,mu)

    print("Lambda " + str(lmbd))
    print("Mu " + str(mu))
    print("Pessoas Servidas " + str(personsServed))
    print("Pessoas médias analíticas no sistema " + str(analyticMeanPersonsOnSystem))
    print("Média de pessoas no sistema " + str(meanPersonsOnSystem))
    print("Intervalo de confiança " + str(confidenceIntervalEndPoints))
    print("Utilização analítica " + str(analyticUtilisation))
    print("Pessoas no desvio padrão do sistema " + str(personsOnSystemStandardDeviation))
            
    


def simulate(lmbd, mu):
    for step in numpy.arange(lmbd, 0.9, 0.05):
        runQueue(step, mu, 10000, 100)





simulate(.12, .13)