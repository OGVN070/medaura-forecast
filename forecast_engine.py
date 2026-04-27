import streamlit as st
from supabase import create_client
import pandas as pd

# --- 1. BAĞLANTI AYARLARI ---
# Lovable'ın onayladığı gerçek adres:
URL = "https://mywkkeeecykncwlooysz.supabase.co"

try:
    # Service Role Key'i kasadan alıyoruz (RLS'yi geçmek için şart!)
    KEY = st.secrets["SUPABASE_KEY"].strip()
    supabase = create_client(URL, KEY)
except Exception as e:
    st.error(f"Kasa hatası: {e}")
    st.stop()

st.set_page_config(page_title="MedAura Dashboard", layout="wide")
st.title("📊 MedAura Satış & Finans Paneli")

# --- 2. VERİ ÇEKME ---
try:
    # RLS'yi bypass ederek tüm kayıtları çekiyoruz
    res = supabase.table("sales_entries").select("*").execute()
    df = pd.DataFrame(res.data)
    
    if not df.empty:
        st.success(f"✅ BAŞARDIK! Güvenlik duvarı geçildi. {len(df)} kayıt yüklendi.")
        
        # Tabloyu gösterelim
        st.subheader("📋 Mevcut Satış Verileri")
        st.dataframe(df, use_container_width=True)
        
        # Grafik için küçük bir ön izleme
        if "revenue_euro" in df.columns:
            st.line_chart(df.set_index("created_at")["revenue_euro"] if "created_at" in df.columns else df["revenue_euro"])
            
    else:
        st.warning("⚠️ Bağlantı kuruldu ama tablo hala boş. Lovable'dan veri girdiğine emin ol.")
except Exception as e:
    st.error(f"Veri çekme hatası (RLS engeli olabilir mi?): {e}")
