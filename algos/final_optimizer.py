from plotly.io import show
import optuna
import numpy as np
import pandas as pd
import random
import warnings
warnings.simplefilter(action='ignore', category=Warning)


def proceed_transaction(transaction, conveyor):
    '''
    Симулирует проведение транзакции через конвейер терминалов,
    возвращает информацию о результатах операции для подсчёта метрик
    '''
    operation = {}
    operation['time_spent'] = 0
    operation['success'] = False
    operation['money_passed_in_usd'] = 0
    operation['payment_id'] = transaction['ID']

    for terminal in conveyor:
        operation['time_spent'] += terminal['AVG_TIME']
        if terminal['CURRENT_SUM'] + transaction['amount'] <= terminal['LIMIT_MAX'] and \
                terminal['CURRENCY'] == transaction['cur'] and \
                terminal['MIN_SUM'] <= transaction['amount'] and \
                terminal['MAX_SUM'] >= transaction['amount']:
            if terminal_random(terminal['CONVERSION']):
                terminal['CURRENT_SUM'] += transaction['amount']
                operation['success'] = True
                operation['money_passed_in_usd'] = transaction['amount'] * \
                    (1 - terminal['COMMISSION']) * terminal['rate']
                break
    return operation


def create_conveyor_naive(transaction, all_terminals):
    '''
    Создаёт конвейер из всех доступных терминалов
    '''
    conveyor = []
    for terminal in all_terminals:
        conveyor.append(terminal)

    # в случайном порядке
    conveyor = sorted(conveyor, key=lambda v: random.random())
    return conveyor


def create_conveyor(transaction, all_terminals, coeffs):
    '''
    Создаёт конвейер из терминалов, которые могут обработать транзакцию
    (учитывает валюту, сумму платежа и лимит терминала по общей сумме)
    '''
    conveyor = []
    for terminal in all_terminals:
        if terminal['CURRENT_SUM'] + transaction['amount'] <= terminal['LIMIT_MAX'] and \
                terminal['CURRENCY'] == transaction['cur'] and \
                terminal['MIN_SUM'] <= transaction['amount'] and \
                terminal['MAX_SUM'] >= transaction['amount']:
            conveyor.append(terminal)

    # установка приоритета среди доступных терминалов:
    conveyor = sorted(
        conveyor, key=lambda v: coeffs[0] * v['COMMISSION'] * 20 + coeffs[1] * v['CONVERSION'] + coeffs[2] * v['AVG_TIME'] +
        coeffs[3] * v['CURRENT_SUM'] / v['LIMIT_MIN'])

    return conveyor


def get_ids_from_conveyor(conveyor):
    '''
    Возвращает список id терминалов для заполнения flow
    '''
    return '-'.join([str(x['ID']) for x in conveyor])


def terminal_random(conv):
    '''
    Проверяет успех проведения транзакции через 
    оператора с заданным CONVERSION для симуляции
    '''
    return random.random() < conv


def calculate_next_line(actual_terminals_list, last_transation, koefs):
    '''
    Симуляция проведения транзакции с учётом информации о существующих терминалах
    '''
    transaction = last_transation
    all_terminals = actual_terminals_list

    # создаём конвейер терминалов
    # conveyor = create_conveyor_naive(transaction, all_terminals)
    conveyor = create_conveyor(transaction, all_terminals, koefs)
    # делаем список id для добавления в столбец flow
    conveyor_ids = get_ids_from_conveyor(conveyor)
    # получаем результаты операции
    operation_result = proceed_transaction(transaction, conveyor)
    return conveyor_ids, operation_result


