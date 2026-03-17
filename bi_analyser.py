import plotly.express as px
import streamlit as st

def ciz_grafik(df, grafik_turu, x_ekseni, y_ekseni):
    """Seçilen türe göre gelişmiş Plotly grafikleri üretir."""
    try:
        # Grafik türüne göre eşleştirme
        if grafik_turu == "Radar":
            fig = px.line_polar(df, r=y_ekseni, theta=x_ekseni, line_close=True, template="plotly_dark")
        elif grafik_turu == "Ağaç Haritası (Treemap)":
            fig = px.treemap(df, path=[x_ekseni], values=y_ekseni)
        elif grafik_turu == "Güneş Işığı (Sunburst)":
            fig = px.sunburst(df, path=[x_ekseni], values=y_ekseni)
        elif grafik_turu == "Şelale (Waterfall)":
            fig = px.bar(df, x=x_ekseni, y=y_ekseni, text=y_ekseni, title="Waterfall Analizi")
        elif grafik_turu == "Huni (Funnel)":
            fig = px.funnel(df, x=y_ekseni, y=x_ekseni)
        elif grafik_turu == "Histogram":
            fig = px.histogram(df, x=x_ekseni, y=y_ekseni, marginal="box")
        elif grafik_turu == "Box":
            fig = px.box(df, x=x_ekseni, y=y_ekseni)
        elif grafik_turu == "Pie":
            fig = px.pie(df, names=x_ekseni, values=y_ekseni)
        else:
            # Standart Bar, Line, Scatter için Plotly kütüphanesinden dinamik çağrı
            func = getattr(px, grafik_turu.lower())
            fig = func(df, x=x_ekseni, y=y_ekseni)
            
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", 
            plot_bgcolor="rgba(0,0,0,0)",
            font_color="white"
        )
        return fig
    except Exception as e:
        st.error(f"Grafik çizim hatası: {e}")
        return None
    