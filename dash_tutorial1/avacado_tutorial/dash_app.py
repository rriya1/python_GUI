import pandas as pd
from dash import Dash,html,dcc

avocado_df=pd.read_csv('E:/RIYA_PERSONAL/CS/python_GUI/dash_tutorial1/avacado_tutorial/avocado.csv')
avocado_type1=avocado_df[(avocado_df.type=='conventional') & (avocado_df.region=='Albany')]

avocado_type1 = avocado_type1.copy()
avocado_type1['Date'] = pd.to_datetime(avocado_type1['Date'])

avocado_type11=avocado_type1.sort_values('Date', ascending=True)

avocado_type11['yearmonth']=avocado_type11['Date'].dt.strftime('%Y-%m')

bag_counts = avocado_type11.groupby('yearmonth').agg({'Small Bags': 'sum', 'Large Bags': 'sum', 'XLarge Bags': 'sum'}).reset_index()

melted_bag_data=bag_counts.melt(id_vars='yearmonth',value_vars=['Small Bags','Large Bags','XLarge Bags'], var_name='bagsize',value_name='Count')

import plotly.express as px
#initializing dash

app_1=Dash(__name__)
app_1.title="Avocados presented with Dash"

#external style sheet
#not sure whats the use 
#external_stylesheet=["href":]


fig=px.bar(melted_bag_data,
           x='yearmonth',
           y='Count',
           color='bagsize',
           title="Variation in purchased bag-sizes according to month of a year(2015-2018)",
           labels={'count':"bag count","yearmonth":"months-yearwise", "bagsize":"type of bag"},
           color_discrete_map={"Small Bags":"#005e66","Large Bags": "#eed350","XLarge Bags":"#567500"},
           )
fig.update_layout(barmode='stack')

app_1.layout=html.Div(
                
                children=[
                    html.Div(
                        children=[
                            html.H1(children="Avocado Insights",
                                    className='headtitle'),
                            html.P(children="This plot will help us visulaize avocado average prices fluctuation with time",
                                   className='textcustom'),
                            dcc.Graph(figure={
                                        "data":[
                                            {
                                                "x": avocado_type11["Date"],
                                                "y": avocado_type11["AveragePrice"],
                                                "type": "lines",
                                            },
                                        ],
                                        "layout":{"title":"Average price vs Date",
                                                  "plot_bgcolor":"#f2f0eb",
                                                  "paper_bgcolor":"#f2f0eb"},
                                            },
                                    ),
                            dcc.Graph(figure={
                                    "data":[
                                        {
                                            "x": avocado_type11['Date'],
                                            "y":avocado_type11['Total Volume'],
                                            "type":"lines",
                                        },
                                            ],
                                    "layout":{"title":"Volume of avocados vs Date",
                                              "plot_bgcolor":"#f2f0eb",
                                              "paper_bgcolor":"#f2f0eb"},
                                            },
                                    ),
                            html.P(children="This plot will help us visulaize purchased avocado bag size monthly",
                                   className='textcustom'),
                            dcc.Graph(figure=fig)
                                ]
                            )
                  
                ])

if __name__ == "__main__":
    app_1.run_server(debug=True)