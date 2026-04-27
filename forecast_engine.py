import streamlit as st
from supabase import create_client
import pandas as pd

# --- BAĞLANTI (Nokta Atışı) ---
# URL'yi Lovable'ın itiraf ettiği yeni adrese göre sabitledik
URL = "https://mywkkeeecykncwlooysz.supabase.co"

try:
    # Key'i kasadan alıyoruz
    KEY = st.secrets["SUPABASE_KEY"].strip()
    supabase = create_client(URL, KEY)
except Exception as e:
    st.error(f"Kasa hatası: {e}")
    st.stop()

st.set_page_config(page_title="MedAura Finans", layout="wide")
st.title("📊 MedAura Satış & Finans Paneli")

# --- VERİ ÇEKME ---
try:
    res = supabase.table("sales_entries").select("*").execute()
    df = pd.DataFrame(res.data)
    
    if not df.empty:
        st.success(f"✅ Sonunda! {len(df)} kayıt çekildi.")
        st.dataframe(df, use_container_width=True)
    else:
        st.warning("⚠️ Bağlantı tamam ama veritabanı tablosu boş.")
except Exception as e:
    st.error(f"Hata detay: {e}")
