import streamlit as st
from supabase import create_client
import pandas as pd

# --- LOVABLE'IN DÜZELTTİĞİ DOĞRU ADRES ---
URL = "https://mywkkeeeckyncwlooysz.supabase.co"


try:
    # Service Role Key'i kasadan alıyoruz
    KEY = st.secrets.get("SUPABASE_SERVICE_ROLE_KEY", st.secrets.get("SUPABASE_KEY", "")).strip()
if not KEY:
    st.error("Service Role Key bulunamadı. Streamlit Secrets'a SUPABASE_SERVICE_ROLE_KEY ekleyin.")
    st.stop()

    supabase = create_client(URL, KEY)
except Exception as e:
    st.error(f"Kasa hatası: {e}")
    st.stop()

st.set_page_config(page_title="MedAura Dashboard", layout="wide")
st.title("📊 MedAura Satış Dashboard")

# --- VERİ ÇEKME ---
try:
    # Bu sefer o 6 kayıt buraya gelecek!
    res = supabase.table("sales_entries").select("*").execute()
    df = pd.DataFrame(res.data)
    
    if not df.empty:
        st.success(f"✅ SONUNDA OLDU! {len(df)} kayıt başarıyla çekildi.")
        st.dataframe(df, use_container_width=True)
    else:
        st.warning("⚠️ Bağlantı kuruldu ama tablo boş. Lovable'dan bir veri girer misin?")
except Exception as e:
    st.error(f"❌ Bağlantı hatası: {e}")
