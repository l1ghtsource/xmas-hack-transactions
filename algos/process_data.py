import pandas as pd


def get_payments_df(df_payments):
    df_payments.drop(columns=['cardToken'], inplace=True)
    df_payments = df_payments[['payment', 'eventTimeRes', 'amount', 'cur']]
    df_payments.rename(columns={'eventTimeRes': 'TIME', 'cur': 'CURRENCY'}, inplace=True)
    df_payments['TIME'] = pd.to_datetime(df_payments['TIME'], errors='coerce')
    return df_payments


def get_providers_df(df_providers):
    df_providers.drop(columns=['LIMIT_BY_CARD'], inplace=True)
    df_providers[df_providers['ID'] == 0]
    df_providers['TIME'] = pd.to_datetime(df_providers['TIME'], errors='coerce')
    return df_providers


def preprocess(df_exchange, df_payments, df_providers):
    df_payments = get_payments_df(df_payments)
    df_providers = get_providers_df(df_providers)

    df_payments_providers = pd.merge(df_payments, df_providers, on='CURRENCY', how='left')

    df_payments_providers = df_payments_providers.rename(columns={
        'TIME_x': 'TIME_payment',
        'TIME_y': 'TIME_provider'
    })

    df_payments_providers = df_payments_providers[df_payments_providers['TIME_provider'] <=
                                                  df_payments_providers['TIME_payment']]

    df_payments_providers['payment_date'] = df_payments_providers['TIME_payment'].dt.date
    max_time_indices = df_payments_providers.groupby(['payment', 'ID'])['TIME_provider'].idxmax()
    df_max_time = df_payments_providers.loc[max_time_indices]

    first_limits = df_payments_providers.groupby(['payment', 'ID', 'payment_date']).agg({
        'TIME_provider': 'min',
        'LIMIT_MIN': 'first',
        'LIMIT_MAX': 'first'
    }).reset_index()

    df_payments_final = pd.merge(
        df_max_time.reset_index(),
        first_limits,
        on=[
            'payment',
            'ID',
            'payment_date'
        ],
        how='left'
    )

    df_payments_final.rename(columns={
        'TIME_provider_x': 'TIME_provider',
        'payment': 'payment_ID',
        'ID': 'provider_ID',
        'LIMIT_MIN_y': 'LIMIT_MIN',
        'LIMIT_MAX_y': 'LIMIT_MAX'
    }, inplace=True)

    df_payments_final = df_payments_final[[
        'payment_ID',
        'amount',
        'CURRENCY',
        'TIME_payment',
        'provider_ID',
        'TIME_provider',
        'CONVERSION',
        'AVG_TIME',
        'MIN_SUM',
        'MAX_SUM',
        'LIMIT_MIN',
        'LIMIT_MAX',
        'COMMISSION'
    ]].reset_index(drop=True)

    return df_payments_final
