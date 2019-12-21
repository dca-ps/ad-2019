class Interval:
    def __init__(self, lowEndPoint, highEndPoint):
        self.lowEndPoint = lowEndPoint
        self.highEndPoint = highEndPoint
    def __str__(self):
        return '{' + str(self.lowEndPoint) + ', ' + str(self.highEndPoint) + '}'