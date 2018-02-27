import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
import numpy as np
from numpy import sqrt, pi, exp

from matplotlib.offsetbox import AnchoredText

from lmfit import  Model
import matplotlib

def gaussian(x, amp, cen, wid):
    "1-d gaussian: gaussian(x, amp, cen, wid)"
    return (amp/(sqrt(2*pi)*wid)) * exp(-(x-cen)**2 /(2*wid**2))

res = np.load('/home/matthias/workspace/larana/projects/out/time-histo/histo-more.npy')

maximas = np.concatenate(res, axis=1)

w = np.arange(0,3456)
b = np.ones(maximas.shape)
x = np.transpose(w * b.T)

fig, ax = plt.subplots(figsize=(10,10))
for sl in range(0,3456,250):
    ax.plot(maximas[sl], 'x')
    ax.set_ylim([950, 1150])
plt.show()