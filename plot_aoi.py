import matplotlib.pyplot as plt
import argparse
import csv
import numpy as np


parser = argparse.ArgumentParser(description='Plotting Time Histograms')
parser.add_argument('-p', dest='prod', action='store_true', default=False, help='production')
args = parser.parse_args()

plt.style.use('./mythesis.mplstyle')

basedir = '/home/matthias/Documents/thesis/gfx/LCS-System/aoi/'
files = ['average.csv', 's.csv', 'p.csv']
df = {'a': None, 's': None, 'p': None}
for fil in files:
    filename = basedir + fil
    d = np.genfromtxt(filename, delimiter=',',skip_header=1, usecols=[5,6] )

    reflec = d[:,1]
    angles = d[:,0]

    # Normalize and flip reflectivity
    max_r = np.min(reflec)
    reflec = (reflec - max_r)
    min_x = np.max(reflec)
    reflec = -reflec/min_x + 1

    # normalize angles
    angles = angles - angles[0]
    df[fil[0]] = (angles,reflec)

a = df['a']
s = df['s']
p = df['p']

print(a)

fig = plt.figure(figsize=(4.670, 3)) #.subplots(1, 1)
ax = fig.add_subplot(111)

ax.plot(a[0], a[1], label='average')
ax.plot(s[0], s[1], label='s-pol')
ax.plot(p[0], p[1], label='p-pol')

ax.set_xlim([0,90])
ax.set_xticks([0,30,60,90])

ax.set_ylim([0,1])

ax.set_xlabel('Angle of Incidence [$^\circ$]')
ax.set_ylabel('Reflectivity')
ax.legend(loc='lower left')

ax.grid(True)
fig.tight_layout()

if not args.prod:
    plt.show()
else:
    plt.savefig('./gfx/LCS-System/aoi/aoi.pdf')