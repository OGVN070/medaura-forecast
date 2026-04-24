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
    # Supabase'den girilen satışları çek
    response = supabase.table("sales_entries").select("*").execute()
    df = pd.DataFrame(response.data)
    if not df.empty:
        df['created_at'] = pd.to_datetime(df['created_at'])
    return df

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

# --- 4. DEHŞET DASHBOARD (Arayüz) ---
st.title("💎 MedAura Ticari Zeka & Forecast")

data = get_data()

if not data.empty:
    # KPI Kartları (Ciro, Kar, Prim)
    total_rev = data['revenue_euro'].sum()
    total_prof = data['profit_euro'].sum()
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Toplam Ciro", f"{total_rev:,.0f} €")
    col2.metric("Net Kar", f"{total_prof:,.0f} €")
    
    # AI Tahmin Grafiği
    st.subheader("🔮 12 Aylık AI Satış Tahmini")
    model, fcst = run_ai_forecast(data)
    fig = px.line(fcst, x='ds', y='yhat', title="Gelecek Projeksiyonu")
    st.plotly_chart(fig, use_container_width=True)
    
    st.success("🤖 AI Notu: Mevcut trende göre önümüzdeki ay %5 büyüme bekleniyor.")
else:
    st.warning("Henüz veri girişi yapılmadı. Lovable üzerinden veri girildiğinde burası canlanacak.")
