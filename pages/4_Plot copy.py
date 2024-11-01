import streamlit as st
import pandas as pd
import altair as alt

# Judul Halaman
st.set_page_config(page_title="Pendapatan Bulanan Toko Helm", layout="wide")
st.title("Pendapatan Bulanan Toko Helm")

# Fungsi untuk Memuat Data
def load_data():
    # Ganti dengan path file CSV Anda
    df = pd.read_csv("Data.csv")  # Pastikan file CSV Anda memiliki kolom 'Tanggal' dan 'Pendapatan'
    df['Tanggal'] = pd.to_datetime(df['Tanggal'], format="%d %B %Y")  # Sesuaikan format tanggal jika berbeda
    return df

# Memuat Data
df = load_data()

# Menambahkan kolom 'Bulan' berdasarkan kolom 'Tanggal'
df['Bulan'] = df['Tanggal'].dt.to_period('M')  # Mengelompokkan data berdasarkan bulan

# Mengelompokkan data untuk menghitung total pendapatan bulanan
pendapatan_bulanan = df.groupby('Bulan')['Pendapatan'].sum().reset_index()
pendapatan_bulanan['Bulan'] = pendapatan_bulanan['Bulan'].dt.to_timestamp()  # Ubah kembali ke timestamp untuk plotting

# Menampilkan Dataframe (Opsional)
st.subheader("Data Pendapatan Bulanan")
st.write(pendapatan_bulanan)

# Membuat Grafik Pendapatan Bulanan
st.subheader("Grafik Pendapatan Bulanan")

chart = (
    alt.Chart(pendapatan_bulanan)
    .mark_line(point=True)  # Menggunakan line chart dengan poin
    .encode(
        x=alt.X("Bulan:T", title="Bulan"),
        y=alt.Y("Pendapatan:Q", title="Total Pendapatan"),
        tooltip=["Bulan:T", "Pendapatan:Q"]
    )
    .properties(width=700, height=400)
    .interactive()  # Membuat chart interaktif
)

# Menampilkan Grafik di Streamlit
st.altair_chart(chart, use_container_width=True)