import numpy
import auxiliar.functions as aux
from entities.queue import Queue
from entities.event import Event
from enums.event_type import EventType
from enums.client_type import ClientType


def run_queue_parallel(lambd1, lambd2, mi1, mi2, simulation_total_rounds,
                       simulation_total_time, priority, preempcao: bool,
                       departure_type, random_generator):

    mean_persons_on_system = 0
    mean_persons_per_round = []

    for _ in range(1, simulation_total_rounds):

        simulation_time = 0
        # Essa fila se refere aos eventos que ocorrerao no futuro
        simulation_queue = Queue()
        # Esta fila se refere aqueles que já chegaram mas ainda não foram processados,
        # eles não podem ser perdidos e tem prioridade de atendimento, visto que já estão na fila.
        waiting_queue = Queue()
        persons_counter = 0
        served_persons = 0
        last_event_time = 0
        area_under_persons_chart = 0
        service_end_time = simulation_total_time

        # Verifica qual caso entrara primeiro (cliente 1 ou 2)
        if aux.next_client_type(lambd1, lambd2) == ClientType.One:
            arrival_time = random_generator.exponential(lambd1)
            simulation_queue.push(Event(EventType.Arrival, arrival_time, ClientType.One))
        else:
            arrival_time = random_generator.exponential(lambd2)
            simulation_queue.push(Event(EventType.Arrival, arrival_time, ClientType.Two))

        while simulation_time <= simulation_total_time and (not simulation_queue.is_queue_empty()):
            # Pega o proximo evento que ira ocorrer (chegada ou saida)
            event = simulation_queue.pop()

            # Caso seja uma chegada
            if event.event_type is EventType.Arrival:
                simulation_time = arrival_time
                area_under_persons_chart += persons_counter * (simulation_time - last_event_time)
                # Aumento o numero de pessoas na fila
                persons_counter += 1
                # Pega o tempo do ultimo evento
                last_event_time = simulation_time

                # Cria o proximo evento de chegada
                if aux.next_client_type(lambd1, lambd2) == ClientType.One:
                    arrival_time = simulation_time + random_generator.exponential(lambd1)
                    simulation_queue.push(Event(EventType.Arrival, arrival_time, ClientType.One))
                else:
                    arrival_time = simulation_time + random_generator.exponential(lambd2)
                    simulation_queue.push(Event(EventType.Arrival, arrival_time, ClientType.Two))

                # Verifica se ele é o unico na fila e pode ser servido imediatamente
                if persons_counter == 1:
                    if event.client_type == ClientType.One:
                        service_end_time = \
                            aux.exit_time_calculation(event, mi1, simulation_time, departure_type, random_generator)
                    else:
                        service_end_time = \
                            aux.exit_time_calculation(event, mi2, simulation_time, departure_type, random_generator)
                    simulation_queue.push(Event(EventType.Departure, service_end_time, event.client_type))
                # Caso já haja um evento sendo servido ele deve ser mantido em uma fila,
                # pois ele chegou mas não sera atendido no momento
                # Precisamos saber de que tipo ele é tambem
                else:
                    # Este push tem que ordenar por prioridade de atendimento, pois estamos falando da fila de atendimento.
                    # **********************************************************************
                    # IMPORTANTE: Caso não haja prioridade, basta trocar por um push normal! (Implementado!)
                    # **********************************************************************
                    waiting_queue.push_queue(event) if priority else waiting_queue.push(event)

            # Caso seja uma saida
            elif event.event_type is EventType.Departure:

                simulation_time = service_end_time
                area_under_persons_chart += persons_counter * (simulation_time - last_event_time)
                # Diminui o numero de pessoas na fila
                persons_counter -= 1
                # Pega o tempo do ultimo evento
                last_event_time = simulation_time
                # Aumenta o numero de pessoas que foram servidas
                served_persons += 1
                # Verifica se há alguem na fila
                if persons_counter > 0:
                    # Pegamos o evento que chegou e esta aguardando e criamos seu evento de saida (Fila)
                    # Esta fila já esta ordenada para prioridade, se houver
                    event = waiting_queue.pop()
                    if event.client_type == 1:
                        service_end_time = \
                            aux.exit_time_calculation(event, mi1, simulation_time, departure_type, random_generator)
                    else:
                        service_end_time = \
                            aux.exit_time_calculation(event, mi2, simulation_time, departure_type, random_generator)
                    simulation_queue.push(Event(EventType.Departure, service_end_time, event.client_type))


        mean_persons_per_round.append(area_under_persons_chart / simulation_total_time)

    for i in range(0, len(mean_persons_per_round)):
        mean_persons_on_system += (mean_persons_per_round[i])
    mean_persons_on_system /= simulation_total_rounds

    # TODO: AJUSTAR AS METRICAS!!
    analytic_utilisation = (lambd1 + lambd2) / (mi1 + mi2)
    persons_on_system_variance = 0

    for i in range(0, len(mean_persons_per_round)):
        persons_on_system_variance += \
            numpy.power(mean_persons_per_round[i] - mean_persons_on_system, 2) / numpy.maximum( len(mean_persons_per_round) - 1, 1)

    persons_on_system_standard_deviation = numpy.sqrt(persons_on_system_variance)

    confidence_interval_end_points = \
        aux.confidence_interval(
            persons_on_system_standard_deviation,
            mean_persons_on_system,
            len(mean_persons_per_round)
        )

    analytic_mean_persons_on_system = aux.little_law(lambd1, lambd2, mi1, mi2)

    print("Lambda clientes 1: " + str(lambd1))
    print("Mi 1: " + str(mi1))
    print("Lambda clientes 2: " + str(lambd2))
    print("Mi 2: " + str(mi2))
    print("# pessoas Servidas: " + str(served_persons))
    print("# médio de pessoas (analítico): " + str(analytic_mean_persons_on_system))
    print("# médio de pessoas: " + str(mean_persons_on_system))
    print("Intervalo de confiança: " + str(confidence_interval_end_points))
    print("Utilização (analítico): " + str(analytic_utilisation))
    print("Pessoas no desvio padrão do sistema: " + str(persons_on_system_standard_deviation) + "\n")

    return (mean_persons_on_system, confidence_interval_end_points, analytic_mean_persons_on_system)