import numpy as np
import matplotlib.pyplot as plt
import glob
from matplotlib import colors
from icecube import icetray, dataio, simclasses, dataclasses
import h5py

f = h5py.File('dimuon_truthinfo.h5', 'r')

numu_energies = list(f['numu_energies'])
mu_1_energies = list(f['mu_1_energies'])
mu_2_energies = list(f['mu_2_energies'])
angles = list(f['angles'])
weights = list(f['weights'])

# # Normalized 2D Histogram Plots (Percentages)
print(len(mu_2_energies))
events = len(numu_energies)
angles = np.rad2deg(angles)
fig, ax2 = plt.subplots(layout='constrained')
H, x_edges, y_edges = np.histogram2d(mu_1_energies,mu_2_energies,bins=[np.logspace(np.log10(1),np.log10(1e6),50),np.logspace(np.log10(1),np.log10(1e6),50)],density=False,weights=weights)
#H, x_edges, y_edges = np.histogram2d(numu_energies,angles,bins=[np.logspace(np.log10(1e2),np.log10(1e6), 50),np.linspace(0,5,10)])
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
#ax2.set_ylabel('Angle (deg)')
ax2.set_yticks(ticks=np.logspace(np.log10(1e2),np.log10(1e6), 50),minor=True)
#ax2.set_yticks(ticks=np.arange(0,6,1))
cbar = plt.colorbar(im,ax=ax2,label=r'Neutrinos$(s^{-1})$')
ax2.set_title(f'Primary vs Secondary Muon Energy\n(Events: {events})')
plt.savefig('muons') 