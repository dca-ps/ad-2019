import numpy
import auxiliar.functions as aux
import auxiliar.begining as begin
import auxiliar.run_queue as run_queue


# Recuperando a ultima semente utilizada pelo gerador de numeros aleatorios (se existir)
random_generator = aux.create_random_generator()


lambdas_question_1 = (round(n, 2) for n in numpy.arange(.05, .91, .05)) # 0.05, 0.1, 0.15, . . . , 0.9
lambdas_question_2 = (round(n, 2) for n in numpy.arange(.05, .61, .05)) # 0.05, 0.1, 0.15, . . . , 0.6
lambdas_question_3 = (round(n, 2) for n in numpy.arange(.05, .61, .05)) # 0.05, 0.1, 0.15, . . . , 0.6
lambdas = (lambdas_question_1, lambdas_question_2, lambdas_question_3)
mi = 1
n_rodadas = 10
total_time = 10000

def simulate(chosen_scenario, mu1, mu2, lambdas1, lambda2, priority, preempcao, distribution_type):
    results = []
    for lambda1 in lambdas1:
        mean_persons_on_system, confidence_interval, analytic_mean_persons_on_system = \
            run_queue.run_queue_parallel(lambda1, lambda2, mu1, mu2, n_rodadas,
                                         total_time, priority, preempcao, distribution_type, random_generator)
        results.append((lambda1, mean_persons_on_system, confidence_interval, analytic_mean_persons_on_system))
    aux.plot(chosen_scenario, results, lambda2)

def init():
    chosen_scenario = begin.get_scenario()
    begin.call_simulation(simulate, chosen_scenario, lambdas)

init()
aux.save_generator_state(random_generator)