import streamlit as st
import pandas as pd
from sklearn.cluster import KMeans

# Konfigurasi halaman aplikasi Streamlit
st.set_page_config(
    page_title="K-Means Clustering",
    page_icon=":bar_chart:"
)

# Fungsi untuk memuat data
@st.cache
def load_data():
    # Ubah path berikut ini sesuai dengan lokasi file CSV Anda
    data_path = "Data.csv"
    df = pd.read_csv(data_path)
    return df

# Fungsi untuk menjalankan K-Means Clustering
def run_kmeans(df, n_clusters=3):
    # Memilih fitur untuk clustering (pastikan kolom ini ada dalam Data.csv Anda)
    features = df[['AGV', 'NOL', 'INK', 'KYT', 'MDS', 'BMC', 'HIU', 'NHK', 'GM', 
                   'ASCA', 'ZEUS', 'CAR', 'HBC', 'JPX', 'NJS', 'DYR', 'G2', 'SRM', 
                   'SRT', 'GOG', 'Masker', 'Kaca', 'Aksesoris', 'Lainnya']]

    # Menjalankan K-Means Clustering
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    kmeans.fit(features)
    
    # Menambahkan hasil cluster ke DataFrame asli
    df['Cluster'] = kmeans.labels_
    return df

# Memuat data
df = load_data()

# Menjalankan K-Means Clustering dengan jumlah cluster yang ditentukan
st.header("K-Means Clustering untuk Data Penjualan")
n_clusters = st.slider("Pilih jumlah cluster:", 2, 10, 3)
clustered_df = run_kmeans(df, n_clusters)

# Menampilkan data cluster
st.subheader("Data dengan Cluster")
st.write(clustered_df[['Tanggal', 'Pendapatan', 'Cluster']])

# Menampilkan tabel per cluster
st.subheader("Hasil Clustering")
for cluster_num in range(n_clusters):
    st.write(f"### Cluster {cluster_num}")
    st.write(clustered_df[clustered_df['Cluster'] == cluster_num][['Tanggal', 'Pendapatan']])