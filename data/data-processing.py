import pandas as pd
import dash
from dash import dcc
from dash import html

from dash.dependencies import Output
from dash.dependencies import Input

import os

import plotly.express as px
import dash_bootstrap_components as dbc
#read csv files
sales_0 = pd.read_csv('daily_sales_data_0.csv')
sales_1 = pd.read_csv('daily_sales_data_1.csv')
sales_2 = pd.read_csv('daily_sales_data_2.csv')

#merge datasets
sales_merged = pd.concat([sales_0,sales_1,sales_2], ignore_index=True)

#filter product
filtered_df = sales_merged[sales_merged['product']=='pink morsel']

#remove $ and convert to integers
filtered_df['price'] = filtered_df['price'].str.replace('$', '')
filtered_df['price'] = pd.to_numeric(filtered_df['price'], downcast='integer', errors='coerce')

#create sales
filtered_df['sales'] = filtered_df['price'] * filtered_df['quantity']

#remove unnecessary columns
filtered_df.drop(columns=["product"], axis=1, inplace=True)
filtered_df.drop(columns=["quantity"], axis=1, inplace=True)
filtered_df.drop(columns=["price"], axis=1, inplace=True)
column_names = list(filtered_df)
print(column_names)



# 1.2 load external / dbc stylesheets. Not necessary but its an option
external_stylesheets = [
    {  "href": "https://fonts.googleapis.com/css2?"
                "family=Lato:wght@400;700&display=swap",
        "rel": "stylesheet",
    },
    dbc.themes.BOOTSTRAP
]

# 1.3 initiate the app
app = dash.Dash(__name__,
                external_stylesheets=external_stylesheets,
                suppress_callback_exceptions=True, # sometimes callbacks dont work which is intended behaviour.
                                                   #This suppresses those notifications
                )

# App layout

app.layout = html.Div([
    html.H4('Historic Sales Records of Pink Morsels'),
    dcc.Graph(id="graph"),
    dcc.Checklist(
        id="checklist",
        options=["sales", "region", "date"],
        inline=True
    ),
])
@app.callback(
    Output("graph", "figure"),
    Input("checklist", "value"))

def update_line_chart(continents):
    df = filtered_df # replace with your own data source

    fig = px.line(df,
        x="date", y="sales", color="region")
    return fig



app.title = "My Dashboard!" # name to be dislplayed eg in browser tab


# Run the app
if __name__ == '__main__':
    app.run(debug=True)