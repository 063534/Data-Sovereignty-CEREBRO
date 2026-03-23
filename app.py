import streamlit as st
import os
import tempfile
import audit_logger
import pandas as pd
import privacy_guard as pg  
import bi_analyser as bi    
import localization
import api_connector  
import forecasting    
import time
import report_gen
import numpy as np
import anomaly_engine  # .py silindi, doğru import bu
from cerebro_brain import ask_cerebro 
from document_processor import process_and_save_pdf

# --- 1. SAYFA AYARLARI ---
st.set_page_config(page_title="Project CEREBRO", page_icon="🧠", layout="wide")

# Dil Ayarları
selected_lang = st.sidebar.selectbox("Dil / Language", ["TR", "EN", "DE"])
lang_pack = localization.get_text(selected_lang)
st.title(lang_pack["title"])

# --- YAN MENÜ (SIDEBAR) ---
st.sidebar.markdown("---") 
st.sidebar.subheader("🔌 Kurumsal Entegrasyon")

if st.sidebar.button("SAP/ERP Canlı Veri Çek"):
    with st.spinner("Kurumsal sunucuya bağlanılıyor..."):
        live_df = api_connector.fetch_live_data("SAP")
        st.sidebar.success("Bağlantı Başarılı!")
        st.sidebar.table(live_df)

# Sistemi Başlat
audit_logger.init_db()
audit_logger.log_kaydet("Aktif_Kullanici", "SISTEM_GIRIS", "CEREBRO v3.0 Başlatıldı.")

with st.sidebar:
    if os.path.exists("neon_logo.png"):
        st.image("neon_logo.png", width=140)
    else:
        st.image("https://cdn-icons-png.flaticon.com/512/6356/6356649.png", width=120)
    
    st.title("Project CEREBRO")
    st.caption("Architect: Betül Sıla Köroğlu")
    st.markdown("---")
    
    st.write("**Hawkins Lab Status:**")
    st.success("🟢 System: ONLINE")
    st.error("🚫 Internet: OFFLINE") 
    st.info("🔒 Gate: CLOSED (Air-Gapped)")
    st.warning("🧠 Engine: M2 Neural Core")
    
    st.markdown("---")
    st.markdown("""<div style="text-align: center;"><br><i>"Hayatta en hakiki mürşit ilimdir."</i><br><br></div>""", unsafe_allow_html=True)
    if os.path.exists("imza.png"):
        st.image("imza.png", use_container_width=True)
    else:
        st.markdown("<h3 style='text-align: center; font-family: Brush Script MT, cursive;'>K. Atatürk</h3>", unsafe_allow_html=True)
    st.markdown("""<div style="text-align: center;"><small>Cumhuriyet'in İzinde, Bilimin Işığında.</small></div>""", unsafe_allow_html=True)

# --- ANA EKRAN ---
st.title("🧠 Project CEREBRO: Enterprise AI Node")
st.markdown("""### *"Friends Don't Lie. Data Doesn't Leak to the Upside Down."*""")

# --- SOHBET HAFIZASI (SESSION STATE) ---
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "Merhaba! Benim adım CEREBRO, sen korumsal bir asistan. Otomatik algıyla analiz yeteneğim var. Ne konuda yardımcı olabilirsem, lütfen sorun."}]

# --- ANA EKRAN SEKME TANIMLARI ---
tab1, tab2, tab3, = st.tabs(["📄 PDF & Chat Analiz", "📊 BI & Trend Analizi (Elite)", "📜 Analiz Arşivi"])

# --- TAB 1: PDF ANALİZ ---
with tab1:
    col1, col2 = st.columns(2)
    with col1:
        coding_languages = ["Otomatik Algıla", "Python", "Java", "C#", "SQL", "JavaScript", "C++", "Go", "Swift", "PHP", "Ruby", "Rust", "HTML/CSS"]
        selected_lang = st.selectbox("Analiz Dilini Seçin:", coding_languages)
with col2:
        uploaded_pdf = st.file_uploader("📂 PDF / Log Yükle (RAG Hafızası)", type=["pdf"])
        if uploaded_pdf:
            with st.spinner("İşleniyor..."):
                with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                    tmp.write(uploaded_pdf.getvalue())
                    tmp_path = tmp.name
                chunk_count = process_and_save_pdf(tmp_path)
                st.success(f"✅ Şifrelendi: {chunk_count} parça hafıza alındı!")
                audit_logger.log_kaydet("Aktif_Kullanici", "PDF_YUKLEME", f"'{uploaded_pdf.name}'")

