from algos.final_optimizer import optimization

if __name__ == '__main__':
    providers = 'data\providers_1.csv'
    payments = 'data\payments_1.csv'
    ex_rates = 'data\ex_rates.csv'

    optimization(providers, payments, ex_rates)
