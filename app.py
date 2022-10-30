# Importing libraries
import json
import plotly.express as px
import pandas as pd

from dash_extensions.enrich import DashProxy, html, dcc, Input, Output
from dash_extensions import WebSocket


# Global variables and constants
tickers_lst = []
URL = "ws://127.0.0.1:5678"
tickers_labels = [f'ticker_{i:02}' for i in range(100)]

# Fill options for tickers checklist
options = []
for ticker in tickers_labels:
    options.append({"label": ticker, "value": ticker})

# Create app and layout
app = DashProxy(prevent_initial_callbacks=True)
app.layout = html.Div([
    WebSocket(url=URL, id="ws"),
    html.H2('Tickers Live Feed'),
    html.Br(),
    dcc.Graph(id='live-graph'),
    html.Br(),
    html.Label('Tickers:'),
    dcc.Checklist(options=options, value=tickers_labels[:5], id='ticker-checklist', inline=True),
])


@app.callback(
    Output(component_id="live-graph", component_property="figure"),
    [Input(component_id="ws", component_property="message"),
     Input(component_id="ticker-checklist", component_property="value")]
)
def update_graph(ws_data, tickers_chosen):
    global tickers_lst

    # Collect data in dataframe
    tickers_lst.append(json.loads(ws_data['data']))
    df = pd.DataFrame.from_records(tickers_lst)
    fig = px.line(df, x='date', y=tickers_chosen)

    # Overfill protection
    if len(tickers_lst) > 60:  # Collect in tickers_lst last 60 items
        tickers_lst.pop(0)

    return fig


if __name__ == '__main__':
    app.run_server()