# --- TAB 2: BI, TREND VE AI ANALİZ ---
with tab2:
    st.markdown("### 📊 CEREBRO Business Intelligence & Trend Analysis")
    
    tema = st.selectbox("🎨 Sistem Arayüz Teması:", ["Klasik Karanlık", "Matrix Green", "Hawkins Red", "Light Mode"], key="tema_v26")
    
    if tema == "Matrix Green":
        st.markdown("<style>.stApp { background-color: #000000; color: #00FF00 !important; }</style>", unsafe_allow_html=True)
    elif tema == "Hawkins Red":
        st.markdown("<style>.stApp { background-color: #1a0000; color: #FF0000 !important; }</style>", unsafe_allow_html=True)
    elif tema == "Light Mode":
        st.markdown("<style>.stApp { background-color: #FFFFFF; color: #31333F !important; }</style>", unsafe_allow_html=True)

    st.info("🔒 Güvenli Mod: Hassas verilere erişim için yetki doğrulaması gereklidir.")
    c_l, c_s = st.columns([1, 2])
    with c_l:
        sifre_input = st.text_input("🔑 Erişim Şifresi:", type="password", key="bi_pass")
    is_authorized = (sifre_input == "12345")
    
    yuklenen_dosyalar = st.file_uploader("📂 Veri Dosyalarını Seçin", type=['xlsx', 'csv'], accept_multiple_files=True)
    
    if yuklenen_dosyalar:
        dfs = []
        for dosya in yuklenen_dosyalar:
            df_temp = pd.read_csv(dosya) if dosya.name.endswith('.csv') else pd.read_excel(dosya)
            dfs.append(pg.mask_dataframe(df_temp.copy(), authorized=is_authorized))
        
        df = dfs[0]
        
        if is_authorized:
            st.success("🔓 YETKİLİ ERİŞİM: Veriler orijinal haliyle açıldı.")
        else:
            st.warning("⚠️ GÜVENLİ MOD: Hassas veriler maskelenmiştir.")

        if len(dfs) > 1:
            st.success(f"📈 Trend Analizi: {len(dfs)} dosya karşılaştırılıyor.")
            c1_d, c2_d = st.columns(2)
            with c1_d:
                st.write(f"📁 1. Dosya: {yuklenen_dosyalar[0].name}")
                st.dataframe(dfs[0].head(10))
            with c2_d:
                st.write(f"📁 2. Dosya: {yuklenen_dosyalar[1].name}")
                st.dataframe(dfs[1].head(10))
        else:
            st.dataframe(df.head(10), use_container_width=True)

        # --- v3.0: OTONOM ANOMALİ TESPİTİ ---
        st.markdown("---")
        with st.expander("🔍 CEREBRO Veri Denetçisi (Anomali Kontrolü)", expanded=True):
            with st.spinner("Veri kalitesi analiz ediliyor..."):
                anomaliler = anomaly_engine.detect_anomalies(df)
                if any("✅" in s for s in anomaliler):
                    st.success(anomaliler[0])
                else:
                    for hata in anomaliler:
                        st.warning(hata)

        # 📈 GRAFİKLER VE AI ANALİZ
        st.markdown("---")
        st.subheader("📈 Analitik Görselleştirme")
        g1, g2, g3 = st.columns(3)
        with g1:
            grafik_list = ["Bar", "Line", "Pie", "Radar", "Treemap", "Sunburst"]
            secilen = st.selectbox("Grafik Türü Seç:", grafik_list)
        with g2:
            x_eks = st.selectbox("X Ekseni:", df.columns)
        with g3:
            y_eks = st.selectbox("Y Ekseni:", df.columns)

        fig = bi.ciz_grafik(df, secilen, x_eks, y_eks)
        if fig:
            st.plotly_chart(fig, use_container_width=True)
            
            if st.button("🧠 CEREBRO: Grafiği ve Veriyi Analiz Et", key="ai_analiz_btn"):
                with st.spinner("AI Analiz Yapıyor..."):
                    ozet_stats = df.describe().to_string()
                    analiz_prompt = f"Aşağıdaki verileri analiz et ve TÜRKÇE bir yönetici özeti hazırla: \n{ozet_stats}"
                    ai_cevap = ask_cerebro(analiz_prompt, "Türkçe") 
                    st.session_state['son_analiz'] = ai_cevap
                    st.info(ai_cevap)

