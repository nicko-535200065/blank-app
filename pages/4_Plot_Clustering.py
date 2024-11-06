from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
import matplotlib.pyplot as plt
from yellowbrick.cluster import SilhouetteVisualizer
from yellowbrick.datasets import load_nfl
import seaborn as sns
from sklearn import preprocessing

import pandas as pd

# Baca file Excel
#file_path = '/content/drive/My Drive/BigData/Students/Data.xlsx'
file_path = '/content/drive/My Drive/BigData/Students/Data_Toko_Helm.xlsx'
df = pd.read_excel(file_path)

df.head()


df2 = df.drop(['Tanggal','Bulan','Tahun', 'Pendapatan','Jumlah','Lainnya'], axis = 1)
df2.head()

#Transpose
df2 = df2.T
df2

#Normalisasi
df2_norm = preprocessing.normalize(df2)
df2_norm = pd.DataFrame(df2_norm)


# Menjalankan K-Means Clustering
kmeans = KMeans(n_clusters=3, random_state=42)
kmeans.fit(df2_norm)

visualizer = SilhouetteVisualizer(kmeans, colors='yellowbrick')

visualizer.fit(df2_norm)
visualizer.show()

score = silhouette_score(df2_norm, kmeans.labels_)
print(f'\nSilhouette Score: {score:.4f}')

df3 = df2
df3['Cluster'] = kmeans.labels_
df3

produk_cluster0 = df3[df3['Cluster'] == 0]
produk_cluster1 = df3[df3['Cluster'] == 1]
produk_cluster2 = df3[df3['Cluster'] == 2]

#Mencari index setiap cluster
idx_0 = produk_cluster0.index
idx_1 = produk_cluster1.index
idx_2 = produk_cluster2.index

df0 = df[idx_0]
df1 = df[idx_1]
df2 = df[idx_2]

#Data di cluster 0
df0['Bulan'] = df['Bulan']
#df0['Tahun'] = df['Tahun']

#Data di cluster 1
df1['Bulan'] = df['Bulan']
#df1['Tahun'] = df['Tahun']

#Data di cluster 2
df2['Bulan'] = df['Bulan']
#df2['Tahun'] = df['Tahun']

colors = ['orange','blue','red','green','magenta','lime','gold','sienna','navy','purple','teal','cyan','tomato','yellowgreen','khaki','crimson','chocolate','wheat', 'silver']

x0 = df0.groupby('Bulan').sum()
x0.plot.bar(color=colors)
plt.xticks([0,1,2,3,4,5,6,7,8,9,10,11], ['Jan', 'Feb', 'Mar','Ap','Mei','Juni','Juli','Ags','Sep','Okt','Nov','Des'],
       rotation=40)
plt.ylabel('Jumlah')
plt.title('Jumlah Penjualan Bulanan di Cluster 1')

x1 = df1.groupby('Bulan').sum()
x1.plot.bar(color=colors)
plt.xticks([0,1,2,3,4,5,6,7,8,9,10,11], ['Jan', 'Feb', 'Mar','Ap','Mei','Juni','Juli','Ags','Sep','Okt','Nov','Des'],
       rotation=40)
plt.ylabel('Jumlah')
plt.title('Jumlah Penjualan Bulanan di Cluster 2')

x2 = df2.groupby('Bulan').sum()
x2.plot.bar(color=colors)
plt.xticks([0,1,2,3,4,5,6,7,8,9,10,11], ['Jan', 'Feb', 'Mar','Ap','Mei','Juni','Juli','Ags','Sep','Okt','Nov','Des'],
       rotation=40)
plt.ylabel('Jumlah')
plt.title('Jumlah Penjualan Bulanan di Cluster 3')

all = df3.groupby('Cluster').sum()
all

A = all.transpose().sum()
A.plot.bar(color=colors)
plt.ylabel('Jumlah')
plt.title('Jumlah Total Penjualan')

A = all.transpose().mean()
A.plot.bar(color=colors)
plt.ylabel('Rata-Rata')
plt.title('Rata-Rata Jumlah Penjualan')

A = all.transpose()
sns.boxplot(data = A)
plt.ylabel('Jumlah')
plt.xlabel('Cluster')
plt.title('Jumlah Penjualan')
