import streamlit as st
import altair as alt
import pandas as pd
from pathlib import Path

# Konfigurasi halaman aplikasi Streamlit
st.set_page_config(
    page_title="Streamlit",
    # page_icon="",
)

# Fungsi yang mengatur penyimpanan data CSV
def save_data(df):
    """Saves the updated inventory data to two CSV files."""
    # Lokasi file di luar folder 'pages' (parent directory)
    main_csv_filename = Path(__file__).parent.parent / "Data.csv"
    
    # Lokasi file di dalam folder 'pages'
    pages_csv_filename = Path(__file__).parent / "Data.csv"
    
    # Menyimpan ke dua lokasi file
    df.to_csv(main_csv_filename, index=False)
    df.to_csv(pages_csv_filename, index=False)
    
    st.success("Data berhasil disimpan ke kedua file CSV.")

# ----------------------------------------------------------------------------- #
# Menampilkan halaman utama aplikasi

"""
# Data Penjualan

**Berikut data penjualan toko helm Kartini.**
Unggah data penjualan melalui file CSV.
"""

st.info(
    """
    Silakan unggah file CSV yang berisi data penjualan.
    Setelah diunggah, Anda dapat memilih untuk menyimpannya.
    """
)

# Komponen untuk mengunggah file
uploaded_file = st.file_uploader("Unggah file CSV", type="csv")

if uploaded_file:
    # Membaca file CSV yang diunggah ke pandas DataFrame
    df = pd.read_csv(uploaded_file)

    # Menampilkan data yang diunggah
    st.write("### Data yang diunggah:")
    st.write(df)

    # Tombol untuk menyimpan data yang diunggah
    if st.button("Simpan data"):
        save_data(df)
