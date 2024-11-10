# pages/4_Product_Clustering.py

import streamlit as st
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score, silhouette_samples
import matplotlib.pyplot as plt

# Fungsi untuk memuat data
@st.cache_data
def load_data():
    data_path = "Data.csv"  # Sesuaikan path dengan lokasi file CSV Anda
    df = pd.read_csv(data_path)
    return df

# Fungsi untuk menjalankan K-Means Clustering pada produk
def run_product_clustering(df, n_clusters=3):
    # Pivot data untuk mendapatkan penjualan per produk
    produk_df = df[['AGV', 'NOL', 'INK', 'KYT', 'MDS', 'BMC', 'HIU', 'NHK', 'GM', 
                    'ASCA', 'ZEUS', 'CAR', 'HBC', 'JPX', 'NJS', 'DYR', 'G2', 
                    'SarungMotor', 'SarungTangan', 'Googles', 'Masker', 'Kaca', 
                    'Aksesoris', 'Lainnya']].sum().to_frame(name='TotalPenjualan')
    produk_df.index.name = 'Produk'
    produk_df = produk_df.reset_index()
    
    # Menjalankan K-Means Clustering
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    cluster_labels = kmeans.fit_predict(produk_df[['TotalPenjualan']])
    
    # Menambahkan hasil ke DataFrame produk
    produk_df['Cluster Produk'] = cluster_labels
    
    # Menghitung Silhouette Score
    silhouette_avg = silhouette_score(produk_df[['TotalPenjualan']], cluster_labels)
    
    return produk_df, silhouette_avg

# Load data
df = load_data()

# Menjalankan K-Means Clustering pada produk
st.header("K-Means Clustering untuk Produk")
n_clusters = st.slider("Pilih jumlah cluster untuk produk:", 2, 10, 3)
clustered_produk_df, silhouette_avg = run_product_clustering(df, n_clusters)

# Menampilkan Silhouette Score rata-rata
st.write(f"### Silhouette Score rata-rata untuk {n_clusters} Cluster Produk: {silhouette_avg:.3f}")

# Menampilkan data dengan cluster produk
st.subheader("Data Produk dengan Cluster")
st.write(clustered_produk_df)

# Menampilkan tabel per cluster produk
st.subheader("Hasil Clustering per Cluster Produk")
for cluster_num in range(n_clusters):
    st.write(f"### Cluster Produk {cluster_num}")
    cluster_data = clustered_produk_df[clustered_produk_df['Cluster Produk'] == cluster_num]
    st.write(cluster_data[['Produk', 'TotalPenjualan']])

# Visualisasi hasil clustering
#fig, ax = plt.subplots(figsize=(10, 6))
#for cluster_num in range(n_clusters):
#    cluster_data = clustered_produk_df[clustered_produk_df['Cluster Produk'] == cluster_num]
#    ax.bar(cluster_data['Produk'], cluster_data['TotalPenjualan'], label=f'Cluster {cluster_num}')

#ax.set_title("Total Penjualan Produk per Cluster")
#ax.set_xlabel("Produk")
#ax.set_ylabel("Total Penjualan")
#plt.xticks(rotation=90)
#plt.legend()
#st.pyplot(fig)