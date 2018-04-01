import numpy as np
from scipy.stats import chisquare
import matplotlib.pyplot as plt
from lmfit import Model
from itertools import chain
from matplotlib.offsetbox import AnchoredText

def gaussian(x, amp, cen, wid):
    "1-d gaussian: gaussian(x, amp, cen, wid)"
    return (amp/(np.sqrt(2*np.pi)*wid)) * np.exp(-(x-cen)**2 /(2*wid**2))

plt.style.use('./mythesis.mplstyle')

def get_normed_histo(data, bins):
    hist, bin_edges = np.histogram(data, bins, range=rng)
    hist = np.divide(hist, np.sum(hist))
    return hist, bin_edges

def get_gauss_fit(hist, edges):
    gmodel = Model(gaussian)
    result = gmodel.fit(hist, x=edges[:-1], amp=1, cen=0, wid=2)
    return result

rng = [-2, 2]
bins = 20*2 + 1

# Chi squared
fig, axes = plt.subplots(3,3, sharey=True, sharex=True, figsize=[4.670, 6])

drx1 = np.linspace(-.5,.5,3)
drx2 = 0
drx3 = np.linspace(-1,1,3)
range1, range2, range3 = np.meshgrid(drx1, drx2, drx3)
print(range1, range3)
for dx,dy,dz, ax in zip(range3.flatten(), range2.flatten(), range1.flatten(), chain(*axes)):
    frame = "-x_{:.1f}".format(dx) + "_y_{:.1f}".format(dy) + "_z_{:.1f}".format(dz)

    df = np.load('output/cross_dist/dist{}.npz'.format(frame))
    dist_d = df['d']
    hist, bin_edges = get_normed_histo(dist_d, bins)
    result = get_gauss_fit(hist, bin_edges)

    ax.bar(bin_edges[:-1], hist, width=(bin_edges[1]-bin_edges[0]), label='full set')
    #ax.bar(bin_edges[:-1], filtered, width=(bin_edges[1]-bin_edges[0]), label="w/o broken")
    ax.plot(bin_edges[:-1], result.best_fit, 'purple', label='best fit', alpha=0.5)

    ax.set_xlim(min(bin_edges), max(bin_edges))
    ax.set_ylim([0,0.35])
    #ax.set_xlabel("$\Delta$ (true - reco) [cm]")

    ax.grid()

    ax.set_axisbelow(True)
    #ax.legend()

    amp = result.params['amp']
    cen = result.params['cen']
    wid = result.params['wid']
    textstr = '$\mu = {:03.2f} \pm {:03.2f} cm$\n' \
              '$\sigma = {:03.2f} \pm {:03.2f} cm$  '.format(cen.value, cen.stderr, wid.value, wid.stderr)

    #anchored_text = AnchoredText(textstr, loc=2)
    #ax.add_artist(anchored_text)

for idx in range(3):
    axes[idx][0].set_ylabel('$\Delta x = {} cm$'.format(drx3[idx]))
    axes[0][idx].set_title('$\Delta z = {} cm$'.format(drx1[idx]))
    axes[2][idx].set_xlabel("$\Delta_{cross}$ [cm]")

#plt.tight_layout()
plt.show()
