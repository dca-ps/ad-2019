import numpy, random
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
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
    plt.xlabel('Taxa média de chegada classe 1 [cliente/s]')
    plt.ylabel('Tempo médio no sistema (s)')
    plt.title('Taxa chegada classe 2: '+ str(lambda2) + str(' [cliente/s]'))
    markersize = 3
    blue_label = mpatches.Patch(color='blue', label='Simulação')
    red_label = mpatches.Patch(color='red', label='Resultado analítico')
    try:
        x, y, errors, analytical_result = zip(*results)
        error_lists = [list(e) for e in zip(*errors)]
        (yerror_bellow, yerror_above) = __interval_in_confidence_points(y, error_lists)
        plt.errorbar(x, y, yerr=[yerror_bellow, yerror_above], fmt=':o',
                     label='Simulacao', markersize=markersize)
        plt.plot(x, analytical_result, ':rd', markersize=markersize)
        plt.legend(handles=[blue_label, red_label])
        plt.plot()
        # plt.show()
        plt.savefig('charts/cenario' + str(chosen_scenario) + '_lambda_'  + str(round(lambda2, 2)) + '.png')
    except Exception as e:
        print('Erro na geracao do grafico:\t' + str(e))
    plt.close('all')

def __interval_in_confidence_points(y_values, error_lists):
    yerror_bellow = []
    yerror_above = []
    for y, error_bellow, error_above in zip(y_values, error_lists[0], error_lists[1]):
        yerror_bellow.append(y - error_bellow)
        yerror_above.append(error_above - y)
    return (yerror_bellow, yerror_above)

