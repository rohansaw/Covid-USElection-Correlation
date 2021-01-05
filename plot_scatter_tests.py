import plotly.express as px
import math
import us


def plot_scatter_tests(df):
    df = df[df['date'] == '2020-10-01']
    stateNames = us.states.mapping('abbr', 'name')
    df['ratePositive'] = df.apply(lambda row: int(math.floor(row['positive'] / row['Population'] * 100000)), axis=1)
    df['rateDeath'] = df.apply(lambda row: int(math.floor(row['death'] / row['Population'] * 100000)), axis=1)
    df['stateName'] = df['state'].map(lambda state: stateNames[state]) 
    make_plot(df)


def make_plot(df):
    fig = px.scatter(df, x="ratePositive", y="rateDeath", color="leader", size="Population", hover_data=['stateName'], text='stateName', color_discrete_sequence=["#EF553B", "#636EFA"])
    fig.update_layout(
        title_text="Deaths per 100.000 Inhabitants in relation to PositiveCases per 100.000 Inhabitants for every state in November 2020",
    )
    fig.update_traces(textposition='top center')
    fig.show()
