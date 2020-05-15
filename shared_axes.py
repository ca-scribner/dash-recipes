"""
from plotly forums.  Lost link...
"""

# import plotly.offline as py
import plotly.graph_objs as go

# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)


def create_figure():
    trace1 = go.Scatter(
        x=[1, 2, 3],
        y=[2, 3, 4]
    )
    trace2 = go.Scatter(
        x=[1, 2, 3],
        y=[5, 5, 5],
        xaxis='x2',
        yaxis='y2'
    )
    trace3 = go.Scatter(
        x=[1, 2, 3],
        y=[600, 700, 800],
        xaxis='x3',
        yaxis='y3'
    )
    trace4 = go.Scatter(
        x=[1, 2, 3],
        y=[7000, 8000, 9000],
        xaxis='x4',
        yaxis='y4'
    )
    data = [trace1, trace2, trace3, trace4]
    layout = go.Layout(
        xaxis=dict(
            domain=[0, 0.45],
            anchor='y'
        ),
        xaxis2=dict(
            domain=[0.55, 1],
            anchor='y2',
            scaleanchor='x'
        ),
        xaxis3=dict(
            domain=[0, 0.45],
            anchor='y3',
            scaleanchor='x'
        ),
        xaxis4=dict(
            domain=[0.55, 1],
            anchor='y4',
            scaleanchor='x'
        ),
        yaxis=dict(
            domain=[0, 0.45],
            anchor='x'
        ),
        yaxis2=dict(
            domain=[0, 0.45],
            anchor='x2'
        ),
        yaxis3=dict(
            domain=[0.55, 1],
            anchor='x3'
        ),
        yaxis4=dict(
            domain=[0.55, 1],
            anchor='x4'
        )
    )
    fig = go.Figure(data=data, layout=layout)
    return fig


app.layout = html.Div(children=[
    html.H1(children='Hello Dash'),

    html.Div(children='''
        Dash: A web application framework for Python.
    '''),

    dcc.Graph(
        id='example-graph',
        figure=create_figure()
    )
])


if __name__ == '__main__':
    app.run_server(debug=True, port=8057)
