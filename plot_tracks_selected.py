from larana.lar_utils import read_tracks, read_laser, disassemble_laser, disassemble_track, make_figure, plot_track, \
    plot_edges, find_unique_polar_idx
import numpy as np

import matplotlib.pyplot as plt

run = 7252
postfix = '-calib'

modulo = 100

base_dir = '/home/data/uboone/laser/processed/sim/'
tracks_filename = "laser-tracks-2-diff.npy".format(run, postfix)
laser_filename = "laser-data-2-diff.npy".format(run, postfix)

tracks = np.load(base_dir + tracks_filename, encoding = 'latin1')
lasers = np.load(base_dir + laser_filename, encoding = 'latin1')

pol_incs = find_unique_polar_idx(lasers)

# loop over all tracks in the file
fig, ax = make_figure()
for pol_idx in pol_incs:

    for idx, (laser, track) in enumerate(zip(lasers[pol_idx], tracks[pol_idx])):

        lasr_entry, lasr_exit, dir, _, evt = disassemble_laser(laser)

        print(lasr_entry, lasr_exit)
        track_points, evt = disassemble_track(track)
        plot_track(track_points.x, track_points.y, track_points.z, ax, linestyle="", marker="o")

        plot_edges(ax, lasr_entry.tolist(), lasr_exit.tolist(), color='black', alpha=0.4)

        ax[0].set_title("Event {}".format(evt))
        if idx % modulo == 0 and idx != 0:
            plt.show()
            fig, ax = make_figure()

plt.show()