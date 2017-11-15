import root_numpy as rn
import ROOT
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
from matplotlib import cm
from collections import namedtuple
import larana.lar_utils as laru

input_filename = '/home/matthias/workspace/my_fieldcorr/output/RecoDispl-exp-roii.root'
input_filename = '/home/matthias/workspace/FieldCalibration/output/RecoCorrection-Sim-corr.root'
input_filename = '/home/data/uboone/laser/scratch/SpaceCharge.root'

dist_raw = laru.get_histos(input_filename)
distortion = laru.make_array(dist_raw).view(np.recarray)

x, y, z = np.meshgrid(np.linspace(laru.TPC.x_min, laru.TPC.x_max, distortion.shape[0]),
                      np.linspace(laru.TPC.y_min, laru.TPC.y_max, distortion.shape[1]),
                      np.linspace(laru.TPC.z_min, laru.TPC.z_max, distortion.shape[2]))


for sl in range(0, distortion.shape[1]):

    f, ax, = plt.subplots(1, 3, figsize=(12, 5))
    #
    dist = distortion[:, sl, :]

    dimens = {0: 'dx',
              1: 'dy',
              2: 'dz',}

    limits = {0: [-50, 50],
              1: [-50, 50],
              2: [-50, 50]}

    ax[1].set_title("z={:.1f} [cm]".format(sl * 1036/101))

    for dim in range(3):
        #qu = ax.contourf(z[sl, :, :], x[sl, :, :], dist.dx, cmap=cm.Spectral, vmin=-20, vmax=20, interpolation=None)
        #qu.cmap.set_over('#FFFFFF')
        im = ax[dim].imshow(dist[dimens[dim]].T, cmap=cm.Spectral) #, vmin=limits[dim][0], vmax=limits[dim][1], interpolation=None)
        im.cmap.set_over('#FFFFFF')


        ax[dim].set_xlabel("x [cm]")

        ax[dim].set_xticks([0, 12, 25])
        ax[dim].set_yticks([0, 12, 25])
        ax[dim].set_yticklabels([-116, 0, 116])
        ax[dim].set_xticklabels([0, 128, 256])

        #
        divider = make_axes_locatable(ax[dim])
        cax = divider.append_axes("right", size="2%", pad=0.05)
        cax.set_title("{} [cm]".format(dimens[dim]))
        plt.colorbar(im, cax)
        ax[dim].invert_yaxis()

    # ax.set_title("y=" + str((start_slice+idx )*((232)/25) - 116) +"cm")
    # #ax.set_title("y=" + str((start_slice + idx) * 10) + "cm")
    # plt.ylabel("delta-x [cm]")

    #plt.savefig("output/dist-x_zx-{}.png".format(slice))

    ax[0].set_ylabel("y [cm]")

    plt.tight_layout(pad=0.4, w_pad=0.5, h_pad=1.0)
    plt.show()