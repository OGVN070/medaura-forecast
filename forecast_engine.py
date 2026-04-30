import streamlit as st
from supabase import create_client
import pandas as pd

# --- RADİKAL ÇÖZÜM: KASAYI KULLANMIYORUZ ---
# Buradaki tırnakların içini Lovable'ın verdiği bilgilerle ELİNLE doldur
# Boşluk kalmadığından emin ol!
URL = "https://mywkkeeecykncwlooysz.supabase.co"
KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im15d2trZWVlY2t5bmN3bG9veXN6Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzY5ODM1NDksImV4cCI6MjA5MjU1OTU0OX0.LDbXq0PJvKFzRYQYYjsyc1oSd3dFAOYRc6n_WSEdwzs"

st.set_page_config(page_title="MedAura Finans", layout="wide")
st.title("📊 MedAura Satış Dashboard")

try:
    # Doğrudan bağlantı kuruyoruz
    supabase = create_client(URL, KEY)
    res = supabase.table("sales_entries").select("*").execute()
    df = pd.DataFrame(res.data)
    
    if not df.empty:
        st.success(f"✅ BİNGO! Sonunda başardık Önder! {len(df)} kayıt geldi.")
        st.dataframe(df, use_container_width=True)
    else:
        st.warning("⚠️ Bağlantı kuruldu ama tablo hala boş.")
except Exception as e:
    st.error(f"❌ Kritik Hata: {e}")
