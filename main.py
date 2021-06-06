from src.database import SQLDatabase
from src.outlier_model import OutlierModel
import pandas as pd
from pathlib import Path
import os
import logging
import plotly.express as px
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
from dash.dependencies import Input, Output

# set and configure logger, stream handler, and file handler
logger = logging.getLogger()
logger.setLevel(logging.INFO)

stream_handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s %(levelname)s :: %(message)s')
stream_handler.setFormatter(formatter)
stream_handler.setLevel(logging.INFO)

file_handler = logging.FileHandler('info.log')
file_handler.setFormatter(formatter)
file_handler.setLevel(logging.DEBUG)

logger.addHandler(stream_handler)
logger.addHandler(file_handler)

# get absolute path of file so relative paths can be used later
cur_path = Path(__file__)
data_path = os.path.join(cur_path.parent, 'data/input/Outliers.csv')

if __name__ == '__main__':

    # read in data from our data base
    db = SQLDatabase(data_path, 'OutlierDB.db', 'OutlierTable')
    db_conn = db.create_connection()
    price_data = pd.read_sql('SELECT * FROM OutlierTable', db_conn)

    # remove any null values from the dataset
    price_data = price_data[price_data['Price'].notna()]
    price_data = price_data[price_data['Date'].notna()]

    # ensure date column is a date
    price_data['Date'] = pd.to_datetime(price_data.Date)

    # sort of our data by date
    price_data = price_data.sort_values(by='Date')

    # calculate rolling average
    price_data['Monthly Rolling Average Price'] = price_data['Price'].rolling(30).mean()

    # get initial time series price
    price_fig = px.line(price_data, x='Date', y=["Price", "Monthly Rolling Average Price"])
    price_fig.update_layout(title_text='Price Data Over Time', title_x=0.5)
    price_fig.update_layout(legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01))
    price_fig.update_yaxes(title_text="Price", title_standoff=25)
    price_fig.update_xaxes(title_text="Date", title_standoff=25)

    # get histogram of price
    price_his = px.histogram(price_data, x='Price', nbins=20, color="Weekday")
    price_his.update_layout(title_text='Histogram of Prices by Day', title_x=0.5)
    price_his.update_xaxes(title_text="Price", title_standoff=25)

    # difference data
    price_data['Price Difference'] = price_data['Price'] - price_data['Price'].shift(1)

    # plot the difference data
    diff_fig = px.line(price_data, x='Date', y="Price Difference")
    diff_fig.update_layout(title_text='Differenced Price Data Over Time', title_x=0.5)
    diff_fig.update_layout(legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01))
    diff_fig.update_yaxes(title_text="Differenced Price", title_standoff=25)
    diff_fig.update_xaxes(title_text="Date", title_standoff=25)

    # train outlier model
    model_obj = OutlierModel(price_data, 0.05)
    model_data = model_obj.train_model()

    # plot outliers
    outliers_fig = px.scatter(model_data, x='Date', y="Price", color='Outlier')
    outliers_fig.update_layout(title_text='Price Data Over Time by Outliers', title_x=0.5)
    outliers_fig.update_layout(legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01))
    outliers_fig.update_yaxes(title_text="Price", title_standoff=25)
    outliers_fig.update_xaxes(title_text="Date", title_standoff=25)

    # initialise very basic Plotly Dash Application
    app = dash.Dash()

    app.layout = html.Div(children=[
        html.H1(children='Outliers Project', style={'textAlign': 'center'}),
        html.Div(children='This application allows users to view and download the outliers in a provided pricing dataset.', style={'textAlign': 'center', 'padding':'10px'}),
        html.Div(children='The application also allows users to dynamically set the main hyper-parameter of the model used to detect the outliers in the dataset.', style={'textAlign': 'center', 'padding': '10px'}),
        html.Div(children='The backend algorithm used to detect the outliers in the dataset is the unsupervised isolation forest algorithm.', style={'textAlign': 'center', 'padding':'10px'}),
        html.H2(children='Exploratory Visualisations', style={'textAlign': 'center'}),
        dcc.Graph(figure=price_fig, id='price-graph'),
        dcc.Graph(figure=price_his, id='price-hist'),
        html.Div(children='The provided outlier dataset is not stationary. This can be seen by the increasing rolling average in the "Price Data Over Time" figure. Based on the "Histogram of Prices by Day" figure, there does not appear to be fluctuations in prices based on the day of the week.',
                 style={'textAlign': 'center', 'padding': '5px'}),
        html.H2(children='Differencing', style={'textAlign': 'center'}),
        html.Div(children='Differencing is applied to the dataset to ensure that it is stationary before it is trained. The results of differencing can be seen below.', style={'textAlign': 'center', 'padding': '10px'}),
        dcc.Graph(figure=diff_fig, id='diff-graph'),
        html.H2(children='Outlier Visualisation and Results', style={'textAlign': 'center'}),
        html.Div(children='The slider below allows users to dynamically adjust the contamination parameter of the outlier model. Contamination is an estimate of the percentage of outliers in a dataset. The default value has been set to 5 percent.',
            style={'textAlign': 'center', 'padding': '10px'}),
        html.Div( children='The higher the contamination parameter is set, the more outliers will be visible in the graph and dataset below.',
            style={'textAlign': 'center', 'padding': '10px'}),
        html.Div([
            dcc.Slider(
                id='slider',
                min=0.0,
                max=10.0,
                step=0.5,
                value=5,
                marks={
                    0: {'label': '0%'},
                    0.5: {'label': '0.5%'},
                    1: {'label': '1.0%'},
                    1.5: {'label': '1.5%'},
                    2: {'label': '2.0%'},
                    2.5: {'label': '2.5%'},
                    3: {'label': '3.0%'},
                    3.5: {'label': '3.5%'},
                    4: {'label': '4.0%'},
                    4.5: {'label': '4.5%'},
                    5: {'label': '5.0%'},
                    5.5: {'label': '5.5%'},
                    6: {'label': '6.0%'},
                    6.5: {'label': '6.5%'},
                    7: {'label': '7.0%'},
                    7.5: {'label': '7.5%'},
                    8: {'label': '8.0%'},
                    8.5: {'label': '8.5%'},
                    9: {'label': '9.0%'},
                    9.5: {'label': '9.5%'},
                    10: {'label': '10.0%'}
                }
            ),
            html.Div(id='slider-output-container')
            ],
            style={'width': '75%', 'marginLeft': 'auto', 'marginRight': 'auto', 'padding':'10px'}
        ),
        dcc.Graph(figure=outliers_fig, id='outliers-graph'),
        html.H3(children='Results Table', style={'textAlign': 'center'}),
        html.Div(children='The full results of the outlier detection model can be viewed and exported from the table below.', style={'textAlign': 'center', 'padding': '10px'}),
        html.Div(children=[
            dash_table.DataTable(
                id='final-table',
                columns=[{"name": i, "id": i} for i in ['Date', 'Price', 'Outlier']],
                data=model_data.to_dict('records'),
                export_format='csv',
                style_table={
                    'maxHeight': '200px',
                    'overflowY': 'scroll',
                }
            )
            ],
            style={'width':'75%', 'marginLeft': 'auto', 'marginRight': 'auto'}
        )
    ])

    # call back function to update outlier plot and data based on slider
    @app.callback([Output('outliers-graph', 'figure'),
                   Output('final-table', 'data')],
                  Input('slider', 'value'))
    def retrain_model(value):

        # convert value to percentage
        contamination = value/100

        # re-train outlier model
        remodel_obj = OutlierModel(price_data, contamination)
        remodel_data = remodel_obj.train_model()

        reoutliers_fig = px.scatter(remodel_data, x='Date', y="Price", color='Outlier')
        reoutliers_fig.update_layout(title_text='Price Data Over Time by Outliers', title_x=0.5)
        reoutliers_fig.update_layout(legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01))
        reoutliers_fig.update_yaxes(title_text="Price", title_standoff=25)
        reoutliers_fig.update_xaxes(title_text="Date", title_standoff=25)

        return reoutliers_fig, remodel_data.to_dict('records')



    app.run_server(debug=True, use_reloader=False)

