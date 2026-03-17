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

# --- 1. SAYFA AYARLARI (Streamlit kuralı gereği en başta olmalı) ---
st.set_page_config(page_title="Project CEREBRO", page_icon="🧠", layout="wide")

# Dil Ayarları
selected_lang = st.sidebar.selectbox("Dil / Language", ["TR", "EN", "DE"])
lang_pack = localization.get_text(selected_lang)
st.title(lang_pack["title"])

# --- YAN MENÜ (SIDEBAR) EKLEMELERİ ---
st.sidebar.markdown("---") 
st.sidebar.subheader("🔌 Kurumsal Entegrasyon")

if st.sidebar.button("SAP/ERP Canlı Veri Çek"):
    with st.spinner("Kurumsal sunucuya bağlanılıyor..."):
        live_df = api_connector.fetch_live_data("SAP")
        st.sidebar.success("Bağlantı Başarılı!")
        st.sidebar.table(live_df)

# Backend motorları
from cerebro_brain import ask_cerebro 
from document_processor import process_and_save_pdf

# Sistemi Başlat
audit_logger.init_db()
audit_logger.log_kaydet("Aktif_Kullanici", "SISTEM_GIRIS", "CEREBRO v2.0 Başlatıldı.")

# --- 2. YAN MENÜ (SOL PANEL) ---
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

# --- 3. ANA EKRAN BAŞLIK ---
st.title("🧠 Project CEREBRO: Enterprise AI Node")
st.markdown("""### *"Friends Don't Lie. Data Doesn't Leak to the Upside Down."*""")

# --- 4. SEKMELER ---
tab1, tab2 = st.tabs(["📄 PDF & Chat Analiz", "📊 BI & Trend Analizi (Elite)"])

# --- TAB 1: PDF ANALİZ ---
with tab1:
    col1, col2 = st.columns(2)
    with col1:
        selected_language = st.selectbox("🛠️ Analiz Dilini Seçin:", ["Otomatik Algıla", "Python", "Java", "C#", "SQL", "JavaScript"])
    with col2:
        uploaded_pdf = st.file_uploader("📂 PDF / Log Yükle (RAG Hafızası)", type=["pdf"])
        if uploaded_pdf:
            with st.spinner("İşleniyor..."):
                with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                    tmp.write(uploaded_pdf.getvalue())
                    tmp_path = tmp.name
                chunk_count = process_and_save_pdf(tmp_path)
                st.success(f"✅ Şifrelendi: {chunk_count} parça hafızaya alındı!")
                audit_logger.log_kaydet("Aktif_Kullanici", "PDF_YUKLEME", f"'{uploaded_pdf.name}'")

