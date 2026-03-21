import sqlite3
import pandas as pd

def init_db():
    """Veri tabanını ve gerekli tabloları ilk kez oluşturur."""
    conn = sqlite3.connect('cerebro_audit.db')
    cursor = conn.cursor()
    
    # 1. Sistem Logları Tablosu (Giriş-çıkış takibi için)
    cursor.execute('''CREATE TABLE IF NOT EXISTS logs 
                      (kullanici TEXT, islem TEXT, detay TEXT, tarih TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
    
    # 2. YENİ: AI Analiz Arşivi Tablosu (v2.7 Kurumsal Hafıza)
    cursor.execute('''CREATE TABLE IF NOT EXISTS analiz_arsivi 
                      (baslik TEXT, analiz_notu TEXT, dosya_yolu TEXT, tarih TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
    
    conn.commit()
    conn.close()

def log_kaydet(kullanici, islem, detay):
    """Sistem hareketlerini kaydeder."""
    conn = sqlite3.connect('cerebro_audit.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO logs (kullanici, islem, detay) VALUES (?, ?, ?)", (kullanici, islem, detay))
    conn.commit()
    conn.close()

def analiz_kaydet(baslik, notu, yol):
    """AI analizlerini ve rapor yollarını veri tabanına kaydeder (v2.7 Özel)."""
    conn = sqlite3.connect('cerebro_audit.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO analiz_arsivi (baslik, analiz_notu, dosya_yolu) VALUES (?, ?, ?)", (baslik, notu, yol))
    conn.commit()
    conn.close()

def analizleri_getir():
    """Kaydedilmiş tüm geçmiş analizleri bir tablo olarak geri döndürür."""
    conn = sqlite3.connect('cerebro_audit.db')
    # En son yapılan analiz en üstte görünecek şekilde çeker
    df = pd.read_sql_query("SELECT * FROM analiz_arsivi ORDER BY tarih DESC", conn)
    conn.close()
    return df
