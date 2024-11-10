
import streamlit as st
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score, silhouette_samples
import matplotlib.pyplot as plt
from pathlib import Path

# Fungsi untuk memuat data
@st.cache_data
def load_data():
    data_path = Path(__file__).parent / "Data_Toko_Helm.xlsx"  # Sesuaikan path dengan lokasi file CSV Anda
    df = pd.read_excel(data_path)
    return df

# Fungsi untuk menjalankan K-Means Clustering pada produk
def run_product_clustering(df, n_clusters=3):
    # Pivot data untuk mendapatkan penjualan per produk
    df2 = df[['AGV', 'NOL', 'INK', 'KYT', 'MDS', 'BMC', 'HIU', 'NHK', 'GM', 
                    'ASCA', 'ZEUS', 'CAR', 'HBC', 'JPX', 'NJS', 'DYR', 'G2', 
                    'SRM', 'SRT', 'GOG', 'Masker', 'Kaca', 
                    'Aksesoris', 'Lainnya']].sum().to_frame(name='TotalPenjualan')
    df2.index.name = 'Produk'
    df2 = df2.reset_index()
    
    # Menjalankan K-Means Clustering
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    cluster_labels = kmeans.fit_predict(df2[['TotalPenjualan']])
    
    # Menambahkan hasil ke DataFrame produk
    df2['Cluster Produk'] = cluster_labels
    
    # Menghitung Silhouette Score
    silhouette_avg = silhouette_score(df2[['TotalPenjualan']], cluster_labels)
    
    return df2, silhouette_avg

# Load data
df = load_data()

# Menjalankan K-Means Clustering pada produk
st.header("K-Means Clustering")
n_clusters = st.slider("Pilih jumlah cluster:", 2, 10, 3)
#n_clusters = 3
clustered_df2, silhouette_avg = run_product_clustering(df, n_clusters)

# Menampilkan Silhouette Score rata-rata
st.write(f"### Silhouette Score rata-rata untuk {n_clusters} Cluster Produk: {silhouette_avg:.3f}")

# Menampilkan data dengan cluster produk
st.subheader("Data Produk dengan Cluster")
st.write(clustered_df2)

# Menampilkan tabel per cluster produk
st.subheader("Hasil Clustering per Cluster Produk")
for cluster_num in range(n_clusters):
    st.write(f"### Cluster Produk {cluster_num}")
    cluster_data = clustered_df2[clustered_df2['Cluster Produk'] == cluster_num]
    st.write(cluster_data[['Produk', 'TotalPenjualan']])
