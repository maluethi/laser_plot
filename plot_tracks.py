from larana.lar_utils import read_tracks, read_laser, disassemble_laser, disassemble_track, make_figure, plot_track, \
    plot_edges
import numpy as np

import matplotlib.pyplot as plt

filename = "/home/data/uboone/laser/7267/tracks/roi/Tracks-7267-859-exp.root"
#filename = "/home/data/uboone/laser/sim/Tracks-lcs2-021-nosce.root"
#filename = "~/mnt/lheppc2/maluethi/larsoft/larana/scratch/Tracks-0024-000-nosce.root"

tracks = read_tracks(filename, identifier="Tracks")
lasers = read_laser(filename)

# generate event id lists, since there are more tracks than events
track_event_id = np.array([track[0] for track in tracks])



# loop over all tracks in the file
for laser in lasers:
    fig, ax = make_figure()
    lasr_entry, lasr_exit, dir, _, evt = disassemble_laser(laser)
    track_list = np.where(track_event_id == evt)

    # loop over all tracks in this event
    for track in tracks[track_list]:
        track_points, evt = disassemble_track(track)
        plot_track(track_points.x, track_points.y, track_points.z, ax, linestyle="", marker="o")

    plot_edges(ax, lasr_entry.tolist(), lasr_exit.tolist(), color='black', alpha=0.4)

    ax[0].set_title("Event {}".format(evt))
    plt.show()