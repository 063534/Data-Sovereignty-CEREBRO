import pandas as pd
import time

def fetch_live_data(source="SAP"):
    """Kurumsal ERP sistemlerinden veri çekme simülasyonu"""
    print(f"Connecting to {source} API...")
    time.sleep(2) # Simülasyon gecikmesi
    # Örnek canlı veri yapısı
    data = {
        "Sistem": [source] * 3,
        "Durum": ["Aktif", "Aktif", "Beklemede"],
        "Veri_Akisi": [120, 450, 30]
    }
    return pd.DataFrame(data)
