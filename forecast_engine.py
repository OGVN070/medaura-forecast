import streamlit as st
from supabase import create_client
import pandas as pd

# --- BAĞLANTI (GERÇEK ADRES) ---
# Ekran görüntüsündeki subdomain'i kullanarak doğru adresi kurduk
URL = "https://forecast-buddy-36.supabase.co"

try:
    # Key'i kasadan alıyoruz (Key hala aynıdır, o değişmez)
    KEY = st.secrets["SUPABASE_KEY"].strip()
    supabase = create_client(URL, KEY)
except Exception as e:
    st.error(f"Kasa hatası: {e}")
    st.stop()

st.set_page_config(page_title="MedAura Dashboard", layout="wide")
st.title("📊 MedAura Satış & Finans Paneli")

# --- VERİ ÇEKME ---
try:
    res = supabase.table("sales_entries").select("*").execute()
    df = pd.DataFrame(res.data)
    
    if not df.empty:
        st.success(f"✅ SONUNDA! Doğru projeye bağlandık. {len(df)} kayıt çekildi.")
        st.dataframe(df, use_container_width=True)
    else:
        st.warning("⚠️ Adres doğru ama tablo şu an boş görünüyor. Lovable'dan bir veri girer misin?")
except Exception as e:
    st.error(f"Bağlantı başarılı ama tablo hatası: {e}")
