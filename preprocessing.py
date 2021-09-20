import mne
from meegkit import star
import numpy as np
from meegkit.asr import ASR
from meegkit.utils.matrix import sliding_window
import os
import pandas as pd
from bp import bandpower
from scipy.signal import welch

ch = ['F3', 'F4', 'O1', 'O2', 'F7', 'F8', 'T7', 'T8', 'P7', 'P8']
info = mne.create_info(ch_names=ch, sfreq=128, ch_types=['eeg'] * len(ch))


def preprocessing(sfreq=128):
    file = os.listdir((rf".\eeg_record\raw_eeg"))
    name = [i for i in file if i.endswith('.csv')][-1]
    raw = pd.read_csv(rf".\eeg_record\raw_eeg\{name}")[ch]
    info = mne.create_info(ch_names=ch, sfreq=128, ch_types=['eeg'] * len(ch))
    data = mne.evoked.detrend(raw.T)
    data = mne.filter.notch_filter(x=data, Fs=128, freqs=[50, 55.8], verbose=False)
    x = data.T
    y, w, _ = star.star(x, 2, verbose=False)
    y /= 1e6

    raw = y.T
    asr = ASR(method='euclid')

    train_idx = np.arange(0 * sfreq, 10 * sfreq, dtype=int)
    _, sample_mask = asr.fit(raw[:, train_idx])
    X = sliding_window(raw, window=int(sfreq), step=int(sfreq))
    Y = np.zeros_like(X)
    for i in range(X.shape[1]):
        Y[:, i, :] = asr.transform(X[:, i, :])

    clean = Y.reshape(len(ch), -1)
    raw3 = mne.io.RawArray(clean, info, verbose=False)
    raw3.save(rf'.\eeg_record\clear_eeg\clear_{name[:-3]}fif', overwrite=True)
    va = np.linspace(0, len(raw3) - 1, 20)

    for j in range(19):
        try:
            os.makedirs(f'./bandPower/{j}/')
            os.makedirs(f'./channel_correlation/{j}/')
            os.makedirs(f'./psd_correlation/{j}/')
        except:
            while len(os.listdir(f'./bandPower/{j}/')) > 10:
                os.remove(f'./bandPower/{j}/' + os.listdir(f'./bandPower/{j}/')[0])

            while len(os.listdir(f'./channel_correlation/{j}/')) > 10:
                os.remove(f'./channel_correlation/{j}/' + os.listdir(f'./channel_correlation/{j}/')[0])

            while len(os.listdir(f'./psd_correlation/{j}/')) > 10:
                os.remove(f'./psd_correlation/{j}/' + os.listdir(f'./psd_correlation/{j}/')[0])

        win = 4 * 128
        freqs, psd = welch(raw3._data[:, int(va[j]):int(va[j + 1])] * 1e6, 128, nperseg=win)
        pd.DataFrame(psd.T, columns=raw3.ch_names).corr(method='pearson').to_csv(
            rf'.\psd_correlation\{j}\{name[:-3]}csv')

        pd.DataFrame((raw3._data[:, int(va[j]):int(va[j + 1])] * 1e6).T, columns=raw3.ch_names)[ch].corr(
            method='pearson').to_csv(rf'.\channel_correlation\{j}\{name[:-3]}csv')

        bandpower(raw3._data[:, int(va[j]):int(va[j + 1])] * 1e6, sf=raw3.info['sfreq'], ch_names=raw3.ch_names,
                  relative=False).loc[ch, :'TotalAbsPow'].to_csv(rf'.\bandPower\{j}\{name[:-3]}csv')


if __name__ == '__main__':
    preprocessing()
