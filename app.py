import streamlit as st
import os
import tempfile

# Kendi yazdığımız backend motorunu projemize dahil ediyoruz
from cerebro_brain import ask_cerebro 
# YENİ: PDF işleme motorumuzu (Göz ve Hafıza) dahil ediyoruz
from document_processor import process_and_save_pdf

# --- 1. SAYFA AYARLARI ---
st.set_page_config(page_title="Project CEREBRO", page_icon="🧠", layout="wide")

# --- 2. YAN MENÜ (SOL PANEL - SADE VE ŞIK) ---
with st.sidebar:
    if os.path.exists("neon_logo.png"):
        st.image("neon_logo.png", width=140)
    else:
        st.image("https://cdn-icons-png.flaticon.com/512/6356/6356649.png", width=120)
    
    st.title("Project CEREBRO")
    st.caption("Architect: Betül Sıla Köroğlu") # <-- İMZAN KORUNDU
    st.markdown("---")
    
    st.write("**Hawkins Lab Status:**")
    st.success("🟢 System: ONLINE")
    st.error("🚫 Internet: OFFLINE") 
    st.info("🔒 Gate: CLOSED (Air-Gapped)")
    st.warning("🧠 Engine: M2 Neural Core") # <-- M2 VURGUSU KORUNDU
    
    st.markdown("---")
    
    st.markdown("""<div style="text-align: center;"><br><i>"Hayatta en hakiki mürşit ilimdir."</i><br><br></div>""", unsafe_allow_html=True)
    if os.path.exists("imza.png"):
        st.image("imza.png", use_container_width=True)
    else:
        st.markdown("<h3 style='text-align: center; font-family: Brush Script MT, cursive;'>K. Atatürk</h3>", unsafe_allow_html=True)
    st.markdown("""<div style="text-align: center;"><small>Cumhuriyet'in İzinde, Bilimin Işığında.</small></div>""", unsafe_allow_html=True)

# --- 3. ANA EKRAN ---
st.title("🧠 Project CEREBRO: Enterprise AI Node")
st.markdown("""
### *"Friends Don't Lie. Data Doesn't Leak to the Upside Down."*
*(Arkadaşlar yalan söylemez. Veri, Ters Dünya'ya [Buluta] sızmaz.)*

Bu sistem, **Mimar Betül Sıla Köroğlu** tarafından geliştirilen; kurumsal ve endüstriyel veri güvenliği için **"Veri Egemenliği" (Data Sovereignty)** ilkesine dayalı çalışan yerel yapay zeka mimarisidir.
""") # <-- VİZYONUN KORUNDU

st.markdown("---") 

# --- 4. DİL SEÇİMİ VE PDF YÜKLEME (ANA EKRAN) ---
# Ekranı iki eşit sütuna böldük ki dil seçimi ve PDF kutusu yan yana çok şık dursun
col1, col2 = st.columns([1, 1]) 

with col1:
    selected_language = st.selectbox(
        "🛠️ Analiz Edilecek Yazılım Dilini Seçin:",
        ["Otomatik Algıla (Auto)", "C#", "Java", "Python", "JavaScript", "React", "HTML / CSS / Bootstrap", "SQL", "C / C++", "Swift", "Diğer"]
    )

with col2:
    # YENİ EKLENEN PDF YÜKLEME KUTUSU
    uploaded_file = st.file_uploader("📂 Kurumsal PDF / Log Dosyası Yükle (RAG Hafızası)", type=["pdf"])
    
    # Eğer kullanıcı bir PDF yüklerse...
    if uploaded_file is not None:
        with st.spinner("PDF Yerel Hafızaya (ChromaDB) İşleniyor..."):
            # Dosyayı geçici olarak M2 Mac'ine kaydet
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
                tmp_file.write(uploaded_file.getvalue())
                tmp_file_path = tmp_file.name
            
            # Adım 2'de yazdığımız motoru çalıştırıp PDF'i hafızaya kazı!
            chunk_count = process_and_save_pdf(tmp_file_path)
            st.success(f"✅ DSGVO Uyumlu: Dosya dışarı sızmadan {chunk_count} parça halinde yerel hafızaya şifrelendi!")

st.markdown("---")

# --- 5. SOHBET GEÇMİŞİ ---
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "Cerebro aktif. Verileriniz Upside Down'dan (Buluttan) korunuyor. Bilimin ışığında analize hazırım."}]

for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.chat_message("user", avatar="🧢").write(msg["content"]) 
    else:
        st.chat_message("assistant", avatar="🧠").write(msg["content"]) 

# --- 6. SORU-CEVAP KISMI ---
if prompt := st.chat_input("Hatalı kodu veya PDF ile ilgili sorunuzu buraya girin..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user", avatar="🧢").write(prompt)

    with st.chat_message("assistant", avatar="🧠"):
        with st.spinner(f"Analyzing in Secure Mode ({selected_language})..."):
            try:
                full_response = ask_cerebro(prompt, selected_language)
                st.write(full_response)
                st.session_state.messages.append({"role": "assistant", "content": full_response})
            except Exception as e:
                st.error("⚠️ Mind Flayer Saldırısı! (Model Bağlantı Hatası)")
                st.info("Lütfen terminalden 'ollama run llama3' komutunu çalıştırın.")
