import matplotlib.pyplot as plt
import argparse
import numpy as np
from numpy import sqrt, pi, exp
import nfft

from larana import lar_utils as laru
import matplotlib as mpl
import matplotlib.cm as cm
from mpl_toolkits.axes_grid1 import make_axes_locatable


parser = argparse.ArgumentParser(description='Plotting Time Histograms')
parser.add_argument('-p', dest='prod', action='store_true', default=False, help='production')
args = parser.parse_args()

plt.style.use('./mythesis.mplstyle')

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
tm = np.mean(t)
t = (t - tm)/t[-1]
stepsize = 100
wires = list(range(0, 3456, stepsize))

N=len(maximas[0])
pow = np.zeros((750,))
fig, ax = plt.subplots(2,1)
b=0
for i in wires:
    try:
        tst = maximas[i]
        msk = np.isinf(tst)
        tstm = tst[~msk]
        tstm = (tstm - np.mean(tstm)) / (np.max(tstm) - np.min(tstm))
        ff = nfft.nfft_adjoint(t[~msk], tst[~msk],N)
    except:
        continue
    #plt.plot(ff.real[N/2:])
    pow = pow + ff.real[N/2:]
    ax[0].plot(tst + b)
    ax[1].plot(ff.real[N/2:] + b*100)
    b += 10

ax[1].set_xlim([0,100])
plt.show()