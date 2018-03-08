import root_numpy as rn
import ROOT
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
from matplotlib import cm
import matplotlib as mp
from collections import namedtuple
import larana.lar_utils as laru

#input_filename = '/home/matthias/workspace/my_fieldcorr/output/RecoDispl-exp-roii.root'
#input_filename = '/home/matthias/workspace/FieldCalibration/output/RecoDispl-ubsim-10.root'
sim_filename = '/home/data/uboone/laser/sim/SpaceCharge.root'
data_filename = '/home/data/uboone/laser/processed/maps/TrueDist-N3-S50-toyMC-Intpl-2side-Anode.root'
#data_filename = '/home/matthias/workspace/his_fieldcal/cmake/RecoCorr-Simu.root'

#data_filename = '/home/matthias/mnt/lheppc2/maluethi/FieldCalibration/build/RecoCorr-Simu1.root'

base = '/home/data/uboone/laser/processed/maps/smooth/'
file = 'RecoCorr-N3-S50-newselectCalibData-2side-Anode-extrasmooth.root'

#base = '/home/matthias/workspace/his_fieldcal/cmake/'
#file = 'RecoCorr-Simu.root'
err = False
res = False
save = False
dist_raw = laru.get_histos(base + file, error=err)

font = {'size'   : 18}

mp.rc('font', **font)


dist_sim = laru.get_histos(sim_filename)

distortion = laru.make_array(dist_raw).view(np.recarray)
simulation = laru.make_array(dist_sim).view(np.recarray)

x, y, z = np.meshgrid(np.linspace(laru.TPC.x_min, laru.TPC.x_max, distortion.shape[0]),
                      np.linspace(laru.TPC.y_min, laru.TPC.y_max, distortion.shape[1]),
                      np.linspace(laru.TPC.z_min, laru.TPC.z_max, distortion.shape[2]))

f, axarr, = plt.subplots(2, 3, figsize=(15, 10.))

axes = [axarr[0:2], axarr[3:5]]

slices = (10, 50)
dist_slice = [sl *1036/101 for sl in slices]
for ax, sl in zip(axarr, slices):
    #
    dist = distortion[:,:, sl]
    siml = simulation[:,:, sl]

    dimens = {0: 'dx',
              1: 'dy',
              2: 'dz',}

    if res or err:
        limits = {0: [-2, 2],
                  1: [-2, 2],
                  2: [-2, 2]}
    else:
        limits = {0: [-10., 10.],
              1: [-20, 20],
              2: [-5, 5]}

    for dim in range(3):
        #qu = ax.contourf(z[sl, :, :], x[sl, :, :], dist.dx, cmap=cm.Spectral, vmin=-20, vmax=20, interpolation=None)
        #qu.cmap.set_over('#FFFFFF')

        data = dist[dimens[dim]].T
        simu = siml[dimens[dim]].T
        if res:
            im = ax[dim].imshow((data-simu), cmap=cm.Spectral, vmin=limits[dim][0], vmax=limits[dim][1], interpolation=None)
        else:
            im = ax[dim].imshow((data), cmap=cm.Spectral, vmin=limits[dim][0], vmax=limits[dim][1], interpolation=None)
        im.cmap.set_over('#FFFFFF')
        im.cmap.set_under('#FFFFFF')

        ax[dim].set_xticks([])
        ax[dim].set_yticks([])

        #
        divider = make_axes_locatable(ax[dim])
        cax = divider.append_axes("right", size="2%", pad=0.05)
        if sl == slices[0]:
            if err:
                cax.set_title("std({}) [cm]".format(dimens[dim]))
            else:
                cax.set_title("{} [cm]".format(dimens[dim]))
        plt.colorbar(im, cax)
        ax[dim].invert_yaxis()

    # ax.set_title("y=" + str((start_slice+idx )*((232)/25) - 116) +"cm")
    # #ax.set_title("y=" + str((start_slice + idx) * 10) + "cm")
    # plt.ylabel("delta-x [cm]")

    #plt.savefig("output/dist-x_zx-{}.png".format(slice))

    ax[0].set_ylabel("y [cm]")

    #plt.tight_layout(pad=0.4, w_pad=0.5, h_pad=1.0)



for idx in range(3):
    axarr[1][idx].set_xlabel("x [cm]")
    axarr[1][idx].set_xticks([0, 12, 25])
    axarr[1][idx].set_xticklabels([0, 128, 256])

for idx in range(2):
    axarr[idx][0].set_ylabel("z = {:.0f}cm\ny [cm]".format(dist_slice[idx]))
    axarr[idx][0].set_yticks([0, 12, 25])
    axarr[idx][0].set_yticklabels([-116, 0, 116])
f.tight_layout()

if err:
    out_name = file[:-5] + '-err.pdf'
else:
    if res:
        out_name = file[:-5] + '.pdf'
    else:
        out_name = file[:-5] + '-full.pdf'

if save:
    f.savefig("/home/matthias/Documents/Presentations/Seminar_26Feb_2018/plots/" + out_name, bbox_inches=0, transparent=True)
print(out_name)
plt.show()