import numpy as np
from scipy.stats import chisquare
import matplotlib.pyplot as plt
from lmfit import  Model
from matplotlib.offsetbox import AnchoredText

def gaussian(x, amp, cen, wid):
    "1-d gaussian: gaussian(x, amp, cen, wid)"
    return (amp/(np.sqrt(2*np.pi)*wid)) * np.exp(-(x-cen)**2 /(2*wid**2))

plt.style.use('./mythesis.mplstyle')

def get_normed_histo(data):
    hist, bin_edges = np.histogram(data, bins, range=rng)
    hist = np.divide(hist, np.sum(hist))
    return hist, bin_edges

def get_gauss_fit(hist, edges):
    gmodel = Model(gaussian)
    result = gmodel.fit(hist, x=edges[:-1], amp=1, cen=0, wid=2)
    return result

# Test plot
n_tot = 4785
n_sel = 3382

maxi = 1000
scale = 6
np.random.seed(4)
p0 = 1.2 * np.random.randn(maxi)
p1 = 0.4 * np.random.randn(50/1000 * maxi) - 2.6
p1 = 0.2 * np.random.randn(80/1000 * maxi) - 2.6
p2 = 0.8 * np.random.randn(100/1000 * maxi) + 3.5
p25 = 0.1 * np.random.randn(10/1000 * maxi) + 3.5
p3 = - np.abs(10 * np.random.randn(300/1000 * maxi))
p4 = np.abs(4 * np.random.randn(10/1000 * maxi))


mask_h = np.tanh(np.linspace(-20,3, 60))/2. + 0.45
mask_l = np.tanh(np.linspace(-5,3, 60))/2. + 0.45
mask = np.concatenate((mask_h, mask_l[::-1]))

all = np.concatenate((p0, p1, p2, p25, p3, p4))
# end test
rng = [-2, 2]
bins = 20*2

# Chi squared
fig, axes = plt.subplots(1,2, sharey=True, figsize=[4.670, 3])

for dx, ax in zip(('0', '+1'), axes):
    df = np.load('output/cross_dist/dist-{}.npy'.format(dx)).flatten()
    hist, bin_edges = get_normed_histo(df)
    result = get_gauss_fit(hist, bin_edges)

    ax.bar(bin_edges[:-1], hist, width=(bin_edges[1]-bin_edges[0]), label='full set')
    #ax.bar(bin_edges[:-1], filtered, width=(bin_edges[1]-bin_edges[0]), label="w/o broken")
    ax.plot(bin_edges[:-1], result.best_fit, 'purple', label='best fit', alpha=0.5)

    ax.set_xlim(min(bin_edges), max(bin_edges))
    ax.set_ylim([0,0.3])
    ax.set_xlabel("$\Delta$ (true - reco) [cm]")

    ax.grid()
    ax.set_title('$\Delta x = {} cm$'.format(dx))
    ax.set_axisbelow(True)
    #ax.legend()

    amp = result.params['amp']
    cen = result.params['cen']
    wid = result.params['wid']
    textstr = '$\mu = {:03.2f} \pm {:03.2f} cm$\n' \
              '$\sigma = {:03.2f} \pm {:03.2f} cm$  '.format(cen.value, cen.stderr, wid.value, wid.stderr)

    #anchored_text = AnchoredText(textstr, loc=2)
    #ax.add_artist(anchored_text)

axes[0].set_ylabel("density")

plt.tight_layout()
plt.show()
