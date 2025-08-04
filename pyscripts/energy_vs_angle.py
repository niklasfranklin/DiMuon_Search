import numpy as np
import matplotlib.pyplot as plt
import glob
from matplotlib import colors
from icecube import icetray, dataio, simclasses, dataclasses
import h5py
import pdbpp

f = h5py.File('dimuon_truthinfo.h5', 'r')

numu_energies = list(f['numu_energies'])
mu_1_energies = list(f['mu_1_energies'])
mu_2_energies = list(f['mu_2_energies'])
angles = list(f['angles'])
weights = list(f['weights'])

### Column Normalized 2D Histogram Plots (Percentages)

events = len(numu_energies)
angles = np.rad2deg(angles)
fig, ax2 = plt.subplots(layout='constrained')

H, x_edges, y_edges = np.histogram2d(numu_energies,angles,bins=[np.logspace(np.log10(1e2),np.log10(1e6), 50),np.linspace(0,5,10)])
#h = bin_edges = np.histogram(numu_energies,bins=[np.logspace(np.log10(1e2),np.log10(1e6), 50),np.linspace(0,5,10)])

col_sums = H.sum(axis=1)          
col_sums[col_sums == 0] = 1
H_norm = H.T / col_sums
masked = np.ma.masked_where(H_norm == 0, H_norm)
X, Y = np.meshgrid(x_edges, y_edges)
im = ax2.pcolormesh(X, Y, masked,shading='flat')
ax2.set_xscale('log')
ax2.set_xlabel(r'$\mu_2$ Energy (GeV)')
ax2.set_ylabel('Angles (deg)')
ax2.set_yticks(ticks=np.arange(0,6,1))
cbar = plt.colorbar(im,ax=ax2,ticks=np.arange(0,1,0.1))
ax2.set_title(f'Secondary Muon Energy vs Opening Angle\n(Events: {events})')
plt.savefig('test') 
breakpoint()
### 1D Histogram Plot