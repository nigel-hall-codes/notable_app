import datetime
import sys

import pandas as pd
from dash import Dash
from dash import dash_table
from dash import html
from dash import dcc
from app.api import API
import dash
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc

api = API()

app = Dash(
    __name__,
    routes_pathname_prefix='/dash/',
    external_stylesheets=[dbc.themes.BOOTSTRAP]
)

server = app.server
app.config.suppress_callback_exceptions = True
app.layout = html.Div(id='main-app', className='row')
top_section = html.Div(className='row', style={"marginTop": "10px"})
physician_list_div = html.Div(className="col-md-4", style={"marginTop": "10px", "marginLeft": "10px"})
appointment_list_div = html.Div(id='notable-appointment-list-div', className="col-md-4", style={"marginTop": "10px", "marginLeft": "10px"})

app.layout.children = [top_section]
app_info_div = html.Div(className='row')
top_section.children = [app_info_div, physician_list_div, appointment_list_div]


def appointmentTable():
    df = pd.DataFrame(columns=["#", "Name", "Time", "kind"])
    return [html.H3("Appointments"), html.H4("", id="notable-selected-physician-name-div"), dash_table.DataTable(id="notable-appointment-table",
                                                 columns=[{"name": i, "id": i} for i in df.columns],
                                                 data=df.to_dict('records'),
                                                 style_table={'overflowX': 'auto',
                                                              'overflowY': 'auto',
                                                              'textAlign': 'right',
                                                              'font_size': '11px',
                                                              'whiteSpace': 'normal',
                                                              'height': 'auto',
                                                              },
                                                 style_cell={'textAlign': 'left'},
                                                 page_size=10,
                                                 sort_action='native',
                                                 filter_action='native'
                                                 )]

def physicianTable():

    df = api.get_physicians()

    return [html.H3("Physicians"), dash_table.DataTable(id="notable-physician-table",
                             columns=[{"name": i, "id": i} for i in df.drop("id", axis=1).columns],
                             data=df.to_dict('records'),
                             style_table={'overflowX': 'auto',
                                          'overflowY': 'auto',
                                          'textAlign': 'right',
                                          'font_size': '11px',
                                          'whiteSpace': 'normal',
                                          'height': 'auto',
                                          },
                             style_cell={'textAlign': 'left'},
                             page_size=10,
                             sort_action='native',
                             filter_action='native'
                             )]

def todays_date_and_notable_label():
    todays_date = datetime.datetime.now().strftime("%m/%d/%Y")
    notable_label = html.H1("Notable", style={"marginTop": "10px", "marginLeft": "10px"})

    todays_date_div = html.H4(todays_date, style={"marginTop": "10px", "marginLeft": "10px"})

    return [notable_label, todays_date_div]


physician_list_div.children = physicianTable()
appointment_list_div.children = appointmentTable()
app_info_div.children = todays_date_and_notable_label()

@app.callback(dash.dependencies.Output('notable-appointment-list-div', "children"),
              [dash.dependencies.Input('notable-physician-table', 'active_cell'),
              dash.dependencies.Input('notable-physician-table', 'data')]
              )
def update_selected_physicians_appointments(active_cell, data):

    if active_cell == None:
        raise PreventUpdate

    today = datetime.datetime.now().strftime("%m-%d-%Y")
    phys_id = data[active_cell['row']]['id']
    appointments_df = api.get_physician_appointments_for_day(phys_id, today)

    return [html.H3(data[active_cell['row']]['Name']), dash_table.DataTable(id="notable-physician-appointments-table",
                                                          columns=[{"name": i, "id": i} for i in appointments_df.columns],
                                                          data=appointments_df.to_dict('records'),
                                                          style_table={'overflowX': 'auto',
                                                                       'overflowY': 'auto',
                                                                       'textAlign': 'right',
                                                                       'font_size': '11px',
                                                                       },
                                                          style_cell={'textAlign': 'left'},
                                                          page_size=10,
                                                          sort_action='native',
                                                          filter_action='native'
                                                      )]


if __name__ == '__main__':
    app.run_server(debug=True)