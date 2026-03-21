from fpdf import FPDF
import pandas as pd

def tr_temizle(metin):
    """Türkçe karakterleri fontun anlayacağı güvenli karakterlere çevirir."""
    kaynak = "şŞıİçÇöÖüÜğĞ"
    hedef = "sSiIcCoOuUgG"
    tablo = str.maketrans(kaynak, hedef)
    return str(metin).translate(tablo)

def create_pdf_report(df, ai_summary, analysis_title):
    pdf = FPDF(orientation='P', unit='mm', format='A4')
    pdf.add_page()
    
    # Standart font (Artık karakter temizlendiği için hata vermez)
    pdf.set_font("helvetica", "B", 16)
    
    # Başlık
    pdf.cell(0, 10, txt=tr_temizle(analysis_title), ln=True, align='C')
    pdf.ln(10)
    
    # 1. Veri Tablosu
    pdf.set_font("helvetica", "B", 12)
    pdf.cell(0, 10, txt=tr_temizle("1. Veri Seti Analiz Ornegi (Ilk 5 Satir)"), ln=True)
    pdf.ln(2)
    
    # Sütun Başlıkları
    pdf.set_font("helvetica", "B", 10)
    cols = list(df.columns)[:5]
    col_width = 190 / len(cols)
    for col in cols:
        pdf.cell(col_width, 8, txt=tr_temizle(col)[:12], border=1, align='C')
    pdf.ln()
    
    # Tablo Verileri
    pdf.set_font("helvetica", "", 9)
    for i in range(min(5, len(df))):
        for col in cols:
            val = str(df.iloc[i][col])[:15]
            pdf.cell(col_width, 8, txt=tr_temizle(val), border=1, align='C')
        pdf.ln()
    
    pdf.ln(10)
    
    # 2. AI Analiz Notları
    pdf.set_font("helvetica", "B", 12)
    pdf.cell(0, 10, txt=tr_temizle("2. CEREBRO AI Stratejik Analiz Notlari"), ln=True)
    pdf.ln(2)
    
    pdf.set_font("helvetica", "", 11)
    # AI'nın cevabını temizleyerek basıyoruz
    pdf.multi_cell(0, 8, txt=tr_temizle(ai_summary))
    
    filename = "CEREBRO_Analiz_Raporu.pdf"
    pdf.output(filename)
    return filename
