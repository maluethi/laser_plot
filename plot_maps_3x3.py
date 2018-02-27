import root_numpy as rn
import ROOT
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
from matplotlib import cm
from collections import namedtuple
import larana.lar_utils as laru

#input_filename = '/home/matthias/workspace/my_fieldcorr/output/RecoDispl-exp-roii.root'
#input_filename = '/home/matthias/workspace/FieldCalibration/output/RecoDispl-ubsim-10.root'
sim_filename = '/home/data/uboone/laser/sim/SpaceCharge.root'
data_filename = '/home/data/uboone/laser/processed/maps/TrueDist-N3-S50-newCalibSelectData-2side-Anode.root'
#data_filename = '/home/matthias/workspace/his_fieldcal/cmake/RecoCorr-Simu.root'

#data_filename = '/home/matthias/mnt/lheppc2/maluethi/FieldCalibration/build/RecoCorr-Simu1.root'

dist_raw = laru.get_histos(data_filename, error=True)



dist_sim = laru.get_histos(sim_filename)

distortion = laru.make_array(dist_raw).view(np.recarray)
simulation = laru.make_array(dist_sim).view(np.recarray)

x, y, z = np.meshgrid(np.linspace(laru.TPC.x_min, laru.TPC.x_max, distortion.shape[0]),
                      np.linspace(laru.TPC.y_min, laru.TPC.y_max, distortion.shape[1]),
                      np.linspace(laru.TPC.z_min, laru.TPC.z_max, distortion.shape[2]))

f, axarr, = plt.subplots(2, 3, figsize=(15, 10))

axes = [axarr[0:2], axarr[3:5]]

print(axarr)
for ax, sl in zip(axarr, (10, 50)):
    #
    dist = distortion[:,:, sl]
    siml = simulation[:,:, sl]

    dimens = {0: 'dx',
              1: 'dy',
              2: 'dz',}

    limits_true = {0: [-10., 10.],
              1: [-15, 15],
              2: [-5, 5]}

    limits_sim = {0: [-2, 2],
                  1: [-2, 2],
                  2: [-2, 2]}

    limits = limits_sim

    ax[1].set_title("z={:.1f} [cm]".format(sl * 1036/101))

    for dim in range(3):
        #qu = ax.contourf(z[sl, :, :], x[sl, :, :], dist.dx, cmap=cm.Spectral, vmin=-20, vmax=20, interpolation=None)
        #qu.cmap.set_over('#FFFFFF')

        data = dist[dimens[dim]].T
        simu = siml[dimens[dim]].T

        im = ax[dim].imshow((data), cmap=cm.Spectral, vmin=limits[dim][0], vmax=limits[dim][1], interpolation=None)

        im.cmap.set_over('#FFFFFF')
        im.cmap.set_under('#FFFFFF')


        ax[dim].set_xlabel("x [cm]")

        ax[dim].set_xticks([0, 12, 25])
        ax[dim].set_yticks([0, 12, 25])
        ax[dim].set_yticklabels([-116, 0, 116])
        ax[dim].set_xticklabels([0, 128, 256])

        #
        divider = make_axes_locatable(ax[dim])
        cax = divider.append_axes("right", size="2%", pad=0.05)
        cax.set_title("std ({}) [cm]".format(dimens[dim]))
        plt.colorbar(im, cax)
        ax[dim].invert_yaxis()

    # ax.set_title("y=" + str((start_slice+idx )*((232)/25) - 116) +"cm")
    # #ax.set_title("y=" + str((start_slice + idx) * 10) + "cm")
    # plt.ylabel("delta-x [cm]")

    #plt.savefig("output/dist-x_zx-{}.png".format(slice))

    ax[0].set_ylabel("y [cm]")

    #plt.tight_layout(pad=0.4, w_pad=0.5, h_pad=1.0)
    f.tight_layout()
    f.savefig("data-100.png", bbox_inches=0, transparent=True)
plt.show()