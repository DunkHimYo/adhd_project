from tensorflow.keras.models import load_model

def feature_data(path=''):
    feature_data = []
    for i in os.listdir(path):
        name = [csv_file for csv_file in os.listdir(f'./{path}/{i}') if csv_file.endswith('.csv')][-1]

        if 'band' in path:
            feature_data.append(
                pd.read_csv(f'./{path}/{i}/' + name, index_col='Chan').loc[:, :'TotalAbsPow'].to_numpy())
        if 'channel_corr' in path:
            feature_data.append(
                pd.read_csv(f'./channel_correlation/{i}/' + name, index_col='Unnamed: 0').to_numpy())
        if 'psd_corr' in path:
            feature_data.append(
                pd.read_csv(f'./psd_correlation/{i}/' + name, index_col='Unnamed: 0').to_numpy())
    print(np.array(feature_data).shape)
    return np.array(feature_data)

def bp_pred(x):
    return load_model(f'./adhd_chking/bp.h5').predict(x)[0]

def corr_pred(x):
    return load_model(f'./adhd_chking/ch_corr.h5').predict(x)[0]

def psd_pred(x):
    return load_model(f'./adhd_chking/psd_corr.h5').predict(x)[0]


if __name__=='__main__':
    import pandas as pd
    import os
    import numpy as np

    c = []
    d = []
    for i in range(19):
        b = []
        for j in os.listdir(rf'C:\Users\tjqn1\PycharmProjects\PyPy\ch_spare_corr\ADHD\{i}'):
            b.append(pd.read_csv(f'./ch_spare_corr/ADHD/{i}/' + j, index_col='Unnamed: 0').to_numpy())
        c.append(b)

    for i in range(19):
        b = []
        for j in os.listdir(rf'C:\Users\tjqn1\PycharmProjects\PyPy\ch_spare_corr\Control\{i}'):
            b.append(pd.read_csv(f'./ch_spare_corr/Control/{i}/' + j, index_col='Unnamed: 0').to_numpy())
        d.append(b)

    q = np.array(c).transpose(1, 0, 2, 3)
    w = np.array(d).transpose(1, 0, 2, 3)

    x = np.append(q, w, axis=0)
    y = np.array([1] * 61 + [0] * 60)