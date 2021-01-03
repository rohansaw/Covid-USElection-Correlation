import plotly.graph_objects as go
import pandas as pd
import numpy as np
from urllib.request import urlopen
import json
from map_layout import play_button, get_mapbox, get_sliders
import us


def plot_map_deaths():
    # ToDo really merge datasets properly
    # df = pd.merge(df_covid, df_polls, left_on='state', right_on='state')
    df = pd.read_csv('./resources/data.csv')
    build_map(df)


def build_map(df):
    df.sort_values(by='date')
    df = pd.pivot_table(df, index=['date', 'state'])
    months = df.index.levels[0].tolist()

    frames = get_frames(months, df)
    data = frames[0]['data']

    layout = go.Layout(
        sliders=get_sliders(months),
        updatemenus=[play_button],
        mapbox=get_mapbox())

    fig = go.Figure(data=data, layout=layout, frames=frames)
    fig.show()


def get_frames(months, df):
    with urlopen('https://raw.githubusercontent.com/PublicaMundi/MappingAPI/master/data/geojson/us-states.json') as response:
        states = json.load(response)

    df.reset_index(level=['state', 'date'], inplace=True)
    print(df)
    fips = us.states.mapping('abbr', 'fips')
    print(fips)
    df['state'] = df['state'].map(lambda state: fips[state])
    print(df)

    return [{
        'name': 'frame_{}'.format(month),
        'data': [{
                'type': 'choropleth',
                'colorscale': "Viridis",
                'geojson': states,
                'locations': df[df['date'] == month]['state'],
                'z': df[df['date'] == month]['death']
            }]
    } for month in months]