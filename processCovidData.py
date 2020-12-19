import pandas as pd


def get_covid_dataset():
    df = pd.read_csv('./resources/us_states_covid19_daily.csv')
    # df = remove_unnecessary_states(df)
    df = parse_data(df)
    return df


def remove_unnecessary_states(df):
    no_states = ['GU', 'AS', 'MP', 'VI', 'PR']
    df = df[df['states'] not in no_states]
    return df


def parse_data(data):
    df = pd.DataFrame(data)
    df.fillna(0, inplace=True)
    #df['date'] = pd.to_datetime(df['date'])
    df['date'] = pd.to_datetime(df['date'],format='%Y%m%d')
    df = df.groupby(by=[df.state, df.date.dt.strftime('%B')]).mean()
    return df