import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
import numpy as np
from numpy import sqrt, pi, exp

from matplotlib.offsetbox import AnchoredText

from lmfit import  Model
import matplotlib
import matplotlib.gridspec as gridspec
import argparse
from larana import lar_utils as laru

def gaussian(x, amp, cen, wid):
    "1-d gaussian: gaussian(x, amp, cen, wid)"
    return (amp/(sqrt(2*pi)*wid)) * exp(-(x-cen)**2 /(2*wid**2))

# argument parser
parser = argparse.ArgumentParser(description='Plotting Time Histograms')
parser.add_argument('-p', dest='prod', action='store_true', default=False, help='production')
args = parser.parse_args()

# main variables for this plot
loc = [500,1750,3000]
raw_event = 305

# loading data
res = np.load('/home/matthias/workspace/larana/projects/out/time-histo/histo-more.npy')
raw = laru.read_raw('$LDATA/7275/rwa/RwaData-7275-006.root')

# reading raw data event
evt_sel = raw['event'] == raw_event
evt_data = raw[evt_sel]
wires_sel = [np.where(evt_data['wire'] == l)[0][0] for l in loc]
wire_data = [evt_data[w]['raw'] for w in wires_sel]
wire_data = np.median(wire_data, axis=1) - np.array(wire_data).T

# defining style and colors
plt.style.use('./mythesis.mplstyle')
prop_cycle = plt.rcParams['axes.prop_cycle']
colors = prop_cycle.by_key()['color'][:3]

# now some processing
maximas = np.concatenate(res, axis=1)

w = np.arange(0,3456)
b = np.ones(maximas.shape)
x = np.transpose(w * b.T)

# and off we go for plotting
fig = plt.figure()
gs1 = gridspec.GridSpec(nrows=2, ncols=2)
ax1 = fig.add_subplot(gs1[0, :])
ax2 = fig.add_subplot(gs1[-1, :-1])
ax3 = fig.add_subplot(gs1[-1, -1])

# do the 2D histogram
ax1.hist2d(x.flatten(), maximas.flatten(), bins=(3456, 2000))
ax1.set_ylim([950, 1100])
#ax1.colorbar(label='N')
ax1.set_xlabel('Wire')
ax1.set_ylabel('ADC tick')

labels = list(range(len(loc)))
print(labels)
for x, y, s in zip(loc, len(loc)*[951], labels):
    print(x)
    ax1.text(x+40,y,str(s+1), color='w')

ax1.vlines(loc, 950, 1100, linewidth=1, linestyles='dashed', colors=colors)

# now we do the histograms and the fits
lo = [1,2,2]
xlimits = [950, 1150]
x = np.arange(0,len(wire_data[:,0]))

wids = []


for (i, l), c in zip(enumerate(loc), colors):
    n, bins, patches = ax3.hist(maximas[l], bins=500, color=c, alpha=0.4)
    raw_signal = -1* wire_data[:, i]
    guess = np.argmax(raw_signal[xlimits[0]:xlimits[1]]) + xlimits[0]

    gmodel = Model(gaussian)
    result = gmodel.fit(n, x=bins[:-1],amp=400, cen=998, wid=10)

    ax3.plot(bins[:-1], result.best_fit, color=c, linestyle='--')

    # plot raw
    res_raw = gmodel.fit(raw_signal, x=x, amp=400, cen=guess, wid=10)
    ax2.plot(raw_signal, color=c, alpha=0.4)
    ax2.plot(x, res_raw.best_fit, color=c, linestyle='--')



    amp = result.params['amp']
    cen = result.params['cen']
    wid = result.params['wid']

    textstr = 'amp: {:03.2f} +/- {:03.2f}\n' \
              'cen: {:03.2f} +/- {:03.2f}\n' \
              'wid: {:03.2f} +/- {:03.2f}'.format(amp.value, amp.stderr,
                                                  cen.value, cen.stderr,
                                                  wid.value, wid.stderr)
    wids.append((cen.value, cen.stderr))

    # these are matplotlib.patch.Patch properties
    #props = dict(boxstyle='round', facecolor=None, alpha=0.5)
    # place a text box in upper left in axes coords
    #ax.text(0.05, 0.95, textstr, transform=ax.transAxes,
    #        verticalalignment='top', bbox=props)

    #anchored_text = AnchoredText(textstr, loc=lo[i])
    #ax2.add_artist(anchored_text)

    amp = result.params['amp']


ax2.grid()
ax2.set_axisbelow(True)
ax2.set_xlim(xlimits)
ax2.set_xlabel('ADC Tick')
ax2.set_ylabel('Amplitude')
ax2.set_ylim([-10,35])

ax3.grid()
ax3.set_axisbelow(True)
ax3.set_xlim(xlimits)
ax3.set_xlabel('ADC Tick')
ax3.set_ylabel('N')

fig.tight_layout()
if not args.prod:
    plt.show()
else:
    plt.savefig('./gfx/EField/time_histo.pdf')
    with open('./gfx/EField/time_hist.txt', 'w') as f:
        for idx, w in enumerate(wids):
            f.write("{},{:03.2f},{:03.2f}\n".format(idx, w[0], w[1]))