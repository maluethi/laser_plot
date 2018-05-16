import matplotlib.pyplot as plt
import argparse
import numpy as np
from numpy import sqrt, pi, exp

from larana import lar_utils as laru
import matplotlib as mpl
import matplotlib.cm as cm
from mpl_toolkits.axes_grid1 import make_axes_locatable


parser = argparse.ArgumentParser(description='Plotting Time Histograms')
parser.add_argument('-p', dest='prod', action='store_true', default=False, help='production')
args = parser.parse_args()

plt.style.use('./mythesis.mplstyle')

v = 1E-5* laru.drift_speed(0.273)

print(v)
#matplotlib.rc('font', **font)
def gaussian(x, amp, cen, wid):
    "1-d gaussian: gaussian(x, amp, cen, wid)"
    return (amp/(sqrt(2*pi)*wid)) * exp(-(x-cen)**2 /(2*wid**2))

#res = np.load('/home/matthias/workspace/larana/projects/out/time-histo/histo-maxima.npy')
res = np.load('/home/matthias/workspace/larana/projects/out/time-histo/histo-more-maxima-cleaned.npz')
df = np.load('/home/matthias/workspace/larana/projects/out/time-histo/time-mean.npz')

wid = df['wid']
cen = df['cen']

maximas = res['max']
#error = np.concatenate(res[:,1], axis=1)
print(maximas.shape)
maximas = maximas.T

# Get the timeing
freq = 0.25
n_max = maximas.shape[1]
t = np.arange(0, n_max/freq, 1/freq)

window_offset = 800
stepsize = 100
wires = list(range(0, 3456, stepsize))
labels = list(range(len(wires)))

cmap = cm.get_cmap('viridis')
norm = mpl.colors.Normalize(vmin=min(wires), vmax=max(wires))
cm = cm.ScalarMappable(norm=norm, cmap=cmap)

b = 0
fig, ax = plt.subplots(figsize=(4.670, 7))
for wire, lbl in zip(wires, labels):
    print(cen[wire])
    ax.plot(t, maximas[wire] + b, 'x', label=lbl, c=cm.to_rgba(wire), markersize=3, alpha=.8)
    b += 10

divider = make_axes_locatable(ax)
cax = divider.append_axes("top", size="2%", pad=0.05)
cax.set_title("wire number", y=3)
cm.set_array(wires)
cbar = plt.colorbar(cm, cax=cax, orientation='horizontal', ticklocation='top')
cbar.set_ticks([0,1000,2000,3000])
#ax.set_ylim([960, 1100])
ax.set_xlim([0, t[-1]])

ax.set_xlabel("t [s]")
ax.set_ylabel("rel. drift time [us]")
#plt.legend(ncol=7, framealpha=1)
fig.tight_layout()

if not args.prod:
    plt.show()
else:
    plt.savefig('./gfx/EField/time_evolution.pdf')