# Importing libraries
import json
import plotly.express as px
import pandas as pd

from dash_extensions.enrich import DashProxy, html, dcc, Input, Output
from dash_extensions import WebSocket


# Global variables and constants
tickers_lst = []
URL = "ws://127.0.0.1:5678"

# Create app
app = DashProxy(prevent_initial_callbacks=True)
app.layout = html.Div([
    html.H3('Tickers Live Feed'),
    html.Div(id="live-values"),
    dcc.Graph(id='live-graph'),
    WebSocket(url=URL, id="ws")
])


@app.callback(Output("live-values", "children"), [Input("ws", "message")])
def update_div(e):
    return f"Response from websocket: {e['data']}"


@app.callback(Output("live-graph", "figure"), [Input("ws", "message")])
def update_graph(e):
    global tickers_lst

    # Collect data in dataframe
    tickers_lst.append(json.loads(e['data']))
    df = pd.DataFrame.from_records(tickers_lst)
    fig = px.line(df, x='date', y=['ticker_00', 'ticker_01', 'ticker_02', 'ticker_03', 'ticker_04'])

    # Overfill protection
    if len(tickers_lst) > 60:  # Collect in tickers_lst last 60 items
        tickers_lst.pop(0)

    return fig


if __name__ == '__main__':
    app.run_server()
