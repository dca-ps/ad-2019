import numpy, random
import matplotlib.pyplot as plt
from entities.interval import Interval
from enums.client_type import ClientType
from enums.distribution_type import DistributionType

SEED_FILENAME = 'seed'

def little_law(lambd1, lambd2, mi1, mi2):
    rho = (lambd1 + lambd2) / (mi1 + mi2)
    return rho / (1 - rho)

def confidence_interval(standard_deviation, sample_mean, sample_size):
    interval = 1.96 * (standard_deviation / numpy.sqrt(sample_size))
    return (sample_mean - interval, sample_mean + interval)

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
        ret = - numpy.log(1.0 - x) / lambd
        return ret

    generator.exponential = exponencial
    return generator

def save_generator_state(generator):
    # A semente do gerador de numeros aleatorios eh persistida em arquivo para ser utilizada na proxima execucao do programa
    final_state = generator.getstate()
    file = open(SEED_FILENAME, 'w')
    file.write(str(final_state))

def next_client_type(lambda1, lambda2):
    n = lambda1 + lambda2
    prob1 = lambda1/n
    x = random.random()
    if(x<=prob1):
        return ClientType.One
    else:
        return ClientType.Two

#Função para calcular o instante de saida.
def exit_time_calculation(event, mi, simulation_time, distribution_type, random_generator):
    if distribution_type == DistributionType.exp :
        return simulation_time + random_generator.exponential(mi)
    if distribution_type == DistributionType.med:
        return simulation_time + 1/mi
    if distribution_type == DistributionType.unif:
        return simulation_time + random.uniform(5,15) if \
            event.client_type == ClientType.One else simulation_time + random.uniform(1,3)


def plot(chosen_scenario, results, lambda2):
    plt.xlabel('Taxa média de chegada (classe 1 / s)')
    plt.ylabel('Tempo médio no sistema (s)')
    plt.title('Taxa chegada classe 2: '+ str(lambda2))
    try:
        x, y, errors = zip(*results)
        plt.plot(x, y)
        errors_lists = [list(e) for e in zip(*errors)]
        lolims = errors_lists[0]
        uplims = errors_lists[1]
        plt.errorbar(x, y, lolims=lolims, uplims=uplims, marker='|', markersize=8,
            linestyle='none')
        # plt.show()
        plt.savefig('charts/cenario' + str(chosen_scenario) + '_lambda2_'  + str(round(lambda2, 2)) + '.png')
    except Exception as e:
        print('Dados insuficientes:\t' + str(e))
    plt.close('all')

