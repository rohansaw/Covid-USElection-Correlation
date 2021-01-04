import plotly.express as px
import math


def plot_scatter_tests(df):
    df = df.groupby(by=[df.state]).agg({'Population': 'mean', 'death': 'mean', 'positive': 'mean'}).reset_index()
    df['ratePositive'] = df.apply(lambda row: int(math.floor(row['positive'] / row['Population'] * 100000)), axis=1)
    df['rateDeath'] = df.apply(lambda row: int(math.floor(row['death'] / row['Population'] * 100000)), axis=1)
    make_plot(df)


def make_plot(df):
    fig = px.scatter(df, x="ratePositive", y="rateDeath", hover_data=['state'])
    fig.update_layout(
        title_text="Deaths/Population in relation to PositiveCases/Population for every state"
    )
    fig.show()
