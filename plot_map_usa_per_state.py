import plotly.graph_objects as go
import pandas as pd
import numpy as np
from processCovidData import get_covid_dataset
from processElectionData import get_election_dataset
import configparser

def merge(df_covid, df_other, left_on, right_on):
    return pd.merge(df_covid, df_other, left_on=left_on, right_on=right_on)


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
    #configparser.read
    config = configparser.ConfigParser()
    config.read('config.ini')
    print(config.sections())
    mapbox_token = config['mapbox']['secret_token']

    #df = pd.read_csv('./resources/data.csv')
    #print(pd.unique(df['date'].values))
    df.sort_values(by='date')
    df = pd.pivot_table(df, index=['date', 'state'])
    #print(df_n)
    #months = pd.unique(df['date'].values).to_list()
    print(df.index)
    months = df.index.levels[0].tolist()
    print(months)
    frames = [{   
    'name':'frame_{}'.format(month),
    'data':[{
        'type':'scattermapbox',
        'lat':df.xs(month)['Latitude'],
        'lon':df.xs(month)['Longitude'],
        'marker':go.scattermapbox.Marker(
            size=df.xs(month)['positiveIncrease']/80,
            color=df.xs(month)['polls_change'],
            showscale=True,
            cmin=-2,
            cmax=4,
            colorbar={'title':'Tägliche Neuinfektionen', 'titleside':'top', 'thickness':4},
        ),
        'customdata':np.stack((df.xs(month)['polls_change'], df.xs(month)['positiveIncrease'],  df.xs(month)['positiveIncrease']), axis=-1),
        'hovertemplate': "<extra></extra><em>%{customdata[0]}  </em><br>🚨  %{customdata[0]}<br>🏡  %{customdata[1]}<br>⚰️  %{customdata[1]}",
    }],           
    } for month in months] 
    sliders = [{
    'transition':{'duration': 0},
    'x':0.08, 
    'len':0.88,
    'currentvalue':{'font':{'size':15}, 'prefix':'📅 ', 'visible':True, 'xanchor':'center'},  
    'steps':[
        {
            'label': str(pd.to_datetime(month,format='%Y-%m-%d').month_name()),
            'method':'animate',
            'args':[
                ['frame_{}'.format(month)],
                {'mode':'immediate', 'frame':{'duration':100, 'redraw': True}, 'transition':{'duration':50}}
              ],
        } for month in months]
    }]

    play_button = [{
    'type':'buttons',
    'showactive':True,
    'x':0.045, 'y':-0.08,
    'buttons':[{ 
        'label':'🎬',
        'method':'animate',
        'args':[
            None,
            {
                'frame':{'duration':100, 'redraw':True},
                'transition':{'duration':50},
                'fromcurrent':True,
                'mode':'immediate',
            }
        ]
        }]
    }],
    print(play_button)
    data = frames[0]['data']

    # Adding all sliders and play button to the layout
    layout = go.Layout(
        sliders=sliders,
        updatemenus=[{
    'type':'buttons',
    'showactive':True,
    'x':0.045, 'y':-0.08,
    'buttons':[{ 
        'label':'🎬',
        'method':'animate',
        'args':[
            None,
            {
                'frame':{'duration':100, 'redraw':True},
                'transition':{'duration':50},
                'fromcurrent':True,
                'mode':'immediate',
            }
        ]
        }]
    }],
        mapbox={
            'accesstoken':mapbox_token,
            'center':{"lat": 37.86, "lon": -98.00},
            'zoom': 4.0,
            'style':'light',
        }
    )

    # Creating the figure
    fig = go.Figure(data=data, layout=layout, frames=frames)

    # Displaying the figure
    fig.show()