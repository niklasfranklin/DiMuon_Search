import numpy as np
import matplotlib.pyplot as plt
import h5py

# This script is used for measuring the incoming neutrino energies that carry over between processing levels.

def divide(x,d):
    q = []
    for i in range(len(x)):
        q.append(x[i]/d[i])
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
        e.append(((x[i]/y[i]))*z[i])
    return e

f_L1 = h5py.File('dimuon_volume_L1.h5', 'r')
f_L2 = h5py.File('dimuon_volume_L2.h5', 'r')
f_Det = h5py.File('dimuon_volume_Det.h5', 'r')
f_X = h5py.File('dimuon_ranged_X.h5', 'r')
f_BDT = h5py.File('dimuon_volume_BDT.h5', 'r')

numu_E_L1 = list(f_L1['numu_energies'])
numu_E_L2 = list(f_L2['numu_energies'])
numu_E_Det = list(f_Det['numu_energies'])
numu_E_X = list(f_X['numu_energies'])
numu_E_BDT = list(f_BDT['numu_energies'])

energy_bins = np.logspace(np.log10(1e2),np.log10(1e6),15)

counts_Det, bin_edges_Det = np.histogram(numu_E_Det,bins=energy_bins)
counts_L1, bin_edges_L1 = np.histogram(numu_E_L1,bins=energy_bins)
counts_L2, bin_edges_L2 = np.histogram(numu_E_L2,bins=energy_bins)
counts_X, bin_edges_X = np.histogram(numu_E_X,bins=energy_bins)
counts_BDT, bin_edges_BDT = np.histogram(numu_E_BDT,bins=energy_bins)

epsilon_astro_DetL1 = divide(counts_L1,counts_Det)
epsilon_astro_L1L2 = divide(counts_L2,counts_L1)
epsilon_astro_L2X = divide(counts_X,counts_L2)
epsilon_astro_XBDT = divide(counts_BDT,counts_X)
epsilon_astro_f = divide(counts_BDT,counts_Det)

fig,ax = plt.subplots(layout='constrained')

ax.plot(bin_edges_L2[:-1],epsilon_astro_DetL1,label=r'$\epsilon_{Det \to L1}$',c='b',linestyle='-')
ax.plot(bin_edges_L2[:-1],epsilon_astro_L1L2,label=r'$\epsilon_{L1 \to L2}$',c='r',linestyle='-')
ax.plot(bin_edges_L2[:-1],epsilon_astro_L2X,label=r'$\epsilon_{L2 \to X}$',c='g',linestyle='-')
ax.plot(bin_edges_L2[:-1],epsilon_astro_XBDT,label=r'$\epsilon_{X \to BDT}$',c='orange',linestyle='-')
ax.plot(bin_edges_L2[:-1],epsilon_astro_f,label=r'$\epsilon_{f}$',c='k',linestyle='-.')

ax.set_xscale('log')
ax.set_xlabel(r'$E_\nu$ (GeV)')
ax.set_ylabel(r'Relative Efficiency $\epsilon^{rel}_{i}$')
ax.legend()
ax.grid(linestyle='--',alpha=0.6)
ax.set_title('Volume Efficiency')
plt.savefig('energyeff_volume')