import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression

def predict_future_trends(df, target_col):
    try:
        # Sadece sayısal ve eksik olmayan verileri al
        data = df[target_col].dropna()
        if len(data) < 3:
            return "⚠️ Tahmin için en az 3 veri noktası gereklidir."

        # X: Zaman indeksi, y: Değerler
        X = np.array(range(len(data))).reshape(-1, 1)
        y = data.values

        # Lineer Regresyon Modeli
        model = LinearRegression()
        model.fit(X, y)

        # Gelecek adım tahmini
        future_step = np.array([[len(data)]])
        prediction = model.predict(future_step)[0]
        
        last_val = y[-1]
        degisim = ((prediction - last_val) / last_val) * 100

        return {
            "tahmin_degeri": round(prediction, 2),
            "degisim_orani": round(degisim, 2),
            "durum": "Artış Trendi 📈" if degisim > 0 else "Azalış Trendi 📉"
        }
    except Exception as e:
        return f"Hata oluştu: {str(e)}"