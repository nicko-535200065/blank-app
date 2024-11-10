import streamlit as st
import altair as alt
import pandas as pd
from pathlib import Path

# Konfigurasi halaman aplikasi Streamlit
st.set_page_config(
    page_title="Streamlit",
    # page_icon="",
)

# Fungsi untuk memuat data dari CSV
def load_data():
    """Loads the inventory data from a CSV file."""
    CSV_FILENAME = Path(__file__).parent / "Data_Toko_Helm.xlsx"
    
    # Membaca data dari CSV ke pandas DataFrame
    try:
        df = pd.read_excel(CSV_FILENAME)
    except FileNotFoundError:
        st.error(f"File {CSV_FILENAME} tidak ditemukan.")
        return None

    return df

#Fungsi untuk menyimpan data ke CSV
def save_data(df):
    """Saves the updated inventory data to two CSV files."""
    #main_csv_filename = Path(__file__).parent.parent / "Data.csv"
    #main_csv_filename = Path(__file__).parent. / "Data.csv"
    pages_csv_filename = Path(__file__).parent / "Data_Toko_Helm.xlsx"
    
    #df.to_csv(main_csv_filename, index=False)
    df.to_csv(pages_csv_filename, index=False)
    
    st.success("Data berhasil disimpan")


# ----------------------------------------------------------------------------- #
# Menampilkan halaman utama aplikasi
"""
# Data Penjualan

Halaman ini menampilkan data penjualan dari toko helm Kartini.
"""

st.info(
    """
    Anda dapat mengunggah file baru untuk menampilkan data baru.
    """
)

# Memuat data dari CSV asli
df = load_data()

if df is None:
    st.stop()

# Tampilkan data saat ini
#st.subheader("Data Saat Ini")
st.write(df)

# Komponen unggah file untuk memperbarui data
#uploaded_file = st.file_uploader("Unggah file CSV atau Excel", type=["csv", "xlsx"])
uploaded_file = st.file_uploader("Unggah file Excel", type=["xlsx"])

if uploaded_file is not None:
    try:
        # Menentukan format file dan membaca sesuai formatnya
        if uploaded_file.name.endswith('.xlsx'):
            new_data = pd.read_excel(uploaded_file)
        #elif uploaded_file.name.endswith('.csv'):
        #    new_data = pd.read_csv(uploaded_file)

        # Menampilkan data baru yang akan diunggah
        #st.subheader("Data yang Diunggah")
        st.write(new_data)
        
        # Konfirmasi untuk mengganti data lama dengan data yang baru
        if st.button("Simpan Data Baru"):
            save_data(new_data)
            st.success("Data baru berhasil diunggah dan disimpan.")
    except Exception as e:
        st.error(f"Terjadi kesalahan saat memuat data: {e}")