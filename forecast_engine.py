import streamlit as st
from supabase import create_client
import pandas as pd

# --- 1. BAĞLANTI ---
try:
    # Kasadan bilgileri çekiyoruz
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_KEY"]
    supabase = create_client(url, key)
except Exception as e:
    st.error(f"Bağlantı hatası: {e}")
    st.stop()

st.set_page_config(page_title="MedAura Dashboard", layout="wide")

# --- 2. VERİ ÇEKME ---
def get_data():
    try:
        # Lovable'ın kullandığı yeni projeden verileri çekiyoruz
        response = supabase.table("sales_entries").select("*").execute()
        return pd.DataFrame(response.data)
    except Exception as e:
        st.error(f"Veri çekilemedi: {e}")
        return pd.DataFrame()

# --- 3. GÖRSELLEŞTİRME ---
st.title("📊 MedAura Satış & Finans Paneli")

df = get_data()

if not df.empty:
    st.success(f"✅ Başardık! {len(df)} kayıt başarıyla yüklendi.")
    st.subheader("📋 Satış Verileri")
    st.dataframe(df, use_container_width=True)
else:
    st.warning("⚠️ Bağlantı tamam ama tablo şu an boş. Lovable'dan yeni bir kayıt girmeyi dene.")
