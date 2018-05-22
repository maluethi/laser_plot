import numpy as np
import matplotlib.pyplot as plt
import scipy.fftpack

import nfft

f1 = 50
f2 = 1

# Number of samplepoints
N = 1200
# sample spacing
T = 1.0 / 800.0
x = np.linspace(0.0, N*T, N)
y = np.sin(f1 * 2.0*np.pi*x) + 0.5*np.sin(f2 * 2.0*np.pi*x)
yf = scipy.fftpack.fft(y)
xf = np.linspace(0.0, 1.0/(2.0*T), N/2)

ynf = nfft.nfft_adjoint(x,y,N)

fig, ax = plt.subplots(2,1)
ax[0].plot(x,y)
ax[1].plot(xf, 2.0/N * np.abs(yf[:N//2]))
ax[1].plot(np.abs(ynf/1000)[N/2:])
plt.show()