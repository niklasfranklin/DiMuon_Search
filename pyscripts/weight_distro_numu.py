import numpy as np
import matplotlib.pyplot as plt
from icecube import icetray, dataio, simclasses, dataclasses
from matplotlib import colors
import pdbpp


d_energies = []
numu_energies = []

for i in range(100):
    filename = f"/n/holylfs05/LABS/arguelles_delgado_lab/Everyone/miaochenjin/DBSearch/SIREN_outputs/0625_NuMu_charm_astro_volume_1e2-1e6/simulation/0625_NuMu_charm_astro_volume_1e2-1e6_seed_{i}_L2Level.zst"
    if i == 334 or i == 641 or i == 801 or i == 807 or i == 893:
        continue

    f = dataio.I3File(filename)
    while f.more():
        frame = f.pop_frame()
        if frame.Stop == icetray.I3Frame.DAQ:
            tree = frame["I3MCTree_preCMC"]
            found = False
            for d in tree:
                
                # Checking for d mesons. In case of a d meson, gets the numu energy, gets the primary muon and its energy
                if (d.pdg_encoding == 411 or 
                d.pdg_encoding == -411  or 
                d.pdg_encoding == 421 or 
                d.pdg_encoding == -421):
                    found = True
                    continue

            if not found: 
                print(tree)
                breakpoint()
            d = tree.get_particle(d)
            d_energies.append(d.energy)
            numu = tree.primaries[0]
            numu_energies.append(numu.energy)
            break

# Plotting Histogram
print(len(numu_energies), len(d_energies))
events = len(numu_energies)
fig, ax = plt.subplots()

ax.hist(numu_energies, bins=np.logspace(np.log10(1),np.log10(1e6), 10), color ='yellow',edgecolor='red', label =r'$\nu_\mu$', histtype='step',density=True,stacked=True)
ax.hist(d_energies, bins=np.logspace(np.log10(1),np.log10(1e6), 10), color ='blue', edgecolor='black', label=r'$D$', histtype='step',density=True,stacked=True)
ax.set_xscale('log')
# plt.figure(figsize=(8,6))
# plt.hist(numu_energies, bins=np.logspace(np.log10(1),np.log10(1e6), 10), color ='green',edgecolor='black', label =r'$\nu_\mu$',alpha=0.5)
# plt.hist(d_plus_energies, bins=np.logspace(np.log10(1),np.log10(1e6), 10), color ='green', edgecolor='black', label=r'$D^+,D^-,D^0,D^{0-}$')
# plt.xscale('log')
ax.set_xlabel('Energy (GeV)')
ax.set_ylabel("Counts")
plt.title(f'Energy Distribution of Outgoing Secondary Muon vs Incoming Neutrino\n(Events: {events})')
plt.legend()
plt.savefig("weightplot")