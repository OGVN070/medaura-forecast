import streamlit as st
from supabase import create_client
import pandas as pd

# LOVABLE'DAN ALDIĞIN YENİ URL'Yİ BURAYA YAPIŞTIR
URL = "https://mywkkeeeckyncwlooysz.supabase.co"
# SERVICE ROLE KEY'İ BURAYA YAPIŞTIR
KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im15d2trZWVlY2t5bmN3bG9veXN6Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzY5ODM1NDksImV4cCI6MjA5MjU1OTU0OX0.LDbXq0PJvKFzRYQYYjsyc1oSd3dFAOYRc6n_WSEdwzs"

st.set_page_config(page_title="MedAura Dashboard", layout="wide")
st.title("📊 MedAura Satış Dashboard")

try:
    # URL'nin sonundaki boşlukları kod içinde temizliyoruz
    supabase = create_client(URL.strip(), KEY.strip())
    res = supabase.table("sales_entries").select("*").execute()
    df = pd.DataFrame(res.data)
    
    if not df.empty:
        st.success(f"✅ SONUNDA BAŞARDIK! {len(df)} kayıt geldi.")
        st.dataframe(df, use_container_width=True)
    else:
        st.warning("⚠️ Bağlantı kuruldu ama tablo boş.")
except Exception as e:
    st.error(f"❌ Bağlantı hatası: {e}")
    st.info(f"Denenen Adres: {URL}")
