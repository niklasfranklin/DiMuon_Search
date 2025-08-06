import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors
import h5py

# This script is used for creating a 2d histogram of the incoming neutrino energy and opening angle between the two outgoing muons.
# The plot is column normalized.

f = h5py.File('dimuon_volume_L2.h5', 'r')

numu_energies = list(f['numu_energies'])
mu_1_energies = list(f['mu_1_energies'])
mu_2_energies = list(f['mu_2_energies'])
angles = list(f['angles'])
weights = list(f['weights'])

events = len(numu_energies)
angles = np.rad2deg(angles)
energy_bins = [np.logspace(np.log10(1e2),np.log10(1e6), 50),np.linspace(0,5,10)]

fig, ax = plt.subplots(layout='constrained')

H, x_edges, y_edges = np.histogram2d(numu_energies,angles,bins=energy_bins)
col_sums = H.sum(axis=1)          
col_sums[col_sums == 0] = 1
H_norm = H.T / col_sums
masked = np.ma.masked_where(H_norm == 0, H_norm)
X, Y = np.meshgrid(x_edges, y_edges)

im = ax.pcolormesh(X, Y, masked,shading='flat')

ax.set_xscale('log')
ax.set_xlabel(r'$\nu_{\mu}$ Energy (GeV)')
ax.set_ylabel(r'$\theta_{\mu\mu}$ (deg$^\circ$)')
ax.set_yticks(ticks=np.arange(0,6,1))
cbar = plt.colorbar(im,ax=ax,ticks=np.arange(0,1,0.1))
ax.set_title(f'Incoming Neutrino Energy vs Opening Angle\n(Events: {events})')
plt.savefig('nuenergy_angle_normalized_2dhistogram') 