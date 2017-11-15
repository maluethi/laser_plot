from larana.lar_tree import LarData
from larana.lar_utils import make_figure, plot_track, plot_edges
import matplotlib.pyplot as plt
from matplotlib.widgets import Button
import matplotlib.collections

filename = "/home/data/uboone/laser/scratch/Tracks-0006-000-with-hits.root"
dimens = {"laser": 0, "reco": 1, "mc": 2}
lard = LarData(filename)
event = lard[2]
sc_zx = []

dim = dimens["mc"]

class Idx():
    def __init__(self, idx=0):
        self.idx = idx

    def nxt(self, val):
        self.idx += 1
        print(self.idx)
        update(self.idx)

    def prv(self, val):
        self.idx -= 1
        print(self.idx)
        update(self.idx)


def plot_tracks(tracks, axes, **kwargs):
    if isinstance(tracks, list):
        for track in tracks:
            plot_track(track.x, track.y, track.z, axes, **kwargs)
    else:
        plot_track(tracks.x, tracks.y, tracks.z, axes, **kwargs)


def update(idx):
    event_data = lard[idx]
    for ax in axes:
        for child in ax.get_children():
            if isinstance(child, matplotlib.collections.PathCollection):
                child.remove()
    plot_tracks(event_data[1], axes, marker="o")
    plot_tracks(event_data[2], axes, marker="x")
    fig.canvas.draw()


fig, axes = make_figure(tpc_box=True)

# callback = Idx()
#
# axgoto= plt.axes([0.6, 0.05, 0.05, 0.04])
# axprev = plt.axes([0.7, 0.05, 0.1, 0.04])
# axnext = plt.axes([0.81, 0.05, 0.1, 0.04])
#
# goto = Button(axgoto, 'Next', hovercolor='0.975')
# button_next = Button(axnext, 'Next', hovercolor='0.975')
# button_prev = Button(axprev, 'Prev', hovercolor='0.975')
#
# button_next.on_clicked(callback.nxt)
# button_prev.on_clicked(callback.prv)

plot_edges(axes, event[0].entry, event[0].exit, color="g")
plot_tracks(event[1], axes, marker="o", color="b")
plot_tracks(event[2], axes, marker="x", color="r")
plt.show()


