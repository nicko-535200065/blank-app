import streamlit as st
import pandas as pd
from pathlib import Path
from st_pages import Page, add_page_title, hide_pages


st.set_page_config(
    page_title="Streamlit",
#    page_icon="",
)


# Menampilkan judul dan deskripsi aplikasi
st.title("Selamat Datang di Aplikasi Clustering")
st.write(
    """
    Aplikasi ini melakukan *clustering* atau pengelompokan data produk penjualan menggunakan metode **K-Means Clustering**.
    Ikuti langkah-langkah di bawah ini untuk memulai:
    """
)

# Langkah-langkah penggunaan aplikasi
st.markdown(
    """
    1. Tekan tombol **Mulai** di bawah ini untuk menuju ke halaman *Data*.
    2. Di halaman *Data*, Terdapat contoh data yang bisa digunakan dan dapat mengunggah file data dalam format **Excel**.
       - Pastikan data memiliki kolom yang sesuai dengan kebutuhan model.
    3. Selanjutnya akan dilakukan uji coba K-mean clustering dengan 3 cluster.
       - Terdapat beberapa grafik yang menampilkan jumlah penjualan bulanan per cluslter, jumlah total penjualan per cluster, rata-rata penjualan per cluster, silhouette score, dan boxplot.
    """
)




st.info(
    """
    Klik Mulai untuk menuju ke halaman data.
    """
)

if st.button("Mulai"):
    st.switch_page("pages/1_Data.py")


