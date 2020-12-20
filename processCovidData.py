import pandas as pd

def merge(df_covid, df_other):
    # df_population = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/2014_usa_states.csv')
    # df_population = remove_unnecessary_states(df_population, 'Postal')
    return pd.merge(df_covid, df_population, left_on='state', right_on='Postal')

def get_population_dataset():
    df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/2014_usa_states.csv')
    return remove_unnecessary_states(df, 'Postal')

def get_latitude_dataset():
    return


def get_covid_dataset():
    df = pd.read_csv('./resources/us_states_covid19_daily.csv')
    df = remove_unnecessary_states(df, 'state')
    df = parse_data(df)
    return df


def remove_unnecessary_states(df, key):
    no_states = ['GU', 'AS', 'MP', 'VI', 'PR']
    df = df[~df[key].isin(no_states)]
    return df


def parse_data(data):
    df = pd.DataFrame(data)
    print(df)
    print("Data")
    df.fillna(0, inplace=True)
    print(len(df))
    print("Data- non-null")
    df = merge(data, get_population_dataset())
    df = merge(data, get_latitude_dataset())
    print("Data- merge")
    print(df)
    df['date'] = pd.to_datetime(df['date'],format='%Y%m%d')
    df = df.groupby(by=[df.state, df.date.dt.strftime('%m %B')]).mean().sort_index()
    df = add_monthly_increase_col(df)
    pd.set_option('display.max_rows', 50)
    print(df)
    return df


def add_monthly_increase_col(df):
    df['increase'] = df['positive'] - df['positive'].shift(1)
    return df
