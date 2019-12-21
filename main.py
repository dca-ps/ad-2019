import numpy
import auxiliar.functions as aux
from entities.queue import Queue
from entities.event import Event
from enums.tipo_evento import TipoEvento


def run_queue(lmbd, mi, simulation_total_rounds, simulation_total_time):
    mean_persons_on_system = 0
    mean_persons_per_round = []

    for rounds_counter in range(1, simulation_total_rounds):
    
        simulation_time = 0
        simulation_queue = Queue()
        persons_counter = 0
        persons_served = 0
        last_event_time = 0
        area_under_persons_chart = 0
        arrival_time = numpy.random.exponential()
        service_end_time = simulation_total_time

        arrival_time = numpy.random.exponential()
        simulation_queue.push(Event(TipoEvento.Arrival, arrival_time))

        while simulation_time <= simulation_total_time and (not simulation_queue.emptyQueue()):
            event = simulation_queue.pop()

            if event.eventType is TipoEvento.Arrival:
                simulation_time = arrival_time
                area_under_persons_chart += persons_counter * (simulation_time - last_event_time)
                persons_counter += 1
                last_event_time = simulation_time
                arrival_time = simulation_time + numpy.random.exponential()
                simulation_queue.push(Event(TipoEvento.Arrival, arrival_time))

                if persons_counter == 1:
                    service_end_time = simulation_time + numpy.random.exponential()
                    simulation_queue.push( Event(TipoEvento.Departure, service_end_time) )
                
            elif event.eventType is TipoEvento.Departure:
                simulation_time = service_end_time
                area_under_persons_chart += persons_counter * (simulation_time - last_event_time)
                persons_counter -= 1
                last_event_time = simulation_time
                persons_served += 1

                if persons_counter > 0:
                    service_end_time = simulation_time + numpy.random.exponential()
                    simulation_queue.push( Event(TipoEvento.Departure, service_end_time) )

        mean_persons_per_round.append(area_under_persons_chart / simulation_total_time)


    for i in range(0, len(mean_persons_per_round)):
        mean_persons_on_system += (mean_persons_per_round[i]) / simulation_total_rounds

    analytic_utilisation = lmbd / mi
    personsOnSystemVariance = 0

    for i in range(0, len(mean_persons_per_round)):
        personsOnSystemVariance += \
            numpy.power(mean_persons_per_round[i] - mean_persons_on_system, 2) / numpy.maximum( len(mean_persons_per_round) - 1, 1)

    persons_on_system_standard_deviation = numpy.sqrt(personsOnSystemVariance)

    confidence_interval_end_points = \
        aux.confidence_interval(
            persons_on_system_standard_deviation,
            mean_persons_on_system,
            len(mean_persons_per_round)
        )

    analytic_mean_persons_on_system = aux.little_law(lmbd, mi)

    print("Lambda " + str(lmbd))
    print("Mi " + str(mi))
    print("Pessoas Servidas " + str(persons_served))
    print("Pessoas médias analíticas no sistema " + str(analytic_mean_persons_on_system))
    print("Média de pessoas no sistema " + str(mean_persons_on_system))
    print("Intervalo de confiança " + str(confidence_interval_end_points))
    print("Utilização analítica " + str(analytic_utilisation))
    print("Pessoas no desvio padrão do sistema " + str(persons_on_system_standard_deviation))
            
    


def simulate(lmbd, mu):
    for step in numpy.arange(lmbd, 0.9, 0.05):
        run_queue(step, mu, 10000, 100)





simulate(.12, .13)