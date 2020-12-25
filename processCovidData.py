import pandas as pd

def merge(df_covid, df_other, left_on, right_on):
    # df_population = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/2014_usa_states.csv')
    # df_population = remove_unnecessary_states(df_population, 'Postal')
    return pd.merge(df_covid, df_other, left_on=left_on, right_on=right_on)

def get_population_dataset():
    df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/2014_usa_states.csv')
    return remove_unnecessary_states(df, 'Postal')

def get_latitude_dataset():
    df = pd.read_csv('./resources/USA_States.csv')
    df.fillna(0, inplace=True)
    return df


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
    df.fillna(0, inplace=True)
    df = merge(data, get_population_dataset(), 'state', 'Postal')
    df = merge(df, get_latitude_dataset(), 'State', 'State')
    df['date'] = pd.to_datetime(df['date'],format='%Y%m%d')
    #remove
    df = df[~(df['date'].dt.month.isin([1,2]))]
    #df['covid_increase'] = df['date'].dt.month.isin([4]) - 
    df.sort_values(by='date')
    #df = df.groupby(by=[df.state, df.date.dt.strftime('%m %B')]).mean().sort_index()
    df = df.groupby(by=[df.state, df.date.dt.strftime('%Y%m')]).mean().reset_index()
    #df = df.groupby(as_index=False, by=[df.state, df.date.dt.strftime('%m %B')]).mean()
    df['otm'] = df.positiveIncrease.diff()
    df['date'] = pd.to_datetime(df['date'],format='%Y%m')
    df.loc[(df['date'].dt.month.isin([3])), 'otm'] = 0.0
    #df[(df['date'].dt.month.isin([1,2]))] = df[~(df['date'].dt.month.isin([1,2]))]
    #df = df.groupby(by=[df.state, df.date.dt.strftime('%m %B')]).mean()
    df = add_monthly_increase_col(df)
    pd.set_option('display.max_rows', 50)
    return df


def add_monthly_increase_col(df):
    df['increase'] = df['positive'] - df['positive'].shift(1)
    return df