def proceed_dataset(providers, ex_rates, payments, koefs):
    terms = pd.read_csv(providers).drop_duplicates(['ID', 'TIME'], keep='last')
    fx = pd.read_csv(ex_rates)
    terms = terms.merge(
        fx,
        how='left',
        left_on='CURRENCY',
        right_on='destination'
    )

    # initial
    first = terms['TIME'].min()
    initial_terms = terms[terms['TIME'] == first]  # .set_index('ID', drop=True)
    initial_terms['CURRENT_SUM'] = 0.0
    initial_terms_d = initial_terms[['ID', 'CONVERSION', 'AVG_TIME', 'MIN_SUM', 'MAX_SUM', 'LIMIT_MIN',
                                     'LIMIT_MAX', 'COMMISSION', 'CURRENCY', 'rate', 'CURRENT_SUM']].to_dict(orient='index')
    actual_terminals_list = list(initial_terms_d.values())

    # updates
    updates_terms = terms[terms['TIME'] != first]
    updates_terms['TYPE'] = '0'
    updates_terms = updates_terms[['TIME', 'TYPE', 'ID', 'CONVERSION', 'AVG_TIME', 'MIN_SUM', 'MAX_SUM', 'COMMISSION']]

    paym = pd.read_csv(payments)
    paym['TYPE'] = '1'
    paym = paym.rename(columns={'eventTimeRes': 'TIME', 'payment': 'ID'})
    paym = paym[['TIME', 'TYPE', 'ID', 'amount', 'cur']]

    union = pd.concat(
        [updates_terms, paym],
        join='outer',
        ignore_index=True
    ).sort_values(["TIME", "TYPE"], ascending=True)

    operation_result_lst = []
    conveyor_ids_lst = []

    for i, row in union.iterrows():
        if row['TYPE'] == '0':
            index = next((index for (index, d) in enumerate(actual_terminals_list) if d['ID'] == row['ID']), None)
            for param in ['CONVERSION', 'AVG_TIME', 'MIN_SUM', 'MAX_SUM', 'COMMISSION']:
                actual_terminals_list[index][param] = row[param]
        else:
            conveyor_ids, operation_result = calculate_next_line(actual_terminals_list, row, koefs)
            operation_result_lst.append(operation_result)
            conveyor_ids_lst.append({"flow": conveyor_ids, 'payment': operation_result['payment_id']})

    oper = pd.DataFrame(operation_result_lst)
    flow = pd.DataFrame(conveyor_ids_lst)
    fee = 0
    for row in actual_terminals_list:
        if row['CURRENT_SUM'] < row['LIMIT_MIN']:
            fee += row['LIMIT_MIN'] * row['rate'] * 0.01

    metrics = {}
    metrics['time_spent'] = oper['time_spent'].sum()
    metrics['money_passed_in_usd'] = oper['money_passed_in_usd'].sum()
    metrics['success_rate'] = round(oper['success'].sum()/oper['success'].count(), 2)
    metrics['fee_in_usd'] = fee

    return metrics, flow


def money_optimization(k, providers, ex_rates, payments):
    m, _ = proceed_dataset(providers, ex_rates, payments, k)
    return m['money_passed_in_usd'] - m['fee_in_usd']


def time_optimization(k, providers, ex_rates, payments):
    m, _ = proceed_dataset(providers, ex_rates, payments, k)
    return m['money_passed_in_usd'] - m['fee_in_usd']


def optimization(providers, payments, ex_rates):
    def objective(trial):
        k = [
            trial.suggest_float(f"k{i}", -1.0, 1.0) for i in range(4)
        ]
        return money_optimization(np.array(k), providers, ex_rates, payments)

    study = optuna.create_study(direction='maximize')
    study.optimize(objective, n_trials=100)

    optimal_k = [study.best_params[f"k{i}"] for i in range(4)]
    print('Оптимальные значения k:', optimal_k)

    m, f = proceed_dataset(providers, ex_rates, payments, np.array(optimal_k))
    print(m)
    if f is not None:
        f.to_csv('result.csv', index=False)

    fig = optuna.visualization.plot_optimization_history(study)
    fig.update_layout(title='История оптимизации', xaxis_title='Номер итерации', yaxis_title='Целевая метрика')

    show(fig)
    fig.write_html('optimization_history.html')
    print("График оптимизации сохранен в файл 'optimization_history.html'")


def w_o_optimization(providers, payments, ex_rates, optimal_k):
    m, f = proceed_dataset(providers, ex_rates, payments, np.array(optimal_k))
    print(m)
    if f is not None:
        f.to_csv('result.csv', index=False)