from larana.lar_utils import read_tracks, read_laser, disassemble_laser, disassemble_track, make_figure, plot_track
import numpy as np

import matplotlib.pyplot as plt

filename = "/home/data/uboone/laser/7267/tracks/Tracks-7267-789.root"

tracks = read_tracks(filename)
lasers = read_laser(filename)

# generate event id lists, since there are more tracks than events
track_event_id = np.array([track[0] for track in tracks])

# loop over all tracks in the file
for laser in lasers:
    fig, ax = make_figure()
    _, _, dir, _, evt = disassemble_laser(laser)
    track_list = np.where(track_event_id == evt)

    # loop over all tracks in this event
    for track in tracks[track_list]:
        track_points, evt = disassemble_track(track)
        plot_track(track_points.x, track_points.y, track_points.z, ax)

    ax[0].set_title("Event {}".format(evt))
    plt.show()