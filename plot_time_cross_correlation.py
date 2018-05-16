import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
import numpy as np
from numpy import sqrt, pi, exp

from matplotlib.offsetbox import AnchoredText

from lmfit import  Model
import matplotlib
from larana import lar_utils as laru


res = np.load('/home/matthias/workspace/larana/projects/out/time-histo/histo-more-maxima.npy')

# Sort the input


srt = np.argsort(res[:,3])
res = res[srt]

maximas = np.concatenate(res[:,0], axis=1) + 900
error = np.concatenate(res[:,1], axis=1)

mm = np.sum(maximas, axis=0).shape

freq = 0.25
n_max = maximas.shape[1]
t = np.arange(0, n_max/freq, 1/freq)


stepsize = 50
loc = list(range(0,3456,stepsize))
labels = list(range(len(loc)))

fig, ax = plt.subplots(figsize=(10,10))
for sl, lbl in zip(range(250,3456,stepsize), labels):
    print(sl)
    ax.plot(t, maximas[sl], 'x', label=lbl)


ax.set_ylim([960, 1100])
ax.set_xlim([0, t[-1]])

plt.xlabel("t [s]")
plt.ylabel("ADC Tick")
#plt.legend(ncol=7, framealpha=1)
plt.show()