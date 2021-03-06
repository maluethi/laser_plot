import larana.lar_utils as lar_u

import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.cm as cm
from mpl_toolkits.axes_grid1 import make_axes_locatable

import numpy as np

cmap = cm.get_cmap('viridis')
x_min, x_max = -0.5, 0
norm_zx = mpl.colors.Normalize(vmin=x_min, vmax=x_max)
cm_zx = cm.ScalarMappable(norm=norm_zx, cmap=cmap)

y_max, y_min  = 0.33, -0.18
norm_zy = mpl.colors.Normalize(vmin=y_min, vmax=y_max)
cm_zy = cm.ScalarMappable(norm=norm_zy, cmap=cmap)

run = 2

base_dir = '/home/data/uboone/laser/processed/'
tracks_filename = "laser-tracks-7252-smooth-new.npy".format(run)
laser_filename = "laser-data-7252-smooth-new-inv.npy".format(run)

#tracks_filename = "sim/laser-tracks-021-diff-inv.npy"
#laser_filename =  "sim/laser-data-021-diff-inv.npy"


tracks = np.load(base_dir + tracks_filename, encoding='latin1')
laser = np.load(base_dir + laser_filename, encoding='latin1')

fig = plt.figure(figsize=(8, 5.), dpi=160)

gs = mpl.gridspec.GridSpec(2, 3) #, hspace=0.05)

ax_zx = fig.add_subplot(gs[0, :])
ax_zy = fig.add_subplot(gs[1, :])
#ax_xy = fig.add_subplot(gs[2, :])

stride = 1

for idx, (laser, track) in enumerate(zip(laser[1::stride], tracks[1::stride])):
    print('processing event {}'.format(track[0]))
    x, y, z = track[1], track[2], track[3]
    laser_entry = np.rec.array([laser[1], laser[2], laser[3]],
                               dtype=[('x', 'f'), ('y', 'f'), ('z', 'f')])
    laser_exit = np.rec.array([laser[4],laser[5],laser[6]],
                              dtype=[('x', 'f'), ('y', 'f'), ('z', 'f')])

    m_zx, b_zx = lar_u.calc_line([laser_entry.z, laser_entry.x], [laser_exit.z, laser_exit.x])
    m_zy, b_zy = lar_u.calc_line([laser_entry.z, laser_entry.y], [laser_exit.z, laser_exit.y])
    m_xy, b_xy = lar_u.calc_line([laser_entry.x, laser_entry.y], [laser_exit.x, laser_exit.y])

    true_zx = np.polyval([m_zx, b_zx], z)
    true_zy = np.polyval([m_zy, b_zy], z)
    true_xy = np.polyval([m_xy, b_xy], x)

    ax_zx.plot(z, x - true_zx, color=cm_zx.to_rgba(np.tan(-m_zx)),  alpha=0.5)
    ax_zy.plot(z, y - true_zy, color=cm_zy.to_rgba(np.tan(m_zy)), alpha=0.5)

    minimum = np.argmin(z)

    stri = '({:2.0f},{:2.0f},{:2.0f}, m: {})'.format(laser_exit.x.item(0), laser_exit.y.item(0), laser_exit.z.item(0), m_zx)

    #ax_zx.text(z[minimum], x[minimum] - true_zx[minimum], stri, fontsize=5)
    #ax_zy.text(z[minimum], y[minimum] - true_zy[minimum], "{}".format(idx), fontsize=5)
    #ax_xy.plot(x, y - true_xy, color=cm_zx.to_rgba(np.tan(m_xy)),  alpha=0.5)


# colorbars
divider = make_axes_locatable(ax_zx)
ax_cb_zx = divider.append_axes("right", size="2%", pad=0.05)
cb_zx = mpl.colorbar.ColorbarBase(ax_cb_zx, cmap=cmap, norm=norm_zx, orientation='vertical')


divider = make_axes_locatable(ax_zy)
ax_cb_zy = divider.append_axes("right", size="2%", pad=0.05)
cb_zy = mpl.colorbar.ColorbarBase(ax_cb_zy, cmap=cmap, norm=norm_zy, orientation='vertical')

# grid / limits
ax_zx.set_ylim([-1, 12])
ax_zx.minorticks_on()
ax_zx.set_xlim([0, 1036])
ax_zx.grid()
ax_zx.grid(which='minor', linestyle=':', linewidth='0.5', color='black')

ax_zy.set_ylim([-20, 20])
ax_zy.minorticks_on()
ax_zy.set_xlim([0, 1036])
ax_zy.set_ylim([-20,20])
ax_zy.grid()
ax_zy.grid(which='minor', linestyle=':', linewidth='0.5', color='black')

# labels
ax_zx.set_title("Track Residuals in Projection z-x and z-y")
ax_zx.set_ylabel("$\Delta$x [cm]")
#ax_zx.set_xticklabels([])

ax_zy.set_xlabel("z [cm]")
ax_zy.set_ylabel("$\Delta$y [cm]")

cb_zx.set_ticks([x_max, x_min])
cb_zx.set_ticklabels(["aimed \n straight", "aimed at \n cathode"])

cb_zy.set_ticks([y_max, y_min])
cb_zy.set_ticklabels(["aimed at\n top", "aimed at \n bottom"])

# general

plt.tight_layout(pad=0.4, w_pad=0.5, h_pad=1.0)
plt.show()
