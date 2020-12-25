import plotly.graph_objects as go
import pandas as pd

from processCovidData import get_covid_dataset
from processElectionData import get_election_dataset

def merge(df_covid, df_other, left_on, right_on):
    return pd.merge(df_covid, df_other, left_on=left_on, right_on=right_on)


def test():
    
    covid = get_covid_dataset()
    election_set = get_election_dataset("https://projects.fivethirtyeight.com/polls/president-general/")    
    #print(covid)
    #print(election_set)
    #df = merge(df, election_set, 'state', 'state')
    #print(election_set.min())
    #print(election_set[election_set.pct_trend_adjusted == election_set.pct_trend_adjusted.min()]) 
    #print(election_set.max())
    df = pd.merge(covid, election_set,how='outer', left_on=['state','date'], right_on = ['state','date'])
    #df.to_csv('./resources/data.csv')
    df = pd.read_csv('./resources/data.csv')
    #df.fillna(method='ffill', inplace=True)
    df.fillna(0, inplace=True)
    #print(df)
    #df = df[~(df['date'].dt.month.isin([3]))]
    df['text'] = df['probableCases']
    limits = [(0,20),(20,30),(30,40),(40,50),(50,60)]
    colors = ["royalblue","crimson","lightseagreen","orange","lightgrey"]
    cities = []
    scale = 5000

    fig = go.Figure()

    for i in range(len(limits)):
        lim = limits[i]
        #print(lim)
        #df_sub = df[lim[0]:lim[1]]
        #df_sub = df['pct_trend_adjusted'].between(lim[0], lim[1], inclusive=False)
        df_sub = df[(df['pct_trend_adjusted'] >= lim[0]) & (df['pct_trend_adjusted'] < lim[1])]
        #print(df_sub)
        fig.add_trace(go.Scattergeo(
            locationmode = 'USA-states',
            lon = df_sub['Longitude'],
            lat = df_sub['Latitude'],
            #text = '{0}: {1}'.format(df_sub['state'], df_sub['positiveIncrease']),
            text = df_sub['state'],
            marker = dict(
                size = df_sub['positiveIncrease']*5,
                color = colors[i],
                line_color='rgb(40,40,40)',
                line_width=0.5,
                sizemode = 'area'
                #hovertext='GDHJ'
                #ticktext='d'
            ),
            name = '{0} - {1}'.format(lim[0],lim[1])))

    fig.update_layout(
            title_text = '2014 US city populations<br>(Click legend to toggle traces)',
            showlegend = True,
            geo = dict(
                scope = 'usa',
                landcolor = 'rgb(217, 217, 217)',
            )
        )
    #fig.write_html("./index.html")
    fig.show()
