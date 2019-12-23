import numpy
import auxiliar.functions as aux
from entities.queue import Queue
from entities.event import Event
from enums.tipo_evento import TipoEvento
import random 



# recuperando a ultima semente utilizada pelo gerador de numeros aleatorios (se existir)
random_generator = aux.create_random_generator()


def client_type(lambda1, lambda2):
    n = lambda1 + lambda2
    prob1 = lambda1/n
    x = random.random()
    if(x<=prob1):
        return 1
    else:
        return 2

def run_queue_parallel(lambd1, lambd2, mi1, mi2, simulation_total_rounds, simulation_total_time, priority, preempcao):

    mean_persons_on_system = 0
    mean_persons_per_round = []

    for _ in range(1, simulation_total_rounds):

        simulation_time = 0
        #Essa fila se refere aos eventos que ocorrerao no futuro
        simulation_queue = Queue()
        #Esta fila se refere aqueles que já chegaram mas ainda não foram processados, eles não podem ser perdidos e tem prioridade de atendimento, visto que já estão na fila.
        waiting_queue = Queue()
        persons_counter = 0
        served_persons = 0
        last_event_time = 0
        area_under_persons_chart = 0
        service_end_time = simulation_total_time

        #Verifica qual caso entrara primeiro (1 ou 2)
        if client_type(lambd1, lambd2) is 1:
            arrival_time = random_generator.exponential(lambd1)
            simulation_queue.push(Event(TipoEvento.Arrival, arrival_time, 1))
        else:
            arrival_time = random_generator.exponential(lambd2)
            simulation_queue.push(Event(TipoEvento.Arrival, arrival_time, 2))
        


        while simulation_time <= simulation_total_time and (not simulation_queue.is_queue_empty()):
            #Pega o proximo evento que ira ocorrer (chegada ou saida)
            event = simulation_queue.pop()
                
            #Caso seja uma chegada
            if event.event_type is TipoEvento.Arrival:
                simulation_time = arrival_time
                area_under_persons_chart += persons_counter * (simulation_time - last_event_time)
                #Aumento o numero de pessoas na fila
                persons_counter += 1
                #Pega o tempo do ultimo evento
                last_event_time = simulation_time
                
                #Crio o proximo evento de chegada
                if client_type(lambd1, lambd2) is 1:
                    arrival_time = simulation_time + random_generator.exponential(lambd1)
                    simulation_queue.push(Event(TipoEvento.Arrival, arrival_time, 1))
                else:
                    arrival_time = simulation_time + random_generator.exponential(lambd2)
                    simulation_queue.push(Event(TipoEvento.Arrival, arrival_time, 2))
                #Verifica se ele é o unico na fila e pode ser servido imediatamente
                if persons_counter == 1:
                    if event.event_class is 1:
                        service_end_time = simulation_time + random_generator.exponential(mi1)
                    else:
                        service_end_time = simulation_time + random_generator.exponential(mi2)
                    simulation_queue.push( Event(TipoEvento.Departure, service_end_time, event.event_class) )
                #Caso já haja um evento sendo servido ele deve ser mantido em uma fila. Pois ele chegou mas não sera atendido no momento
                #Precisamos saber de que tipo ele é tambem
                else:
                    #Este push tem que ordenar por prioridade de atendimento, pois estamos falando da fila de atendimento.
                    #**********************************************************************
                    #IMPORTANTE: Caso não haja prioridade, basta trocar por um push normal! (Implementado!)
                    #**********************************************************************
                    waiting_queue.push_queue(event) if priority is True else waiting_queue.push(event)
                    
            #Caso seja uma saida
            elif event.event_type is TipoEvento.Departure:
                
                simulation_time = service_end_time
                area_under_persons_chart += persons_counter * (simulation_time - last_event_time)
                #Diminui o numero de pessoas na fila
                persons_counter -= 1
                #Pega o tempo do ultimo evento
                last_event_time = simulation_time
                #Aumenta o numero de pessoas que foram servidas
                served_persons += 1
                #Verifica se há alguem na fila
                if persons_counter > 0:
                    #Pegamos o evento que chegou e esta aguardando e criamos seu evento de saida (Fila)
                    #Esta fila já esta ordenada para prioridade, se houver
                    event = waiting_queue.pop()
                    if event.event_class is 1:
                        service_end_time = simulation_time + random_generator.exponential(mi1)
                    else:
                        service_end_time = simulation_time + random_generator.exponential(mi2)                    
                    simulation_queue.push(Event(TipoEvento.Departure, service_end_time, event.event_class) )
                    

        mean_persons_per_round.append(area_under_persons_chart / simulation_total_time)


    for i in range(0, len(mean_persons_per_round)):
        mean_persons_on_system += (mean_persons_per_round[i]) 
    mean_persons_on_system /= simulation_total_rounds

    #TODO: AJUSTAR AS METRICAS!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    analytic_utilisation = lambd1 / mi
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

    analytic_mean_persons_on_system = aux.little_law(lambd1, mi)

    print("Lambda " + str(lambd1))
    print("Mi " + str(mi))
    print("Pessoas Servidas " + str(served_persons))
    print("Pessoas médias analíticas no sistema " + str(analytic_mean_persons_on_system))
    print("Média de pessoas no sistema " + str(mean_persons_on_system))
    print("Intervalo de confiança " + str(confidence_interval_end_points))
    print("Utilização analítica " + str(analytic_utilisation))
    print("Pessoas no desvio padrão do sistema " + str(persons_on_system_standard_deviation) + "\n")




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

        simulation_queue.push(Event(TipoEvento.Arrival, arrival_time, 0))

        while simulation_time <= simulation_total_time and (not simulation_queue.is_queue_empty()):
            event = simulation_queue.pop()

            if event.event_type is TipoEvento.Arrival:
                simulation_time = arrival_time
                area_under_persons_chart += persons_counter * (simulation_time - last_event_time)
                persons_counter += 1
                last_event_time = simulation_time
                arrival_time = simulation_time + random_generator.exponential(lambd)
                simulation_queue.push(Event(TipoEvento.Arrival, arrival_time, random.randint(0, 1)))

                if persons_counter == 1:
                    service_end_time = simulation_time + random_generator.exponential(mi)
                    simulation_queue.push( Event(TipoEvento.Departure, service_end_time, event.event_class) )

            elif event.event_type is TipoEvento.Departure:
                simulation_time = service_end_time
                area_under_persons_chart += persons_counter * (simulation_time - last_event_time)
                persons_counter -= 1
                last_event_time = simulation_time
                served_persons += 1

                if persons_counter > 0:
                    service_end_time = simulation_time + random_generator.exponential(mi)
                    simulation_queue.push(Event(TipoEvento.Departure, service_end_time, event.event_class) )

        mean_persons_per_round.append(area_under_persons_chart / simulation_total_time)


    for i in range(0, len(mean_persons_per_round)):
        mean_persons_on_system += (mean_persons_per_round[i]) 
    mean_persons_on_system /= simulation_total_rounds

    analytic_utilisation = lambd1 / mi
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

    analytic_mean_persons_on_system = aux.little_law(lambd, mi)

    print("Lambda " + str(lambd))
    print("Mi " + str(mi))
    print("Pessoas Servidas " + str(served_persons))
    print("Pessoas médias analíticas no sistema " + str(analytic_mean_persons_on_system))
    print("Média de pessoas no sistema " + str(mean_persons_on_system))
    print("Intervalo de confiança " + str(confidence_interval_end_points))
    print("Utilização analítica " + str(analytic_utilisation))
    print("Pessoas no desvio padrão do sistema " + str(persons_on_system_standard_deviation) + "\n")


