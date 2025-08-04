import numpy as np
import nuflux as nf
import h5py
import matplotlib.pyplot as plt

Phi = []
nu_cos_zenith = []
nu_flux = []

f = h5py.File('dimuon_ranged_L2.h5', 'r')

flux = nf.makeFlux('honda2006')
nu_type = nf.NuMu

nu_energy = list(f['numu_energies']) # in GeV
Phi = list(f['Phi'])

# breakpoint()

for i in range(len(nu_energy)):
 nu_flux.append(((nu_energy[i])**3)*Phi[i])

energy_bins = np.logspace(np.log10(1e2),np.log10(1e6), 50)

fig, ax = plt.subplots(layout='constrained')
# ax.hist(nu_energy,bins=energy_bins,weights=Phi,histtype='step',log=True,linestyle='--')
ax.scatter(nu_energy,nu_flux)
ax.set_xscale('log')
ax.set_yscale('log')
ax.set_xlabel(r'$E_\nu$ (GeV)')
ax.set_ylabel(r'$E^{3}_{\nu}$d$\Phi$')
plt.savefig('nuflux')
breakpoint()