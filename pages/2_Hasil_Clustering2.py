import streamlit as st
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
import matplotlib.pyplot as plt
from yellowbrick.cluster import SilhouetteVisualizer
from sklearn import preprocessing
import seaborn as sns
import pandas as pd
from pathlib import Path

st.set_page_config(
    page_title="Streamlit Clustering Analysis",
)

# Membaca data
if "data_baru" in st.session_state:
    df = st.session_state["data_baru"]
    st.info("Menggunakan data baru")
else:
    file_path = Path(__file__).parent / "Data_Toko_Helm.xlsx"
    df = pd.read_excel(file_path)

st.title("Hasil Analisis Clustering Penjualan Toko Helm Kartini")

# Data preprocessing
df2 = df.drop(['Tanggal', 'Bulan', 'Tahun', 'Pendapatan', 'Jumlah', 'Lainnya'], axis=1)
df2 = df2.T
df2_norm = preprocessing.normalize(df2)
df2_norm = pd.DataFrame(df2_norm)

# Menjalankan K-Means Clustering
kmeans = KMeans(n_clusters=3, random_state=42)
kmeans.fit(df2_norm)

# Menambahkan label cluster
df3 = df2.copy()
df3['Cluster'] = kmeans.labels_

# Memisahkan data berdasarkan cluster
clusters = {}
for i in range(3):
    clusters[i] = df[df3['Cluster'] == i]

# Plot jumlah penjualan per bulan untuk setiap cluster
st.subheader("Plot Jumlah Penjualan Bulanan per Cluster")
colors = ['orange', 'blue', 'red']
bulan_labels = ['Jan', 'Feb', 'Mar', 'Apr', 'Mei', 'Juni', 'Juli', 'Ags', 'Sep', 'Okt', 'Nov', 'Des']

for i, cluster_data in clusters.items():
    x = cluster_data.groupby('Bulan').sum()
    fig, ax = plt.subplots()
    x.plot.bar(color=colors, ax=ax)
    ax.set_xticks(range(12))
    ax.set_xticklabels(bulan_labels, rotation=40)
    ax.set_ylabel('Jumlah')
    ax.set_title(f'Jumlah Penjualan Bulanan di Cluster {i + 1}')
    st.pyplot(fig)

    st.write(f"**Analisis Cluster {i + 1}:**")
    st.write(
        f"- Cluster {i + 1} menunjukkan pola penjualan unik di beberapa bulan tertentu. "
        f"Bulan dengan penjualan tertinggi adalah {bulan_labels[x['Jumlah'].idxmax() - 1]}."
    )

# Total dan rata-rata penjualan per cluster
st.subheader("Jumlah Total dan Rata-Rata Penjualan per Cluster")
total_sales = df3.groupby('Cluster').sum().sum(axis=1)
avg_sales = df3.groupby('Cluster').mean().mean(axis=1)

# Total sales
fig, ax = plt.subplots()
total_sales.plot.bar(color=colors, ax=ax)
ax.set_ylabel("Jumlah")
ax.set_title("Jumlah Total Penjualan per Cluster")
st.pyplot(fig)
st.write(
    "Jumlah total penjualan memberikan gambaran kontribusi penjualan setiap cluster terhadap total keseluruhan."
)

# Average sales
fig, ax = plt.subplots()
avg_sales.plot.bar(color=colors, ax=ax)
ax.set_ylabel("Rata-rata")
ax.set_title("Rata-rata Jumlah Penjualan per Cluster")
st.pyplot(fig)
st.write(
    "Rata-rata penjualan menunjukkan bahwa beberapa cluster memiliki variasi besar dalam penjualan bulanannya."
)

# Silhouette Score dan Visualisasi
st.subheader("Silhouette Score")
fig, ax = plt.subplots()
visualizer = SilhouetteVisualizer(kmeans, colors='yellowbrick', ax=ax)
visualizer.fit(df2_norm)
st.pyplot(fig)

score = silhouette_score(df2_norm, kmeans.labels_)
st.write(
    f"**Silhouette Score: {score:.4f}**. "
    "Nilai ini menunjukkan seberapa baik cluster yang terbentuk. "
    "Semakin mendekati 1, semakin baik pemisahan antar cluster."
)

# Boxplot distribusi penjualan
st.subheader("Distribusi Penjualan per Cluster")
fig, ax = plt.subplots()
sns.boxplot(data=df3.iloc[:, :-1], ax=ax)
ax.set_ylabel("Jumlah")
ax.set_xlabel("Cluster")
ax.set_title("Boxplot Jumlah Penjualan per Cluster")
st.pyplot(fig)
st.write(
    "Distribusi penjualan menunjukkan bagaimana data tersebar di setiap cluster. "
    "Outlier dapat membantu mengidentifikasi pola penjualan yang tidak biasa."
)
