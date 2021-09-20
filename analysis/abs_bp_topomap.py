import pandas as pd
import os
import numpy as np
import matplotlib.pyplot as plt
import yasa
from sklearn.decomposition import PCA

bp_adhd = []
bp_control = []
for i in range(19):
    b = []
    for j in os.listdir(f'./bp_spare_corr/ADHD/{i}'):
        b.append(pd.read_csv(f'./bp_spare_corr/ADHD/{i}/' + j, index_col='Chan').loc[:, :'TotalAbsPow'].to_numpy())
    bp_adhd.append(b)

for i in range(19):
    b = []
    for j in os.listdir(f'./bp_spare_corr/Control/{i}'):
        b.append(pd.read_csv(f'./bp_spare_corr/Control/{i}/' + j, index_col='Chan').loc[:, :'TotalAbsPow'].to_numpy())
    bp_control.append(b)

adhd_data = np.array(bp_adhd).transpose(1, 0, 2, 3)
control_data = np.array(bp_control).transpose(1, 0, 2, 3)
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



fig = plt.figure(num=None, figsize=(8, 5))
delta=pd.Series(dict(zip(ch_names,pca_compression(adhd_data)[:,7])))
a=yasa.topoplot(delta,title='ADHD',vmax=150,vmin=80,fig=fig, subplot=(1, 2, 1),cbar_title='Abs BandPower')
delta=pd.Series(dict(zip(ch_names,pca_compression(control_data)[:,7])))
yasa.topoplot(delta,title='Control',vmax=150,vmin=80, fig=fig, subplot=(1, 2, 2),cbar_title='Abs BandPower')
plt.suptitle('Total BandPower',fontsize=20)
plt.show()
