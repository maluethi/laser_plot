import pickle
import larana.lar_utils as laru
import larana.geom as geom
import matplotlib.pyplot as plt
import numpy as np

import matplotlib as mpl
from mpl_toolkits.axes_grid1 import make_axes_locatable

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

cmap = plt.get_cmap('viridis')
data = False

rng = [-2, 2]
stp = 0.5
rng = np.arange(rng[0], rng[1], stp)
xrange, yrange, zrange = np.meshgrid(rng, rng, rng)

base_dir = '/home/data/uboone/laser/processed/'
for dx, dy, dz in zip(xrange.flatten(), yrange.flatten(), zrange.flatten()):

    postfix = "-x_{:.1f}".format(dx) + "_y_{:.1f}".format(dy) + "_z_{:.1f}".format(dz)
    data = False
    if data:
        dx = 'data'
        fram = '1'
        laser_file1 = base_dir + "laser-data-7267-smooth-calib-calib.npy"
        track_file1 = base_dir + "laser-tracks-7267-smooth.npy"
        laser_file2 = base_dir + "laser-data-7252-smooth-calib-inv.npy"
        track_file2 = base_dir + "laser-tracks-7252-smooth-inv.npy"
    else:
        fram = 'sim'
        laser_file1 = base_dir + "laser-data-31-cross.npy"
        track_file1 = base_dir + "laser-tracks-31-cross.npy"
        laser_file2 = base_dir + "laser-data-23-cross-calib{}.npy".format(postfix)
        track_file2 = base_dir + "laser-tracks-23-cross.npy"


    laser1 = np.load(laser_file1)
    laser2 = np.load(laser_file2)

    track1 = np.load(track_file1)
    track2 = np.load(track_file2)

    with open("/home/matthias/workspace/larana/projects/out/cross-{}.txt".format(fram), "rb") as fp:   # Unpickling
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
    side = [False for _ in data]
    #fig, ax = laru.make_figure()


    fig, ax = laru.make_figure()

    for idx, df in enumerate(data):
        idx1 = df[0]
        idx2 = df[1]

        d_true = df[2][0]
        pt1_true = df[2][1]
        pt2_true = df[2][2]

        drec = df[3][0]
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
        dist_d[idx] = d - drec

        #dist_d.append(d - dist_d)

        if close_to_track_edge(pt1_reco, tr1) or close_to_track_edge(pt2_reco, tr2):
            #if close_to_track_edge(la1_exit.tolist(), tr1, dist=40):
            #    pass
            edge[idx] = True

        if 256 - p[0] < 10 or 256 - m[0] < 10:
            side[idx] = True

        if plot:
            if dist_d[idx] > 1.2:
                print(d, drec, d - drec, idx)
                print(p, m)
                print(np.array(p) - np.array(m))
                fig, ax = laru.make_figure(link_axes=False)
                laru.plot_track(tr1[1], tr1[2], tr1[3], ax, **{'color': 'r'})
                laru.plot_track(tr2[1], tr2[2], tr2[3], ax, **{'color': 'g'})
                laru.plot_edges(ax, la1_entry.tolist(), la1_exit.tolist(), color='black', alpha=0.4)
                laru.plot_edges(ax, la2_entry.tolist(), la2_exit.tolist(), color='black', alpha=0.4)
                laru.plot_point(ax, p, marker='o')
                laru.plot_point(ax, m, marker='x')
                laru.plot_edges(ax, pt1_reco, pt2_reco)
                laru.plot_edges(ax, pt1_true, pt2_true)
                for a in ax:
                    a.set_aspect('equal')
                plt.show()
    #    if dist_d[idx] > 0.5:
    #        laru.plot_point(ax, pt1_reco, **{'marker': 'o', 'color': cmap(d/10), 'markersize': 3})
    #divider = make_axes_locatable(ax[2])
    #ax_cb_zx = divider.append_axes("right", size="2%", pad=0.05)
    #cb_zx = mpl.colorbar.ColorbarBase(ax_cb_zx, cmap=cmap, orientation='vertical')
    #plt.show()

    dist_d_no_edge = np.array([d for d, edg in zip(dist_d, side) if edg])
    dist_reco_noedge = [dr for dr, edg in zip(dreco, edge) if edg is False]
    dist_true_noedge = [dt for dt, edg, rec in zip(dist_true, edge, dist_reco_noedge) if edg is False]

    print("saved to dist{}.npz".format(postfix))
    np.savez('output/cross_dist/dist{}.npz'.format(postfix), d=dist_d, dtrue=dtrue, dreco=np.array(dreco))


    if plot:
        plt.hist2d(dist_d, dtrue, bins=[200,40], range=[[-2,2],[0,10]])
        plt.show()
        fig, ax = plt.subplots(1,1)
        rng = [-5,5]
        bins = 50*2
        ax.hist(dist_d, bins=bins, range=rng)
        plt.hist(dist_d_no_edge, bins=bins, range=rng)
        plt.grid()
        ax.set_xlim(rng)
        plt.show()

        fig, ax = plt.subplots(1,1)
        dx_reco = np.array([df[3][1][0] - df[3][2][0] for df in data])
        dy_reco = np.array([df[3][1][1] - df[3][2][1] for df in data])
        dz_reco = np.array([df[3][1][2] - df[3][2][2] for df in data])
        plt.hist(dx_reco, bins=bins, range=rng, label='x', alpha=0.6)
        plt.hist(dy_reco, bins=bins, range=rng, label='y', alpha=0.6)
        plt.hist(dz_reco, bins=bins, range=rng, label='z', alpha=0.6)
        plt.legend()
        plt.show()

        fig, ax = plt.subplots(1,1)
        dx_true = np.array([df[2][1][0] - df[2][2][0] for df in data])
        dy_true = np.array([df[2][1][1] - df[2][2][1] for df in data])
        dz_true = np.array([df[2][1][2] - df[2][2][2] for df in data])
        plt.hist(dx_true, bins=bins, range=rng, label='x', alpha=0.6)
        plt.hist(dy_true, bins=bins, range=rng, label='y', alpha=0.6)
        plt.hist(dz_true, bins=bins, range=rng, label='z', alpha=0.6)
        plt.legend()
        plt.show()
