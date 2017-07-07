import matplotlib.pyplot as plt
import numpy as np


las_infiles = ["./data/hist-amplitude-roi.npy", "./data/hist-integral-roi.npy", "./data/hist-width-roi.npy"]
cos_infiles = ["./data/hist-amplitude-cosmic.npy", "./data/hist-integral-cosmic.npy", "./data/hist-width-cosmic.npy"]

dims = ["amplitude", "integral", "width"]
fig, axes = plt.subplots(nrows=3, ncols=len(las_infiles))


for col, [las_filename, cos_filename] in enumerate(zip(las_infiles, cos_infiles)):
    print(las_filename, cos_filename)
    las_data = np.load(las_filename)
    cos_data = np.load(cos_filename)

    axes[0][col].set_title(dims[col])

    for plane, [[las_hist, las_bins], [cos_hist, cos_bins]] in enumerate(zip(las_data, cos_data)):
        las_center = (las_bins[:-1] + las_bins[1:]) / 2
        cos_center = (cos_bins[:-1] + cos_bins[1:]) / 2

        axes[plane][col].bar(las_center, las_hist, align='center', width=5)
        axes[plane][col].bar(cos_center, cos_hist, align='center', width=5)
#
# fig, axes = plt.subplots(nrows=1, ncols=1)
#
# axes.bar(center, sig_hist, align='center', width=5)
# axes.bar(center, bkg_hist, align='center', width=5)
#
plt.show()