import plotly.express as px


def plot_scatter_tests(df):
    # only use last date for every state
    make_plot(df)


def make_plot(df):
    fig = px.scatter(df, x="pct_trend_adjusted", y="totalTestsViral", hover_data=['state'])
    fig.show()
