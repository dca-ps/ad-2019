import numpy
from entities.interval import Interval

def little_law(lmbd, mi):
    rho = lmbd / mi
    return rho / (1 - rho)

def confidence_interval(standard_deviation, sample_mean, sample_size):
    interval = 1.96 * (standard_deviation / numpy.sqrt(sample_size))
    return Interval(sample_mean - interval, sample_mean + interval)