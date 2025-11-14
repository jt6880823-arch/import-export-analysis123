# model.py
import pandas as pd
from sklearn.cluster import KMeans
from statsmodels.tsa.arima.model import ARIMA
import numpy as np

def cluster_countries(df, n_clusters=3):
    """Simple clustering based on export/import values"""
    features = df[['Export', 'Import']].fillna(0)
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    df['Cluster'] = kmeans.fit_predict(features)
    return df

def forecast_trade(series, steps=30):
    """Forecast next 30 days using ARIMA"""
    if len(series) < 10:
        return [series.mean()] * steps  # fallback
    
    try:
        model = ARIMA(series, order=(1,1,1))
        fitted = model.fit()
        forecast = fitted.forecast(steps=steps)
        return forecast.tolist()
    except:
        return [series.mean()] * steps