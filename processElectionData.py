import requests
import pandas as pd
from bs4 import BeautifulSoup


def get_election_dataset(url):
    states = get_states(url)
    polls = []
    for state in states:
        polls.append(parse_data(state=state, data=get_data(state=state['name'], url=url)))
    return pd.concat(polls)


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


def parse_data(data, state):
    df = pd.DataFrame(data)
    df['date'] = pd.to_datetime(df['date'])
    df['state'] = df['state'].apply(lambda x: x.replace(state['name'], state['shorthand']))
    df = df.groupby(by=[df.state, df.date.dt.strftime('%B'), df.candidate]).mean()
    return df


def get_data(state, url):
    url = url + state.lower() + "/polling-average.json"
    r = requests.get(url)
    return r.json()
