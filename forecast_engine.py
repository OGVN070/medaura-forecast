import streamlit as st
from supabase import create_client
import pandas as pd
from prophet import Prophet
import plotly.express as px

# --- 1. BAĞLANTI ---
URL = "https://vbmzsfrbfgbxfbqlrutx.supabase.co"
KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdWJhc2UiLCJhdWQiOiJhdXRoZW50aWNhdGVkIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MTM5ODUwMTQsImV4cCI6MjAyOTU2MTAxNH0.CIn8v0y1Wf9O9fWp_M0vX_Uv6P8v0v0v0v0v0v0v0v0"
supabase = create_client(URL, KEY)

st.set_page_config(page_title="MedAura Sales Forecast", layout="wide")

# --- 2. VERİ ÇEKME FONKSİYONU ---
def get_data():
    try:
        response = supabase.table("sales_entries").select("*").execute()
        df = pd.DataFrame(response.data)
        return df
    except Exception as e:
        st.error(f"Veri çekme hatası: {e}")
        return pd.DataFrame()

# --- 3. DASHBOARD BAŞLIĞI ---
st.title("📊 MedAura Satış & Finans Paneli")

raw_data = get_data()

# --- 4. VERİ ANALİZ VE GÖSTERİM ---
if not raw_data.empty:
    st.success(f"✅ Veritabanında {len(raw_data)} kayıt bulundu!")
    
    # Veritabanındaki 'status' kolonunda ne yazdığını görelim
    if 'status' in raw_data.columns:
        unique_status = raw_data['status'].unique()
        st.info(f"💡 Veritabanındaki Kayıt Türleri: {list(unique_status)}")
        
        # Filtreleme için temizlik
        raw_data['status_check'] = raw_data['status'].astype(str).str.strip().str.lower()
        
        # Filtreleri Lovable'ın muhtemel dillerine göre genişletelim
        actuals = raw_data[raw_data['status_check'].isin(['invoice', 'fatura', 'kesilmiş fatura (invoice)'])]
        forecasts = raw_data[raw_data['status_check'].isin(['forecast', 'tahmin', 'tahmin (forecast)'])]

        # --- TABLO GÖRÜNÜMÜ ---
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("✅ GERÇEKLEŞEN (Fatura)")
            if not actuals.empty:
                st.dataframe(actuals, use_container_width=True)
            else:
                st.warning("Eşleşen 'fatura' kaydı yok.")

        with col2:
            st.subheader("🎯 HEDEFLER (Forecast)")
            if not forecasts.empty:
                st.dataframe(forecasts, use_container_width=True)
            else:
                st.warning("Eşleşen 'tahmin' kaydı yok.")
    
    # Veritabanında ne varsa ham olarak görelim (Hata ayıklamak için en iyisi)
    with st.expander("🔍 Tüm Veritabanını Ham Olarak Listele (İncele)"):
        st.write(raw_data)

else:
    st.error("❌ Veritabanı şu an boş görünüyor. Lovable üzerinden bir kayıt girmeyi deneyin.")
    st.info("Eğer Lovable'da veri görüyorsanız, Supabase RLS ayarlarını veya API anahtarlarını kontrol etmeliyiz.")
