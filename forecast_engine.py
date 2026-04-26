import streamlit as st
from supabase import create_client
import pandas as pd

# --- 1. BAĞLANTI (Kasa Uyumlu) ---
URL = "https://vbmzsfrbfgbxfbqlrutx.supabase.co"
try:
    KEY = st.secrets["SUPABASE_KEY"]
    supabase = create_client(URL, KEY)
except:
    st.error("Kasa anahtarı hatası!")
    st.stop()

st.set_page_config(page_title="MedAura Satış Paneli", layout="wide")

# --- 2. VERİ ÇEKME ---
def get_data():
    try:
        response = supabase.table("sales_entries").select("*").execute()
        return pd.DataFrame(response.data)
    except Exception as e:
        st.error(f"Veri çekme hatası: {e}")
        return pd.DataFrame()

# --- 3. DASHBOARD ---
st.title("📊 MedAura Satış & Finans Paneli")

df = get_data()

if not df.empty:
    st.success(f"✅ Başardık Önder! Veritabanında {len(df)} kayıt bulundu.")
    
    # Lovable'ın farklı kolon isimleri kullanma ihtimaline karşı akıllı tablo:
    # Hangi kolonlar varsa onları gösterelim
    cols_to_show = [c for c in ['customer_name', 'customer', 'product_name', 'product', 'region', 'revenue_euro', 'status'] if c in df.columns]
    
    st.subheader("📋 Güncel Kayıt Listesi")
    st.dataframe(df[cols_to_show], use_container_width=True)
    
    # Ham veriyi merak edenler için (Alt kısımda)
    with st.expander("🔍 Tüm Detayları Gör"):
        st.write(df)
else:
    st.warning("⚠️ Bağlantı kuruldu ama tablo hala boş görünüyor. Supabase 'Table Editor' ekranını yenileyip verilerin oraya düştüğünden emin ol.")
