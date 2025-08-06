import numpy as np
import matplotlib.pyplot as plt
import h5py

def divide(x,d):
    q = []
    for i in range(len(x)):
        q.append(x[i]/d)
    return q

def sec_tenyears(x):
 sec = 3.1536e8
 y = round(sum(x)*sec,2)
 return y

def atmos(x):
    e = []
    for i in range(len(x)):
        e.append(4.8e-8*(x[i]/100)**-3.7)
    return e

def astro(x):
    e = []
    for i in range(len(x)):
        e.append(1.68e-18*(x[i]/1e5)**-2.58)
    return e

def reweigh(x,y,z):
    e = []
    for i in range(len(x)):
        e.append(((x[i]/y[i])+1)*z[i])
    return e

f_L1 = h5py.File('dimuon_ranged_L1.h5', 'r')
f_L2 = h5py.File('dimuon_ranged_L2.h5', 'r')
f_Det = h5py.File('dimuon_ranged_Det.h5', 'r')
f_X = h5py.File('dimuon_ranged_X.h5', 'r')
f_BDT = h5py.File('dimuon_ranged_BDT.h5', 'r')

numu_E_L1 = list(f_L1['numu_energies'])
numu_E_L2 = list(f_L2['numu_energies'])
numu_E_Det = list(f_Det['numu_energies'])
numu_E_X = list(f_X['numu_energies'])
numu_E_BDT = list(f_BDT['numu_energies'])

mu1_E_L2 = list(f_L2['mu_1_energies'])
mu2_E_L2 = list(f_L2['mu_2_energies'])

theta_L1 = np.rad2deg(list(f_L1['angles']))
theta_L2 = np.rad2deg(list(f_L2['angles']))
theta_Det = np.rad2deg(list(f_Det['angles']))
theta_X = np.rad2deg(list(f_X['angles']))
theta_BDT = np.rad2deg(list(f_BDT['angles']))

S_max_L2 = list(f_L2['S_max'])

w_L1 = divide(list(f_L1['weights']),1989)
w_L2 = divide(list(f_L2['weights']),1989)
w_Det = divide(list(f_Det['weights']),1989)
w_X = divide(list(f_X['weights']),1989)
w_BDT = divide(list(f_BDT['weights']),1989)

w_new_L1 = reweigh(atmos(numu_E_L1),astro(numu_E_L1),w_L1)
w_new_L2 = reweigh(atmos(numu_E_L2),astro(numu_E_L2),w_L2)
w_new_Det = reweigh(atmos(numu_E_Det),astro(numu_E_Det),w_Det)
w_new_X = reweigh(atmos(numu_E_X),astro(numu_E_X),w_X)
w_new_BDT = reweigh(atmos(numu_E_BDT),astro(numu_E_BDT),w_BDT)

energy_bins = np.logspace(np.log10(1e2),np.log10(1e6), 50)
angle_bins = np.linspace(0,40,41)
sep_bins = np.linspace(0,120,25)

fig, ax = plt.subplots(layout='constrained')
# breakpoint()
# ax.hist(S_max_L2,bins=sep_bins,edgecolor='r',histtype='step',label='Charm Dimuon (Max. Sep.)',weights=w_new_L2,log=True)
# ax.hist(theta_L1,bins=angle_bins,edgecolor='b',histtype='step',label=f'L1Level',linestyle='-',weights=w_new_L1,log=True)
ax.hist(theta_L2,bins=angle_bins,edgecolor='r',histtype='step',label='L2Level',linestyle='-',weights=w_new_L2,log=True)
ax.hist(theta_X,bins=angle_bins,edgecolor='g',histtype='step',label=f'XLevel',linestyle='-',weights=w_new_X)
ax.hist(theta_BDT,bins=angle_bins,edgecolor='k',histtype='step',label=f'BDT Reco',linestyle=':',weights=w_new_BDT)
# ax.set_yscale('log')
ax.set_xlabel(r'$\theta_{\mu\mu}$ (deg$^\circ$)')
# ax.set_xlabel(r'Double Track Separation (m)')
ax.set_ylabel(r'Event Rate (Predicted) $(s^{-1})$')
ax.set_title('Simulated Dimuon Events for L2,XLevel')
ax.grid()
ax.legend()
plt.savefig('reangle')
# breakpoint()