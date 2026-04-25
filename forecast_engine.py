import streamlit as st
from supabase import create_client
import pandas as pd
from prophet import Prophet
import plotly.express as px

# --- 1. BAĞLANTI (Görseldeki URL ve Key bilgilerini buraya yapıştır) ---
URL = "https://vbmzsfrbfgbxfbqlrutx.supabase.co"
KEY = "sb_publishable_m3NadgtQs-AijCRabSPm6A_UQ0eRfiN"
supabase = create_client(URL, KEY)

st.set_page_config(page_title="MedAura AI Forecast", layout="wide")

# --- 2. VERİ ÇEKME VE ANALİZ ---
def get_data():
    response = supabase.table("sales_entries").select("*").execute()
    df = pd.DataFrame(response.data)
    if not df.empty:
        df['created_at'] = pd.to_datetime(df['created_at'])
        # Status sütununa göre ayrım yap (Lovable bunu 'forecast' veya 'invoice' olarak kaydediyor)
        actuals = df[df['status'] == 'invoice']
        forecasts = df[df['status'] == 'forecast']
        return actuals, forecasts
    return pd.DataFrame(), pd.DataFrame()

# --- 3. AI TAHMİN MOTORU (Prophet) ---
def run_ai_forecast(df, horizon=6):
    # Veriyi Prophet formatına getir (ds: tarih, y: değer)
    forecast_df = df.groupby('created_at')['revenue_euro'].sum().reset_index()
    forecast_df.columns = ['ds', 'y']
    forecast_df['ds'] = forecast_df['ds'].dt.tz_localize(None)

    m = Prophet(yearly_seasonality=True, daily_seasonality=False, weekly_seasonality=False)
    m.fit(forecast_df)
    
    future = m.make_future_dataframe(periods=horizon, freq='MS')
    forecast = m.predict(future)
    return m, forecast

# --- 4. YÖNETİCİ ÖZET PANELLERİ (RENKLİ) ---
st.title("📊 MedAura Satış & Finans Paneli")

actuals, forecasts = get_data()

# Renk Paleti Tanımlama
COLOR_SCHEME = ["#00B4D8", "#90E0EF", "#0077B6", "#48CAE4"]

def render_summary_table(df_in, title, color):
    if df_in.empty:
        st.info(f"{title} için henüz kayıt bulunmuyor.")
        return

    # Hesaplama Mantığı
    # MF Maliyeti = Satış Fiyatı - Kar (Bize maliyeti verir)
    df_in['MF_Maliyet'] = df_in['revenue_euro'] - df_in['profit_euro']
    
    # İstenen Kolonlar
    df_in['Ciro_Hariç'] = df_in['revenue_euro']
    df_in['Ciro_Dahil'] = df_in['revenue_euro'] * 1.20
    df_in['Net_Ciro_MF_Dusus_Haric'] = df_in['revenue_euro'] - df_in['MF_Maliyet']

    # 1. TABLO: DETAYLI ÖZET
    st.subheader(f"📋 {title} - Detaylı Ürün & Müşteri Özeti")
    customer_table = df_in.groupby(['customer_name', 'region', 'product_name']).agg({
        'qty_paid': 'sum',
        'qty_free': 'sum',
        'Ciro_Hariç': 'sum',
        'Ciro_Dahil': 'sum',
        'Net_Ciro_MF_Dusus_Haric': 'sum'
    }).reset_index()

    st.dataframe(customer_table.style.format({
        'Ciro_Hariç': '{:,.2f} €',
        'Ciro_Dahil': '{:,.2f} €',
        'Net_Ciro_MF_Dusus_Haric': '{:,.2f} €'
    }).background_gradient(cmap='Blues', subset=['Net_Ciro_MF_Dusus_Haric']), use_container_width=True)

    # 2. TABLO: BÖLGE BAZLI NET CİRO
    st.subheader(f"🌍 {title} - Bölge Net Ciro (KDV Hariç)")
    region_table = df_in.groupby('region').agg({
        'Net_Ciro_MF_Dusus_Haric': 'sum'
    }).reset_index()
    
    st.dataframe(region_table.style.format({
        'Net_Ciro_MF_Dusus_Haric': '{:,.2f} €'
    }), use_container_width=True)

# Dashboard Bölümleri
st.markdown(f"<h3 style='color:{COLOR_SCHEME[0]}'>✅ GERÇEKLEŞEN FATURALAR</h3>", unsafe_allow_html=True)
render_summary_table(actuals, "Gerçekleşen", COLOR_SCHEME[0])

st.markdown("---")

st.markdown(f"<h3 style='color:{COLOR_SCHEME[2]}'>🎯 HEDEFLER (FORECAST)</h3>", unsafe_allow_html=True)
render_summary_table(forecasts, "Tahminler", COLOR_SCHEME[2])

st.markdown("---")

# Renkli AI Grafiği
if not actuals.empty:
    st.subheader("📈 Renkli AI Gelecek Projeksiyonu")
    model, fcst = run_ai_forecast(actuals)
    fig = px.line(fcst, x='ds', y='yhat', 
                  title="Fatura Trendine Göre Gelecek Tahmini",
                  color_discrete_sequence=[COLOR_SCHEME[0]]) # Grafiği renklendirdik
    fig.update_traces(line=dict(width=4)) # Çizgiyi kalınlaştırdık
    st.plotly_chart(fig, use_container_width=True)
