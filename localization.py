import streamlit as st

def get_text(lang="TR"):
    texts = {
        "TR": {
            "title": "CEREBRO: Veri Egemenliği Üssü",
            "upload": "Dosya Yükle (Excel/CSV)",
            "analysis": "AI Analizini Başlat",
            "privacy_guard": "Gizlilik Koruması Aktif",
            "trend": "Trend Analizi"
        },
        "EN": {
            "title": "CEREBRO: Data Sovereignty Node",
            "upload": "Upload File (Excel/CSV)",
            "analysis": "Start AI Analysis",
            "privacy_guard": "Privacy Guard Active",
            "trend": "Trend Analysis"
        },
        "DE": {
            "title": "CEREBRO: Daten-Souveränitätsknoten",
            "upload": "Datei hochladen (Excel/CSV)",
            "analysis": "KI-Analyse starten",
            "privacy_guard": "Datenschutz aktiv",
            "trend": "Trendanalyse"
        }
    }
    return texts.get(lang, texts["TR"])
