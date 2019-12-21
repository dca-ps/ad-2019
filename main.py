import numpy, math
import auxiliar.functions as aux
from entities.queue import Queue
from entities.event import Event
from enums.tipo_evento import TipoEvento


# recuperando a ultima semente utilizada pelo gerador de numeros aleatorios (se existir)
random_generator = aux.create_random_generator()

def run_queue(lambd, mi, simulation_total_rounds, simulation_total_time):

    mean_persons_on_system = 0
    mean_persons_per_round = []

    for _ in range(1, simulation_total_rounds):

        simulation_time = 0
        simulation_queue = Queue()
        persons_counter = 0
        served_persons = 0
        last_event_time = 0
        area_under_persons_chart = 0
        arrival_time = random_generator.exponential(lambd)
        service_end_time = simulation_total_time

        simulation_queue.push(Event(TipoEvento.Arrival, arrival_time))

        while simulation_time <= simulation_total_time and (not simulation_queue.is_queue_empty()):
            event = simulation_queue.pop()

            if event.event_type is TipoEvento.Arrival:
                simulation_time = arrival_time
                area_under_persons_chart += persons_counter * (simulation_time - last_event_time)
                persons_counter += 1
                last_event_time = simulation_time
                arrival_time = simulation_time + random_generator.exponential(lambd)
                simulation_queue.push(Event(TipoEvento.Arrival, arrival_time))

                if persons_counter == 1:
                    service_end_time = simulation_time + random_generator.exponential(mi)
                    simulation_queue.push( Event(TipoEvento.Departure, service_end_time) )

            elif event.event_type is TipoEvento.Departure:
                simulation_time = service_end_time
                area_under_persons_chart += persons_counter * (simulation_time - last_event_time)
                persons_counter -= 1
                last_event_time = simulation_time
                served_persons += 1

                if persons_counter > 0:
                    service_end_time = simulation_time + random_generator.exponential(mi)
                    simulation_queue.push( Event(TipoEvento.Departure, service_end_time) )

        mean_persons_per_round.append(area_under_persons_chart / simulation_total_time)


    for i in range(0, len(mean_persons_per_round)):
        mean_persons_on_system += (mean_persons_per_round[i]) / simulation_total_rounds

    analytic_utilisation = lambd / mi
    persons_on_system_variance = 0

    for i in range(0, len(mean_persons_per_round)):
        persons_on_system_variance += \
            math.pow(mean_persons_per_round[i] - mean_persons_on_system, 2) / max( len(mean_persons_per_round) - 1, 1)

    persons_on_system_standard_deviation = math.sqrt(persons_on_system_variance)

    confidence_interval_end_points = \
        aux.confidence_interval(
            persons_on_system_standard_deviation,
            mean_persons_on_system,
            len(mean_persons_per_round)
        )

    analytic_mean_persons_on_system = aux.little_law(lambd, mi)

    print("Lambda " + str(lambd))
    print("Mi " + str(mi))
    print("Pessoas Servidas " + str(served_persons))
    print("Pessoas médias analíticas no sistema " + str(analytic_mean_persons_on_system))
    print("Média de pessoas no sistema " + str(mean_persons_on_system))
    print("Intervalo de confiança " + str(confidence_interval_end_points))
    print("Utilização analítica " + str(analytic_utilisation))
    print("Pessoas no desvio padrão do sistema " + str(persons_on_system_standard_deviation) + "\n")


lambdas = (round(n, 2) for n in numpy.arange(.05, .91, .05)) # 0.05, 0.1, 0.15, . . . , 0.9
mi = .4

def simulate(mu):
    for lambd in lambdas:
        run_queue(lambd, mu, 2, 100000)


simulate(mi)


aux.save_generator_state(random_generator)