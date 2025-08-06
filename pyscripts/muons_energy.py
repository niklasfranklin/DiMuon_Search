import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors
import h5py

# This scirpt plots the secondary outgoing muon energy as a function of the primary outgoing muon energy.

f = h5py.File('dimuon_volume_L2.h5', 'r')

numu_energies = list(f['numu_energies'])
mu_1_energies = list(f['mu_1_energies'])
mu_2_energies = list(f['mu_2_energies'])
angles = list(f['angles'])
weights = list(f['weights'])

events = len(numu_energies)
angles = np.rad2deg(angles)

energy_range = np.logspace(np.log10(10),np.log10(1e6),50)
energy_bins = [energy_range,energy_range]

fig, ax2 = plt.subplots(layout='constrained')

H, x_edges, y_edges = np.histogram2d(mu_1_energies,mu_2_energies,bins=energy_bins,density=False,weights=weights)
col_sums = H.sum(axis=1)          
col_sums[col_sums == 0] = 1
H_norm =(H.T/col_sums)
masked = np.ma.masked_where(H_norm== 0, H_norm)
X, Y = np.meshgrid(x_edges, y_edges)
im = ax2.pcolormesh(X, Y, masked,shading='flat',norm=colors.SymLogNorm(linthresh=1e-10))

ax2.set_xscale('log')
ax2.set_yscale('symlog')
ax2.set_xlabel(r'$\mu_1$ Energy (GeV)')
ax2.set_ylabel(r'$\mu_2$ Energy (GeV)')
ax2.set_yticks(ticks=np.logspace(np.log10(1e2),np.log10(1e6), 50),minor=True)

cbar = plt.colorbar(im,ax=ax2,label=r'Event Rate $(s^{-1})$')

ax2.set_title(f'Primary vs Secondary Muon Energy\n(Events: {events})')
plt.savefig('muons') 