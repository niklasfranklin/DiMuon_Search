import numpy as np
import nuflux as nf
import matplotlib.pyplot as plt
import h5py

# This script produces a 1D histogram that models the event rate as a function of incoming neutrino energy. There are multiple series, each representing a
# level of processing.

f_L1 = h5py.File('dimuon_volume_L1.h5', 'r')
f_L2 = h5py.File('dimuon_volume_L2.h5', 'r')
f_Det = h5py.File('dimuon_volume_Det.h5', 'r')
f_X = h5py.File('dimuon_volume_X.h5', 'r')
f_BDT = h5py.File('dimuon_volume_BDT.h5', 'r')

numu_E_L1 = list(f_L1['numu_energies'])
numu_E_L2 = list(f_L2['numu_energies'])
numu_E_Det = list(f_Det['numu_energies'])
numu_E_X = list(f_X['numu_energies'])
numu_E_BDT = list(f_BDT['numu_energies'])

Phi_L1 = list(f_L1['Phi'])
Phi_L2 = list(f_L2['Phi'])
Phi_Det = list(f_Det['Phi'])
Phi_X = list(f_X['Phi'])
Phi_BDT = list(f_BDT['Phi'])

flux = nf.makeFlux('honda2006')
nu_type = nf.NuMu

def divide(x,d):
    q = []
    for i in range(len(x)):
        q.append(x[i]/d)
    return q

def sum10(x):
 sec = 3.1536e8
 y = round(sum(x)*sec)
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

w_Det = divide(list(f_Det['weights']),1989)
w_L1 = divide(list(f_L1['weights']),1989)
w_L2 = divide(list(f_L2['weights']),1989)
w_X = divide(list(f_X['weights']),1989)
w_BDT = divide(list(f_BDT['weights']),1989)

w_new_Det = reweigh(Phi_Det,astro(numu_E_Det),w_Det)
w_new_L1 = reweigh(Phi_L1,astro(numu_E_L1),w_L1)
w_new_L2 = reweigh(Phi_L2,astro(numu_E_L2),w_L2)
w_new_X = reweigh(Phi_X,astro(numu_E_X),w_X)
w_new_BDT = reweigh(Phi_BDT,astro(numu_E_BDT),w_BDT)

energy_bins = np.logspace(np.log10(1e2),np.log10(1e6), 21)

fig, ax = plt.subplots(layout='constrained')

ax.hist(numu_E_Det,bins=energy_bins,edgecolor='k',histtype='step',label=f'DetLevel ({sum10(w_new_Det)})',linestyle=':',weights=w_new_Det,log=True)
ax.hist(numu_E_L1,bins=energy_bins,edgecolor='b',histtype='step',label=f'L1Level ({sum10(w_new_L1)})',linestyle='-',weights=w_new_L1,log=True,alpha=0.35)
ax.hist(numu_E_L2,bins=energy_bins,edgecolor='r',histtype='step',label=f'L2Level ({sum10(w_new_L2)})',linestyle='-',weights=w_new_L2,log=True)
ax.hist(numu_E_X,bins=energy_bins,edgecolor='g',histtype='step',label=f'XLevel ({sum10(w_new_X)})',linestyle='-',weights=w_new_X,log=True)
ax.hist(numu_E_BDT,bins=energy_bins,edgecolor='orange',histtype='step',label=f'BDT Reco ({sum10(w_new_BDT)})',linestyle='-',weights=w_new_BDT,log=True)

ax.set_xscale('log')
ax.set_xlabel(r'$\nu_\mu$ Energy (GeV)')
ax.set_ylabel(r'Event Rate $(s^{-1})$')
ax.set_title('Volume Injection')
ax.legend(title='Events')
ax.grid(linestyle='--',alpha=0.6)
plt.savefig('level_weights')         


    