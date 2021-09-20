import os.path as op
import mne
from mne.datasets import fetch_fsaverage
import matplotlib.pyplot as plt

raw=mne.io.read_raw_fif(r'C:\Users\tjqn1\PycharmProjects\PyPy\ADHD\ADHD_1.fif',preload=True)

fs_dir = fetch_fsaverage(verbose=True)
subjects_dir = op.dirname(fs_dir)
subject = mne.datasets.fetch_infant_template('6mo', subjects_dir, verbose=True)


bem_dir = op.join(subjects_dir, subject, 'bem')
fname_src = op.join(bem_dir, f'{subject}-oct-6-src.fif')
src = mne.read_source_spaces(fname_src)

fname_bem = op.join(bem_dir, f'{subject}-5120-5120-5120-bem-sol.fif')
bem = mne.read_bem_solution(fname_bem)

fname_1020 = op.join(subjects_dir, subject, 'montages', '10-20-montage.fif')
mon = mne.channels.read_dig_fif(fname_1020)
mon.rename_channels(
    {f'EEG{ii:03d}': ch_name for ii, ch_name in enumerate(raw.ch_names, 1)})
trans = mne.channels.compute_native_head_t(mon)
raw.set_montage(mon)
raw.plot_sensors(sphere=1,show_names=True,title='Channel Topomap')
plt.show()

fig = plt.figure()
fig = mne.viz.create_3d_figure(size=(800, 600), bgcolor='white',)
fig = mne.viz.plot_alignment(
    raw.info, subject=subject, subjects_dir=subjects_dir, trans=trans,
    src=src, bem=bem, coord_frame='mri', mri_fiducials=True, show_axes=True,
    surfaces=('white', 'outer_skin', 'inner_skull', 'outer_skull'),eeg=['projected'],fig=fig)
mne.viz.set_3d_view(figure=fig, azimuth=90, elevation=90, distance=0.5,
                    focalpoint=(0., -0.01, 0.02))
