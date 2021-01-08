import plotly.graph_objects as go
import pandas as pd
import numpy as np
from urllib.request import urlopen
import json
from map_layout import play_button, get_mapbox, get_sliders
import us
import math


def plot_map_deaths(df_covid):
    build_map(df_covid)


def build_map(df):
    df.sort_values(by='date')
    df = pd.pivot_table(df, index=['date', 'state'])
    months = df.index.levels[0].tolist()

    frames = get_frames(months, df)
    data = frames[0]['data']

    layout = go.Layout(
        sliders=get_sliders(months),
        updatemenus=[play_button],
        mapbox=get_mapbox(),
        title_text="Corona realted Deaths/Inhabitants per State evolution over Time")

    fig = go.Figure(data=data, layout=layout, frames=frames)
    #fig.show()
    fig.write_html("./html/deaths_state.html")


def get_frames(months, df):
    with urlopen('https://raw.githubusercontent.com/PublicaMundi/MappingAPI/master/data/geojson/us-states.json') as response:
        states = json.load(response)

    df.reset_index(level=['state', 'date'], inplace=True)
    fips = us.states.mapping('abbr', 'fips')
    stateNames = us.states.mapping('abbr', 'name')
    df['fips'] = df['state'].map(lambda state: fips[state])
    df['stateName'] = df['state'].map(lambda state: stateNames[state])
    df['deathRate'] = df.apply(lambda row: int(math.floor(row['death'] / row['Population'] * 100000)), axis=1)
    df['text'] = df.apply(lambda row: '<b>' + row['stateName'] + '</b> <br>' + 'Deaths/100.000: ' + str(row['deathRate']), axis=1)

    return [{
        'name': 'frame_{}'.format(month),
        'data': [{
                'type': 'choropleth',
                'colorscale': "orrd",
                'geojson': states,
                'locations': df[df['date'] == month]['fips'],
                'text': df[df['date'] == month]['text'],
                'z': df[df['date'] == month]['deathRate'],
                'hoverinfo': 'text',
                'colorbar': {'title': 'Deaths / 100.000 Inhabitants', 'titleside': 'top', 'thickness': 4},
            }]
    } for month in months]