import streamlit as st
from supabase import create_client
import pandas as pd

# --- BAĞLANTI (HATA DÜZELTİLDİ) ---
# Burada "supabaase" değil "supabase" olmalı
URL = "https://mywkkeeecykncwlooysz.supabase.co"

try:
    # Anahtarı kasadan alıyoruz
    KEY = st.secrets["SUPABASE_KEY"].strip()
    supabase = create_client(URL, KEY)
except Exception as e:
    st.error(f"Kasa hatası: {e}")
    st.stop()

st.set_page_config(page_title="MedAura Dashboard", layout="wide")
st.title("📊 MedAura Satış Dashboard")

# --- VERİ ÇEKME ---
try:
    res = supabase.table("sales_entries").select("*").execute()
    df = pd.DataFrame(res.data)
    
    if not df.empty:
        st.success(f"✅ SONUNDA BAŞARDIK! {len(df)} kayıt çekildi.")
        st.dataframe(df, use_container_width=True)
    else:
        st.warning("⚠️ Adres artık doğru ama tablo boş görünüyor.")
except Exception as e:
    st.error(f"❌ Hata: {e}")
