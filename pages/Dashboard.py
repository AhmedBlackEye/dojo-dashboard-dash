# import dash
# from dash import html, dcc, Input, Output, callback
# import pandas as pd
# import plotly.express as px
# from components.metric import metric

# dash.register_page(__name__, path="/")


# #################################### Data Extraction ####################################
# def load_data():
#     data = pd.read_csv("./data/customer_a.csv")
#     data["transaction_timestamp"] = pd.to_datetime(data["transaction_timestamp"])
#     return data


# weekday_order = [
#     "Monday",
#     "Tuesday",
#     "Wednesday",
#     "Thursday",
#     "Friday",
#     "Saturday",
#     "Sunday",
# ]
# data = load_data()
# ##Current Month
# current_end_date = data["transaction_timestamp"].max()
# current_month_start_date = current_end_date - pd.DateOffset(months=1)
# current_month_data = data[
#     (data["transaction_timestamp"] >= current_month_start_date)
#     & (data["transaction_timestamp"] <= current_end_date)
# ]
# ### Previous Month
# prev_month_end_date = current_month_start_date - pd.DateOffset(days=1)
# prev_start_date = prev_month_end_date - pd.DateOffset(months=1)
# prev_month_data = data[
#     (data["transaction_timestamp"] >= prev_start_date)
#     & (data["transaction_timestamp"] <= prev_month_end_date)
# ]
# ### Current Week
# current_week_start_date = current_end_date - pd.DateOffset(weeks=1)
# current_week_data = data[
#     (data["transaction_timestamp"] >= current_week_start_date)
#     & (data["transaction_timestamp"] <= current_end_date)
# ]

# ### Previous Week
# prev_week_end_date = current_week_start_date - pd.DateOffset(days=1)
# prev_week_start_date = prev_week_end_date - pd.DateOffset(weeks=1)
# prev_week_data = data[
#     (data["transaction_timestamp"] >= prev_week_start_date)
#     & (data["transaction_timestamp"] <= prev_week_end_date)
# ]


# #################################### Metrics ####################################
# def get_metrics_layout(current_data, prev_data):
#     total_sales = current_data["amount"].sum()
#     last_months_sales = prev_data["amount"].sum()
#     sales_pct_change = (total_sales - last_months_sales) / total_sales * 100
#     sales_metric = metric(
#         "Total Page Views", total_sales, sales_pct_change, img_name="sales"
#     )

#     transaction_num = len(current_data)
#     prev_transaction_num = len(prev_data)
#     transaction_pct_change = (
#         (transaction_num - prev_transaction_num) / transaction_num * 100
#     )
#     transaction_metric = metric(
#         "Number Of Transaction",
#         transaction_num,
#         transaction_pct_change,
#         img_name="transactions",
#     )

#     avg_sale_value = current_data["amount"].mean()
#     prev_avg_sale_value = prev_data["amount"].mean()
#     avg_sale_pct_change = (avg_sale_value - prev_avg_sale_value) / avg_sale_value * 100
#     avg_sale_metric = metric(
#         "Average Sale", avg_sale_value, avg_sale_pct_change, img_name="coin"
#     )

#     most_transaction_postcode_area = current_data["postcode_area"].mode()[0]
#     prev_most_transaction_postcode_area = prev_data["postcode_area"].mode()[0]
#     most_transaction_postcode_metric = metric(
#         "Most Transaction in",
#         most_transaction_postcode_area,
#         prev_most_transaction_postcode_area,
#         img_name="location",
#         is_num_metric=False,
#     )
#     return html.Div(
#         className="stats lg:max-w-screen-lg w-full max-[600px]:grid-cols-1 max-[600px]:grid-rows-4 max-[700px]:grid-cols-2 max-[700px]:grid-rows-2 max-[800px]:grid-cols-4 max-[800px]:grid-rows-1",
#         children=[
#             sales_metric,
#             transaction_metric,
#             avg_sale_metric,
#             most_transaction_postcode_metric,
#         ],
#     )


