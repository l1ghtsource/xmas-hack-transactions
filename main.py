import argparse
from algos.final_optimizer import optimization, w_o_optimization
import pandas as pd

def main(args):
    providers = args.providers
    payments = args.payments
    ex_rates = args.ex_rates
    USE_DATASET_1 = args.dataset_1
    USE_DATASET_2 = args.dataset_2
    
    if USE_DATASET_1:
        optimal_k = [-0.5755060280729672, 0.19288650105021032, 0.8738533920662923, -0.8690379202212117]
        w_o_optimization(providers, payments, ex_rates, optimal_k)
        payments = 'data\payments_1.csv'
    elif USE_DATASET_2:
        optimal_k = [0.017245344096524978, 0.32770832537823447, 0.2802537193422929, -0.2777648210606486]
        w_o_optimization(providers, payments, ex_rates, optimal_k)
        payments = 'data\payments_2.csv'
    else:
        optimization(providers, payments, ex_rates)
        
    f = pd.read_csv('result.csv') 
    df = pd.merge(pd.read_csv(payments), f, on='payment', how='inner')
    df.to_csv('merged_results.csv', index=False)
    

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Optimization script with dataset choice and file paths.")
    
    parser.add_argument('--providers', type=str, default='data\providers_1.csv', help='Path to providers CSV file')
    parser.add_argument('--payments', type=str, default='data\payments_1.csv', help='Path to payments CSV file')
    parser.add_argument('--ex_rates', type=str, default='data\ex_rates.csv', help='Path to exchange rates CSV file')
    
    parser.add_argument('--dataset_1', action='store_true', help='Use dataset 1 (if specified)')
    parser.add_argument('--dataset_2', action='store_true', help='Use dataset 2 (if specified)')

    args = parser.parse_args()
    main(args)

