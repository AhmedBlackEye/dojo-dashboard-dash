import dash
from dash import html, dcc, Input, Output, callback
import pandas as pd
import plotly.express as px
from components.metric import metric
from utils.get_data import *
from utils.graphs import *
from utils.model import add_predicted_sales, visualize_forecast

dash.register_page(__name__)


#################################### Metrics ####################################
def get_metrics_layout(current_data, prev_data):
    total_sales = current_data["amount"].sum()
    last_months_sales = prev_data["amount"].sum()
    sales_pct_change = (total_sales - last_months_sales) / total_sales * 100
    sales_metric = metric(
        "Total Page Views", total_sales, sales_pct_change, img_name="sales"
    )

    transaction_num = len(current_data)
    prev_transaction_num = len(prev_data)
    transaction_pct_change = (
        (transaction_num - prev_transaction_num) / transaction_num * 100
    )
    transaction_metric = metric(
        "Number Of Transaction",
        transaction_num,
        transaction_pct_change,
        img_name="transactions",
    )

    avg_sale_value = current_data["amount"].mean()
    prev_avg_sale_value = prev_data["amount"].mean()
    avg_sale_pct_change = (avg_sale_value - prev_avg_sale_value) / avg_sale_value * 100
    avg_sale_metric = metric(
        "Average Sale", avg_sale_value, avg_sale_pct_change, img_name="coin"
    )

    most_transaction_postcode_area = current_data["postcode_area"].mode()[0]
    prev_most_transaction_postcode_area = prev_data["postcode_area"].mode()[0]
    most_transaction_postcode_metric = metric(
        "Most Transaction in",
        most_transaction_postcode_area,
        prev_most_transaction_postcode_area,
        img_name="location",
        is_num_metric=False,
    )
    return html.Div(
        className="stats lg:max-w-screen-lg w-full max-[600px]:grid-cols-1 max-[600px]:grid-rows-4 max-[700px]:grid-cols-2 max-[700px]:grid-rows-2 max-[800px]:grid-cols-4 max-[800px]:grid-rows-1",
        children=[
            sales_metric,
            transaction_metric,
            avg_sale_metric,
            most_transaction_postcode_metric,
        ],
    )


def get_dashboard_layout(data):
    return html.Div(
        className="grid grid-cols-8 bg-base-100 mt-10 rounded-xl",
        children=[
            dcc.Graph(
                className="col-span-5",
                figure=get_sales_over_time(data),
            ),
            dcc.Graph(
                className="col-span-3",
                figure=get_sales_per_card_type(data),
            ),
            dcc.Graph(
                className="col-span-4",
                figure=get_sales_per_weekday(data),
            ),
            dcc.Graph(className="col-span-4", figure=get_sales_per_location(data)),
        ],
    )


layout = html.Div(
    children=[
        html.Nav(
            className="tabs tabs-boxed",
            children=[
                html.A("This Month", className="tab tab-lg", id="dashboard-tab-1"),
                html.A("This Week", className="tab tab-lg", id="dashboard-tab-2"),
            ],
        ),
        dcc.Loading(
            id="loading",
            className="loading loading-dots loading-lg",
            children=[
                html.Div(
                    id="dashboard-tab-content",
                    className="p-4 text-center",
                )
            ],
        ),
    ],
)

is_tab_1 = True


@callback(
    [
        Output("dashboard-tab-content", "children"),
        Output("dashboard-tab-1", "className"),
        Output("dashboard-tab-2", "className"),
    ],
    [
        Input("dashboard-tab-1", "n_clicks"),
        Input("dashboard-tab-2", "n_clicks"),
    ],
)
def render_tab_content(tab1_clicks, tab2_clicks):
    global is_tab_1
    if is_tab_1:
        current_data = current_month_data
        prev_data = prev_month_data
        tab1_class = "tab tab-lg tab-active"
        tab2_class = "tab tab-lg"
    else:
        current_data = current_week_data
        prev_data = prev_week_data
        tab1_class = "tab tab-lg"
        tab2_class = "tab tab-lg tab-active"

    content_text = html.Div(
        children=[
            get_metrics_layout(current_data, prev_data),
            get_dashboard_layout(current_data),
        ]
    )
    is_tab_1 = not is_tab_1

    return content_text, tab1_class, tab2_class
