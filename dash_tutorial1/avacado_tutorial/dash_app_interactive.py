import pandas as pd
from dash import Dash,html,dcc
import numpy as np
from dash.dependencies import Input,Output

avocado_df=pd.read_csv('E:/RIYA_PERSONAL/CS/python_GUI/dash_tutorial1/avacado_tutorial/avocado.csv')
avocado_df = avocado_df.copy()
avocado_df['Date'] = pd.to_datetime(avocado_df['Date'])
avocado_df=avocado_df.sort_values('Date', ascending=True)

avocado_type1=avocado_df[(avocado_df.type=='conventional') & (avocado_df.region=='Albany')]

avocado_type1 = avocado_type1.copy()
avocado_type1['Date'] = pd.to_datetime(avocado_type1['Date'])

avocado_type11=avocado_type1.sort_values('Date', ascending=True)

avocado_type11['yearmonth']=avocado_type11['Date'].dt.strftime('%Y-%m')

bag_counts = avocado_type11.groupby('yearmonth').agg({'Small Bags': 'sum', 'Large Bags': 'sum', 'XLarge Bags': 'sum'}).reset_index()

melted_bag_data=bag_counts.melt(id_vars='yearmonth',value_vars=['Small Bags','Large Bags','XLarge Bags'], var_name='bagsize',value_name='Count')

# data for dropdown-interactivity
regions=avocado_df["region"].sort_values().unique()
avocado_types=avocado_df["type"].sort_values().unique()

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

app_1.layout=html.Div(#Div1
             children=[
                html.Div(#Div2
                children=[
                    html.H1(children="Avocado Insights", className="headtitle")
                ]
                ),#/Div2
                html.Div(#Div3
                className="menu",
                children=[
                    html.Div(#Div4
                    children=[
                        html.Div("Region",className="menutitle"),#/Div5
                        dcc.Dropdown(#dropdown
                        id="regionfilter",
                        options=[{"label":region, "value": region}
                                for region in regions],
                        value="Albany",
                        clearable=False,
                        className="dropdown"
                        )#/dropdown
                    ]
                    ),#/Div4
                    html.Div(#Div6
                    children=[
                        html.Div("Type",className="menutitle"),#/Div7
                        dcc.Dropdown(#dropdown
                        id="typefilter",
                        options=[{"label":avocado_type, "value": avocado_type}
                                for avocado_type in avocado_types],
                        value="organic",
                        clearable=False,
                        searchable=False,
                        className="dropdown"
                        )#/dropdown
                    ]
                    ),#/Div6
                    html.Div(#Div8
                    children=[
                        html.Div("Date",className="menutitle"),#/Div9
                        dcc.DatePickerRange(#date
                            className="rangepicker",
                            id="daterange",
                            min_date_allowed=avocado_type1["Date"].min().date(),
                            max_date_allowed=avocado_type1["Date"].max().date(),
                            start_date=avocado_type1["Date"].min().date(),
                            end_date=avocado_type1["Date"].max().date()
                        )#/date
                    ]
                    )#/Div8
                ]
                ),#/Div3
                html.Div(#Div10
                children=[
                    html.Div(#Div11
                    children=[
                        dcc.Graph(id="avgpricedate",config={"displayModeBar":False})
                    ]
                    ),#/Div11
                    html.Div(#Div12
                    children=[
                        dcc.Graph(id="volumedate",config={"displayModeBar":False})
                    ]
                    ),#Div12
                    html.Div(#Div13
                    children=[
                        dcc.Graph(figure=fig)
                    ]
                    )#/Div13
                ]
                )#/Div10
             ]#children of Div 1 end
)#/Div1



@app_1.callback(
    Output("avgpricedate","figure"),
    Output("volumedate","figure"),
    Input("regionfilter","value"),
    Input("typefilter","value"),
    Input("daterange","start_date"),
    Input("daterange","end_date")
)
def update_charts(region,avocado_type, start_date, end_date):
    global avocado_df
    print(avocado_df)
    start=np.datetime64(start_date)
    end=np.datetime64(end_date)
    r=str(region)
    at=str(avocado_type)
    filtered_data=avocado_df[
        (avocado_df['region']==r) &
        (avocado_df['type']==at) &
        (avocado_df['Date']>= start) &
        (avocado_df['Date']<= end)
    ]
    print(filtered_data)
    # Placeholder variables used in the above filtering
    price_chart_figure = {
        "data": [
            {
                "x": filtered_data["Date"],
                "y": filtered_data["AveragePrice"],
                "type": "lines",
                "hovertemplate": "$%{y:.2f}<extra></extra>",
            },
        ],
        "layout": {
            "title": {
                "text": "Average Price of Avocados",
                "x": 0.05,
                "xanchor": "left",
            },
            "xaxis": {"fixedrange": True},
            "yaxis": {"tickprefix": "$", "fixedrange": True},
            "colorway": ["#00754a"],
            "plot_bgcolor":"#f2f0eb",
            "paper_bgcolor":"#f2f0eb"
        },
    }

    volume_chart_figure = {
        "data": [
            {
                "x": filtered_data["Date"],
                "y": filtered_data["Total Volume"],
                "type": "lines",
            },
        ],
        "layout": {
            "title": {"text": "Avocados Sold", "x": 0.05, "xanchor": "left"},
            "xaxis": {"fixedrange": True},
            "yaxis": {"fixedrange": True},
            "colorway": ["#00754a"],
            "plot_bgcolor":"#f2f0eb",
            "paper_bgcolor":"#f2f0eb"
        },
    }
    return price_chart_figure, volume_chart_figure

if __name__ == "__main__":
    app_1.run_server(debug=True)