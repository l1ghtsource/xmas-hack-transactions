import streamlit as st
import pandas as pd
from get_course import get_course

import sys
import os
sys.path.append(os.getcwd())

from algos.final_optimizer import optimization


@st.cache_data
def load_csv(file):
    return pd.read_csv(file)


@st.cache_data
def load_local_dataset(dataset_num):
    payments = pd.read_csv(f'data\payments_{dataset_num}.csv')
    providers = pd.read_csv(f'data\providers_{dataset_num}.csv')
    ex_rates = pd.read_csv('data\ex_rates.csv')
    return payments, providers, ex_rates


st.set_page_config(
    page_title='ФлоуЧейн',
    page_icon='📈'
)

st.title('📈 ФлоуЧейн')
st.header('Выбор источника данных')


data_source = st.radio(
    'Выберите источник данных:',
    ['Использовать первый датасет', 'Использовать второй датасет', 'Загрузить свой датасет']
)

payments = None
providers = None

if data_source in ['Использовать первый датасет', 'Использовать второй датасет']:
    dataset_num = '1' if data_source == 'Использовать первый датасет' else '2'
    try:
        payments, providers, ex_rates = load_local_dataset(dataset_num)
        st.success(f'Датасет {dataset_num} успешно загружен!')
    except FileNotFoundError:
        st.error(f'Файлы датасета {dataset_num} не найдены в локальной директории.')
else:
    st.header('Загрузка файлов')
    uploaded_payments = st.file_uploader(
        'Загрузите Payments:',
        accept_multiple_files=False,
        type='csv',
        key='payments',
        help='Файл должен быть в формате .csv и соответствовать формату референсных файлов payments_1.csv и payments_2.csv'
    )
    
    uploaded_providers = st.file_uploader(
        'Загрузите Providers:',
        accept_multiple_files=False,
        type='csv',
        key='providers',
        help='Файл должен быть в формате .csv и соответствовать формату референсных файлов providers_1.csv и providers_2.csv'
    )
    
    ex_rates_file = st.file_uploader(
        'Загрузите Ex_Rates:',
        accept_multiple_files=False,
        type='csv',
        key='ex_rates',
        help='Файл должен быть в формате .csv и соответствовать формату референсного файла ex_rates.csv'
    )
    if uploaded_payments and uploaded_providers and ex_rates_file:
        payments = load_csv(uploaded_payments)
        providers = load_csv(uploaded_providers)
        ex_rates = load_csv(ex_rates_file)
        st.success('Файлы payments и providers успешно загружены!')

if payments is not None and providers is not None:
    st.header('Курсы валют')
    use_uploaded_ex_rates = st.checkbox(
        'Использовать актуальный курс валют с биржи',
        value=False,
        help='Если чекбокс выбран, текущие курсы валют будут получены с биржи в режиме реального времени.'
    )

    if use_uploaded_ex_rates:
        ex_rates = get_course()
        st.info('Используется актуальный курс валют с биржи.')

    if data_source == 'Использовать первый датасет':
        results = 1
    elif data_source == 'Использовать второй датасет':
        results = 2
    else:
        optimization(uploaded_providers, uploaded_payments, ex_rates_file)
        results = 3
        
    print(results)
else:
    st.warning('Выберите источник данных для продолжения.')