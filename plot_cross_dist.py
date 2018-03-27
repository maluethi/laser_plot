import pickle
import larana.lar_utils as laru
import larana.geom as geom
import matplotlib.pyplot as plt
import numpy as np


def close_to_track_edge(pt, track, dist=30):
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
laser_file1 = base_dir + "laser-data-7267-smooth-calib-calib.npy"
track_file1 = base_dir + "laser-tracks-7267-smooth.npy"
laser_file2 = base_dir + "laser-data-7252-smooth-calib-inv.npy"
track_file2 = base_dir + "laser-tracks-7252-smooth-inv.npy"

#laser_file1 = base_dir + "laser-data-31-cross.npy"
#track_file1 = base_dir + "laser-tracks-31-cross.npy"
#laser_file2 = base_dir + "laser-data-23-cross.npy"
#track_file2 = base_dir + "laser-tracks-23-cross.npy"


laser1 = np.load(laser_file1)
laser2 = np.load(laser_file2)

track1 = np.load(track_file1)
track2 = np.load(track_file2)


with open("/home/matthias/workspace/larana/projects/out/cross-1.txt", "rb") as fp:   # Unpickling
    data = pickle.load(fp)

stride = 1
plot = False

data = data[::stride]

dist_true = []
dist_d = []

dreco = np.array([df[2][0] for df in data])
dtrue = np.zeros(dreco.shape)
dist_d = np.zeros(dreco.shape)

print(dist_d.shape)

edge = [False for _ in data]
#fig, ax = laru.make_figure()

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

    la1 = laser1[idx1]
    la2 = laser2[idx2]

    la1_entry, la1_exit, la1_dir, la1_pos, event = laru.disassemble_laser(la1)
    la2_entry, la2_exit, la2_dir, la2_pos, event = laru.disassemble_laser(la2)

    d, p, m = geom.get_closest_distance(la1_entry.tolist(), la1_exit.tolist(),
                                        la2_entry.tolist(), la2_exit.tolist())
    dtrue[idx] = d
    dist_d[idx] = d - d_reco

    #dist_d.append(d - dist_d)

    if close_to_track_edge(pt1_reco, tr1) or close_to_track_edge(pt2_reco, tr2):
        if close_to_track_edge(la1_exit.tolist(), tr1, dist=40):
            pass
        edge[idx] = True


dist_d_no_edge = [d for d, edg in zip(dist_d, edge) if not edg]
dist_reco_noedge = [dr for dr, edg in zip(dreco, edge) if edg is False]
dist_true_noedge = [dt for dt, edg, rec in zip(dist_true, edge, dist_reco_noedge) if edg is False]



fig, ax = plt.subplots(1,1)

rng = [-15,15]
bins = 30*4
ax.hist(dist_d, bins=bins, range=rng)
plt.hist(dist_d_no_edge, bins=bins, range=rng)
plt.grid()
ax.set_xlim(rng)
plt.show()
