import streamlit as st
from supabase import create_client
import pandas as pd

# --- BAĞLANTI (ADRESİ DOĞRUDAN YAZDIK) ---
URL = "https://mywkkeeecykncwlooysz.supabase.co"

# Key'i yine kasadan çekelim (güvenlik için)
try:
    KEY = st.secrets["SUPABASE_KEY"].strip()
    supabase = create_client(URL, KEY)
except Exception as e:
    st.error(f"Kasa (Secrets) okuma hatası: {e}")
    st.stop()

st.set_page_config(page_title="MedAura Dashboard", layout="wide")
st.title("📊 MedAura Satış & Finans Paneli")

# --- VERİ ÇEKME ---
try:
    # Lovable'ın bahsettiği o 6 kaydı çekmeyi deniyoruz
    res = supabase.table("sales_entries").select("*").execute()
    df = pd.DataFrame(res.data)
    
    if not df.empty:
        st.success(f"✅ Bağlantı kuruldu! {len(df)} kayıt başarıyla çekildi.")
        st.dataframe(df, use_container_width=True)
    else:
        st.warning("⚠️ Adres doğru ama tablo şu an boş görünüyor.")
except Exception as e:
    st.error(f"Veri çekilirken hata oluştu: {e}")
