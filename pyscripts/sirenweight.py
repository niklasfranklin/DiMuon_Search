import numpy as np
import matplotlib.pyplot as plt
import glob
from matplotlib import colors
from icecube import icetray, dataio, simclasses, dataclasses
import h5py
#import pdbpp

f = h5py.File('dimuon_ranged_X.h5', 'r')

numu_energies = list(f['numu_energies'])
mu_1_energies = list(f['mu_1_energies'])
mu_2_energies = list(f['mu_2_energies'])
angles = list(f['angles'])
weights = list(f['weights'])

events = len(numu_energies)
angles = np.rad2deg(angles)

fig, ax = plt.subplots(layout='constrained')

energy_bins = np.logspace(np.log10(5e2),np.log10(1e4), 14)
angle_bins = np.linspace(0,15,40)

H, x_edges, y_edges = np.histogram2d(numu_energies,angles,bins=[energy_bins,angle_bins],weights=weights)

x_centers = (x_edges[:-1] + x_edges[1:]) / 2
y_centers = (y_edges[:-1] + y_edges[1:]) / 2

col_sums = H.sum(axis=1)          
col_sums[col_sums == 0] = 1
H_norm = H.T / col_sums

median_cumsum = []
top_cumsum = [] 
bottom_cumsum = []
H_sum =  []
# breakpoint()
for i in range(np.shape(H_norm)[1]):
    H_sum.append(sum(H_norm[:,i]))
    cumsum = np.cumsum(H_norm[:,i])
    index = np.where(cumsum > 0.5)[0][0]
    median_cumsum.append(angle_bins[index])
    index = np.where(cumsum > 0.01)[0][0]
    bottom_cumsum.append(angle_bins[index])
    index = np.where(cumsum > 0.99)[0][0]
    top_cumsum.append(angle_bins[index])
# breakpoint()
masked = np.ma.masked_where(H.T == 0, H.T)
X, Y = np.meshgrid(x_edges, y_edges)
im = ax.pcolormesh(X, Y, masked,norm=colors.SymLogNorm(linthresh=1e-10))
ax.plot(x_centers,top_cumsum,c="r",linestyle="dashed",label='98%')
ax.plot(x_centers,median_cumsum,c='r',marker='o',label='Median')
ax.plot(x_centers,bottom_cumsum,c="r",linestyle="dashed",label='1%')
ax.set_xscale('log')
ax.set_xlabel(r'$\nu_\mu$ Energy (GeV)')
ax.set_ylabel(r'Angles (deg)')
cbar = plt.colorbar(im,ax=ax,label=r'Event Rate $(s^{-1})$')
ax.set_title(f'Neutrino Energy vs Opening Angle (BDT Volume)\n[Events: {events}]')
ax.legend()
plt.savefig('siren')