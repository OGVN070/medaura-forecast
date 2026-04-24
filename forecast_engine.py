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

# --- 4. DEHŞET DASHBOARD (Arayüz) ---
st.title("📈 MedAura Sales Forecast")

# Veriyi çekelim (Yeni fonksiyona göre actuals ve forecasts dönüyor)
actuals, forecasts = get_data()

# Eğer herhangi bir veri varsa (Tahmin veya Fatura)
if not actuals.empty or not forecasts.empty:
    # KPI Kartları için hesaplamalar
    total_rev = actuals['revenue_euro'].sum() if not actuals.empty else 0
    target_rev = forecasts['revenue_euro'].sum() if not forecasts.empty else 0
    total_prof = actuals['profit_euro'].sum() if not actuals.empty else 0
    
    # Dashboard Başlığı ve Kartlar
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    
    col1.metric("Gerçekleşen Ciro (Fatura)", f"{total_rev:,.0f} €")
    col2.metric("Hedeflenen Ciro (Tahmin)", f"{target_rev:,.0f} €")
    
    # Başarı Oranı Hesaplama
    progress = (total_rev / target_rev) * 100 if target_rev > 0 else 0
    col3.metric("Hedef Gerçekleşme %", f"% {progress:.1f}")

    st.markdown("---")
    
    # 2. Satır Kartlar (Kar ve Prim Bilgisi)
    c1, c2 = st.columns(2)
    c1.metric("Toplam Net Kar", f"{total_prof:,.0f} €")
    # Örnek prim: Karın %2'si olarak hesaplansın
    c2.metric("Hesaplanan Prim Havuzu", f"{total_prof * 0.02:,.0f} €")

    # AI Tahmini: Sadece gerçek fatura verileri üzerinden geleceği öngörelim
    if not actuals.empty:
        st.subheader("📈 12 Aylık AI Satış Tahmini")
        model, fcst = run_ai_forecast(actuals)
        fig = px.line(fcst, x='ds', y='yhat', 
                     title="Mevcut Fatura Trendine Göre Gelecek Projeksiyonu",
                     labels={'ds': 'Tarih', 'yhat': 'Tahmini Ciro (€)'})
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("💡 Henüz fatura kesilmemiş. AI tahmini yapabilmek için gerçek satış verisi (invoice) bekleniyor.")

else:
    st.warning("⚠️ Henüz veri girişi yapılmadı. Lovable üzerinden 'Forecast' veya 'Fatura' girdiğinizde burası canlanacak.")
