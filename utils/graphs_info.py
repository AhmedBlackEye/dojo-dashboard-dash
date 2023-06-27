# import pandas as pd
# from dash import html


# def get_sales_over_time_info(data):
#     daily_sales = (
#         data.groupby(data["transaction_timestamp"].dt.date)["amount"]
#         .sum()
#         .reset_index()
#     )
#     total_revenue = daily_sales["amount"].sum()
#     average_sale = daily_sales["amount"].mean()
#     highest_sale = daily_sales["amount"].max()
#     most_transaction_day = data["transaction_timestamp"].dt.date.value_counts().idxmax()
#     most_profitable_day = daily_sales.loc[
#         daily_sales["amount"].idxmax(), "transaction_timestamp"
#     ]
#     return [
#         html.Li(f"Total Revenue: £{round(total_revenue,2)}"),
#         html.Li(f"Average Sales Value: £{round(average_sale,2)}"),
#         html.Li(f"Highest Sale: £{round(highest_sale,2)}"),
#         html.Li(f"Most Transaction day: {most_transaction_day}"),
#         html.Li(f"Most Profitable Day: {most_profitable_day}"),
#         ,
#     ]
