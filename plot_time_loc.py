from larana.lar_utils import read_tracks, read_laser, disassemble_laser, disassemble_track, make_figure, plot_track, \
    plot_edges
import matplotlib.pyplot as plt
fig, ax = make_figure()

entries = ([111.5, 12.2, 1036.5], [111, 5, 1036.5], [101.5, 12.2,1036.5], [101.5, 5,1036.5])
exits = ([256, 80, 357], [256, -40, 357], [100.2, 80, 0], [100.2, -40 , 0])
for en, ex in zip(entries, exits):
    plot_edges(ax, en, ex)

plt.show()