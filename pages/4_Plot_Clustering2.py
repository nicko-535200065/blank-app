import streamlit as st
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from yellowbrick.cluster import SilhouetteVisualizer
from yellowbrick.datasets import load_nfl
import seaborn as sns
import pandas as pd
from sklearn import preprocessing
import matplotlib.pyplot as plt
from pathlib import Path

# Konfigurasi halaman aplikasi Streamlit
st.set_page_config(
    page_title="Clustering Produk Toko Helm",
)

# Fungsi untuk memuat data
@st.cache_data
def load_data():
    file_path = Path(__file__).parent / "Data_Toko_Helm.xlsx"
    df = pd.read_excel(file_path)
    return df

# Memuat data
df = load_data()

# Menampilkan beberapa baris pertama data asli
st.subheader("Data Penjualan Asli")
st.write(df.head())

# Menghilangkan kolom yang tidak diperlukan untuk clustering
df2 = df.drop(['Tanggal', 'Bulan', 'Tahun', 'Pendapatan', 'Jumlah', 'Lainnya'], axis=1)

# Melakukan transpose data
df2 = df2.T

# Normalisasi data
df2_norm = preprocessing.normalize(df2)
df2_norm = pd.DataFrame(df2_norm)

# Menjalankan K-Means Clustering
kmeans = KMeans(n_clusters=3, random_state=42)
kmeans.fit(df2_norm)

# Visualisasi silhouette dengan Yellowbrick
st.subheader("Silhouette Score untuk Cluster Produk")
fig, ax = plt.subplots(figsize=(6, 6))
visualizer = SilhouetteVisualizer(kmeans, colors='yellowbrick', ax=ax)
visualizer.fit(df2_norm)
st.pyplot(fig)

# Menampilkan nilai silhouette score
score = silhouette_score(df2_norm, kmeans.labels_)
st.write(f"Silhouette Score rata-rata untuk 3 cluster: {score:.4f}")

# Menyimpan hasil clustering ke dalam DataFrame
df3 = df2.copy()
df3['Cluster'] = kmeans.labels_

# Menampilkan data tiap produk di masing-masing cluster
st.subheader("Data Produk per Cluster")
for i in range(3):
    st.write(f"### Cluster {i+1}")
    st.write(df3[df3['Cluster'] == i].index.tolist())

# Mengelompokkan data ke dalam DataFrame baru berdasarkan cluster
produk_cluster0 = df3[df3['Cluster'] == 0]
produk_cluster1 = df3[df3['Cluster'] == 1]
produk_cluster2 = df3[df3['Cluster'] == 2]

# Membuat tabel total penjualan bulanan berdasarkan cluster
df['Bulan'] = df['Bulan'].astype(str)
df0 = df.loc[produk_cluster0.index]
df1 = df.loc[produk_cluster1.index]
df2 = df.loc[produk_cluster2.index]

# Plot jumlah penjualan per bulan untuk setiap cluster
st.subheader("Plot Jumlah Penjualan Bulanan per Cluster")
colors = ['orange', 'blue', 'red', 'green', 'magenta', 'lime', 'gold', 'sienna', 'navy', 'purple', 'teal', 'cyan', 'tomato', 'yellowgreen', 'khaki', 'crimson', 'chocolate', 'wheat', 'silver']
bulan_labels = ['Jan', 'Feb', 'Mar', 'Apr', 'Mei', 'Juni', 'Juli', 'Ags', 'Sep', 'Okt', 'Nov', 'Des']

for i, data in enumerate([df0, df1, df2]):
    x = data.groupby('Bulan').sum()
    fig, ax = plt.subplots()
    x.plot.bar(color=colors, ax=ax)
    ax.set_xticks(range(12))
    ax.set_xticklabels(bulan_labels, rotation=40)
    ax.set_ylabel('Jumlah')
    ax.set_title(f'Jumlah Penjualan Bulanan di Cluster {i+1}')
    st.pyplot(fig)

# Plot jumlah total penjualan untuk semua produk per cluster
all_sales = df3.groupby('Cluster').sum()
all_sales_transpose = all_sales.transpose()
fig, ax = plt.subplots()
all_sales_transpose.sum().plot.bar(color=colors, ax=ax)
ax.set_ylabel("Jumlah")
ax.set_title("Jumlah Total Penjualan per Cluster")
st.pyplot(fig)

# Plot rata-rata penjualan untuk setiap cluster
fig, ax = plt.subplots()
all_sales_transpose.mean().plot.bar(color=colors, ax=ax)
ax.set_ylabel("Rata-rata")
ax.set_title("Rata-rata Jumlah Penjualan per Cluster")
st.pyplot(fig)

# Plot distribusi penjualan dengan boxplot per cluster
st.subheader("Distribusi Penjualan per Cluster")
fig, ax = plt.subplots()
sns.boxplot(data=all_sales_transpose, ax=ax)
ax.set_ylabel("Jumlah")
ax.set_xlabel("Cluster")
ax.set_title("Boxplot Jumlah Penjualan per Cluster")
st.pyplot(fig)
