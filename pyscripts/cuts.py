import h5py
import numpy as np
import matplotlib.pyplot as plt

def val(key,f):
    val = f[key][()]
    return val

def real_val(keys):
    e = []
    for i in range(len(keys)):
        e.append(keys[i])
    return e

L3 = h5py.File('L3_cuts.h5','r')
print(L3.keys())

print('\n',
      'Cut Summary:','\n',
      'fallback > 2: ',L3['fallback > 2'][()],'\n',
      'fallback > 2: ',val('fallback > 2',L3),'\n',
      'cos(zenith) > 0.2: ',L3['cos(zenith) > 0.2'][()],'\n',
      'pulse_hm DOM hits < 15: ',L3['pulse_hm DOM hits < 15'][()],'\n',
      'track_dh DOM hits <= 6: ',L3['track_dh DOM hits <= 6'][()],'\n',
      'track_dh length < 200: ',L3['track_dh length < 200'][()],'\n',
    )

breakpoint()

criteria = ['fallback > 2','cos(zenith) > 0.2','pulse_hm DOM hits < 15: ','track_dh DOM hits <= 6','track_dh length < 200']
cut_events = [val('fallback > 2',L3),L3['cos(zenith) > 0.2'][()],L3['pulse_hm DOM hits < 15'][()],L3['track_dh DOM hits <= 6'][()],L3['track_dh length < 200'][()],]

fig, ax = plt.subplots(layout='constrained')
bar_labels = ax.bar(criteria,cut_events)
ax.bar_label(bar_labels)
ax.set_xlabel("Selection Criteria")
ax.set_ylabel("Number of Cut Frames")
ax.set_xticks(criteria, criteria, rotation=45)
plt.savefig('cuts')

# breakpoint()