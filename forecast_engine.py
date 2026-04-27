import streamlit as st
from supabase import create_client
import pandas as pd

# --- 1. BAĞLANTI ---
try:
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_KEY"]
    supabase = create_client(url, key)
except Exception as e:
    st.error(f"Bağlantı hatası: {e}")
    st.stop()

st.set_page_config(page_title="MedAura Finans", layout="wide")

# --- 2. VERİ ÇEKME ---
def get_data():
    try:
        res = supabase.table("sales_entries").select("*").execute()
        return pd.DataFrame(res.data)
    except Exception as e:
        st.error(f"Veri çekme hatası: {e}")
        return pd.DataFrame()

# --- 3. PANEL ---
st.title("📊 MedAura Satış & Finans Paneli")

df = get_data()

if not df.empty:
    st.success(f"✅ Bağlantı Başarılı! {len(df)} kayıt bulundu.")
    st.dataframe(df, use_container_width=True)
else:
    st.warning("⚠️ Tablo şu an boş görünüyor.")