# --- v3.1: GELECEK TAHMİNLEME (KAHİN MODÜLÜ) ---
        st.markdown("---")
        st.subheader("🔮 CEREBRO AI: Gelecek Öngörü Sistemi")
        
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        if numeric_cols:
            col_to_predict = st.selectbox("Tahmin Edilecek Parametre:", numeric_cols, key="fore_col")
            
            if st.button("🚀 Geleceği Projekte Et"):
                with st.spinner("Matematiksel modeller çalıştırılıyor..."):
                    sonuc = forecasting.predict_future_trends(df, col_to_predict)
                    
                    if isinstance(sonuc, dict):
                        c1, c2, c3 = st.columns(3)
                        c1.metric("Gelecek Tahmini", f"{sonuc['tahmin_degeri']}")
                        c2.metric("Beklenen Değişim", f"%{sonuc['degisim_orani']}")
                        c3.info(f"**Yapay Zeka Notu:** {sonuc['durum']}")
                    else:
                        st.error(sonuc)
        
        # --- PDF RAPORLAMA VE KAYIT ---
        if 'son_analiz' in st.session_state:
            st.markdown("---")
            st.subheader("📑 Kurumsal Raporlama Merkezi")
            if st.button("📄 1. Raporu PDF Olarak Hazırla", key="pdf_gen_v2"):
                with st.spinner("PDF Hazırlanıyor..."):
                    report_file = report_gen.create_pdf_report(df, st.session_state['son_analiz'], "CEREBRO Stratejik Analiz")
                    st.session_state['hazir_rapor_yolu'] = report_file
                    audit_logger.analiz_kaydet("Stratejik Analiz", st.session_state['son_analiz'], report_file)
                    st.success("✅ Rapor Hazırlandı ve Arşive Kaydedildi!")

            if 'hazir_rapor_yolu' in st.session_state:
                with open(st.session_state['hazir_rapor_yolu'], "rb") as f:
                    st.download_button("📥 2. PDF Raporunu İndir", f, file_name="CEREBRO_Rapor.pdf", mime="application/pdf", key="dl_v30_final")

# --- TAB 3: ANALİZ ARŞİVİ ---
with tab3:
    st.markdown("### 📜 Kurumsal Analiz Arşivi")
    arsiv_df = audit_logger.analizleri_getir()
    if not arsiv_df.empty:
        st.dataframe(arsiv_df, use_container_width=True)
        st.markdown("---")
        secenekler = (arsiv_df['baslik'] + " - " + arsiv_df['tarih']).tolist()
        secilen = st.selectbox("Detayını Görmek İstediğiniz Analiz:", secenekler)
        idx = secenekler.index(secilen)
        st.write("**📝 AI Analiz Notu:**")
        st.success(arsiv_df.iloc[idx]['analiz_notu'])
    else:
        st.warning("Henüz kaydedilmiş bir analiz bulunamadı.")

# --- 5. SOHBET GEÇMİŞİ (STABİL VERSİYON) ---
st.markdown("---")
st.subheader("💬 CEREBRO Kurumsal Asistan")

# Mesajları ekranda göster
for msg in st.session_state.messages:
    avatar = "🧢" if msg["role"] == "user" else "🧠"
    st.chat_message(msg["role"], avatar=avatar).write(msg["content"])

# Yazılı Chat Girişi
if prompt := st.chat_input("Mesajınızı buraya yazın..."):
    # Kullanıcı mesajını ekle ve göster
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user", avatar="🧢").write(prompt)
    
    # CEREBRO Yanıtı
    with st.chat_message("assistant", avatar="🧠"):
        with st.spinner("CEREBRO Düşünüyor..."):
            # selected_lang sidebar'dan geliyor
            response = ask_cerebro(prompt, "Türkçe") 
            st.write(response)
            st.session_state.messages.append({"role": "assistant", "content": response})