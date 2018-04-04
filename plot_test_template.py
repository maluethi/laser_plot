import matplotlib.pyplot as plt
import numpy as np

plt.style.use('./mythesis.mplstyle')
x = np.linspace(0,2*np.pi, 100)
y = np.sin(x)

fig, ax = plt.subplots(2, 1)

ax[0].plot(x, np.sin(x))
ax[1].plot(x, np.cos(x))

ax[1].set_xlabel('Phase')
for a in ax:
    a.set_ylabel('Ampli')

plt.show()
