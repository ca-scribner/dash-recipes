"""
Recipe shows how to assemble heatmaps and scatter plots as subplits in the same figure

Key challenges:
-   colorbar for heatmap and legend for scatter plot are automatically placed on the figure coordinate system, not
    relative to the subplot.  Need to handle that yourself by controlling controlling colorbar/legend position
-   all scatter subplots share the same legend.  This might be a problem?  Might be able to add more?
"""

from plotly.subplots import make_subplots
import plotly.graph_objs as go
import pandas as pd
import numpy as np


import dash
import dash_core_components as dcc
import dash_html_components as html

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)


def update_figure():
    dates = pd.date_range(start='2019-01-01', periods=6, freq='MS')
    values = list(range(4))
    z = np.arange(len(dates) * len(values)).reshape(len(values), -1)

    n_rows = 4
    # colorbar_length is each row's portion of the vertical height, scaled down to give some spacing
    # Is there a better way to do this from the fig subplots definition itself?
    colorbar_length = 1 / n_rows * 0.95
    # Make colorbar_y positions.  Index this to 1-indexed rather than 0-indexed and starting from top row of 1 and
    # bottom row of n to match the row convention of plotly subplots
    colorbar_y = [1 - ((i - 0.5) / n_rows) for i in range(n_rows + 1)]

    fig = make_subplots(rows=n_rows, cols=1, specs=[[{}] for i in range(n_rows)],
                        shared_xaxes=True, shared_yaxes=True,
                        vertical_spacing=0.02)

    i_middle = (n_rows // 2) + 1

    # Make some heatmaps
    for i in range(1, i_middle):
        trace_heatmap = go.Heatmap(
            x=dates,
            y=values,
            z=z,
            colorbar={'y': colorbar_y[i], 'len': colorbar_length}
        )
        fig.append_trace(trace_heatmap, i, 1)

    # Make some scatter plots
    for i in range(i_middle, n_rows + 1):
        trace1 = go.Scatter(
            x=dates,
            y=z[2, :],
            showlegend=True,
        )
        fig.append_trace(trace1, i, 1)

    # I think these amount to the same thing, but the second is probably better as it doesn't presume to know the 
    # internal structure?
    fig['layout'].update(height=600, width=600, title='Stacked Subplots with Shared X-Axes')
    fig.update_layout(legend={'y': colorbar_y[3]})
    return fig


app.layout = html.Div([
    dcc.Graph(
        figure=update_figure(),
        id='my-figure'),
])


if __name__ == '__main__':
    app.run_server(debug=True, port=8058)
