import numpy as np
import matplotlib.pyplot as plt
import h5py

# This script is used for measuring the amount of dimuon events that carry over between processing levels.

def divide(x,d):
    q = []
    for i in range(len(x)):
        q.append(x[i]/d)
    return q

def sum10(x):
 sec = 3.1536e8
 y = round(sum(x)*sec)
 return y

def atmos(x):
    e = []
    for i in range(len(x)):
        e.append(4.8e-8*(x[i]/100)**-3.7)
    return e

def astro(x):
    e = []
    for i in range(len(x)):
        e.append(1.68e-18*(x[i]/1e5)**-2.58)
    return e

def reweigh(x,y,z):
    e = []
    for i in range(len(x)):
        e.append(((x[i]/y[i]))*z[i])
    return e

f_L1 = h5py.File('dimuon_volume_L1.h5', 'r')
f_L2 = h5py.File('dimuon_volume_L2.h5', 'r')
f_Det = h5py.File('dimuon_volume_Det.h5', 'r')
f_X = h5py.File('dimuon_volume_X.h5', 'r')
f_BDT = h5py.File('dimuon_volume_BDT.h5', 'r')

numu_E_L1 = list(f_L1['numu_energies'])
numu_E_L2 = list(f_L2['numu_energies'])
numu_E_Det = list(f_Det['numu_energies'])
numu_E_X = list(f_X['numu_energies'])
numu_E_BDT = list(f_BDT['numu_energies'])

Phi_L1 = list(f_L1['Phi'])
Phi_L2 = list(f_L2['Phi'])
Phi_Det = list(f_Det['Phi'])
Phi_X = list(f_X['Phi'])
Phi_BDT = list(f_BDT['Phi'])

w_L1 = divide(list(f_L1['weights']),1989)
w_L2 = divide(list(f_L2['weights']),1989)
w_Det = divide(list(f_Det['weights']),1989)
w_X = divide(list(f_X['weights']),1989)
w_BDT = divide(list(f_BDT['weights']),1989)

w_L1_astro = sum10(w_L1)
w_L2_astro = sum10(w_L2)
w_Det_astro = sum10(w_Det)
w_X_astro = sum10(w_X)
w_BDT_astro = sum10(w_BDT)

w_L1_atmos = sum10(reweigh(Phi_L1,astro(numu_E_L1),w_L1))
w_L2_atmos = sum10(reweigh(Phi_L2,astro(numu_E_L2),w_L2))
w_Det_atmos = sum10(reweigh(Phi_Det,astro(numu_E_Det),w_Det))
w_X_atmos = sum10(reweigh(Phi_X,astro(numu_E_X),w_X))
w_BDT_atmos = sum10(reweigh(Phi_BDT,astro(numu_E_BDT),w_BDT))

levels = ['Det','L1','L2','X','BDT']

events_astro = [w_Det_astro,w_L1_astro,w_L2_astro,w_X_astro,w_BDT_astro]
events_atmos = [w_Det_atmos,w_L1_atmos,w_L2_atmos,w_X_atmos,w_BDT_atmos]

epsilon_astro_DetL1 = round(w_L1_astro/w_Det_astro,2)
epsilon_astro_L1L2 = round(w_L2_astro/w_L1_astro,2)
epsilon_astro_L2X = round(w_X_astro/w_L2_astro,2)
epsilon_astro_XBDT = round(w_BDT_astro/w_X_astro,2)
epsilon_astro_f = round(w_BDT_astro/w_Det_astro,2)

epsilon_atmos_DetL1 = round(w_L1_atmos/w_Det_atmos,2)
epsilon_atmos_L1L2 = round(w_L2_atmos/w_L1_atmos,2)
epsilon_atmos_L2X = round(w_X_atmos/w_L2_atmos,2)
epsilon_atmos_XBDT = round(w_BDT_atmos/w_X_atmos,2)
epsilon_atmos_f = round(w_BDT_atmos/w_Det_atmos,2)

fig,ax = plt.subplots(layout='constrained')
ax.plot(levels,events_atmos,marker='o',c='r',label=r'''Atmos Flux $\epsilon_{f} =$'''f'''{epsilon_atmos_f}''')
ax.plot(levels,events_astro,marker='^',c='k',label=r'''Astro Flux $\epsilon_{f} =$'''f'''{epsilon_astro_f}''')
ax.set_yscale('log')
ax.set_xlabel('MEOWS Levels')
ax.set_ylabel('Events / 10 years')

ax.text('L1',w_L1_astro, r'''$\epsilon_{Det \to L1} =$'''f'''{epsilon_astro_DetL1}''')
ax.text('L2',w_L2_astro+50, r'''$\epsilon_{L1 \to L2} =$'''f'''{epsilon_astro_L1L2}''')
ax.text('X',w_X_astro+50, r'''$\epsilon_{L2 \to X} =$'''f'''{epsilon_astro_L2X}''')
ax.text('BDT',w_BDT_astro+50, r'''$\epsilon_{X \to BDT} =$'''f'''{epsilon_astro_XBDT}''')

ax.text('L1',w_L1_atmos, r'''$\epsilon_{Det \to L1} =$'''f'''{epsilon_atmos_DetL1}''',c='r')
ax.text('L2',w_L2_atmos, r'''$\epsilon_{L1 \to L2} =$'''f'''{epsilon_atmos_L1L2}''',c='r')
ax.text('X',w_X_atmos, r'''$\epsilon_{L2 \to X} =$'''f'''{epsilon_atmos_L2X}''',c='r')
ax.text('BDT',w_BDT_atmos, r'''$\epsilon_{X \to BDT} =$'''f'''{epsilon_atmos_XBDT}''',c='r')

ax.legend()
ax.set_title('Volume Efficiency')
ax.grid(linestyle='--',alpha=0.6)
plt.savefig('eventcounts_volume')