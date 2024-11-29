import streamlit as st
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
import matplotlib.pyplot as plt
from yellowbrick.cluster import SilhouetteVisualizer
from sklearn import preprocessing
import seaborn as sns
import pandas as pd
from pathlib import Path

# Konfigurasi halaman
st.set_page_config(
    page_title="Analisis Clustering",
    layout="wide"
)

# Membaca data
if "data_baru" in st.session_state:
    df = st.session_state["data_baru"]
    st.info("Menggunakan data baru.")
else:
    file_path = Path(__file__).parent / "Data_Toko_Helm.xlsx"
    df = pd.read_excel(file_path)

# Menampilkan judul
st.title("Hasil Analisis Clustering Data Penjualan")

# Dropdown untuk memilih cluster
if st.button("Kembali"):
    st.switch_page("pages/1_Data.py")

# Proses Data
df2 = df.drop(['Tanggal', 'Bulan', 'Tahun', 'Pendapatan', 'Jumlah', 'Lainnya'], axis=1).T
df2_norm = pd.DataFrame(preprocessing.normalize(df2))

# Menjalankan K-Means Clustering
kmeans = KMeans(n_clusters=3, random_state=42)
kmeans.fit(df2_norm)
df2['Cluster'] = kmeans.labels_

# Membagi data berdasarkan cluster
clusters = [df2[df2['Cluster'] == i] for i in range(3)]

# Menampilkan visualisasi dan analisis
st.header("Visualisasi dan Analisis")

## Pola Penjualan Bulanan per Cluster
st.subheader("Pola Penjualan Bulanan per Cluster")
colors = ['orange', 'blue', 'red']
bulan_labels = ['Jan', 'Feb', 'Mar', 'Apr', 'Mei', 'Juni', 'Juli', 'Ags', 'Sep', 'Okt', 'Nov', 'Des']

for i, cluster_data in enumerate(clusters):
    fig, ax = plt.subplots()
    cluster_data.groupby('Bulan').sum().plot.bar(color=colors[i % len(colors)], ax=ax)
    ax.set_xticks(range(12))
    ax.set_xticklabels(bulan_labels, rotation=40)
    ax.set_ylabel('Jumlah')
    ax.set_title(f'Jumlah Penjualan Bulanan di Cluster {i}')
    st.pyplot(fig)

st.write("**Interpretasi:** Pola penjualan bulanan ini menunjukkan tren penjualan setiap cluster, membantu mengidentifikasi periode dengan penjualan tinggi.")

## Jumlah Total dan Rata-rata Penjualan per Cluster
st.subheader("Jumlah Total dan Rata-rata Penjualan per Cluster")
cluster_totals = df2.groupby('Cluster').sum().sum(axis=1)
cluster_means = df2.groupby('Cluster').mean().mean(axis=1)

fig, ax = plt.subplots(1, 2, figsize=(15, 5))
cluster_totals.plot.bar(color=colors, ax=ax[0])
ax[0].set_title("Jumlah Total Penjualan per Cluster")
ax[0].set_ylabel("Jumlah")

cluster_means.plot.bar(color=colors, ax=ax[1])
ax[1].set_title("Rata-rata Penjualan per Cluster")
ax[1].set_ylabel("Rata-rata")

st.pyplot(fig)

st.write("**Interpretasi:** Penjualan total dan rata-rata memberikan informasi tentang kontribusi setiap cluster terhadap keseluruhan penjualan.")

## Silhouette Score
st.subheader("Silhouette Score")
fig, ax = plt.subplots()
visualizer = SilhouetteVisualizer(kmeans, ax=ax, colors='yellowbrick')
visualizer.fit(df2_norm)
st.pyplot(fig)

sil_score = silhouette_score(df2_norm, kmeans.labels_)
st.write(f"Silhouette Score: **{sil_score:.4f}**")
st.write("**Interpretasi:** Skor Silhouette menunjukkan kualitas pengelompokan, dengan nilai mendekati 1 mengindikasikan clustering yang baik.")

## Distribusi Penjualan dengan Boxplot
st.subheader("Distribusi Penjualan per Cluster")
fig, ax = plt.subplots()
sns.boxplot(data=df2.drop('Cluster', axis=1).transpose(), ax=ax)
ax.set_ylabel("Jumlah")
ax.set_xlabel("Cluster")
ax.set_title("Boxplot Jumlah Penjualan per Cluster")
st.pyplot(fig)

st.write("**Interpretasi:** Boxplot memberikan informasi tentang penyebaran dan outlier dalam penjualan di setiap cluster.")
