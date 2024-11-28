import streamlit as st
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
import matplotlib.pyplot as plt
from yellowbrick.cluster import SilhouetteVisualizer
from sklearn import preprocessing
import pandas as pd
from pathlib import Path
import seaborn as sns

st.set_page_config(
    page_title="Analisis Clustering Penjualan",
    layout="wide",
)

# Membaca data
if "data_baru" in st.session_state:
    df = st.session_state["data_baru"]
    st.info("Menggunakan data baru.")
else:
    file_path = Path(__file__).parent / "Data_Toko_Helm.xlsx"
    df = pd.read_excel(file_path)

"""
# Hasil Analisis Clustering Penjualan
"""

if st.button("Kembali"):
    st.switch_page("pages/1_Data.py")

# Memproses data
df2 = df.drop(['Tanggal', 'Bulan', 'Tahun', 'Pendapatan', 'Jumlah', 'Lainnya'], axis=1)
df2 = df2.T
df2_norm = preprocessing.normalize(df2)
df2_norm = pd.DataFrame(df2_norm)

# Menjalankan K-Means Clustering
kmeans = KMeans(n_clusters=3, random_state=42)
kmeans.fit(df2_norm)

# Menambahkan label cluster ke data
df3 = df2.copy()
df3['Cluster'] = kmeans.labels_

produk_clusters = [df3[df3['Cluster'] == i] for i in range(3)]
df_by_cluster = [df.iloc[produk.index] for produk in produk_clusters]

# Plot Jumlah Penjualan Bulanan per Cluster
st.subheader("Visualisasi Pola Penjualan Bulanan per Cluster")
st.write("""
Visualisasi ini menunjukkan jumlah penjualan setiap bulan untuk masing-masing cluster. 
Dari grafik, kita dapat membaca pola penjualan dominan pada bulan tertentu dan membandingkan tren antar cluster. 
Kegunaannya adalah untuk mengetahui bulan dengan penjualan terbaik di setiap cluster.
""")
bulan_labels = ['Jan', 'Feb', 'Mar', 'Apr', 'Mei', 'Juni', 'Juli', 'Ags', 'Sep', 'Okt', 'Nov', 'Des']
colors = ['orange', 'blue', 'red']

for i, data in enumerate(df_by_cluster):
    x = data.groupby('Bulan').sum()
    fig, ax = plt.subplots()
    x.plot.bar(color=colors, ax=ax)
    ax.set_xticks(range(12))
    ax.set_xticklabels(bulan_labels, rotation=40)
    ax.set_ylabel('Jumlah')
    ax.set_title(f'Jumlah Penjualan Bulanan di Cluster {i+1}')
    st.pyplot(fig)

# Total dan rata-rata penjualan
all_sales = df3.groupby('Cluster').sum().transpose()
total_sales = all_sales.sum()
average_sales = all_sales.mean()

st.subheader("Jumlah Total Penjualan per Cluster")
st.write("""
Grafik ini menunjukkan total penjualan dari setiap cluster. 
Cluster dengan nilai tertinggi memiliki kontribusi penjualan terbesar. 
Kegunaannya adalah untuk mengetahui cluster mana yang mendominasi penjualan.
""")
fig, ax = plt.subplots()
total_sales.plot.bar(color=colors, ax=ax)
ax.set_ylabel("Jumlah Total")
ax.set_title("Jumlah Total Penjualan per Cluster")
st.pyplot(fig)

st.subheader("Rata-rata Penjualan per Cluster")
st.write("""
Grafik ini menunjukkan rata-rata penjualan untuk setiap cluster. 
Rata-rata membantu memahami performa cluster dibandingkan cluster lain secara konsisten.
""")
fig, ax = plt.subplots()
average_sales.plot.bar(color=colors, ax=ax)
ax.set_ylabel("Rata-rata")
ax.set_title("Rata-rata Penjualan per Cluster")
st.pyplot(fig)

# Silhouette Score dan Visualisasi
st.subheader("Silhouette Score")
st.write("""
Visualisasi ini menunjukkan seberapa baik data di setiap cluster dikelompokkan. 
Nilai mendekati 1 berarti cluster terdefinisi dengan baik. 
Silhouette Score memberikan informasi tentang efektivitas clustering.
""")
fig, ax = plt.subplots()
visualizer = SilhouetteVisualizer(kmeans, colors='yellowbrick', ax=ax)
visualizer.fit(df2_norm)
st.pyplot(fig)

score = silhouette_score(df2_norm, kmeans.labels_)
st.write(f"Silhouette Score: {score:.4f}")

# Distribusi Penjualan (Boxplot)
st.subheader("Distribusi Penjualan per Cluster")
st.write("""
Boxplot menunjukkan distribusi penjualan di setiap cluster. 
Dari sini, dapat dilihat outlier atau penyimpangan data yang signifikan. 
Kegunaannya adalah untuk memahami variabilitas penjualan dalam cluster.
""")
fig, ax = plt.subplots()
sns.boxplot(data=all_sales, ax=ax)
ax.set_ylabel("Jumlah")
ax.set_xlabel("Cluster")
ax.set_title("Boxplot Jumlah Penjualan per Cluster")
st.pyplot(fig)
