import streamlit as st
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
import matplotlib.pyplot as plt
from yellowbrick.cluster import SilhouetteVisualizer
from yellowbrick.datasets import load_nfl
import seaborn as sns
from sklearn import preprocessing
import numpy as np
import pandas as pd
from pathlib import Path


st.set_page_config(
    page_title="Streamlit",
#    page_icon="",
)


# Baca file Excel
#file_path = '/content/drive/My Drive/BigData/Students/Data.xlsx'
file_path = Path(__file__).parent / "Data_Toko_Helm.xlsx"
df = pd.read_excel(file_path)
#df.head()

st.header("Plot")
n_clusters = st.slider("Pilih jumlah cluster:", 2, 10, 3)


df2 = df.drop(['Tanggal','Bulan','Tahun', 'Pendapatan','Jumlah','Lainnya'], axis = 1)
#df2.head()

#Transpose
df2 = df2.T
#df2

#Normalisasi
df2_norm = preprocessing.normalize(df2)
df2_norm = pd.DataFrame(df2_norm)


# Menjalankan K-Means Clustering
kmeans = KMeans(n_clusters=3, random_state=42)
kmeans.fit(df2_norm)


#Menjalankan Plot Silhouette
st.subheader("Silhouette Score")
fig, ax = plt.subplots()
visualizer = SilhouetteVisualizer(kmeans, colors='yellowbrick')
visualizer.fit(df2_norm)
visualizer.show()
st.pyplot(fig)


score = silhouette_score(df2_norm, kmeans.labels_)
st.write(f'\nSilhouette Score: {score:.4f}')

df3 = df2
df3['Cluster'] = kmeans.labels_
#df3





# Membuat dictionary untuk menyimpan DataFrame per cluster
produk_clusters = {}
dfs = {}

# Loop untuk membagi data berdasarkan cluster dan menyimpannya dalam dictionary
for i in range(n_clusters):
    # Memisahkan data untuk setiap cluster dari `df3`
    produk_clusters[f'produk_cluster{i}'] = df3[df3['Cluster'] == i]
    # Mengambil subset data dari `df` menggunakan indeks dari produk_clusters
    dfs[f'df{i}'] = df.iloc[produk_clusters[f'produk_cluster{i}'].index]

    # Menambahkan kolom 'Bulan' (dan 'Tahun' jika diperlukan) ke setiap DataFrame cluster
    dfs[f'df{i}']['Bulan'] = df['Bulan'].values
    # dfs[f'df{i}']['Tahun'] = df['Tahun'].values  # Uncomment jika ingin menambahkan kolom 'Tahun'

# Plot jumlah penjualan per bulan untuk setiap cluster
st.subheader("Plot Jumlah Penjualan Bulanan per Cluster")
colors = ['orange', 'blue', 'red', 'green', 'magenta', 'lime', 'gold', 'sienna', 'navy', 'purple', 
          'teal', 'cyan', 'tomato', 'yellowgreen', 'khaki', 'crimson', 'chocolate', 'wheat', 'silver']
bulan_labels = ['Jan', 'Feb', 'Mar', 'Apr', 'Mei', 'Juni', 'Juli', 'Ags', 'Sep', 'Okt', 'Nov', 'Des']

# Loop untuk plotting data dari setiap cluster
for i in range(n_clusters):
    data = dfs[f'df{i}']
    x = data.groupby('Bulan').sum()

    fig, ax = plt.subplots()
    x.plot.bar(color=colors[:len(x)], ax=ax)  # Mengatur warna sesuai jumlah data
    ax.set_xticks(range(12))
    ax.set_xticklabels(bulan_labels, rotation=40)
    ax.set_ylabel('Jumlah')
    ax.set_title(f'Jumlah Penjualan Bulanan di Cluster {i+1}')
    st.pyplot(fig)

#colors = ['orange','blue','red','green','magenta','lime','gold','sienna','navy','purple','teal','cyan','tomato','yellowgreen','khaki','crimson','chocolate','wheat', 'silver']

#x0 = df0.groupby('Bulan').sum()
#x0.plot.bar(color=colors)
#plt.xticks([0,1,2,3,4,5,6,7,8,9,10,11], ['Jan', 'Feb', 'Mar','Ap','Mei','Juni','Juli','Ags','Sep','Okt','Nov','Des'],
#       rotation=40)
#plt.ylabel('Jumlah')
#plt.title('Jumlah Penjualan Bulanan di Cluster 1')

#x1 = df1.groupby('Bulan').sum()
#x1.plot.bar(color=colors)
#plt.xticks([0,1,2,3,4,5,6,7,8,9,10,11], ['Jan', 'Feb', 'Mar','Ap','Mei','Juni','Juli','Ags','Sep','Okt','Nov','Des'],
#       rotation=40)
#plt.ylabel('Jumlah')
#plt.title('Jumlah Penjualan Bulanan di Cluster 2')

#x2 = df2.groupby('Bulan').sum()
#x2.plot.bar(color=colors)
#plt.xticks([0,1,2,3,4,5,6,7,8,9,10,11], ['Jan', 'Feb', 'Mar','Ap','Mei','Juni','Juli','Ags','Sep','Okt','Nov','Des'],
#       rotation=40)
#plt.ylabel('Jumlah')
#plt.title('Jumlah Penjualan Bulanan di Cluster 3')

#Jumlah total dan rata-rata per cluster
all = df3.groupby('Cluster').sum()
#all

A = all.transpose().sum()
#A.plot.bar(color=colors)
plt.ylabel('Jumlah')
plt.title('Jumlah Total Penjualan')


# Plot jumlah total penjualan untuk semua produk per cluster
st.subheader("Jumlah Total dan Rata-Rata Penjualan per Cluster")
#all_sales = df3.groupby('Cluster').sum()
#all_sales_transpose = all_sales.transpose()
fig, ax = plt.subplots()
A.plot.bar(color=colors, ax=ax)
ax.set_ylabel("Jumlah")
ax.set_title("Jumlah Total Penjualan per Cluster")
st.pyplot(fig)

# Plot rata-rata
A = all.transpose().mean()
#A.plot.bar(color=colors)
plt.ylabel('Rata-Rata')
plt.title('Rata-Rata Jumlah Penjualan')

# Plot rata-rata penjualan untuk setiap cluster
fig, ax = plt.subplots()
A.plot.bar(color=colors, ax=ax)
ax.set_ylabel("Rata-rata")
ax.set_title("Rata-rata Jumlah Penjualan per Cluster")
st.pyplot(fig)

#Boxplot
A = all.transpose()
#sns.boxplot(data = A)
plt.ylabel('Jumlah')
plt.xlabel('Cluster')
plt.title('Jumlah Penjualan')

# Plot distribusi penjualan dengan boxplot per cluster
st.subheader("Distribusi Penjualan per Cluster")
fig, ax = plt.subplots()
sns.boxplot(data=A, ax=ax)
ax.set_ylabel("Jumlah")
ax.set_xlabel("Cluster")
ax.set_title("Boxplot Jumlah Penjualan per Cluster")
st.pyplot(fig)