lambdas1 = (round(n, 2) for n in numpy.arange(.05, .91, .05)) # 0.05, 0.1, 0.15, . . . , 0.9
lambdas2 = (round(n, 2) for n in numpy.arange(.05, .61, .05)) # 0.05, 0.1, 0.15, . . . , 0.6
mi = 1
n_rodadas = 10
total_time = 10000

def simulate(mu1, mu2, lambdas1, lambda2, priority, preempecao):
    for lambd in lambdas1:
        run_queue_parallel(lambd, lambda2, mu1, mu2, n_rodadas, total_time, priority, preempecao)


def inicialization():
    print("************************************************\n")
    print("             SIMULADOR AD 2019.2\n")
    print("     UNIVERDIDADE FEDERAL DO RIO DE JANEIRO\n")
    print("           PROFESSOR DANIEL SADOC\n")
    print("************************************************\n")
    print("************************************************\n")
    print("          AUTORES EM ORDEM ALFABETICA\n")
    print("               ANDRE TARDELLI\n")
    print("                DANIEL AMARAL\n")
    print("               DANIEL CARDOSO\n")
    print("               GABRIEL BARBOSA\n")
    print("************************************************\n")
    print("Escolha o cenario de simulacao:\n")
    print("1-Exercicio 3 parte 1\n")
    print("2-Exercicio 3 parte 2 (Mudanca no grafico gerado)\n")
    print("3-Exercicio 4 parte 1 Prioridade sem preempção\n")
    print("4-Exercicio 4 parte 2 Prioridade sem preempção (Mudanca no grafico gerado)\n")
    print("Restante do trabalho em desenvolvimento")
    print("***********************************************\n")
    chooseed = input("Escolha uma opção:")
    if(chooseed == "1"):
        print("Inicializando a simulacao para o exercicio 1, parte 1")
        print("Inicializando cenario 1")
        mu1 = 1
        mu2 = 0
        simulate(mu1, mu2,lambdas1,0,False,False)
        print("Inicializando cenario 2")
        mu1 = 1
        mu2 = 0.5
        simulate(mu1, mu2,lambdas2,0.2,False,False)
        print("Inicializando cenario 3")
        mu1 = 1/1
        mu2 = 1/0.5
        simulate(mu1, mu2,lambdas2,0.2,False,False)
        print("Inicializando cenario 4")
        #mu1 = 1
        #mu2 = 0.5
        #simulate(mu1, mu2,[0.08],0.2,False,False)
        print("TODO")
    if(chooseed == "2"):
        print("TODO 2")
        #print("Inicializando a simulacao para o exercicio 1, parte 1")
        #mu1 = 1
        #mu2 = 0.5
        #simulate(mu1, mu2,lambdas1,0,False,False)
    if(chooseed == "3"):
        print("TODO 3")
        #print("Inicializando a simulacao para o exercicio 1, parte 1")
        #mu1 = 1
        #mu2 = 0.5
        #simulate(mu1, mu2,lambdas1,0,False,False)
    if(chooseed == "4"):
        print("TODO 4")
        #print("Inicializando a simulacao para o exercicio 1, parte 1")
        #mu1 = 1
        #mu2 = 0
        #simulate(mu1, mu2,lambdas1,0,False,False)
        
    
    
    

inicialization()


aux.save_generator_state(random_generator)