import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Sayfa Ayarları
st.set_page_config(page_title="Excel Analizi", page_icon="📊", layout="wide")

st.title("📊 CEREBRO: Görsel Veri ve Excel Analizi")
st.markdown("---")
st.info("İçinde sayısal veriler olan bir Excel (.xlsx) dosyası yükleyin, CEREBRO anında analiz etsin.")

# Dosya Yükleme Alanı
uploaded_file = st.file_uploader("Excel Dosyanızı Buraya Yükleyin", type=["xlsx", "xls"])

if uploaded_file:
    try:
        # Excel'i Oku
        df = pd.read_excel(uploaded_file)
        st.success("✅ Veri seti CEREBRO tarafından başarıyla okundu!")

        # Veri Önizlemesi
        st.write("### 🔍 Veri Önizlemesi (İlk 5 Satır)")
        st.dataframe(df.head())

        # Sayısal Sütunları Tespit Et
        numeric_cols = df.select_dtypes(include=['number']).columns.tolist()

        if len(numeric_cols) >= 2:
            st.write("---")
            st.write("### 📈 Korelasyon Matrisi (Değişkenler Arası İlişki)")
            
            # Grafik Çizimi
            fig, ax = plt.subplots(figsize=(8, 6))
            sns.heatmap(df[numeric_cols].corr(), annot=True, cmap="coolwarm", fmt=".2f", ax=ax)
            st.pyplot(fig)
            
        else:
            st.warning("⚠️ Grafik çizebilmek için Excel dosyasında en az 2 adet sayısal sütun bulunmalıdır.")

    except Exception as e:
        st.error(f"Excel okunurken bir hata oluştu: {str(e)}")
        