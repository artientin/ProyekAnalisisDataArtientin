import pandas as pd
from PIL import Image
import plotly.express as px
import streamlit as st

# Pengaturan default untuk Plotly
px.defaults.template = 'plotly_dark'
px.defaults.color_continuous_scale = 'greens'

# Gambar sidebar
img = Image.open('assets/gambar.png')
st.sidebar.image(img)

# Teks sidebar
st.sidebar.markdown("""
    <h1 style="text-align: center;">Dibuat oleh Artientin</h1>
""", unsafe_allow_html=True)

# Membaca data
data_cleaned = pd.read_csv('all_data.csv')

# Pilih tahun
year = data_cleaned['year'].unique()
selected_year = st.sidebar.selectbox("Pilih Tahun:", year)

# Data untuk tahun yang dipilih
data_selected_year = data_cleaned[data_cleaned['year'] == selected_year]
pm25_threshold = 75
exceeding_days = (data_selected_year.groupby(['year', 'month', 'day'])['PM2.5'].mean() > pm25_threshold).value_counts()

# NO2 untuk tahun yang dipilih
monthly_NO2 = data_cleaned[data_cleaned['year'] == selected_year].groupby('month')['NO2'].mean().reset_index()

# PM25 untuk tahun yang dipilih
yearly_PM25 = data_cleaned.groupby('year')['PM2.5'].mean().reset_index()

# Data Hujan
data_cleaned['is_rain'] = data_cleaned['RAIN'] > 0

# Header
st.markdown("""
    <h1 style="text-align: center; font-family: Arial; color: #77DD77;">Dashboard Analisis Kualitas Udara di Tiantan</h1>
""", unsafe_allow_html=True)

# Navbar
st.markdown("""
    <style>
    .nav-tabs {
        display: flex;
        justify-content: center;
        width: 100%;
        margin-top: 20px;
        border-bottom: 2px solid #ccc;
    }
    .nav-tabs > div > button {
        background-color: #007BFF;
        color: white;
        font-size: 16px;
        font-weight: bold;
        border-radius: 0;
        padding: 10px 20px;
        border: none;
        margin: 0 10px;
    }
    .nav-tabs > div > button:hover {
        background-color: #0056b3;
        color: #fff;
    }
    .nav-tabs > div > button:focus {
        background-color: #0056b3;
        color: #fff;
    }
    </style>
""", unsafe_allow_html=True)

# Membuat tiga tab
st.markdown('<div class="nav-tabs"></div>', unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["Analisis Berdasarkan Tahun", "Analisis Tahun 2013-2017", "Dataset"])

with tab1:
    st.subheader(f"Analisis Data pada Tahun {selected_year}")
    
    # Distribusi Bulan Berdasarkan Tingkat NO2
    fig_no2 = px.line(monthly_NO2, x='month', y='NO2', 
                       title=f'Distribusi Bulan Berdasarkan Tingkat NO2 Tahun {selected_year}',
                       labels={'month': 'Bulan', 'NO2': 'Konsentrasi NO2 (µg/m³)'})
    st.plotly_chart(fig_no2)

    # Persentase Hari yang Melebihi Ambang Batas PM2.5
    labels = ['Di Atas Ambang Batas', 'Di Bawah Ambang Batas']
    fig_pie = px.pie(values=exceeding_days, names=labels,
                     title=f'Persentase Hari dengan Konsentrasi PM2.5 Melebihi Ambang Batas pada Tahun {selected_year}',
                     color=labels, color_discrete_sequence=['red', 'green'])
    st.plotly_chart(fig_pie)

with tab2:
    st.subheader("Analisis Data untuk Periode 2013-2017")
    
    # Tren Tahunan Konsentrasi PM2.5
    fig_yearly_pm25 = px.bar(yearly_PM25, x='year', y='PM2.5',
                              title='Tren Tahunan Konsentrasi PM2.5 di Tiantan (2013-2017)',
                              labels={'year': 'Tahun', 'PM2.5': 'Rata-rata Konsentrasi PM2.5 (µg/m³)'})
    st.plotly_chart(fig_yearly_pm25)

    # Box Plot SO2
    fig_box = px.box(data_cleaned, x='is_rain', y='SO2',
                      title='Perbandingan Konsentrasi SO2 Saat Hujan dan Tidak Hujan',
                      labels={'is_rain': 'Hujan', 'SO2': 'Konsentrasi SO2 (µg/m³)'})
    fig_box.update_xaxes(tickvals=[0, 1], ticktext=['Tidak Hujan', 'Hujan'])
    st.plotly_chart(fig_box)

with tab3:
    st.subheader(f"Tabel Dataset untuk Tahun {selected_year}")
    st.dataframe(data_selected_year)
