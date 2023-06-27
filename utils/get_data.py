import pandas as pd


def load_data():
    data = pd.read_csv("./data/customer_b.csv")
    data["transaction_timestamp"] = pd.to_datetime(data["transaction_timestamp"])
    return data


weekday_order = [
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
    "Sunday",
]
data = load_data()
data.dropna(inplace=True)
##Current Month
current_end_date = data["transaction_timestamp"].max()
current_month_start_date = current_end_date - pd.DateOffset(months=1)
current_month_data = data[
    (data["transaction_timestamp"] >= current_month_start_date)
    & (data["transaction_timestamp"] <= current_end_date)
]
### Previous Month
prev_month_end_date = current_month_start_date - pd.DateOffset(days=1)
prev_start_date = prev_month_end_date - pd.DateOffset(months=1)
prev_month_data = data[
    (data["transaction_timestamp"] >= prev_start_date)
    & (data["transaction_timestamp"] <= prev_month_end_date)
]
### Current Week
current_week_start_date = current_end_date - pd.DateOffset(weeks=1)
current_week_data = data[
    (data["transaction_timestamp"] >= current_week_start_date)
    & (data["transaction_timestamp"] <= current_end_date)
]

### Previous Week
prev_week_end_date = current_week_start_date - pd.DateOffset(days=1)
prev_week_start_date = prev_week_end_date - pd.DateOffset(weeks=1)
prev_week_data = data[
    (data["transaction_timestamp"] >= prev_week_start_date)
    & (data["transaction_timestamp"] <= prev_week_end_date)
]
