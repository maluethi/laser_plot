import pickle
import larana.lar_utils as laru
import larana.geom as geom
import matplotlib.pyplot as plt
import numpy as np



base_dir = '/home/data/uboone/laser/processed/'
laser_file1 = base_dir + "laser-data-7267-smooth-calib.npy"
track_file1 = base_dir + "laser-tracks-7267-smooth.npy"
laser_file2 = base_dir + "laser-data-7252-smooth-calib-inv.npy"
track_file2 = base_dir + "laser-tracks-7252-smooth-inv.npy"


laser1 = np.load(laser_file1)
laser2 = np.load(laser_file2)

track1 = np.load(track_file1)
track2 = np.load(track_file2)


with open("/home/matthias/workspace/larana/projects/out/cross-1.txt", "rb") as fp:   # Unpickling
    data = pickle.load(fp)

stride = 25
plot = False

#data = data[::stride]
plt.style.use('./mythesis.mplstyle')

dist_true = [df[2][0] for df in data]
dist_reco = [df[3][0] for df in data]
dist_d = [df[2][0] - df[3][0] for df in data]
edge = [False for _ in data]
#fig, ax = laru.make_figure()

df = data[600]

idx1 = df[0]
idx2 = df[1]

d_true = df[2][0]
pt1_true = df[2][1]
pt2_true = df[2][2]

d_reco = df[3][0]
pt1_reco = df[3][1]
pt2_reco = df[3][2]

tr1 = track1[idx1]
tr2 = track2[idx2]

la1 = laser1[idx1]
la2 = laser2[idx2]

la1_entry, la1_exit, la1_dir, la1_pos, event = laru.disassemble_laser(la1)
la2_entry, la2_exit, la2_dir, la2_pos, event = laru.disassemble_laser(la2)

fig, ax = laru.make_figure(tex=True)
laru.plot_track(tr1[1], tr1[2], tr1[3], ax, **{'color': 'tab:orange'})
laru.plot_track(tr2[1], tr2[2], tr2[3], ax, **{'color': 'tab:blue'})
laru.plot_edges(ax, la1_entry.tolist(), la1_exit.tolist(), color='black', alpha=0.4)
laru.plot_edges(ax, la2_entry.tolist(), la2_exit.tolist(), color='black', alpha=0.4)


laru.plot_edges(ax, pt1_reco, pt2_reco, **{'color': 'black', 'marker': None})
laru.plot_edges(ax, pt1_true, pt2_true, **{'color': 'black', 'marker': '*', 'markersize': 5})
laru.plot_point(ax, pt1_reco, **{'color': 'tab:orange', 'marker': 'o', 'markersize': 5})
laru.plot_point(ax, pt2_reco, **{'color': 'tab:blue', 'marker': 'o', 'markersize': 5})


ax[0].set_xlim([402, 406])
ax[0].set_ylim([234, 242])
ax[1].set_ylim([-68, -52])
ax[0].get_xaxis().get_label().set_visible(False)
plt.setp(ax[0].get_xticklabels(), visible=False)

for a in ax:
    a.grid()

plt.show()


