import streamlit as st
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
import matplotlib.pyplot as plt

# Konfigurasi halaman aplikasi Streamlit
st.set_page_config(
    page_title="Streamlit",
#    page_icon=":bar_chart:"
)

# Fungsi untuk memuat data
@st.cache_data
def load_data():
    # Ubah path berikut ini sesuai dengan lokasi file CSV Anda
    data_path = "Data.csv"
    df = pd.read_csv(data_path)
    return df

# Fungsi untuk menjalankan K-Means Clustering dan menghitung Silhouette Score
def run_kmeans(df, n_clusters=3):
    # Memilih fitur untuk clustering (pastikan kolom ini ada dalam Data.csv Anda)
    produk_kategori = ['AGV', 'NOL', 'INK', 'KYT', 'MDS', 'BMC', 'HIU', 'NHK', 'GM', 
                       'ASCA', 'ZEUS', 'CAR', 'HBC', 'JPX', 'NJS', 'DYR', 'G2', 'SRM', 
                       'SRT', 'GOG', 'Masker', 'Kaca', 'Aksesoris', 'Lainnya']
    
    # Menjalankan K-Means Clustering
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    cluster_labels = kmeans.fit_predict(df[produk_kategori])
    
    # Menghitung Silhouette Score
    score = silhouette_score(df[produk_kategori], cluster_labels)
    
    # Menambahkan hasil cluster ke DataFrame asli
    df['Cluster'] = cluster_labels
    return df, score

# Memuat data
df = load_data()

# Menjalankan K-Means Clustering dengan jumlah cluster yang ditentukan
st.header("Plot K-Means Clustering")
n_clusters = st.slider("Pilih jumlah cluster:", 2, 10, 3)
clustered_df, silhouette_avg = run_kmeans(df, n_clusters)

# Menampilkan Silhouette Score
#st.write(f"### Silhouette Score untuk {n_clusters} Cluster: {silhouette_avg:.3f}")

# Menampilkan data dengan cluster
#st.subheader("Data dengan Cluster")
#st.write(clustered_df[['Tanggal', 'Pendapatan', 'Cluster']])

# Menghitung total jumlah terjual per cluster untuk kolom kategori helm
produk_kategori = ['AGV', 'NOL', 'INK', 'KYT', 'MDS', 'BMC', 'HIU', 'NHK', 'GM', 
                   'ASCA', 'ZEUS', 'CAR', 'HBC', 'JPX', 'NJS', 'DYR', 'G2', 'SRM', 
                   'SRT', 'GOG', 'Masker', 'Kaca', 'Aksesoris', 'Lainnya']
cluster_sums = clustered_df.groupby('Cluster')[produk_kategori].sum().sum(axis=1)

# Membuat plot bar jumlah terjual per cluster
st.subheader("Plot Jumlah Terjual per Cluster")
plt.figure(figsize=(8, 6))
plt.bar(cluster_sums.index, cluster_sums.values, color='skyblue')
plt.xlabel("Cluster")
plt.ylabel("Jumlah Terjual")
plt.title("Jumlah Terjual per Cluster")
st.pyplot(plt)