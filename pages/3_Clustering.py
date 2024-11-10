import streamlit as st
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn import preprocessing
from pathlib import Path
from scipy.spatial.distance import cdist

st.set_page_config(
    page_title="Streamlit",
    # page_icon="",  # Uncomment jika ada ikon khusus
)

# Baca file Excel
file_path = Path(__file__).parent / "Data_Toko_Helm.xlsx"
df = pd.read_excel(file_path)

st.header("Clustering")

# Pilih jumlah cluster
n_clusters = 3

# Persiapan data
df2 = df.drop(['Tanggal', 'Bulan', 'Tahun', 'Pendapatan', 'Jumlah', 'Lainnya'], axis=1)
df2 = df2.T  # Transpose

# Normalisasi data
df2_norm = preprocessing.normalize(df2)
df2_norm = pd.DataFrame(df2_norm)

# Menjalankan K-Means Clustering
kmeans = KMeans(n_clusters=n_clusters, random_state=42)
kmeans.fit(df2_norm)

# Menambahkan hasil clustering ke DataFrame df3
df3 = df2.copy()  # Menyimpan versi asli df2 yang sudah ditranspose
df3['Cluster'] = kmeans.labels_


# Menghitung jarak ke centroid
#centroids = kmeans.cluster_centers_
#df3['Jarak_Centroid'] = cdist(df2_norm, centroids).min(axis=1)  # Jarak terdekat ke centroid masing-masing cluster

# Menampilkan Data Produk dengan Cluster
st.subheader("Data Produk dengan 3 Cluster")
st.write(df3['Cluster'])
#st.write(df3[['Cluster', 'Jarak_Centroid']])

for cluster_num in range(n_clusters):
    st.write(f"### Cluster {cluster_num}")
    st.write(df3['Cluster'][df3['Cluster'] == cluster_num])
    #st.write(df3['Jarak_Centroid'][df3['Cluster'] == cluster_num])

# Menampilkan silhouette score
score = silhouette_score(df2_norm, kmeans.labels_)
#st.write(f'\nSilhouette Score: {score:.4f}')