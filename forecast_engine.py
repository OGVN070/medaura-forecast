import streamlit as st
from supabase import create_client
import pandas as pd

# Bağlantıyı kasadan (Secrets) alıyoruz
try:
    url = st.secrets["SUPABASE_URL"].strip()
    key = st.secrets["SUPABASE_KEY"].strip()
    supabase = create_client(url, key)
except Exception as e:
    st.error(f"Kasa okuma hatası: {e}")
    st.stop()

st.title("📊 MedAura Satış Dashboard")

# Veri çekme işlemi
try:
    res = supabase.table("sales_entries").select("*").execute()
    df = pd.DataFrame(res.data)
    
    if not df.empty:
        st.success(f"✅ Başardık! {len(df)} kayıt başarıyla yüklendi.")
        st.dataframe(df, use_container_width=True)
    else:
        st.warning("⚠️ Bağlantı tamam ama veritabanı boş görünüyor.")
except Exception as e:
    st.error(f"Bağlantı hatası: {e}")
