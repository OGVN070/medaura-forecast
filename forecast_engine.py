import streamlit as st
from supabase import create_client
import pandas as pd
import socket

st.set_page_config(page_title="Hata Dedektifi", layout="wide")
st.title("🕵️‍♂️ MedAura Bağlantı Dedektifi")

# --- TEST VERİLERİ (DOĞRUDAN YAZILDI) ---
URL = "https://mywkkeeecykncwlooysz.supabase.co"
# Aşağıdaki KEY kısmına Lovable'ın verdiği Service Role Key'i yapıştır
KEY = "BURAYA_LOVABLE_SERVICE_ROLE_KEYI_YAPISTIR"

# 1. TEST: İnternet adresi çözülebiliyor mu?
st.subheader("1. Aşama: DNS Testi")
try:
    hostname = "mywkkeeecykncwlooysz.supabase.co"
    ip_address = socket.gethostbyname(hostname)
    st.success(f"✅ Adres bulundu! IP: {ip_address}")
except Exception as e:
    st.error(f"❌ Adres internette bulunamıyor! Hata: {e}")

# 2. TEST: Supabase Bağlantısı
st.subheader("2. Aşama: Supabase Bağlantı Testi")
try:
    supabase = create_client(URL, KEY)
    res = supabase.table("sales_entries").select("*").limit(1).execute()
    st.success("✅ Supabase ile el sıkışıldı!")
    st.write("Gelen ilk veri:", res.data)
except Exception as e:
    st.error(f"❌ Bağlantı başarısız! Detay: {e}")
