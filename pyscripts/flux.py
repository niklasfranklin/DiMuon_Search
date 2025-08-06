import numpy as np
import nuflux as nf
import h5py
import matplotlib.pyplot as plt

# This scipt was only for testing the nuflux module. The honda2006 flux model is what is used for atmosphereic flux
# in the event rate level plots.

Phi = []
nu_cos_zenith = []
nu_flux = []

f = h5py.File('dimuon_ranged_L2.h5', 'r')

flux = nf.makeFlux('honda2006')
nu_type = nf.NuMu

nu_energy = list(f['numu_energies'])
Phi = list(f['Phi'])


for i in range(len(nu_energy)):
 nu_flux.append(((nu_energy[i])**3)*Phi[i])

energy_bins = np.logspace(np.log10(1e2),np.log10(1e6), 50)

fig, ax = plt.subplots(layout='constrained')
ax.scatter(nu_energy,nu_flux)
ax.set_xscale('log')
ax.set_yscale('log')
ax.set_xlabel(r'$E_\nu$ (GeV)')
ax.set_ylabel(r'$E^{3}_{\nu}$d$\Phi$')
plt.savefig('nuflux')