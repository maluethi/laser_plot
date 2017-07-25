from larana.lar_data import LarData
import numpy as np
from glob import glob1


def get_plane_idx(dt, plane_id):
    if plane_id < 0 or plane_id > 2:
        raise ValueError("plane must be 0,1 or 2, it was {}".format(plane_id))
    return np.where(dt == plane_id)


def get_ampl(dt, eventid, plane):
    hit = dt.get_hits(eventid)
    return hit.peak_amp[get_plane_idx(hit.plane, plane)]


def get_integral(dt, eventid, plane):
    hit = dt.get_hits(eventid)
    return hit.integral[get_plane_idx(hit.plane, plane)]


def get_width(dt, eventid, plane):
    hit = dt.get_hits(eventid)
    start_tick = hit.start_tick[get_plane_idx(hit.plane, plane)]
    end_tick = hit.end_tick[get_plane_idx(hit.plane, plane)]

    return end_tick - start_tick

# little script that calculates histograms of the input files using the above getter functions
# the output data format is the following:
# [[histogram1, bins1], [histogram2, bins2], [histogram3, bins3]]
#
# if you want to add another dimension: add a label to dims, add a getter functions and define the ranges


# Get all the files
outdir = "./data/"
qualifier = "roi"
base_dir = "/home/data/uboone/laser/7267/out/{}/".format(qualifier)
filenames = sorted(glob1(base_dir, "LaserReco-*"))

dims = ["amplitude", "width", "integral"]
getters = [get_ampl, get_width, get_integral]

histos = {dim: {plane: [] for plane in range(3)} for dim in dims}
edges = {dim: {plane: [] for plane in range(3)} for dim in dims}
getters = {dim: getter for dim, getter in zip(dims, getters)}

ampl_ranges = {0: [-2000, 0], 1: [0, 2000], 2: [0, 2000]}
ampl_bins = 500
width_ranges = {0: [0,150], 1: [0, 150], 2: [0, 150]}
width_bins = 150
inte_ranges = {0: [0, 5000], 1: [0, 5000], 2: [0, 5000]}
inte_bins = 500

ranges = {dim: r for r,dim in zip([ampl_ranges, width_ranges, inte_ranges],dims) }
bins = {dim: bins for dim, bins in zip(dims, [ampl_bins, width_bins, inte_bins])}

for filename in filenames:
    print('processing file {}'.format(filename))
    data = LarData(base_dir + filename)
    data.read_hits(planes='u')
    data.read_ids()

    for idx in range(data.n_entries):

        for plane in range(3):
            for dim in dims:
                hist, edge = np.histogram(getters[dim].__call__(data, idx, plane), bins=bins[dim], range=ranges[dim][plane])
                histos[dim][plane].append(hist)
                edges[dim][plane] = edge


hist = {dim: {plane: []} for dim in dims for plane in range(3)}
for dim in dims:
    for plane in range(3):
        hist[dim][plane] = np.sum(histos[dim][plane], axis=0)

    dim_data = [[hist[dim][pl], edges[dim][pl]] for pl in range(3)]
    print("saving {}".format(dim))
    np.save("./data/hist-{}-{}.npy".format(dim, qualifier), dim_data)






