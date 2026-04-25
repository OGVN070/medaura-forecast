import streamlit as st
from supabase import create_client
import pandas as pd
from prophet import Prophet
import plotly.express as px

# --- 1. BAĞLANTI ---
URL = "https://vbmzsfrbfgbxfbqlrutx.supabase.co"
KEY = "sb_publishable_m3NadgtQs-AijCRabSPm6A_UQ0eRfiN"
supabase = create_client(URL, KEY)

st.set_page_config(page_title="MedAura Sales Forecast", layout="wide")

# --- 2. VERİ ÇEKME ---
def get_data():
    try:
        response = supabase.table("sales_entries").select("*").execute()
        df = pd.DataFrame(response.data)
        if not df.empty:
            # Tarih dönüşümü
            df['created_at'] = pd.to_datetime(df['created_at'])
            
            # Status sütunundaki boşlukları sil ve hepsini küçük harfe çevirerek karşılaştır
            df['status_clean'] = df['status'].get(df['status'], df['status']).astype(str).str.strip().str.lower()
            
            actuals = df[df['status_clean'] == 'invoice']
            forecasts = df[df['status_clean'] == 'forecast']
            
            return actuals, forecasts
    except Exception as e:
        st.error(f"Veri çekme hatası: {e}")
    return pd.DataFrame(), pd.DataFrame()

# --- 3. AI TAHMİN MOTORU ---
def run_ai_forecast(df, horizon=6):
    forecast_df = df.groupby('created_at')['revenue_euro'].sum().reset_index()
    forecast_df.columns = ['ds', 'y']
    forecast_df['ds'] = forecast_df['ds'].dt.tz_localize(None)
    m = Prophet(yearly_seasonality=True, daily_seasonality=False, weekly_seasonality=False)
    m.fit(forecast_df)
    future = m.make_future_dataframe(periods=horizon, freq='MS')
    forecast = m.predict(future)
    return m, forecast

# --- 4. YÖNETİCİ ÖZET PANELLERİ ---
st.title("📊 MedAura Satış & Finans Paneli")

actuals, forecasts = get_data()
COLOR_SCHEME = ["#00B4D8", "#90E0EF", "#0077B6", "#48CAE4"]

def render_summary_table(df_in, title):
    if df_in.empty:
        st.info(f"{title} için henüz kayıt bulunmuyor.")
        return

    # Hesaplamalar
    df_in['MF_Maliyet'] = df_in['revenue_euro'] - df_in['profit_euro']
    df_in['Net_Ciro_MF_Dusus_Haric'] = df_in['revenue_euro'] - df_in['MF_Maliyet']
    df_in['Ciro_Dahil'] = df_in['revenue_euro'] * 1.20

    # 1. TABLO: DETAYLI ÖZET (Şemadaki kolon isimlerini kullandım: customer, product, region)
    st.subheader(f"📋 {title} - Detaylı Ürün & Müşteri Özeti")
    customer_table = df_in.groupby(['customer', 'region', 'product']).agg({
        'qty_paid': 'sum',
        'qty_free': 'sum',
        'revenue_euro': 'sum',
        'Ciro_Dahil': 'sum',
        'Net_Ciro_MF_Dusus_Haric': 'sum'
    }).reset_index()

    st.dataframe(customer_table.style.format({
        'revenue_euro': '{:,.2f} €',
        'Ciro_Dahil': '{:,.2f} €',
        'Net_Ciro_MF_Dusus_Haric': '{:,.2f} €'
    }), use_container_width=True)

    # 2. TABLO: BÖLGE BAZLI NET CİRO
    st.subheader(f"🌍 {title} - Bölge Net Ciro (KDV Hariç)")
    region_table = df_in.groupby('region').agg({'Net_Ciro_MF_Dusus_Haric': 'sum'}).reset_index()
    st.dataframe(region_table.style.format({'Net_Ciro_MF_Dusus_Haric': '{:,.2f} €'}), use_container_width=True)

# Dashboard Görünümü
st.markdown(f"<h3 style='color:{COLOR_SCHEME[0]}'>✅ GERÇEKLEŞEN FATURALAR</h3>", unsafe_allow_html=True)
render_summary_table(actuals, "Gerçekleşen")

st.markdown("---")

st.markdown(f"<h3 style='color:{COLOR_SCHEME[2]}'>🎯 HEDEFLER (FORECAST)</h3>", unsafe_allow_html=True)
render_summary_table(forecasts, "Tahminler")

# AI Grafiği
if not actuals.empty:
    st.markdown("---")
    st.subheader("📈 AI Gelecek Projeksiyonu")
    model, fcst = run_ai_forecast(actuals)
    fig = px.line(fcst, x='ds', y='yhat', title="Trend Analizi", color_discrete_sequence=[COLOR_SCHEME[0]])
    st.plotly_chart(fig, use_container_width=True)
