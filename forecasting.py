import numpy as np
import pandas as pd

def predict_next_quarter(df, column_name):
    """Basit doğrusal artış ile gelecek çeyrek tahmini"""
    if column_name in df.columns:
        current_mean = df[column_name].mean()
        # %10 büyüme simülasyonu
        prediction = current_mean * 1.10
        return round(prediction, 2)
    return None
