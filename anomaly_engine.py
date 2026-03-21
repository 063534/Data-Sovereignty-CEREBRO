import pandas as pd
import numpy as np

def detect_anomalies(df):
    report = []
    
    # 1. Eksik Veri Analizi
    missing_data = df.isnull().sum()
    for col, count in missing_data.items():
        if count > 0:
            report.append(f"⚠️ **{col}** sütununda {count} adet eksik veri bulundu.")

    # 2. Sayısal Anomaliler (Z-Score)
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    for col in numeric_cols:
        mean = df[col].mean()
        std = df[col].std()
        if std > 0:
            outliers = df[(df[col] - mean).abs() > 3 * std]
            if not outliers.empty:
                report.append(f"🚨 **{col}** sütununda {len(outliers)} adet aşırı sapma (outlier) tespit edildi!")

    return report if report else ["✅ Veri setinde belirgin bir anomali rastlanmadı."]