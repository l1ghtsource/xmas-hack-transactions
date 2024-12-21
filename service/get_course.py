import pandas as pd
import requests
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv('API_KEY')

currencies = [
    'AZN', 'EUR', 'HKD', 'KRW', 'AUD', 'MXN', 'PEN', 'RUB', 'BRL', 'JPY',
    'KZT', 'NGN', 'PHP', 'ZAR', 'MYR', 'TJS', 'KES', 'THB', 'TRY', 'UZS', 'USD', 'GHS'
]


def get_exchange_rate(currency):
    url = f'https://v6.exchangerate-api.com/v6/{API_KEY}/latest/USD'
    response = requests.get(url)
    data = response.json()
    if response.status_code == 200 and 'conversion_rates' in data:
        return data['conversion_rates'].get(currency, None)
    else:
        print(f'Ошибка получения данных для {currency}')
        return None


def get_course():
    rates = []
    for currency in currencies:
        rate = get_exchange_rate(currency)
        rates.append(rate)

    df = pd.DataFrame({
        'rate': rates,
        'destination': currencies
    })

    return df
