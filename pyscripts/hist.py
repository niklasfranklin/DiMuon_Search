import numpy as np
import matplotlib.pyplot as plt
import glob
from matplotlib import colors
from matplotlib.collections import LineCollection
from matplotlib.colors import ListedColormap, BoundaryNorm
from icecube import icetray, dataio, simclasses, dataclasses
import h5py
# import pdbpp

f = h5py.File('dimuon_truthinfo.h5', 'r')

numu_energies = list(f['numu_energies'])
mu_1_energies = list(f['mu_1_energies'])
mu_2_energies = list(f['mu_2_energies'])
angles = list(f['angles'])
weights = list(f['weights'])

events = len(numu_energies)
angles = np.rad2deg(angles)

energy_bins = np.logspace(np.log10(10),np.log10(1e6), 50)
angle_bins = np.linspace(0,180,10)

H,x_edges,y_edges,image = plt.hist2d(numu_energies,angles,bins=[energy_bins,angle_bins],weights=weights)

x_centers = (x_edges[:-1] + x_edges[1:]) / 2
y_centers = (y_edges[:-1] + y_edges[1:]) / 2

col_sums = H.sum(axis=1)          
col_sums[col_sums == 0] = 1
H_norm = H.T/col_sums

median_cumsum = []
top_cumsum = [] 
bottom_cumsum = []
median_weights = []
H_sum =  []

#breakpoint()
for i in range(np.shape(H_norm)[1]):
    H_sum.append(sum(H_norm[:,i]))
    cumsum = np.cumsum(H_norm[:,i])
    index = np.where(cumsum > 0.5)[0][0]
    median_cumsum.append(angle_bins[index])
    median_weights.append(weights[index])
    index = np.where(cumsum > 0.01)[0][0]
    bottom_cumsum.append(angle_bins[index])
    index = np.where(cumsum > 0.99)[0][0]
    top_cumsum.append(angle_bins[index])

fig, ax = plt.subplots()
ax.set_xscale('log')
H_new,x,y,i = plt.hist2d(x_centers,median_cumsum,bins=[energy_bins,angle_bins],weights=median_weights)
H_worm = H_new.T/col_sums
masked = np.ma.masked_where(H_worm == 0, H_worm)
X,Y = np.meshgrid(x,y)

ax.pcolormesh(X,Y,masked,shading='flat')
# ax.imshow(H,cmap='viridis')

# cbar = plt.colorbar(image,ax=ax)
ax.plot(x_centers,median_cumsum,c='red',marker='o')
ax.plot(x_centers,top_cumsum,c="white",linestyle="dashed")
ax.plot(x_centers,bottom_cumsum,c="white",linestyle="dashed")
ax.set_xscale('log')
# ax.set_xlabel(r'$\mu_2 ' \
#  '$ Energy (GeV)')
# ax.set_xlabel(r'$\nu_\mu' \
# '$ Energy (GeV)')
# ax.set_ylabel('Angles (deg)')
# ax.set_xticks(ticks=xcenters,minor=True)
# ax.set_title(f'Median Distribution of Angles for NuMu Energy Range\n100 GeV to 10 TeV (Events: {events})')
plt.savefig('histogram')
breakpoint()