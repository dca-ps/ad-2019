import numpy, random, math
from entities.interval import Interval

SEED_FILENAME = 'seed'

def little_law(lambd, mi):
    rho = lambd / mi
    return rho / (1 - rho)

def confidence_interval(standard_deviation, sample_mean, sample_size):
    interval = 1.96 * (standard_deviation / numpy.sqrt(sample_size))
    return Interval(sample_mean - interval, sample_mean + interval)

def create_random_generator():
    # recuperando a ultima semente utilizada pelo gerador de numeros aleatorios (se existir)
    generator = random
    try:
        seed = open(SEED_FILENAME, 'r').read()
        generator.seed(seed)
    except:
        pass

    def exponencial(lambd):
        x = generator.random()
        ret = - math.log(1.0 - x) / lambd
        return ret

    generator.exponential = exponencial
    return generator

def save_generator_state(generator):
    # A semente do gerador de numeros aleatorios eh persistida em arquivo para ser utilizada na proxima execucao do programa
    final_state = generator.getstate()
    file = open(SEED_FILENAME, 'w')
    file.write(str(final_state))