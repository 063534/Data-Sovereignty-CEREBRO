import sqlite3
from datetime import datetime

# Kara Kutumuzun (Veri tabanının) adı
DB_NAME = "cerebro_audit.db"

def init_db():
    """Veri tabanını ve log tablosunu oluşturur (Yoksa sıfırdan kurar)."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # DSGVO (GDPR) standartlarına uygun Audit Log tablosu
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS audit_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tarih_saat TEXT,
            kullanici TEXT,
            islem_tipi TEXT,
            detay TEXT
        )
    ''')
    conn.commit()
    conn.close()

def log_kaydet(kullanici, islem_tipi, detay):
    """Sistemde yapılan bir işlemi saniyesi saniyesine veri tabanına yazar."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    su_an = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    cursor.execute('''
        INSERT INTO audit_logs (tarih_saat, kullanici, islem_tipi, detay)
        VALUES (?, ?, ?, ?)
    ''', (su_an, kullanici, islem_tipi, detay))
    
    conn.commit()
    conn.close()
    print(f"🔒 [KAYIT ALINDI] {su_an} | {islem_tipi}")

def loglari_goster():
    """Kara kutudaki tüm kayıtları okur ve ekrana basar."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM audit_logs")
    kayitlar = cursor.fetchall()
    
    print("\n--- 📋 CEREBRO AUDIT LOG (DENETİM KAYITLARI) ---")
    for kayit in kayitlar:
        print(f"ID: {kayit[0]} | Tarih: {kayit[1]} | Kullanıcı: {kayit[2]} | İşlem: {kayit[3]} | Detay: {kayit[4]}")
    print("------------------------------------------------\n")
    
    conn.close()

# --- TEST AŞAMASI ---
if __name__ == "__main__":
    # 1. Veri tabanını kur
    init_db()
    
    # 2. Örnek işlemler kaydedelim (Sanki biri CEREBRO'yu kullanıyormuş gibi)
    log_kaydet("Betül_Admin", "SISTEM_GIRISI", "Sisteme başarılı giriş yapıldı.")
    log_kaydet("Betül_Admin", "PDF_YUKLEME", "Guvenlik_Raporu.pdf dosyası ChromaDB'ye yüklendi.")
    log_kaydet("Kullanici_1", "SORU_SORMA", "Soru: Maliyetler ne kadar? Cevap: CEREBRO yanıt üretti.")
    
    # 3. Kaydedilen logları okuyalım
    loglari_goster()
    