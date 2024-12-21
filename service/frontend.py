import streamlit as st
import pandas as pd
from parsers import get_course


@st.cache_data
def load_csv(file):
    return pd.read_csv(file)


st.set_page_config(
    page_title='ФлоуЧейн',
    page_icon='📈'
)

st.title('📈 ФлоуЧейн')
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
    st.success('Все файлы успешно загружены!')

    use_uploaded_ex_rates = st.checkbox(
        'Использовать ex_rates из загруженного файла',
        value=True,
        help='Если чекбокс снят, текущие курсы валют будут получены с биржи в режиме реального времени.'
    )

    if not use_uploaded_ex_rates:
        local_ex_rates_path = get_course()
        st.info('Используется актуальный курс валют с биржи, для использования вашего файла активируйте соответствующий чекбокс.')
    else:
        ex_rates = load_csv(ex_rates_file)

    payments = load_csv(uploaded_payments)
    providers = load_csv(uploaded_providers)

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
