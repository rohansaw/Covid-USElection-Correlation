import plotly.graph_objects as go
import pandas as pd
import numpy as np
from map_layout import play_button, get_mapbox, get_sliders


def plot_map(df_polls, df_covid):
    # ToDo really merge datasets properly
    # df = pd.merge(df_covid, df_polls, left_on='state', right_on='state')
    df = pd.read_csv('./resources/data.csv')
    build_map(df)


def test():
    #covid = get_covid_dataset()
    #election_set = get_election_dataset("https://projects.fivethirtyeight.com/polls/president-general/")
    #print(covid)
    #print(election_set)
    #df = merge(df, election_set, 'state', 'state')
    #print(election_set.min())
    #print(election_set[election_set.pct_trend_adjusted == election_set.pct_trend_adjusted.min()])
    #print(election_set.max())
    #df = pd.merge(covid, election_set,how='outer', left_on=['state','date'], right_on = ['state','date'])
    #df = pd.read_csv('./resources/data.csv')
    #df.fillna(method='ffill', inplace=True)
    #df.fillna(0, inplace=True)
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
    return [{
        'name': 'frame_{}'.format(month),
        'data': [{
            'type': 'scattermapbox',
            'lat': df.xs(month)['Latitude'],
            'lon':df.xs(month)['Longitude'],
            'marker':go.scattermapbox.Marker(
                size=df.xs(month)['positiveIncrease']/80,
                color=df.xs(month)['polls_change'],
                showscale=True,
                cmin=-2,
                cmax=4,
                colorbar={'title': 'Tägliche Neuinfektionen',
                          'titleside': 'top', 'thickness': 4},
            ),
            'customdata': np.stack((df.xs(month)['polls_change'], df.xs(month)['positiveIncrease'],  df.xs(month)['positiveIncrease']), axis=-1),
            'hovertemplate': "<extra></extra><em>%{customdata[0]}  </em><br>🚨  %{customdata[0]}<br>🏡  %{customdata[1]}<br>⚰️  %{customdata[1]}",
        }],
    } for month in months]
