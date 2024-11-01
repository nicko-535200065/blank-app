import streamlit as st
import altair as alt
import pandas as pd
from pathlib import Path


st.set_page_config(
    page_title="Streamlit",
#    page_icon="",
)

# Fungsi yang mengatur pembacaan dan penyimpanan data CSV

def load_data():
    """Loads the inventory data from a CSV file."""
    CSV_FILENAME = Path(__file__).parent / "Data.csv"
    
    # Membaca data dari CSV ke pandas DataFrame
    try:
        df = pd.read_csv(CSV_FILENAME)
    except FileNotFoundError:
        st.error(f"File {CSV_FILENAME} tidak ditemukan.")
        return None

    return df

def save_data(df):
    """Saves the updated inventory data back to the CSV file."""
    CSV_FILENAME = Path(__file__).parent / "Data.csv"
    df.to_csv(CSV_FILENAME, index=False)
    st.success("Perubahan berhasil disimpan ke file CSV.")

# ----------------------------------------------------------------------------- #
# Menampilkan halaman utama aplikasi

"""
#  Data Penjualan

**Berikut data penjualan toko helm Kartini.**
Halaman ini membaca dan menulis langsung dari/ke file dataset.
"""

st.info(
    """
    Gunakan tabel di bawah ini untuk menambah, menghapus, dan mengedit item.
    Jangan lupa untuk menyimpan perubahan setelah selesai.
    """
)

# Memuat data dari CSV
df = load_data()

if df is None:
    st.stop()

# Tampilkan data dengan tabel yang dapat diedit
edited_df = st.data_editor(
    df,
    disabled=[""],  # Jangan izinkan pengeditan kolom ''.
    num_rows="dynamic",  # Izinkan penambahan/penghapusan baris.
    column_config={
        #"Pendapatan": st.column_config.NumberColumn(format="Rp.%.2f"),
    },
    key="inventory_table",
)

# Tombol untuk menyimpan perubahan
if st.button("Simpan perubahan"):
    save_data(edited_df)

