import streamlit as st
from supabase import create_client
import pandas as pd

# --- BAĞLANTI (Garantili Yöntem) ---
# Adresi doğrudan, tertemiz bir şekilde tanımlıyoruz
raw_url = "https://mywkkeeecykncwlooysz.supabase.co"
URL = raw_url.strip()

try:
    # Key'i kasadan çekiyoruz
    KEY = st.secrets["SUPABASE_KEY"].strip()
    supabase = create_client(URL, KEY)
except Exception as e:
    st.error(f"Kasa (Secrets) okuma hatası: {e}")
    st.stop()

st.set_page_config(page_title="MedAura Dashboard", layout="wide")
st.title("📊 MedAura Satış & Finans Paneli")

# --- VERİ ÇEKME ---
try:
    # Service Role Key sayesinde RLS'yi aşıp 6 kaydı çekiyoruz
    res = supabase.table("sales_entries").select("*").execute()
    df = pd.DataFrame(res.data)
    
    if not df.empty:
        st.success(f"✅ SONUNDA! {len(df)} kayıt başarıyla yüklendi.")
        st.dataframe(df, use_container_width=True)
    else:
        st.warning("⚠️ Bağlantı tamam ama tablo şu an boş. Lovable'dan bir veri girer misin?")
except Exception as e:
    # Eğer hala hata verirse burası bize detay verecek
    st.error(f"Hata detayı: {e}")
