import streamlit as st
from supabase import create_client
import pandas as pd
import plotly.express as px

# --- AYARLAR VE BAĞLANTI ---
st.set_page_config(page_title="MedAura Finansal Analiz", layout="wide")

URL = st.secrets["SUPABASE_URL"].strip()
KEY = st.secrets["SUPABASE_KEY"].strip()
supabase = create_client(URL, KEY)

# --- VERİ ÇEKME FONKSİYONU ---
def get_data():
    res = supabase.table("sales_entries").select("*").execute()
    df = pd.DataFrame(res.data)
    if not df.empty:
        df['created_at'] = pd.to_datetime(df['created_at'])
        # Sayısal alanların doğru tipte olduğundan emin olalım
        df[['qty_paid', 'revenue_euro', 'profit_euro']] = df[['qty_paid', 'revenue_euro', 'profit_euro']].apply(pd.to_numeric)
    return df

df = get_data()

# --- DASHBOARD ARAYÜZÜ ---
st.title("📊 MedAura Satış & Kar Dashboard")
st.markdown("---")

if not df.empty:
    # 1. SATIR: KPI METRİKLERİ
    col1, col2, col3, col4 = st.columns(4)
    
    total_revenue = df['revenue_euro'].sum()
    total_profit = df['profit_euro'].sum()
    total_sales_count = len(df)
    avg_profit_rate = (total_profit / total_revenue) * 100 if total_revenue > 0 else 0

    col1.metric("Toplam Ciro", f"€{total_revenue:,.0f}")
    col2.metric("Toplam Kar", f"€{total_profit:,.0f}")
    col3.metric("Satış Adedi", f"{total_sales_count} İşlem")
    col4.metric("Ort. Kar Marjı", f"%{avg_profit_rate:.1f}")

    st.markdown("---")

    # 2. SATIR: GRAFİKLER
    c1, c2 = st.columns(2)

    with c1:
        st.subheader("Bölge Bazlı Satış Dağılımı")
        fig_region = px.pie(df, values='revenue_euro', names='region', hole=0.4,
                            color_discrete_sequence=px.colors.sequential.RdBu)
        st.plotly_chart(fig_region, use_container_width=True)

    with c2:
        st.subheader("Ürün Bazlı Karlılık (Euro)")
        fig_prod = px.bar(df, x='product_name', y='profit_euro', color='product_name',
                          text_auto='.2s', title="Ürünlerin Kar Katkısı")
        st.plotly_chart(fig_prod, use_container_width=True)

    # 3. SATIR: DETAYLI TABLO
    with st.expander("Tüm İşlem Detaylarını Gör"):
        st.dataframe(df.sort_values(by="created_at", ascending=False), use_container_width=True)

else:
    st.info("Henüz görüntülenecek veri bulunamadı. Lovable üzerinden giriş yapın.")

# Sağ alt köşeye küçük bir yenileme butonu
if st.button("Verileri Güncelle"):
    st.rerun()
