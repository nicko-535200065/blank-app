import streamlit as st
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
import matplotlib.pyplot as plt
from yellowbrick.cluster import SilhouetteVisualizer
from sklearn import preprocessing
import seaborn as sns
import pandas as pd
from pathlib import Path

st.set_page_config(page_title="Analisis Clustering Penjualan")

# Membaca data
file_path = Path(__file__).parent / "Data_Toko_Helm.xlsx"
df = pd.read_excel(file_path)

st.title("Hasil Analisis Clustering Penjualan Toko Helm Kartini")

# Data preprocessing
df2 = df.drop(['Tanggal', 'Bulan', 'Tahun', 'Pendapatan', 'Jumlah', 'Lainnya'], axis=1).T
df2_norm = preprocessing.normalize(df2)
df2_norm = pd.DataFrame(df2_norm)

# Menjalankan K-Means Clustering
kmeans = KMeans(n_clusters=3, random_state=42)
kmeans.fit(df2_norm)

# Menambahkan cluster ke data
df3 = df2.copy()
df3['Cluster'] = kmeans.labels_
clusters = {i: df[df3['Cluster'] == i] for i in range(3)}

# Visualisasi: Pola Penjualan Bulanan
st.subheader("1. Pola Penjualan Bulanan per Cluster")
for i, cluster_data in clusters.items():
    x = cluster_data.groupby('Bulan').sum()
    fig, ax = plt.subplots()
    x.plot.bar(ax=ax)
    ax.set_title(f"Pola Penjualan Cluster {i + 1}")
    ax.set_ylabel("Jumlah")
    ax.set_xlabel("Bulan")
    st.pyplot(fig)
    st.write(f"Pola penjualan bulanannya berbeda-beda, dapat digunakan untuk strategi pemasaran spesifik.")

# Visualisasi: Total Penjualan
st.subheader("2. Total Penjualan per Cluster")
total_sales = df3.groupby('Cluster').sum().sum(axis=1)
fig, ax = plt.subplots()
total_sales.plot.bar(ax=ax, color=['orange', 'blue', 'red'])
ax.set_title("Total Penjualan per Cluster")
ax.set_ylabel("Jumlah")
st.pyplot(fig)
st.write("Memberikan gambaran kontribusi masing-masing cluster terhadap total penjualan.")

# Visualisasi: Rata-Rata Penjualan
st.subheader("3. Rata-Rata Penjualan per Cluster")
avg_sales = df3.groupby('Cluster').mean().mean(axis=1)
fig, ax = plt.subplots()
avg_sales.plot.bar(ax=ax, color=['orange', 'blue', 'red'])
ax.set_title("Rata-Rata Penjualan per Cluster")
ax.set_ylabel("Jumlah")
st.pyplot(fig)
st.write("Menunjukkan seberapa stabil penjualan di setiap cluster.")

# Visualisasi: Silhouette Score
st.subheader("4. Silhouette Score")
fig, ax = plt.subplots()
visualizer = SilhouetteVisualizer(kmeans, colors='yellowbrick', ax=ax)
visualizer.fit(df2_norm)
st.pyplot(fig)
score = silhouette_score(df2_norm, kmeans.labels_)
st.write(f"Silhouette Score: {score:.4f}")
st.write("Mengukur kualitas clustering. Semakin mendekati 1, semakin baik pemisahan antar cluster.")

# Visualisasi: Boxplot Distribusi
st.subheader("5. Distribusi Penjualan per Cluster")
fig, ax = plt.subplots()
sns.boxplot(data=df3.iloc[:, :-1], ax=ax)
ax.set_title("Distribusi Penjualan per Cluster")
ax.set_xlabel("Cluster")
ax.set_ylabel("Jumlah")
st.pyplot(fig)
st.write("Distribusi dan outlier pada penjualan membantu mengidentifikasi pola yang tidak biasa.")
