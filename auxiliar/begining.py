from enums.distribution_type import DistributionType

def get_scenario():
    print('************************************************\n')
    print('             SIMULADOR AD 2019.2\n')
    print('     UNIVERDIDADE FEDERAL DO RIO DE JANEIRO\n')
    print('           PROFESSOR DANIEL SADOC\n')
    print('************************************************')
    print('************************************************\n')
    print('          AUTORES EM ORDEM ALFABETICA:\n')
    print('               ANDRE TARDELLI')
    print('                DANIEL AMARAL')
    print('               DANIEL CARDOSO')
    print('               GABRIEL BARBOSA\n')
    print('************************************************\n')
    print('Escolha o cenario de simulacao:\n')
    print('1 - Exercicio 3 parte 1')
    print('2 - Exercicio 3 parte 2 (Mudanca no grafico gerado)')
    print('3 - Exercicio 4 parte 1 Prioridade sem preempção')
    print('4 - Exercicio 4 parte 2 Prioridade sem preempção (Mudanca no grafico gerado)')
    print('t - Todos os anteriores\n')
    print('Restante do trabalho em desenvolvimento')
    print('***********************************************\n')
    return input('Escolha uma opção: ')


def call_simulation(simulate, scenario, lambdas):
    all = 't'

    def print_case(case):
        print('Inicializando caso ' + str(case))

    if (scenario == '1' or scenario == all):
        print('\nInicializando a simulacao para o exercicio 3, parte 1')
        scene = '1'

        case = 1
        print_case(case)
        mu1 = 1
        mu2 = 0
        simulate(scene + '.' + str(case), mu1, mu2, lambdas[0], 0, False, False, DistributionType.exp)

        case = 2
        print_case(case)
        mu1 = 1
        mu2 = 0.5
        simulate(scene + '.' + str(case), mu1, mu2, lambdas[1], 0.2, False, False, DistributionType.exp)

        case = 3
        print_case(case)
        mu1 = 1
        mu2 = 0.5
        simulate(scene + '.' + str(case), mu1, mu2, lambdas[2], 0.2, False, False, DistributionType.med)

        case = 4
        print_case(case)
        # TODO: CORRIGIR AS METRICAS DESTE CENARIO
        mu1 = 1
        mu2 = 0.5
        simulate(scene + '.' + str(case), mu1, mu2, [0.08], 0.2, False, False, DistributionType.unif)

    if (scenario == '2' or scenario == all):
        # TODO:Mudar a exibição dos gráficos!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        print('\nInicializando a simulacao para o exercicio 3, parte 2')
        print('Neste caso há uma mudança no grafico gerado em comparação com a opção 1')
        scene = '2'

        case = 1
        print_case(case)
        mu1 = 1
        mu2 = 0
        simulate(scene + '.' + str(case), mu1, mu2, lambdas[0], 0, False, False, DistributionType.exp)

        case = 2
        print_case(case)
        mu1 = 1
        mu2 = 0.5
        simulate(scene + '.' + str(case), mu1, mu2, lambdas[1], 0.2, False, False, DistributionType.exp)

        case = 3
        print_case(case)
        mu1 = 1
        mu2 = 0.5
        simulate(scene + '.' + str(case), mu1, mu2, lambdas[2], 0.2, False, False, DistributionType.med)

        case = 4
        print_case(case)
        # TODO: CORRIGIR AS METRICAS DESTE CENARIO
        mu1 = 1
        mu2 = 0.5
        simulate(scene + '.' + str(case), mu1, mu2, [0.08], 0.2, False, False, DistributionType.unif)

    if (scenario == '3' or scenario == all):
        print('\nInicializando a simulacao para o exercicio 4, parte 1')
        scene = '3'

        case = 1
        print_case(case)
        mu1 = 1
        mu2 = 0
        simulate(scene + '.' + str(case), mu1, mu2, lambdas[0], 0, False, False, DistributionType.exp)

        case = 2
        print_case(case)
        mu1 = 1
        mu2 = 0.5
        simulate(scene + '.' + str(case), mu1, mu2, lambdas[1], 0.2, True, False, DistributionType.exp)

        case = 3
        print_case(case)
        mu1 = 1
        mu2 = 0.5
        simulate(scene + '.' + str(case), mu1, mu2, lambdas[2], 0.2, True, False, DistributionType.med)

        case = 4
        print_case(case)
        # TODO: CORRIGIR AS METRICAS DESTE CENARIO
        mu1 = 1
        mu2 = 0.5
        simulate(scene + '.' + str(case), mu1, mu2, [0.08], 0.2, True, False, DistributionType.unif)

    if (scenario == '4' or scenario == all):
        print('\nInicializando a simulacao para o exercicio 4, parte 2')
        scene = '4'

        case = 1
        print_case(case)
        mu1 = 1
        mu2 = 0
        simulate(scene + '.' + str(case), mu1, mu2, lambdas[0], 0, False, False, DistributionType.exp)

        case = 2
        print_case(case)
        mu1 = 1
        mu2 = 0.5
        simulate(scene + '.' + str(case), mu1, mu2, lambdas[1], 0.2, True, False, DistributionType.exp)

        case = 3
        print_case(case)
        mu1 = 1
        mu2 = 0.5
        simulate(scene + '.' + str(case), mu1, mu2, lambdas[2], 0.2, True, False, DistributionType.med)

        case = 4
        print_case(case)
        # TODO: CORRIGIR AS METRICAS DESTE CENARIO
        mu1 = 1
        mu2 = 0.5
        simulate(scene + '.' + str(case), mu1, mu2, [0.08], 0.2, True, False, DistributionType.unif)