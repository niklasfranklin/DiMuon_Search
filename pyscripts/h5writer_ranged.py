import numpy as np
import nuflux as nf
import glob
import os
from icecube import icetray, dataio, simclasses, dataclasses
import h5py
import pdbpp

# L1Level = []
# L2Level = []
# DetLevel = []

# sim = os.walk('/n/holylfs05/LABS/arguelles_delgado_lab/Everyone/miaochenjin/DBSearch/SIREN_outputs/0625_NuMu_charm_astro_volume_1e2-1e6/simulation/')
# for root,dir,files in sim:
#     for file in files:
# #         # if file.endswith('L1Level.zst'):
#         #     L1Level.append(file)
#         if file.endswith('L2Level.zst'):
#             L2Level.append(file)
#         # if file.endswith('DetLevel.zst'):
#         #     DetLevel.append(file)
# breakpoint()
for i in range(1):
    filename = f"/n/holylfs05/LABS/arguelles_delgado_lab/Everyone/miaochenjin/DBSearch/SIREN_outputs/0723_NuMu_charm_astro_ranged_1e2-1e6/simulation/0723_NuMu_charm_astro_ranged_1e2-1e6_seed_{i}_L2Level.zst"

# filenames=glob.glob(r"/n/holylfs05/LABS/arguelles_delgado_lab/Everyone/miaochenjin/DBSearch/SIREN_outputs/0723_NuMu_charm_astro_ranged_1e2-1e6/simulation/0723_NuMu_charm_astro_ranged_1e2-1e6_seed_**_L2Level.zst")

numu_energies = []
mu_1_energies = []
mu_2_energies = []
angles = []
Phi = []
S_max = []
weights = []

flux = nf.makeFlux('honda2006')
nu_type = nf.NuMu

# f = dataio.I3FrameSequence(filenames)
f = dataio.I3File(filename)

# breakpoint()
while f.more():
    frame = f.pop_frame()
    if frame.Stop == icetray.I3Frame.DAQ:
        frame.Put('A',dataclasses.I3Double(1))
        tree = frame["I3MCTree"]
        w = frame['SIREN_EventWeight']
        # numu_reco = frame['energy_reco_new']
        head = tree.get_head() 
        head_children = tree.children(head)
        head_child_pdg = head_children[0].pdg_encoding 
        head_child_energy = head_children[0].energy

        if head_child_pdg == 13 or head_child_pdg == -13:
                
            for d in head_children: 

                if (d.pdg_encoding == 411 or 
                d.pdg_encoding == -411  or 
                d.pdg_encoding == 421 or 
                d.pdg_encoding == -421):

                    for d_child in tree.children(d):

                        if d_child.pdg_encoding == 13 or d_child.pdg_encoding == -13 and d_child.energy > 10 and head_child_energy > 10:

                            mu_1_energies.append(head_child_energy)
                            mu_2_energies.append(d_child.energy)
                            numu = tree.primaries[0]
                            numu_energies.append(numu.energy)

                            mu_1 = head_children[0] 
                            mu_2 = d_child 

                            dir_1 = np.array([mu_1.dir.x,mu_1.dir.y,mu_1.dir.z])
                            dir_2 = np.array([mu_2.dir.x,mu_2.dir.y,mu_2.dir.z])
                            dot = np.dot(dir_1,dir_2)
                            angle = np.arccos(dot)
                            angles.append(angle)

                            L_mu1 = mu_1.pos.rho
                            L_mu2 = mu_2.pos.rho
                            cos = np.cos(angle)
                            S_max.append(np.sqrt((L_mu1**2+L_mu2**2)-(2*L_mu1*L_mu2*cos)))
                            # S_max.append(L_mu2*np.tan(angle))
                            # S_max.append(L_mu2*angle)
                            Phi.append(flux.getFlux(nu_type,numu.energy,np.cos(numu.pos.theta))) 
                            weights.append(w.value)
                            # numu_reco_energies.append(numu_reco.energy)
                            # breakpoint()
                            break 
                        else:
                            del[frame]
                            continue
                    break
# breakpoint()
# with h5py.File("dimuon_ranged_L2.h5", "w") as f:
#     f.create_dataset("numu_energies", data=numu_energies)
#     f.create_dataset("mu_1_energies", data=mu_1_energies)
#     f.create_dataset("mu_2_energies", data=mu_2_energies)
#     f.create_dataset("angles",data=angles)
#     f.create_dataset("weights",data=weights) 
#     f.create_dataset("S_max",data=S_max)
#     f.create_dataset('Phi',data=Phi)