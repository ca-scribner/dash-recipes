# from https://dash.plotly.com/datatable/dropdowns
import dash
import dash_html_components as html
import dash_table
import pandas as pd
from collections import OrderedDict


app = dash.Dash(__name__)

df = pd.DataFrame(OrderedDict([
    ('climate', ['Sunny', 'Snowy', 'Sunny', 'Rainy']),
    ('temperature', [13, 43, 50, 30]),
    ('city', ['NYC', 'Montreal', 'Miami', 'NYC'])
]))


app.layout = html.Div([
    dash_table.DataTable(
        id='table-dropdown',
        data=df.to_dict('records'),
        columns=[{"name": i, "id": i} for i in df.columns],
        # columns=[
            # {'id': 'climate', 'name': 'climate', 'presentation': 'dropdown'},
            # {'id': 'temperature', 'name': 'temperature'},
            # {'id': 'city', 'name': 'city', 'presentation': 'dropdown'},
        # ],

        editable=True,
        dropdown={
            'climate': {
                'options': [
                    {'label': i, 'value': i}
                    for i in df['climate'].unique()
                ]
            },
            'city': {
                'options': [
                    {'label': i, 'value': i}
                    for i in df['city'].unique()
                ]
            }
        }
    ),
    html.Div(id='table-dropdown-container')
])


if __name__ == '__main__':
    # Hacky way to auto pick a port
    ports = range(8850, 8860, 1)
    for port in ports:
        try:
            print(f"TRYING PORT {port}")
            app.run_server(debug=True, port=port)
        except OSError:
            continue
        break