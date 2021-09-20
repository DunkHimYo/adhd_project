from sklearn.decomposition import PCA
from mne.viz import plot_connectivity_circle
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import os
import numpy as np

psd_adhd = []
psd_control = []
for i in range(19):
    b = []
    for j in os.listdir(f'./psd_spare_corr4/ADHD/{i}'):
        b.append(pd.read_csv(f'./psd_spare_corr4/ADHD/{i}/' + j, index_col='Unnamed: 0').to_numpy())
    psd_adhd.append(b)

for i in range(19):
    b = []
    for j in os.listdir(f'./psd_spare_corr4/Control/{i}'):
        b.append(pd.read_csv(f'./psd_spare_corr4/Control/{i}/' + j, index_col='Unnamed: 0').to_numpy())
    psd_control.append(b)

adhd_data = np.array(psd_adhd).transpose(1, 0, 2, 3)
control_data = np.array(psd_control).transpose(1, 0, 2, 3)
x = np.append(adhd_data, control_data, axis=0)
y = np.array([1] * 61 + [0] * 60)
ch_names=['Fp1','Fp2','F3','F4','C3','C4','P3','P4','O1','O2','F7','F8','T7','T8','P7','P8','Fz','Cz','Pz']

def pca_compression(data):
    shape = data.shape

    pca = PCA(n_components=1)
    X3 = data.reshape(-1, shape[-1] * shape[-2])

    W3 = pca.fit_transform(X3)
    face_mean = pca.mean_.reshape(shape[-2], shape[-1])
    face_p1 = pca.components_[0].reshape(shape[-2], shape[-1])

    return face_mean + face_p1


fig = plt.figure(num=None, figsize=(8, 4))
figure,axis=plot_connectivity_circle(pca_compression(adhd_data),node_names=ch_names,title='Freqs Domain Corr ADHD',n_lines=30,vmin=0.2,vmax=0.8, fig=fig,subplot=(1, 2,1),colorbar_size=0.3,colormap=sns.color_palette("coolwarm", as_cmap=True),textcolor='black',facecolor='white',node_edgecolor='white')
figure,axis=plot_connectivity_circle(pca_compression(control_data),node_names=ch_names, title='Freqs Domain Corr Control',n_lines=30,vmin=0.2,vmax=0.8,fig=fig,subplot=(1, 2,2),colorbar_size=0.3,colormap=sns.color_palette("coolwarm", as_cmap=True),textcolor='black',facecolor='white',node_edgecolor='white')
plt.show()
