import streamlit as st
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
import matplotlib.pyplot as plt
from yellowbrick.cluster import SilhouetteVisualizer
import seaborn as sns
from sklearn import preprocessing
import pandas as pd
from pathlib import Path

st.set_page_config(
    page_title="Analisis Penjualan Toko Helm",
)

# Load Data
if "data_baru" in st.session_state:
    df = st.session_state["data_baru"]
    st.info("Menggunakan data baru")
else:        
    file_path = Path(__file__).parent / "Data_Toko_Helm.xlsx"
    df = pd.read_excel(file_path)

"""
# Analisis Penjualan Toko Helm
Analisis clustering pada pola penjualan produk toko helm berdasarkan data penjualan.
"""

# Kembali ke halaman utama
if st.button("Kembali"):
    st.switch_page("pages/1_Data.py")

# Preprocessing Data
df2 = df.drop(['Tanggal', 'Bulan', 'Tahun', 'Pendapatan', 'Jumlah', 'Lainnya'], axis=1).T
df2_norm = preprocessing.normalize(df2)
df2_norm = pd.DataFrame(df2_norm)

# K-Means Clustering
kmeans = KMeans(n_clusters=3, random_state=42)
kmeans.fit(df2_norm)

df3 = df2
df3['Cluster'] = kmeans.labels_

# Menampilkan hasil visualisasi
produk_clusters = [df3[df3['Cluster'] == i] for i in range(3)]
bulan_labels = ['Jan', 'Feb', 'Mar', 'Apr', 'Mei', 'Juni', 'Juli', 'Ags', 'Sep', 'Okt', 'Nov', 'Des']
colors = ['orange', 'blue', 'red']

### Visualisasi Pola Penjualan Bulanan
st.subheader("Pola Penjualan Bulanan per Cluster")
st.markdown("""
**Interpretasi**:  
Grafik berikut menunjukkan distribusi penjualan produk di setiap cluster berdasarkan bulan.  
- Perhatikan pola naik-turunnya penjualan tiap bulan untuk masing-masing cluster.  
- Kegunaannya: membantu memahami musim penjualan atau bulan dengan permintaan tinggi pada masing-masing cluster.
""")
for i, cluster_data in enumerate(produk_clusters):
    x = df.iloc[cluster_data.index].groupby('Bulan').sum()
    fig, ax = plt.subplots()
    x.plot.bar(color=colors[i], ax=ax)
    ax.set_xticks(range(12))
    ax.set_xticklabels(bulan_labels, rotation=40)
    ax.set_ylabel('Jumlah Penjualan')
    ax.set_title(f'Cluster {i+1}')
    st.pyplot(fig)

### Total dan Rata-Rata Penjualan per Cluster
st.subheader("Jumlah Total dan Rata-Rata Penjualan")
all_sales = df3.groupby('Cluster').sum().transpose()

# Total Penjualan
st.markdown("""
**Interpretasi**:  
Grafik berikut menunjukkan jumlah total penjualan untuk masing-masing cluster:  
- Cluster dengan total penjualan tertinggi menunjukkan kategori produk yang mendominasi.  
""")
fig, ax = plt.subplots()
all_sales.sum().plot.bar(color=colors, ax=ax)
ax.set_ylabel("Jumlah Penjualan")
ax.set_title("Total Penjualan per Cluster")
st.pyplot(fig)

# Rata-Rata Penjualan
st.markdown("""
**Interpretasi**:  
Grafik berikut menunjukkan rata-rata jumlah penjualan di setiap cluster:  
- Berguna untuk membandingkan performa rata-rata tiap cluster.  
""")
fig, ax = plt.subplots()
all_sales.mean().plot.bar(color=colors, ax=ax)
ax.set_ylabel("Rata-rata Penjualan")
ax.set_title("Rata-rata Penjualan per Cluster")
st.pyplot(fig)

### Skor Silhouette
st.subheader("Silhouette Score dan Visualisasi")
st.markdown("""
**Interpretasi**:  
Silhouette Score digunakan untuk mengevaluasi seberapa baik setiap data cocok dengan cluster-nya masing-masing.  
- Nilai lebih mendekati 1 menunjukkan cluster yang lebih baik.  
""")
fig, ax = plt.subplots()
visualizer = SilhouetteVisualizer(kmeans, colors='yellowbrick', ax=ax)
visualizer.fit(df2_norm)
st.pyplot(fig)

silhouette_avg = silhouette_score(df2_norm, kmeans.labels_)
st.markdown(f"**Silhouette Score: {silhouette_avg:.4f}**")

### Distribusi Penjualan (Boxplot)
st.subheader("Distribusi Penjualan per Cluster")
st.markdown("""
**Interpretasi**:  
Boxplot menunjukkan sebaran data penjualan di setiap cluster:  
- Identifikasi outlier dan distribusi nilai penjualan per cluster.  
""")
fig, ax = plt.subplots()
sns.boxplot(data=all_sales, ax=ax)
ax.set_ylabel("Jumlah Penjualan")
ax.set_xlabel("Cluster")
ax.set_title("Boxplot Penjualan per Cluster")
st.pyplot(fig)
