import streamlit as st
import pandas as pd


@st.cache_data
def load_csv(file):
    return pd.read_csv(file)


st.title('FlowChain')
st.header('Загрузка файлов')

uploaded_payments = st.file_uploader(
    'Загрузите Payments (2 файла):',
    accept_multiple_files=True,
    type='csv',
    key='payments',
    help='Файлы должны быть в формате .csv и соответствовать форматам референсных файлов payments_1.csv и payments_2.csv'
)

uploaded_providers = st.file_uploader(
    'Загрузите Providers (2 файла):',
    accept_multiple_files=True,
    type='csv',
    key='providers',
    help='Файлы должны быть в формате .csv и соответствовать форматам референсных файлов providers_1.csv и providers_2.csv'
)

ex_rates_file = st.file_uploader(
    'Загрузите  Ex_Rates:',
    type='csv',
    key='ex_rates',
    help='Файл должен быть в формате .csv и соответствовать формату референсного файла ex_rates.csv'
)

if len(uploaded_payments) == 2 and len(uploaded_providers) == 2 and ex_rates_file is not None:
    st.success('Все файлы успешно загружены!')

    use_uploaded_ex_rates = st.checkbox(
        'Использовать ex_rates из загруженного файла',
        value=True,
        help='Если чекбокс снят, текущие курсы валют будут получены с биржи в режиме реального времени.'
    )

    if not use_uploaded_ex_rates:
        local_ex_rates_path = 'local_ex_rates.csv'  # тут сделать вызов парсера
        ex_rates = load_csv(local_ex_rates_path)
        st.info('Используется актуальный курс валют с биржи, для использования вашего файла активируйте соответствующий чекбокс.')
    else:
        ex_rates = load_csv(ex_rates_file)

    payments_1 = load_csv(uploaded_payments[0])
    payments_2 = load_csv(uploaded_payments[1])
    providers_1 = load_csv(uploaded_providers[0])
    providers_2 = load_csv(uploaded_providers[1])

    payments = pd.concat([payments_1, payments_2], ignore_index=True)
    providers = pd.concat([providers_1, providers_2], ignore_index=True)

    st.header('Выбор стратегии')

    strategies = {
        'Сбалансированная': 'balanced',
        'Максимизация успешной транзакции': 'maximize_success',
        'Минимизация времени': 'minimize_time',
        'Максимизация прибыли': 'maximize_profit',
    }

    selected_strategy = st.radio('Выберите стратегию:', list(strategies.keys()))

    if selected_strategy:
        st.write(f'Вы выбрали стратегию: {selected_strategy}')

        # тут сделать вызов алгоритма из algos
        if strategies[selected_strategy] == 'balanced':
            result = payments
        elif strategies[selected_strategy] == 'maximize_success':
            result = payments
        elif strategies[selected_strategy] == 'minimize_time':
            result = payments
        elif strategies[selected_strategy] == 'maximize_profit':
            result = payments

        st.header('Результаты')
        csv = result.to_csv(index=False).encode('utf-8')
        st.download_button(
            label='Скачать результат в CSV',
            data=csv,
            file_name='result.csv',
            mime='text/csv',
        )
else:
    st.warning('Загрузите все необходимые файлы для продолжения.')
