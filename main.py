import argparse
from algos.final_optimizer import optimization, w_o_optimization

def main(args):
    providers = args.providers
    payments = args.payments
    ex_rates = args.ex_rates
    USE_DATASET_1 = args.dataset_1
    USE_DATASET_2 = args.dataset_2
    
    if USE_DATASET_1:
        optimal_k = [-0.9962513294274908, 0.48830840996012714, 0.8385587739627488, -0.7024426931951558]
        w_o_optimization(providers, payments, ex_rates, optimal_k)
    elif USE_DATASET_2:
        optimal_k = [-0.9962513294274908, 0.48830840996012714, 0.8385587739627488, -0.7024426931951558]
        w_o_optimization(providers, payments, ex_rates, optimal_k)
    else:
        optimization(providers, payments, ex_rates)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Optimization script with dataset choice and file paths.")
    
    parser.add_argument('--providers', type=str, default='data\providers_1.csv', help='Path to providers CSV file')
    parser.add_argument('--payments', type=str, default='data\payments_1.csv', help='Path to payments CSV file')
    parser.add_argument('--ex_rates', type=str, default='data\ex_rates.csv', help='Path to exchange rates CSV file')
    
    parser.add_argument('--dataset_1', action='store_true', help='Use dataset 1 (if specified)')
    parser.add_argument('--dataset_2', action='store_true', help='Use dataset 2 (if specified)')

    args = parser.parse_args()
    main(args)

