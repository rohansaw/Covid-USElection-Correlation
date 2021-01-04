import plotly.express as px
import math


def plot_scatter_tests(df):
    # only use last date for every state
    make_plot(df)


def make_plot(df):
    df = df.groupby(by=[df.state]).agg({'Population': 'mean', 'death': 'mean', 'positive': 'mean'}).reset_index()
    df['ratePositive'] = df.apply(lambda row: int(math.floor(row['positive'] / row['Population'] * 100000)), axis=1)
    df['rateDeath'] = df.apply(lambda row: int(math.floor(row['death'] / row['Population'] * 100000)), axis=1)
    fig = px.scatter(df, x="ratePositive", y="rateDeath", hover_data=['state'])
    fig.show()