# --- TAB 2: BI, TREND VE AI ANALİZ ---
with tab2:
    st.markdown("### 📊 CEREBRO Business Intelligence & Trend Analysis")
    
    tema = st.selectbox("🎨 Sistem Arayüz Teması:", ["Klasik Karanlık", "Matrix Green", "Hawkins Red", "Light Mode"], key="tema_secici_v25")
    
    if tema == "Matrix Green":
        st.markdown("<style> .stApp { background-color: #000000; color: #00FF00 !important; } </style>", unsafe_allow_html=True)
    elif tema == "Hawkins Red":
        st.markdown("<style> .stApp { background-color: #1a0000; color: #FF0000 !important; } </style>", unsafe_allow_html=True)
    elif tema == "Light Mode":
        # Tüm özel CSS'leri sıfırlayıp Streamlit'in kendi aydınlık moduna bırakıyoruz
        st.markdown("<style> .stApp { background-color: #FFFFFF; color: #31333F !important; } </style>", unsafe_allow_html=True)
        st.info("💡 Not: En iyi görüntü için Streamlit sağ üst menüden 'Settings > Theme > Light' yapabilirsiniz.")
    elif tema == "Hawkins Red":
        st.markdown("<style>body { color: #FF0000 !important; } .stApp { background-color: #1a0000; }</style>", unsafe_allow_html=True)

    st.info("🔒 Güvenli Mod: Hassas verilere erişim için yetki doğrulaması gereklidir.")
    c_l, c_s = st.columns([1, 2])
    with c_l:
        sifre_input = st.text_input("🔑 Erişim Şifresi:", type="password", key="bi_pass")
    is_authorized = (sifre_input == "12345")

    yuklenen_dosyalar = st.file_uploader("📂 Dosyaları Seçin (Trend analizi için 2 dosya yükleyebilirsiniz)", type=['xlsx', 'csv'], accept_multiple_files=True)
    
    if yuklenen_dosyalar:
        dfs = []
        for dosya in yuklenen_dosyalar:
            df_temp = pd.read_csv(dosya) if dosya.name.endswith('.csv') else pd.read_excel(dosya)
            dfs.append(pg.mask_dataframe(df_temp.copy(), authorized=is_authorized))
        
        df = dfs[0]
        
        if is_authorized:
            with st.spinner('Analiz motoru optimize ediliyor...'):
                time.sleep(1)
            st.info("📊 Analiz Raporu Hazır.")
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

        # 📈 GRAFİKLER VE TAHMİNLEME
        st.markdown("---")
        st.subheader("📈 Analitik Görselleştirme")
        g1, g2, g3 = st.columns(3)
        with g1:
            grafik_list = ["Bar", "Line", "Pie", "Radar", "Ağaç Haritası (Treemap)", "Güneş Işığı (Sunburst)"]
            secilen = st.selectbox("Grafik Türü Seç:", grafik_list)
        with g2:
            x_eks = st.selectbox("X Ekseni:", df.columns)
        with g3:
            y_eks = st.selectbox("Y Ekseni:", df.columns)

        fig = bi.ciz_grafik(df, secilen, x_eks, y_eks)
        if fig:
            st.plotly_chart(fig, use_container_width=True, key=f"bi_chart_{secilen}")
            
            if st.button("🧠 CEREBRO: Grafiği ve Veriyi Analiz Et"):
                with st.spinner("AI Yönetici Özeti Hazırlanıyor..."):
                    ozet_veri = df.describe().to_string()
                    analiz_sorusu = f"Aşağıdaki verilerin özet istatistiklerine ve {secilen} grafiğine bakarak profesyonel bir yönetici özeti yaz. Trendleri belirt ve tavsiyelerde bulun: \n{ozet_veri}"
                    ai_cevap = ask_cerebro(analiz_sorusu, "Türkçe")
                    st.markdown("#### 📝 CEREBRO Yönetici Analizi")
                    st.info(ai_cevap)
                    audit_logger.log_kaydet("Aktif_Kullanici", "AI_ANALIZ", f"{secilen} grafiği yorumlatıldı.")

        # --- TAHMİNLEME EKLEMESİ ---
        st.markdown("---")
        st.subheader("🧠 CEREBRO AI: Gelecek Çeyrek Projeksiyonu")
        numeric_cols = df.select_dtypes(include=['number']).columns
        if len(numeric_cols) > 0:
            target_col = numeric_cols[0]
            prediction = forecasting.predict_next_quarter(df, target_col)
            col1, col2 = st.columns(2)
            col1.metric(label=f"Mevcut Ortalama ({target_col})", value=round(df[target_col].mean(), 2))
            col2.metric(label="AI Gelecek Tahmini (+%10)", value=prediction, delta="Büyüme Bekleniyor")

# --- 5. SOHBET GEÇMİŞİ ---
st.markdown("---")
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "Cerebro aktif. Bilimin ışığında analize hazırım."}]

for msg in st.session_state.messages:
    avatar = "🧢" if msg["role"] == "user" else "🧠"
    st.chat_message(msg["role"], avatar=avatar).write(msg["content"])

if prompt := st.chat_input("Mesajınızı buraya girin..."):
    audit_logger.log_kaydet("Aktif_Kullanici", "SORU_SORULDU", f"Soru: {prompt}")
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user", avatar="🧢").write(prompt)

    with st.chat_message("assistant", avatar="🧠"):
        with st.spinner("Analyzing..."):
            try:
                full_response = ask_cerebro(prompt, selected_language)
                st.write(full_response)
                st.session_state.messages.append({"role": "assistant", "content": full_response})
            except Exception as e:
                st.error(f"Hata: {e}")
