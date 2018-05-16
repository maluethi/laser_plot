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
error_estimate = 0.2

to_mm = 1E-5
v_drift = laru.drift_speed(0.273) * to_mm # mm/us
v_drift_plus = laru.drift_speed((1 + error_estimate) * 0.273) * to_mm # cm/us
v_drift_minus = laru.drift_speed((1 - error_estimate) * 0.273) * to_mm # cm/us

print(v_drift_plus - v_drift_minus, )

# main variables for this plot
loc = [500,1750,3000]
raw_event = 305

# ADC to units: fixed time scaling 1 ADC Tick = 0.5us
#               12bit ADC 2Vpp
tick2time = 0.5
meas2volt = 0.488

window_offset = 900

time_limit = np.array([460, 560]) + window_offset*tick2time

print(v_drift)
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
maximas = (np.concatenate(res, axis=1) + window_offset) * tick2time

n_wires = maximas.shape[0]
n_timeticks = maximas.shape[1]
print(maximas.shape)

w = np.arange(0,n_wires)
b = np.ones(maximas.shape)
x = np.transpose(w * b.T)

# and off we go for plotting
fig = plt.figure(figsize=(4.670, 8))
gs1 = gridspec.GridSpec(nrows=3, ncols=1)
ax_2dhisto = fig.add_subplot(gs1[1, :])
ax_rawwave = fig.add_subplot(gs1[0, :])
ax_histogr = fig.add_subplot(gs1[2, :])

# do the 2D histogram
ax_2dhisto.hist2d(x.flatten(), maximas.flatten(), bins=(n_wires, 1000))
ax_2dhisto.set_ylim(time_limit)
#ax1.colorbar(label='N')
ax_2dhisto.set_xlabel('Wire')
ax_2dhisto.set_ylabel('t[$\mu s$]')

labels = list(range(len(loc)))
print(labels)
for x, y, s in zip(loc, len(loc)*[time_limit[0]], labels):
    print(x)
    ax_2dhisto.text(x + 40, y, str(s + 1), color='w')

ax_2dhisto.vlines(loc, time_limit[0], time_limit[1], linewidth=1, linestyles='dashed', colors=colors)

# now we do the histograms and the fits
lo = [1,2,2]
xlimits = np.array([950, 1150])
x = (np.arange(0,len(wire_data[:,0])) + window_offset) * tick2time
wids = []

for (i, l), c in zip(enumerate(loc), colors):
    n, bins, patches = ax_histogr.hist(maximas[l], bins=1000, color=c, alpha=0.4)
    raw_signal = -1* wire_data[:, i]
    guess = (np.argmax(raw_signal[xlimits[0]:xlimits[1]]) + xlimits[0] + window_offset) * tick2time

    gmodel = Model(gaussian)
    result = gmodel.fit(n, x=bins[:-1], amp=400, cen=998/2, wid=10)

    ax_histogr.plot(bins[:-1], result.best_fit, color=c, linestyle='--')

    # plot raw
    print(guess)
    res_raw = gmodel.fit(raw_signal, x=x, amp=400, cen=guess, wid=5)
    ax_rawwave.plot(x, raw_signal, color=c, alpha=0.4)
    ax_rawwave.plot(x, res_raw.best_fit, color=c, linestyle='--')



    amp = result.params['amp']
    cen = result.params['cen']
    wid = result.params['wid']


    txt_time = 'amp: {:03.2f} +/- {:03.2f}\n' \
              'cen: {:03.2f} +/- {:03.2f}\n' \
              'wid: {:03.2f} +/- {:03.2f}'.format(amp.value, amp.stderr,
                                                  cen.value, cen.stderr,
                                                  wid.value, wid.stderr)

    d_cen = v_drift * cen.value
    d_wid = np.around(v_drift * wid.value,1)
    d_wid_m = np.around(d_wid - v_drift_minus * wid.value, 1)
    d_wid_p = np.around(v_drift_plus * wid.value - d_wid, 1)

    txt_dist = 'wid [mm]: {:03.1f}, - {:03.1f}, + {:03.1f}\n'.format(d_wid, d_wid_m, d_wid_p)

    wids.append((cen.value, wid.value, d_wid, d_wid_m, d_wid_p))
    print(txt_time)
    print()
    print(txt_dist)
    # these are matplotlib.patch.Patch properties
    #props = dict(boxstyle='round', facecolor=None, alpha=0.5)
    # place a text box in upper left in axes coords
    #ax.text(0.05, 0.95, textstr, transform=ax.transAxes,
    #        verticalalignment='top', bbox=props)

    #anchored_text = AnchoredText(textstr, loc=lo[i])
    #ax2.add_artist(anchored_text)



ax_rawwave.grid()
ax_rawwave.set_axisbelow(True)
ax_rawwave.set_xlim(time_limit)
ax_rawwave.set_xlabel('t[$\mu s$]')
ax_rawwave.set_ylabel('A [$mV$]')
ax_rawwave.set_ylim([-10, 35])

for label, ((x,y), c) in enumerate(zip([(940,30), (974,30), (992,30)], colors)):
    ax_rawwave.text(x, y, str(label + 1), color=c)

ax_histogr.grid()
ax_histogr.set_axisbelow(True)
ax_histogr.set_xlim(time_limit)
ax_histogr.set_xlabel('t[$\mu s$]')
ax_histogr.set_ylabel('N')


for label, (y, c) in enumerate(zip([250,250,250], colors)):
    ax_histogr.text(wids[label][0] - 5, y, str(label + 1), color=c)

fig.tight_layout()
if not args.prod:
    plt.show()
else:
    plt.savefig('./gfx/EField/time_histo.pdf')
    with open('./gfx/EField/time_histo.txt', 'w') as f:
        for idx, w in enumerate(wids):
            f.write("{},{:03.2f},{:03.2f},{:03.1f},{:03.1f}\n".format(idx, w[0], w[1], w[2], max([w[3], w[4]])))