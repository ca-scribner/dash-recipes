# https://community.plotly.com/t/dynamic-list-of-dcc-components/14752

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, ALL, State


app = dash.Dash(__name__)
app.config['suppress_callback_exceptions'] = True


app.layout = html.Div(
    children=[
        html.H1(children='Hello Dash'),
        html.Div(id='step_list', children=[]),
        html.Button('Add Step', id='add_step_button'),  # These could be combined to single ID dict like below too
        html.Button('Remove Step', id='remove_step_button'),
        html.Div(id='tester_div'),
    ]
)


# Use dash.callback_context to know which button was pressed.
# Not sure why we need these on the same callback here, but keeping true to the OP use
@app.callback(
    Output('step_list', 'children'),
    [Input('add_step_button', 'n_clicks'),
     Input('remove_step_button', 'n_clicks')],
    [State('step_list', 'children')])
def add_remove_step(add_clicks, remove_clicks, div_list):
    # Identify who was clicked
    ctx = dash.callback_context
    if not ctx.triggered:
        triggered_id = 'No clicks yet'
    else:
        triggered_id = ctx.triggered[0]['prop_id'].split('.')[0]

    # Act
    if triggered_id == 'add_step_button':
        div_list += [html.Div(
            # Index dropdown's using the next available index
            children=[
                'Menu:',
                dcc.Dropdown(id={'type': 'dropdown', 'index': len(div_list)},
                             options=[{'label': v, 'value': v} for v in ['select1', 'select2', 'select3']])
            ])]
    elif len(div_list) > 0 and triggered_id == 'remove_step_button':
        div_list = div_list[:-1]
    return div_list


# Print all the dropdowns dynamically using a pattern matching callback
# https://dash.plotly.com/pattern-matching-callbacks
@app.callback(
    Output('tester_div', 'children'),
    [Input({'type': 'dropdown', 'index': ALL}, 'value')])
def a_function(input):
    return [html.H1(element) for element in input]


if __name__ == '__main__':
    app.run_server(debug=True)
