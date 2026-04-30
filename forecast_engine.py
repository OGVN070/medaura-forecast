import streamlit as st
from supabase import create_client
import pandas as pd

# Bilgileri kasadan çekiyoruz (En güvenli yol)
URL = st.secrets["SUPABASE_URL"].strip()
KEY = st.secrets["SUPABASE_KEY"].strip()

st.set_page_config(page_title="MedAura Dashboard", layout="wide")
st.title("📊 MedAura Satış Dashboard")

try:
    supabase = create_client(URL, KEY)
    
    # Lovable'ın en çok kullandığı tablo adını deniyoruz
    res = supabase.table("sales_entries").select("*").execute()
    df = pd.DataFrame(res.data)
    
    if not df.empty:
        st.success(f"✅ BAŞARDIK! {len(df)} kayıt listeleniyor.")
        st.dataframe(df, use_container_width=True)
    else:
        st.warning("⚠️ Bağlantı tamam ama 'sales_entries' tablosu boş.")
        st.info("💡 Lovable ekranına gidip 1-2 yeni satış girişi yapar mısın? Veriler anında buraya düşecek.")

except Exception as e:
    st.error(f"❌ Bir şeyler ters gitti: {e}")
