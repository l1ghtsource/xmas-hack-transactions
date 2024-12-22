import streamlit as st
import pandas as pd
from get_course import get_course

import sys
import os
sys.path.append(os.getcwd())

from algos.final_optimizer import optimization, w_o_optimization


@st.cache_data
def load_csv(file):
    return pd.read_csv(file)


@st.cache_data
def load_local_dataset(dataset_num):
    uploaded_payments = f'data\payments_{dataset_num}.csv'
    uploaded_providers = f'data\providers_{dataset_num}.csv'
    ex_rates_file = 'data\ex_rates.csv'
    payments = pd.read_csv(uploaded_payments)
    providers = pd.read_csv(uploaded_providers)
    ex_rates = pd.read_csv(ex_rates_file)
    return payments, providers, ex_rates, uploaded_payments, uploaded_providers, ex_rates_file


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
        payments, providers, ex_rates, uploaded_payments, uploaded_providers, ex_rates_file = load_local_dataset(dataset_num)
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
        payments = load_csv(uploaded_payments).to_csv('payments_temp.csv', index=False)
        providers = load_csv(uploaded_providers).to_csv('providers_temp.csv', index=False)
        ex_rates = load_csv(ex_rates_file).to_csv('ex_rates_temp.csv', index=False)
        uploaded_payments = 'payments_temp.csv'
        uploaded_providers = 'providers_temp.csv'
        ex_rates_file = 'ex_rates_temp.csv'
        st.success('Файлы payments и providers успешно загружены!')

if uploaded_payments is not None and uploaded_providers is not None:
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
        trial_number = 54
        optimal_value = 1074162.7686020422
        optimal_k = [-0.5755060280729672, 0.19288650105021032, 0.8738533920662923, -0.8690379202212117]
        metrics = {
            'Time Spent': '1,393,060.0', 
            'Money Passed in USD': '1,073,497.73', 
            'Success Rate': '26%',
            'Fee in USD': '6,758.80'
        }
        
       # w_o_optimization(uploaded_providers, uploaded_payments, ex_rates_file, optimal_k)
        
        st.subheader('Результат работы алгоритма (оптимальные цепочки)')
        
        file_path = r'.\results\result_1.csv'
        with open(file_path, 'rb') as f:
            st.download_button(
                label='Скачать результат в CSV',
                data=f,
                file_name='result_1.csv',
                mime='text/csv',
            )
        
        st.subheader('Информация о лучшем испытании')
        st.markdown(
            f'''
            - **Номер испытания:** {trial_number}
            - **Оптимальное значение:** {optimal_value:.2f}
            '''
        )

        st.subheader('Оптимальные значения коэффициентов (k)')
        st.write(optimal_k)

        st.subheader('Метрики')
        for metric, value in metrics.items():
            st.write(f"**{metric}:** {value}")
            
    elif data_source == 'Использовать второй датасет':
        trial_number = 26
        optimal_value = 1136394.6537694214
        optimal_k = [0.017245344096524978, 0.32770832537823447, 0.2802537193422929, -0.2777648210606486]
        metrics = {
            'Time Spent': '1,808,654.0', 
            'Money Passed in USD': '1,126,143.63', 
            'Success Rate': '28%',
            'Fee in USD': '2,765.34' 
        }
        
        # w_o_optimization(uploaded_providers, uploaded_payments, ex_rates_file, optimal_k)
        
        st.subheader('Результат работы алгоритма (оптимальные цепочки)')
        
        file_path = r'.\results\result_2.csv'
        with open(file_path, 'rb') as f:
            st.download_button(
                label='Скачать результат в CSV',
                data=f,
                file_name='result_2.csv',
                mime='text/csv',
            )
        
        st.subheader('Информация о лучшем испытании')
        st.markdown(
            f'''
            - **Номер испытания:** {trial_number}
            - **Оптимальное значение:** {optimal_value:.2f}
            '''
        )

        st.subheader('Оптимальные значения коэффициентов (k)')
        st.write(optimal_k)

        st.subheader('Метрики')
        for metric, value in metrics.items():
            st.write(f"**{metric}:** {value}") 
 
    else:
        optimization(uploaded_providers, uploaded_payments, ex_rates_file)
        
        st.subheader('Результат работы алгоритма (оптимальные цепочки)')
        
        file_path = 'result_merged.csv'
        with open(file_path, 'rb') as f:
            st.download_button(
                label='Скачать результат в CSV',
                data=f,
                file_name='result_merged.csv',
                mime='text/csv',
        )
        
else:
    st.warning('Выберите источник данных для продолжения.')