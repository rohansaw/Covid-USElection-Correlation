import plotly.graph_objects as go
import pandas as pd
import numpy as np
from map_layout import play_button, get_mapbox, get_sliders


def plot_map(df):
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
        mapbox=get_mapbox(),
        title_text="Does a relationship exists between Trumps popularity in a specific state and the local developments in the covid-crisis?")

    fig = go.Figure(data=data, layout=layout, frames=frames)
    
    #fig.show()
    fig.write_html("./html/map_usa_per_state.html")


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
                cmax=2,
                colorbar={'title': 'Popularity Trump Development',
                          'titleside': 'top', 'thickness': 4},
            ),
            'customdata': np.stack((round(df.xs(month)['polls_change'],2), round(df.xs(month)['positiveIncrease'],0), ), axis=-1),
            'hovertemplate': "🚨 Ø tägl. Neuinfektionen: %{customdata[1]}<br>Trumps Zustimmungsentwicklung: %{customdata[0]}",
        }],
    } for month in months]
