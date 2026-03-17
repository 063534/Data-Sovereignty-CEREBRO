import re

def mask_text(text):
    """Metin içindeki hassas verileri maskeler (Sohbet kısmı için)."""
    text = re.sub(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', "[E-POSTA_GIZLENDI]", text)
    text = re.sub(r'\b(?:\+?\d{1,3}[- ]?)?\(?\d{3}\)?[- ]?\d{3}[- ]?\d{4}\b', "[TELEFON_GIZLENDI]", text)
    text = re.sub(r'\b[A-Z]{2}\d{2}[A-Z0-9]{12,30}\b', "[IBAN_GIZLENDI]", text)
    return text

def mask_dataframe(df, authorized=False):
    """
    authorized=False ise hassas sütunları maskeler.
    authorized=True ise orijinal veriyi gösterir.
    """
    if authorized:
        return df 
    
    # Maskelenecek kelime listesini genişlettik
    sensitive_keywords = [
        'ad', 'soyad', 'isim', 'name', 'surname', 
        'email', 'tel', 'phone', 'iban', 'maas', 
        'salary', 'not', 'kimlik', 'tc', 'adres'
    ]
    
    df_masked = df.copy()
    
    for col in df_masked.columns:
        # Sütun isminde bu kelimelerden biri geçiyorsa (Örn: 'Sınav Notu' içinde 'not' geçer)
        col_lower = col.lower()
        if any(key in col_lower for key in sensitive_keywords):
            df_masked[col] = "🔒 [YETKİSİZ ERİŞİM]"
            
    return df_masked