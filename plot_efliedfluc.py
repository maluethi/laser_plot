from larana.lar_utils import drift_speed
import numpy as np
import matplotlib.pyplot as plt

def E_approx(v, E0=0.273):
    v0 = drift_speed(E0)*1E-6
    return (v - v0) / m + E0

scale = 1E-6 # to mm
v_var = 0.02
v_var = 1.93/956

E0 = 0.273
v0 = drift_speed(E0) * scale

rng = 0.01
Em = (1-rng) * E0
Ep = (1+rng) * E0


dE = Ep - Em
dv = (drift_speed(Ep) - drift_speed(Em)) * scale

m = dv/dE
print(m)

E = np.linspace(0.1,0.5, 500)
v = drift_speed(E) * scale

v_approx = m*(E - E0) + v0

v_set = np.linspace(0.05,0.16,100)
Eapp = E_approx(v_set)

dvp = (1 + v_var) * v0
dvm = (1 - v_var) * v0
dva = (dvp - dvm)


Eappm = E_approx(dvm)
Eappp = E_approx(dvp)

sigma_E = (Eappp - Eappm) / E0
print(1/m *dva / E0)
print(sigma_E)


plt.plot(E, v)
#plt.plot(E, v_approx)
plt.plot(Eapp,v_set)
plt.vlines(E0, 0, drift_speed(E0)*scale)
plt.hlines(v0, 0, E0)
plt.hlines(dvp, 0, Eappp, 'red')
plt.hlines(dvm, 0, Eappm, 'red')


plt.xlim([0.1,0.5])
plt.ylim([0.05, v[-1]])
plt.show()
