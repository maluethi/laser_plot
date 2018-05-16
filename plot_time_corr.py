import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.cm as cm

from mpl_toolkits.mplot3d import Axes3D
import numpy as np

# cmap stuff
cmap = cm.get_cmap('viridis')
norm = mpl.colors.Normalize(vmin=-500, vmax=500)
cm = cm.ScalarMappable(norm=norm, cmap=cmap)


data = np.load('/home/matthias/workspace/larana/projects/out/time-histo/time-corr.npz')
df = np.load('/home/matthias/workspace/larana/projects/out/time-histo/time-mean.npz')

wid = df['wid']
cen = df['cen']


stride = 1
maximas = data['max'][::stride]
dists = data['dist'][::stride]
wires = data['wire'][::stride]

print(wires.shape)
offsets = [w for w in range(-50,51)]

fig = plt.figure() #.subplots(1, 1)
ax = fig.add_subplot(111, projection='3d')

stride_corr = 50
for idx, (dist, maxima, wire) in enumerate(zip(dists, maximas, wires)):
    dist = dist[::stride_corr]
    maxima = maxima[::stride_corr]

    ax.scatter(idx*50*stride*np.ones(len(dist)), cen[wire] + dist, maxima, c=cm.to_rgba(offsets), alpha=0.2)
    #ax[0].plot(x, i + y, '*')
    #ax[0].plot(x, i + y_slice, '*')
    #ax[1].axvline(len(x))
wire_loc = np.linspace(0, 3455, len(cen))
print(wire_loc)
cset = ax.plot(wire_loc, cen, zdir='z')
ax.set_ylim([-700,700])
plt.show()