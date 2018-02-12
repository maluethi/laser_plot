from larana.lar_utils import read_tracks, read_laser, disassemble_laser, disassemble_track, make_figure, plot_track, \
    plot_edges
import numpy as np

import matplotlib.pyplot as plt

run = 7267

base_dir = '/home/matthias/workspace/larana/projects/out/'
tracks_filename = "laser-tracks-{}.npy".format(run)
laser_filename = "laser-data-{}.npy".format(run)

tracks = np.load(base_dir + tracks_filename, encoding = 'latin1')
lasers = np.load(base_dir + laser_filename, encoding = 'latin1')


# loop over all tracks in the file
for laser, track in zip(lasers, tracks):
    fig, ax = make_figure()
    lasr_entry, lasr_exit, dir, _, evt = disassemble_laser(laser)

    print(lasr_entry, lasr_exit)

    track_points, evt = disassemble_track(track)
    plot_track(track_points.x, track_points.y, track_points.z, ax, linestyle="", marker="o")

    plot_edges(ax, lasr_entry.tolist(), lasr_exit.tolist(), color='black', alpha=0.4)

    ax[0].set_title("Event {}".format(evt))
    plt.show()