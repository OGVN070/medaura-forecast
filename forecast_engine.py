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
st.title("📈 MedAura Satış Tahmini & Yönetici Paneli")

# Veriyi çekelim
actuals, forecasts = get_data()

if not actuals.empty or not forecasts.empty:
    # --- ÜST KPI KARTLARI ---
    total_rev = actuals['revenue_euro'].sum() if not actuals.empty else 0
    target_rev = forecasts['revenue_euro'].sum() if not forecasts.empty else 0
    total_prof = actuals['profit_euro'].sum() if not actuals.empty else 0
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Gerçekleşen Ciro (Fatura)", f"{total_rev:,.0f} €")
    col2.metric("Hedeflenen Ciro (Tahmin)", f"{target_rev:,.0f} €")
    progress = (total_rev / target_rev) * 100 if target_rev > 0 else 0
    col3.metric("Genel Başarı Oranı", f"% {progress:.1f}")

    st.markdown("---")

    # --- YÖNETİCİ ÖZET TABLOSU FONKSİYONU ---
    def get_summary(df_in):
        if df_in.empty: return pd.DataFrame()
        # Gruplama
        summary = df_in.groupby(['region', 'product_name']).agg({
            'qty_paid': 'sum',
            'qty_free': 'sum',
            'revenue_euro': 'sum',
            'profit_euro': 'sum'
        }).reset_index()
        
        # Hesaplamalar
        summary['Toplam Adet'] = summary['qty_paid'] + summary['qty_free']
        summary['Ciro (KDV Dahil)'] = summary['revenue_euro'] * 1.20
        summary['Ciro (KDV Hariç)'] = summary['revenue_euro']
        summary['MF Maliyeti (KDV Hariç)'] = summary['Ciro (KDV Hariç)'] - summary['profit_euro']
        summary['Brüt Kar'] = summary['profit_euro']
        return summary

    act_sum = get_summary(actuals)
    tar_sum = get_summary(forecasts)

    st.subheader("📋 Bölge & Ürün Bazlı Yönetici Özeti")
    
    # Gerçekleşen ve Hedef tablolarını birleştirme
    if not act_sum.empty and not tar_sum.empty:
        merged = pd.merge(
            act_sum, tar_sum, 
            on=['region', 'product_name'], 
            how='outer', suffixes=('_Gerçek', '_Hedef')
        ).fillna(0)
        
        # Gerçekleşme Yüzdesi (Ciro bazlı)
        merged['Başarı %'] = (merged['Ciro (KDV Hariç)_Gerçek'] / merged['Ciro (KDV Hariç)_Hedef']) * 100
        
        # Tabloyu Formatlama
        final_table = merged[[
            'region', 'product_name', 'Toplam Adet_Gerçek', 
            'Ciro (KDV Dahil)_Gerçek', 'Ciro (KDV Hariç)_Gerçek', 
            'MF Maliyeti (KDV Hariç)_Gerçek', 'Brüt Kar_Gerçek', 'Başarı %'
        ]]
        
        st.dataframe(
            final_table.style.format({
                "Ciro (KDV Dahil)_Gerçek": "{:,.0f} €",
                "Ciro (KDV Hariç)_Gerçek": "{:,.0f} €",
                "MF Maliyeti (KDV Hariç)_Gerçek": "{:,.0f} €",
                "Brüt Kar_Gerçek": "{:,.0f} €",
                "Başarı %": "%{:.1f}"
            }), 
            use_container_width=True
        )

    st.markdown("---")

    # --- AI TAHMİN GRAFİĞİ ---
    if not actuals.empty:
        st.subheader("📈 12 Aylık AI Satış Tahmini (Fatura Bazlı)")
        model, fcst = run_ai_forecast(actuals)
        fig = px.line(fcst, x='ds', y='yhat', title="Mevcut Fatura Trendine Göre Gelecek Projeksiyonu")
        st.plotly_chart(fig, use_container_width=True)
    
else:
    st.warning("⚠️ Veri girişi bekleniyor. Lovable üzerinden veri girildiğinde raporlar canlanacak.")
