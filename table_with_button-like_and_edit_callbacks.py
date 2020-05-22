import pandas as pd
import numpy as np
import dash
import dash_html_components as html
from dash.dependencies import State, Input, Output
import dash_table

columns = "abcde"
df = pd.DataFrame(np.random.rand(10, len(columns)), columns=list("abcde"))
app = dash.Dash(__name__)


@app.callback(
    [
        Output("table", "data"),
        Output("edit-time", "children"),
    ],
    [
        Input("table", "data_timestamp"),
        Input("table", "active_cell"),
    ],
    [
        State("table", "data"),
        State("table", "data_previous"),
    ]
)
def table_data_update_dispatcher(data_timestamp, active_cell, data, data_previous):
    """
    This callback wraps all actions that will result in the table data being output
    """
    # Escape if we have no data.  This might not be intention if app's data is empty?
    if data is None and data_previous is None:
        return dash.no_update

    ctx = dash.callback_context
    if ctx.triggered[0]["prop_id"] == "table.data_timestamp":
        return table_edit_callback(data, data_previous), data_timestamp
    elif ctx.triggered[0]["prop_id"] == "table.active_cell":
        return table_on_click_via_active_cell(active_cell, data), data_timestamp
    else:
        # During app boot (?) the callback fires without normal trigger events, which can slip down here.  Can't end
        # without a return because that will set table.data == None in perpetuity
        return dash.no_update


def table_edit_callback(data, data_previous):
    """
    Compares two dash table data entities, printing the (row, column) locations of any differences
    """
    # Determine where the change occurred
    diff = diff_dashtable(data, data_previous)

    for d in diff:
        r_changed = d['index']
        c_changed = d['column_name']
        print(f"Caught a change in the table at {r_changed} {c_changed}!")

        # # If the column is empty it won't be in the dict.  Use .get to handle this with empty string as default
        # data[r_changed][CHANGED_COLUMN] = f"{data[r_changed].get(CHANGED_COLUMN, '')} {CHANGED_PAD_START}{c_changed}{CHANGED_PAD_END}"
    return data


def table_on_click_via_active_cell(active_cell, rows):
    """
    Hack to make a cell in a DashTable act like a button.

    If any cell in column 'a' is clicked, it overwrites this row's data in column b with the value in column a
    """
    if active_cell is None:
        return rows

    # If I click on a particular column (say suggestion X), put that value into a different column (say blessed clf)
    if active_cell['column_id'] == 'a':
        rows[active_cell['row']]['b'] = rows[active_cell['row']]['a']

    return rows


def diff_dashtable(data, data_previous, row_id_name=None):
    """Generate a diff of Dash DataTable data.

    Modified from: https://community.plotly.com/t/detecting-changed-cell-in-editable-datatable/26219/2

    Parameters
    ----------
    data: DataTable property (https://dash.plot.ly/datatable/reference)
        The contents of the table (list of dicts)
    data_previous: DataTable property
        The previous state of `data` (list of dicts).

    Returns
    -------
    A list of dictionaries in form of [{row_id_name:, column_name:, current_value:,
        previous_value:}]
    """
    df, df_previous = pd.DataFrame(data=data), pd.DataFrame(data_previous)

    if row_id_name is not None:
        # If using something other than the index for row id's, set it here
        for _df in [df, df_previous]:

            # Why do this?  Guess just to be sure?
            assert row_id_name in _df.columns

            _df = _df.set_index(row_id_name)
    else:
        row_id_name = "index"

    # Pandas/Numpy says NaN != NaN, so we cannot simply compare the dataframes.  Instead we can either replace the
    # NaNs with some unique value (which is fastest for very small arrays, but doesn't scale well) or we can do
    # (from https://stackoverflow.com/a/19322739/5394584):
    # Mask of elements that have changed, as a dataframe.  Each element indicates True if df!=df_prev
    df_mask = ~((df == df_previous) | ((df != df) & (df_previous != df_previous)))

    # ...and keep only rows that include a changed value
    df_mask = df_mask.loc[df_mask.any(axis=1)]

    changes = []

    # This feels like a place I could speed this up if needed
    for idx, row in df_mask.iterrows():
        row_id = row.name

        # Act only on columns that had a change
        row = row[row.eq(True)]

        for change in row.iteritems():

            changes.append(
                {
                    row_id_name: row_id,
                    "column_name": change[0],
                    "current_value": df.at[row_id, change[0]],
                    "previous_value": df_previous.at[row_id, change[0]],
                }
            )

    return changes


def get_app_layout():
    children = [
        html.H1(id="header"),
        dash_table.DataTable(
            id='table',
            columns=[{"name": c, "id": c} for c in columns],
            data=df.to_dict('records'),
            editable=True,
        ),
        html.H2(id='edit-time'),
    ]

    return html.Div(children)


app.layout = get_app_layout()


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
