import pandas as pd
import numpy as np
import random
import datetime
from tqdm import tqdm


def load_data():
    print("Загрузка данных...")
    providers = pd.read_csv('data/providers_1.csv')
    payments = pd.read_csv('data/payments_1.csv')
    rates = pd.read_csv('data/ex_rates.csv')
    print("Данные загружены.")
    return providers, payments, rates


def convert_currency(amount, cur_from, cur_to, rates):
    if cur_from == cur_to:
        return amount
    rate = rates[rates['destination'] == cur_to]['rate'].values[0]
    return amount * rate


class PaymentSimulator:
    def __init__(self, providers, rates):
        self.providers = providers
        self.rates = rates
        self.provider_data = {}

    def simulate_payment(self, payment, chain):
        total_amount = payment['amount']
        cur = payment['cur']
        transaction_time = 0
        total_commission = 0
        total_fees = 0
        success = False

        for provider_id in chain:
            provider = self.providers[self.providers['ID'] == provider_id]

            # проверяем валюту провайдера и платежа
            provider_currency = provider['CURRENCY'].values[0]
            if cur != provider_currency:
                total_amount = convert_currency(total_amount, cur, provider_currency, self.rates)
                cur = provider_currency

            # проверка лимитов
            limit_max = provider['LIMIT_MAX'].values[0]
            limit_min = provider['LIMIT_MIN'].values[0]
            if total_amount > limit_max:
                continue  # платёж не проходит
            if total_amount < limit_min:
                total_fees += 0.01 * limit_min  # штраф за недостижение минимального лимита

            # время обработки и комиссия
            avg_time = provider['AVG_TIME'].values[0]
            commission = provider['COMMISSION'].values[0]

            transaction_time += avg_time
            total_commission += commission * total_amount

            # вероятность успешности
            conversion = provider['CONVERSION'].values[0]
            if random.random() < conversion:
                success = True
                break

        if success:
            return transaction_time, total_commission, total_fees, total_amount - total_commission - total_fees
        else:
            return transaction_time, total_commission, total_fees, 0  # платёж не прошел

# генетический алгоритм для оптимизации


class GeneticOptimizer:
    def __init__(self, payments, providers, simulator, population_size=50, generations=100, mutation_rate=0.1):
        self.payments = payments
        self.providers = providers
        self.simulator = simulator
        self.population_size = population_size
        self.generations = generations
        self.mutation_rate = mutation_rate

    def generate_population(self):
        print("Генерация начальной популяции...")
        population = []
        for _ in range(self.population_size):
            chain = random.sample(self.providers['ID'].tolist(), len(self.providers))
            population.append(chain)
        print("Популяция сгенерирована.")
        return population

    def fitness(self, chain):
        # вычисление метрики для цепочки
        total_time = 0
        total_commission = 0
        total_fees = 0
        total_profit = 0

        for _, payment in tqdm(
                self.payments.iterrows(),
                total=len(self.payments),
                desc="Обработка платежей", leave=False):
            transaction_time, commission, fees, profit = self.simulator.simulate_payment(payment, chain)
            total_time += transaction_time
            total_commission += commission
            total_fees += fees
            total_profit += profit

        # оценка с учетом прибыли, времени и штрафов
        fitness_value = total_profit - total_time - total_fees
        return fitness_value

    def mutate(self, chain):
        # мутация цепочки
        if random.random() < self.mutation_rate:
            idx1, idx2 = random.sample(range(len(chain)), 2)
            chain[idx1], chain[idx2] = chain[idx2], chain[idx1]
        return chain

    def crossover(self, parent1, parent2):
        # перекрещивание двух цепочек
        split_idx = random.randint(1, len(parent1) - 1)
        child = parent1[:split_idx] + parent2[split_idx:]
        return child

    def optimize(self):
        print("Начало оптимизации...")
        population = self.generate_population()

        for generation in range(self.generations):
            print(f"Поколение {generation+1}/{self.generations}...")
            # оценка всех цепочек
            fitness_scores = [self.fitness(chain) for chain in tqdm(population, desc="Оценка популяции", leave=False)]

            # сортировка по убыванию
            sorted_population = [chain for _, chain in sorted(zip(fitness_scores, population), reverse=True)]

            # отбор лучших
            new_population = sorted_population[:self.population_size // 2]

            # скрещивание и мутация
            for i in range(self.population_size // 2, self.population_size):
                parent1, parent2 = random.sample(new_population, 2)
                child = self.crossover(parent1, parent2)
                child = self.mutate(child)
                new_population.append(child)

            population = new_population

        # выбираем лучшую цепочку
        best_chain = sorted_population[0]
        print("Оптимальная цепочка провайдеров найдена.")
        return best_chain


# def main():
#     providers, payments, rates = load_data()
#     simulator = PaymentSimulator(providers, rates)
#     optimizer = GeneticOptimizer(payments, providers, simulator)
#     best_chain = optimizer.optimize()

#     print("Оптимальная цепочка провайдеров:", best_chain)


# if __name__ == "__main__":
#     main()
