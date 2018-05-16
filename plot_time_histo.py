import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
import numpy as np
from numpy import sqrt, pi, exp

from matplotlib.offsetbox import AnchoredText

from lmfit import  Model
import matplotlib
font = {'family' : 'normal',
        'size'   : 25}

matplotlib.rc('font', **font)

def gaussian(x, amp, cen, wid):
    "1-d gaussian: gaussian(x, amp, cen, wid)"
    return (amp/(sqrt(2*pi)*wid)) * exp(-(x-cen)**2 /(2*wid**2))

res = np.load('/home/matthias/workspace/larana/projects/out/time-histo/histo-more.npy')

maximas = np.concatenate(res, axis=1)

w = np.arange(0,3456)
b = np.ones(maximas.shape)
x = np.transpose(w * b.T)
loc = list(range(250,3456,250))

fig, ax = plt.subplots(figsize=(15,7))

plt.hist2d(x.flatten(), maximas.flatten(), bins=(3456, 2000))
plt.ylim([950, 1100])
plt.colorbar(label='N')
plt.xlabel('Wire')
plt.ylabel('ADC tick')


labels = list(range(len(loc)))
print(labels)
for x, y, s in zip(loc, len(loc)*[951], labels):
    print(x)
    ax.text(x+10,y,str(s), size=25, color='w')

plt.vlines(loc, 950, 1100, linestyles='dashed', colors='white')
fig.tight_layout()
plt.show()

exit()

loc = [500, 2000, 3000]
lo = [1,2,2]
for i, l in enumerate(loc):
    fig, ax = plt.subplots(figsize=(10,10))

    n, bins, patches = ax.hist(maximas[l], bins=2000)



    gmodel = Model(gaussian)
    result = gmodel.fit(n, x=bins[:-1],amp=400, cen=998, wid=10)

    plt.plot(bins[:-1], result.best_fit, 'r-')

    ax.set_xlim([950, 1100])
    print(result.fit_report())
    ax.set_xlabel('ADC Tick')
    ax.set_ylabel('N')

    amp = result.params['amp']
    cen = result.params['cen']
    wid = result.params['wid']

    textstr = 'amp: {:03.2f} +/- {:03.2f}\n' \
              'cen: {:03.2f} +/- {:03.2f}\n' \
              'wid: {:03.2f} +/- {:03.2f}'.format(amp.value, amp.stderr, cen.value, cen.stderr, wid.value, wid.stderr)

    # these are matplotlib.patch.Patch properties
    #props = dict(boxstyle='round', facecolor=None, alpha=0.5)
    # place a text box in upper left in axes coords
    #ax.text(0.05, 0.95, textstr, transform=ax.transAxes,
    #        verticalalignment='top', bbox=props)

    anchored_text = AnchoredText(textstr, loc=lo[i])
    ax.add_artist(anchored_text)

    amp = result.params['amp']
    print(amp.value)
    ax.grid()
    ax.set_axisbelow(True)
    fig.tight_layout()
    plt.show()





