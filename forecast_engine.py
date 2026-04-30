import streamlit as st
from supabase import create_client
import pandas as pd

# --- BAĞLANTI (Adresi Doğrudan Tanımlıyoruz) ---
# Lovable'ın onayladığı gerçek adres:
URL = "https://mywkkeeecykncwlooysz.supabase.co"

try:
    # Anahtarı kasadan (Secrets) çekiyoruz
    KEY = st.secrets["SUPABASE_KEY"].strip()
    supabase = create_client(URL, KEY)
except Exception as e:
    st.error(f"Kasa okuma hatası: {e}")
    st.stop()

st.set_page_config(page_title="MedAura Dashboard", layout="wide")
st.title("📊 MedAura Satış Dashboard")

# --- VERİ ÇEKME ---
try:
    # Lovable'ın bahsettiği o 6 kaydı çekmeyi deniyoruz
    res = supabase.table("sales_entries").select("*").execute()
    df = pd.DataFrame(res.data)
    
    if not df.empty:
        st.success(f"✅ SONUNDA! {len(df)} kayıt başarıyla çekildi.")
        st.dataframe(df, use_container_width=True)
    else:
        st.warning("⚠️ Bağlantı tamam ama tablo boş görünüyor.")
except Exception as e:
    st.error(f"❌ Bağlantı hatası detayı: {e}")
    st.info(f"Denenen URL: {URL}")
