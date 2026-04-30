import streamlit as st
from supabase import create_client, Client
import pandas as pd

URL = "https://mywkkeeeckyncwlooysz.supabase.co"

try:
    KEY = st.secrets["SUPABASE_SERVICE_ROLE_KEY"]
except KeyError:
    st.error("❌ SUPABASE_SERVICE_ROLE_KEY secret tanımlı değil. Streamlit Cloud → Settings → Secrets'a ekleyin.")
    st.stop()

if not KEY:
    st.error("❌ SUPABASE_SERVICE_ROLE_KEY boş.")
    st.stop()

supabase: Client = create_client(URL, KEY)

df = pd.DataFrame(supabase.table("sales_entries").select("*").execute().data)
st.dataframe(df)

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