# #################################### Graphs ####################################
# ################## Sales Over Time Graph ##################
# def get_sales_over_time(data):
#     sales_over_time = (
#         data.groupby("transaction_timestamp")["amount"].sum().cumsum().reset_index()
#     )

#     return px.line(
#         sales_over_time,
#         x="transaction_timestamp",
#         y="amount",
#         title="Sales Over Time",
#         labels={"transaction_timestamp": "Time", "amount": "Sales"},
#     )


# ################## Sales Per Days Graph ##################
# def get_sales_per_weekday(data):
#     sales_per_weekday = (
#         data.groupby(data["transaction_timestamp"].dt.day_name())["amount"]
#         .sum()
#         .reset_index()
#     )
#     sales_per_weekday["transaction_timestamp"] = pd.Categorical(
#         sales_per_weekday["transaction_timestamp"],
#         categories=weekday_order,
#         ordered=True,
#     )

#     sales_per_weekday = sales_per_weekday.sort_values("transaction_timestamp")
#     return px.bar(
#         sales_per_weekday,
#         x="transaction_timestamp",
#         y="amount",
#         title="Sales Per Day",
#         labels={"transaction_timestamp": "Day", "Sales": "Amount"},
#     )


# ################## Sales Per Location Graph ##################
# def get_sales_per_location(data):
#     locations_sales = data.groupby("postcode_area")["amount"].sum().reset_index()
#     return px.pie(
#         locations_sales,
#         values="amount",
#         names="postcode_area",
#         title="Sales by Location",
#         labels={"amount": "Sales Amount", "postcode_area": "Location"},
#     )


# #################################### Rendering ####################################


# def get_dashboard_layout(data):
#     return html.Div(
#         className="grid grid-cols-6",
#         children=[
#             dcc.Graph(
#                 className="col-span-3",
#                 figure=get_sales_over_time(data),
#             ),
#             dcc.Graph(
#                 className="col-span-3",
#                 figure=get_sales_per_location(data),
#             ),
#             dcc.Graph(
#                 className="col-span-2",
#                 figure=get_sales_per_weekday(data),
#             ),
#             dcc.Graph(
#                 className="col-span-2",
#                 figure=get_sales_per_weekday(data),
#             ),
#             dcc.Graph(
#                 className="col-span-2",
#                 figure=get_sales_per_weekday(data),
#             ),
#         ],
#     )


# layout = html.Div(
#     children=[
#         html.Nav(
#             className="tabs tabs-boxed",
#             children=[
#                 html.A("This Month", className="tab tab-lg", id="dashboard-tab-1"),
#                 html.A("This Week", className="tab tab-lg", id="dashboard-tab-2"),
#             ],
#         ),
#         dcc.Loading(
#             id="loading",
#             className="loading loading-dots loading-lg",
#             children=[
#                 html.Div(
#                     id="dashboard-tab-content",
#                     className="p-4 text-center",
#                 )
#             ],
#         ),
#     ],
# )

# is_tab_1 = True


# @callback(
#     [
#         Output("dashboard-tab-content", "children"),
#         Output("dashboard-tab-1", "className"),
#         Output("dashboard-tab-2", "className"),
#     ],
#     [
#         Input("dashboard-tab-1", "n_clicks"),
#         Input("dashboard-tab-2", "n_clicks"),
#     ],
# )
# def render_tab_content(tab1_clicks, tab2_clicks):
#     global is_tab_1
#     if is_tab_1:
#         current_data = current_month_data
#         prev_data = prev_month_data
#         tab1_class = "tab tab-lg tab-active"
#         tab2_class = "tab tab-lg"
#     else:
#         current_data = current_week_data
#         prev_data = prev_week_data
#         tab1_class = "tab tab-lg"
#         tab2_class = "tab tab-lg tab-active"

#     content_text = html.Div(
#         children=[
#             get_metrics_layout(current_data, prev_data),
#             get_dashboard_layout(current_data),
#         ]
#     )
#     is_tab_1 = not is_tab_1

#     return content_text, tab1_class, tab2_class
