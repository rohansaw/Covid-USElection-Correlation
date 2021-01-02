import plotly.graph_objects as go
import pandas as pd
from plotly.subplots import make_subplots


def plot_state_line(df_polls, df_covid, state):
    df_polls = df_polls[df_polls['state'] == state]
    df_covid = df_covid[df_covid['state'] == state]
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(
        go.Scatter(x=df_polls['date'], y=df_polls['pct_trend_adjusted'], name="Trump voters %", line=dict(color="#ff4c4c")),
        secondary_y=False,
    )

    fig.add_trace(
        go.Scatter(x=df_covid['date'], y=df_covid['positive'], name="Covid Positives", line=dict(color="#35b235")),
        secondary_y=True,
    )

    fig.update_layout(
        title_text="Covid Cases and Approval"
    )

    fig.update_xaxes(title_text="xaxis title")
    fig.update_yaxes(title_text="<b>Trump poll</b>", secondary_y=False)
    fig.update_yaxes(title_text="<b>Covid postives</b>", secondary_y=True)
    fig.show()

