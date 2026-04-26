import streamlit as st
from supabase import create_client
import pandas as pd

# --- 1. BAĞLANTI (Önder için temizlendi) ---
URL = "https://vbmzsfrbfgbxfbqlrutx.supabase.co"
# Bu anahtar RLS engellerini aşar ve doğrudan veriyi çeker
KEY = st.secrets.get("SUPABASE_KEY") if "SUPABASE_KEY" in st.secrets else "EY_BURAYA_SUPABASE_EKRANINDAKI_SERVICE_ROLE_KEYI_YAPISTIR"

# Eğer KEY hala tırnak içindeyse, lütfen Supabase ekranındaki 
# 'service_role' (secret) kısmındaki butona basıp buraya yapıştır.

try:
    supabase = create_client(URL, KEY)
except Exception as e:
    st.error(f"Bağlantı kurulum hatası: {e}")

st.set_page_config(page_title="MedAura Sales Forecast", layout="wide")

# --- 2. VERİ ÇEKME ---
def get_data():
    try:
        # sales_entries tablosundan tüm veriyi çek
        response = supabase.table("sales_entries").select("*").execute()
        return pd.DataFrame(response.data)
    except Exception as e:
        st.error(f"Veri çekme hatası: {e}")
        return pd.DataFrame()

# --- 3. DASHBOARD ---
st.title("📊 MedAura Satış & Finans Paneli")

df = get_data()

if not df.empty:
    st.success(f"✅ Başardık Önder! Veritabanında {len(df)} kayıt bulundu.")
    st.dataframe(df, use_container_width=True)
else:
    st.warning("⚠️ Bağlantı kuruldu ama tablo şu an boş görünüyor. Lovable'dan bir veri girmeyi dene.")
    st.info("İpucu: Supabase ekranındaki 'service_role' anahtarını kullandığından emin ol.")
