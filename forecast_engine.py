import streamlit as st
from supabase import create_client
import pandas as pd

# Kasa bilgilerini alıyoruz ve gizli boşlukları temizliyoruz (.strip())
try:
    url = st.secrets["SUPABASE_URL"].strip()
    key = st.secrets["SUPABASE_KEY"].strip()
    supabase = create_client(url, key)
except Exception as e:
    st.error(f"⚠️ Kasa (Secrets) hatası: {e}")
    st.stop()

st.set_page_config(page_title="MedAura Dashboard", layout="wide")
st.title("📊 MedAura Satış Dashboard")

try:
    # Verileri çekiyoruz
    res = supabase.table("sales_entries").select("*").execute()
    df = pd.DataFrame(res.data)
    
    if not df.empty:
        st.success(f"✅ BAĞLANTI TAMAM! {len(df)} kayıt çekildi.")
        st.dataframe(df, use_container_width=True)
    else:
        st.warning("⚠️ Adres doğru ama tablo boş görünüyor. Lovable'dan yeni bir kayıt ekle.")
except Exception as e:
    st.error(f"❌ Bağlantı hatası detayı: {e}")
