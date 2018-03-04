import pickle
import larana.lar_utils as laru
import larana.geom as geom
import matplotlib.pyplot as plt
import numpy as np


def close_to_edge(pt, track, dist=20):
    x, y, z = track[1], track[2], track[3]

    idx_min = np.argmin(z)
    idx_max = np.argmax(z)

    pt_min = [x[idx_min], y[idx_min], z[idx_min]]
    pt_max = [x[idx_max], y[idx_max], z[idx_max]]

    d_min = geom.distance(pt, pt_min)
    d_max = geom.distance(pt, pt_max)
    if d_min < dist or d_max < dist:
        return True
    else:
        return False

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

stride = 10

data = data[::stride]

dist_true = [df[2][0] for df in data]
dist_reco = [df[3][0] for df in data]
dist_d = [df[2][0] - df[3][0] for df in data]
edge = [False for _ in data]
fig, ax = laru.make_figure()

for idx, df in enumerate(data):
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
    if close_to_edge(pt1_reco, tr1) or close_to_edge(pt2_reco, tr2):
        edge[idx] = True

        laru.plot_track(tr1[1], tr1[2], tr1[3], ax, **{'color': 'r'})
        laru.plot_track(tr2[1], tr2[2], tr2[3], ax, **{'color': 'g'})
        laru.plot_point(ax, pt1_reco)
        laru.plot_edges(ax, pt1_reco, pt2_reco)
plt.show()
    #laru.plot_edges(ax, pt1_true, pt2_true)
print(edge)


no_edge = [d for d, edg in zip(dist_d, edge) if not edg]

plt.hist(dist_d, bins=10)
plt.hist(no_edge, bins=10)
plt.show()


plt.hist2d(dist_true, dist_reco, bins=100)
plt.show()