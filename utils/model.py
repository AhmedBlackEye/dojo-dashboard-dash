import plotly.express as px
from .get_data import data
import plotly.graph_objects as go
import numpy as np
from sklearn.metrics import mean_absolute_error, mean_squared_error
from sklearn.model_selection import train_test_split
import pandas as pd
from prophet import Prophet


def prepare_data(data):
    return (
        data.groupby(data["transaction_timestamp"].dt.date)["amount"]
        .sum()
        .reset_index()
        .rename(columns={"transaction_timestamp": "ds", "amount": "y"})
    )


def split_data(df, test_size=0.3, random_state=42):
    return train_test_split(df, test_size=test_size, random_state=random_state)


def train_prophet_model(train_df):
    model = Prophet(growth="linear")
    model.fit(train_df)
    return model


def make_predictions(model, future_dates):
    forecast = model.predict(future_dates)
    return forecast


def mean_absolute_percentage_error(y_true, y_pred):
    """Calculates MAPE given y_true and y_pred"""
    y_true, y_pred = np.array(y_true), np.array(y_pred)
    return np.mean(np.abs((y_true - y_pred) / y_true)) * 100


def evaluate_model(y_true, y_pred):
    # Ensure that y_pred has the same length as y_true
    y_pred = y_pred[: len(y_true)]

    # Evaluate the model
    mae = mean_absolute_error(y_true, y_pred)
    mse = mean_squared_error(y_true, y_pred)
    rmse = mean_squared_error(y_true, y_pred, squared=False)

    mean_percentage_error = mean_absolute_percentage_error(y_true, y_pred)

    print("Mean Absolute Error (MAE):", mae)
    print("Mean Squared Error (MSE):", mse)
    print("Root Mean Squared Error (RMSE):", rmse)
    print("Mean Percentage Error (MPE):", mean_percentage_error)


df_daily_sales = prepare_data(data)
train_df, test_df = split_data(df_daily_sales)
model = train_prophet_model(train_df)
future_dates = model.make_future_dataframe(periods=30)
forecast = make_predictions(model, future_dates)
y_true = test_df["y"].values
y_pred = forecast.loc[len(train_df) :, "yhat"].values
evaluate_model(y_true, y_pred)


def visualize_forecast():
    fig = px.line(forecast, x="ds", y="yhat", title="Predicted Sales")
    fig.update_layout(xaxis_title="Date", yaxis_title="Sales")
    return fig


def add_predicted_sales(fig):
    predicted_trace = go.Scatter(
        x=forecast["ds"], y=forecast["yhat"], mode="lines", name="Predicted Sales"
    )
    fig.add_trace(predicted_trace)
    return fig
