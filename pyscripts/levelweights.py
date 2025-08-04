import numpy as np
import matplotlib.pyplot as plt
from icecube import icetray, dataio, simclasses, dataclasses
import h5py
import pdbpp

def divide(x,d):
    q = []
    for i in range(len(x)):
        q.append(x[i]/d)
    return q

def sec_tenyears(x):
 sec = 3.1536e8
 y = round(sum(x)*sec,2)
 return y

f_L1 = h5py.File('dimuon_L1.h5', 'r')
f_L2 = h5py.File('dimuon_L2.h5', 'r')
f_Det = h5py.File('dimuon_Det.h5', 'r')
f_X = h5py.File('dimuon_XLevel.h5', 'r')
    
numu_energies_L1 = list(f_L1['numu_energies'])
numu_energies_L2 = list(f_L2['numu_energies'])
numu_energies_Det = list(f_Det['numu_energies'])

weights_L1 = list(f_L1['weights'])
weights_L2 = list(f_L2['weights'])
weights_Det = list(f_Det['weights'])

pred_weights_L1 = divide(list(f_L1['weights']),2000)
pred_weights_L2 = divide(list(f_L2['weights']),2000)
pred_weights_Det = divide(list(f_Det['weights']),2000)

energy_bins = np.logspace(np.log10(1e2),np.log10(1e6), 50)

fig, ax = plt.subplots(layout='constrained')


# ax.hist(numu_energies_L1,bins=energy_bins,edgecolor='b',histtype='step',label=f'L1Level ({sec_tenyears(pred_weights_L1)})',linestyle='-',weights=pred_weights_L1,log=True,alpha=0.35)
# ax.hist(numu_energies_L2,bins=energy_bins,edgecolor='r',histtype='step',label=f'L2Level ({sec_tenyears(pred_weights_L2)})',linestyle='-',weights=pred_weights_L2,log=True)
# ax.hist(numu_energies_Det,bins=energy_bins,edgecolor='k',histtype='step',label=f'DetLevel ({sec_tenyears(pred_weights_Det)})',linestyle=':',weights=pred_weights_Det,log=True)
ax.hist(numu_energies_Det,bins=energy_bins,edgecolor='k',histtype='step',label=f'DetLevel ({sec_tenyears(pred_weights_Det)})',linestyle=':',weights=pred_weights_Det,log=True)

ax.set_xscale('log')
# ax.set_yscale('symlog')
ax.set_xlabel(r'$\nu_\mu$ Energy (GeV)')
ax.set_ylabel(r'Events Per Second (Predicted) $(s^{-1})$')
ax.set_title('Simulated Dimuon Events for Levels L1,L2,Det')
ax.legend()
plt.savefig('level')
breakpoint()
