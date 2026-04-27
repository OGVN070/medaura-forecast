import streamlit as st
from supabase import create_client
import pandas as pd

# --- 1. BAĞLANTI (Kasa Uyumlu) ---
try:
    # Bilgileri Streamlit Secrets'tan (Kasadan) çekiyoruz
    URL = st.secrets["SUPABASE_URL"]
    KEY = st.secrets["SUPABASE_KEY"]
    supabase = create_client(URL, KEY)
except Exception as e:
    st.error(f"Kasa (Secrets) bağlantı hatası: {e}")
    st.stop()

st.set_page_config(page_title="MedAura Satış Paneli", layout="wide")

# --- 2. VERİ ÇEKME ---
def get_data():
    try:
        # Lovable'ın itiraf ettiği o 6 kaydı çekiyoruz
        response = supabase.table("sales_entries").select("*").execute()
        return pd.DataFrame(response.data)
    except Exception as e:
        st.error(f"Veritabanından veri çekilemedi: {e}")
        return pd.DataFrame()

# --- 3. DASHBOARD ---
st.title("📊 MedAura Satış & Finans Paneli")

df = get_data()

if not df.empty:
    st.success(f"✅ Başardık Önder! Yeni projede {len(df)} kayıt bulundu.")
    
    # Lovable'ın yeni kolon isimlerine göre tabloyu döküyoruz
    st.subheader("📋 Güncel Satış Kayıtları")
    st.dataframe(df, use_container_width=True)
    
    with st.expander("🔍 Ham Veri Detaylarını İncele"):
        st.write(df)
else:
    st.warning("⚠️ Bağlantı kuruldu ama yeni proje tablosu hala boş görünüyor.")
    st.info(f"Bağlanılan URL: {URL}")
