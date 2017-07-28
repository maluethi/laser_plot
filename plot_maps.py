import root_numpy as rn
import ROOT
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
from matplotlib import cm
from collections import namedtuple
import larana.lar_utils as laru

input_filename = '/home/matthias/workspace/my_fieldcorr/output/RecoDispl-exp-roii.root'
input_filename = '/home/matthias/workspace/FieldCalibration/output/RecoCorrection-10.root'


dist_raw = laru.get_histos(input_filename)
distortion = laru.make_array(dist_raw).view(np.recarray)

x, y, z = np.meshgrid(np.linspace(laru.TPC.x_min, laru.TPC.x_max, distortion.shape[0]),
                      np.linspace(laru.TPC.y_min, laru.TPC.y_max, distortion.shape[1]),
                      np.linspace(laru.TPC.z_min, laru.TPC.z_max, distortion.shape[2]))


for sl in range(0, distortion.shape[2]):

    f, ax, = plt.subplots(1,1, figsize=(8, 2.3), dpi=260)
    #
    dist = distortion[sl, : , :]

    #qu = ax.contourf(z[sl, :, :], x[sl, :, :], dist.dx, cmap=cm.Spectral, vmin=-20, vmax=20, interpolation=None)
    #qu.cmap.set_over('#FFFFFF')
    im = ax.imshow(dist.dx, cmap=cm.Spectral, vmin=-10, vmax=10, interpolation=None)
    im.cmap.set_over('#FFFFFF')
    #
    #plt.xlabel("z [cm]")
    #plt.ylabel("x [cm]")
    #plt.xticks([0, 25, 50, 75, 100])
    #plt.yticks([0, 12, 25])

    #ax.set_xticklabels([0, 250, 500, 750, 1000])
    #ax.set_yticklabels([0,128,256])

    #
    divider = make_axes_locatable(ax)
    cax = divider.append_axes("right", size="2%", pad=0.05)
    plt.colorbar(im, cax)
    ax.invert_yaxis()

    # ax.set_title("y=" + str((start_slice+idx )*((232)/25) - 116) +"cm")
    # #ax.set_title("y=" + str((start_slice + idx) * 10) + "cm")
    # plt.ylabel("delta-x [cm]")

    #plt.savefig("output/dist-x_zx-{}.png".format(slice))

    plt.show()