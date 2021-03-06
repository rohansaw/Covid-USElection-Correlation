import requests
import pandas as pd
from bs4 import BeautifulSoup


def get_election_dataset(url):
    states = get_states(url)
    polls = []
    for state in states:
        state_data = get_data(state=state['name'], url=url)
        polls.append(parse_data(state=state, data=state_data))
    df = pd.concat(polls)
    df = add_leader_col(df)
    return df


def get_states(url):
    res = []
    html_doc = requests.get(url)
    soup = BeautifulSoup(html_doc.text, 'html.parser')
    items = soup.findAll("select", {"class": "select-state"})
    soup = BeautifulSoup(str(items), 'html.parser')
    items = soup.findAll("option")

    bad_items = ['All', 'National']

    for item in items:
        if not item.has_attr('disabled') and item.text not in bad_items:
            res.append({
                'shorthand': item['value'],
                'name': item.text.replace(" ", "-")})
    return res


def get_winner(trump_val, biden_val):
    if trump_val > biden_val:
        return 'Trump'
    return 'Biden'


def add_leader_col(df):
    df['leader'] = df.apply (lambda row: get_winner(row['pct_trend_adjusted'], row['biden_trend']), axis=1)
    return df

def parse_data_biden(data,state):
    df = pd.DataFrame(data)
    df['date'] = pd.to_datetime(df['date'])
    state['name'] = state['name'].replace("-", " ")
    df['state'] = df['state'].apply(lambda x: x.replace(state['name'], state['shorthand']))
    df = df[(df['candidate'].isin(['Joseph R. Biden Jr.']))]
    df.sort_values(by='date')
    df = df[~(df['date'].dt.month.isin([1,2]))]
    df = df.groupby(by=[df.state, df.date.dt.strftime('%Y%m')]).mean().reset_index()
    df['date'] = pd.to_datetime(df['date'],format='%Y%m')
    df['polls_change'] = df.pct_trend_adjusted.diff()
    df.loc[(df['date'].dt.month.isin([3])), 'polls_change'] = 0.0
    df = df.rename(columns={"pct_trend_adjusted": "biden_trend"})
    return df[['state', 'date', 'biden_trend']]


def parse_data(data, state):
    df = pd.DataFrame(data)
    df_biden = parse_data_biden(data, state)
    df['date'] = pd.to_datetime(df['date'])
    state['name'] = state['name'].replace("-", " ")
    df['state'] = df['state'].apply(lambda x: x.replace(state['name'], state['shorthand']))
    df = df[~(df['candidate'].isin(['Joseph R. Biden Jr.']))]
    df.sort_values(by='date')
    df = df[~(df['date'].dt.month.isin([1,2]))]
    df = df.groupby(by=[df.state, df.date.dt.strftime('%Y%m')]).mean().reset_index()
    df['date'] = pd.to_datetime(df['date'],format='%Y%m')
    df['polls_change'] = df.pct_trend_adjusted.diff()
    df.loc[(df['date'].dt.month.isin([3])), 'polls_change'] = 0.0
    df = add_monthly_increase_col(df)
    df = pd.merge(df, df_biden, how='outer', left_on=['state','date'], right_on=['state', 'date'])
    return df


def add_monthly_increase_col(df):
    df['increase'] = df['pct_trend_adjusted'] - df['pct_trend_adjusted'].shift(2)
    return df


def normalized(abs_val, inhabitants):
    return


def get_data(state, url):
    url = url + state.lower() + "/polling-average.json"
    r = requests.get(url)
    return r.json()
