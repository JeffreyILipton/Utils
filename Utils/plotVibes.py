import os
import numpy as np
import matplotlib.pyplot as plt
import scipy

'''
0 time(min)
1 temp (C)
2 storage modulus (MPa)
3 Loss modulus (MPa)
4 stress (MPa)
5 Tan Delta
6 Freq (Hz)
7 Drive Froce (N)
8 Amplitude (um)
9 Strain (%)
10 Displacement (um)
11 Static Force (N)
12 Position (mm)
13 Length (mm)
14 Force (N)
15 Stiffness (N/m)
16 GCA Pressure (kPa)
'''
Channels = ["time", "temp", "Storage Modulus",  "Loss Modulus", "Stress",   "Tan Delta",    "Freq", "Drive Force",  "Amplitude","Strain",   "Dispalcement", "Static Force", "Position","Length","Force","Stiffness","Pressure"]
Units =    ["min",  "C",    "MPa",              "MPa",          "MPa",      "",             "Hz",   "N",            "um",       "%",        "um",           "N",            "mm",       "mm",   "N",    "N/m",      "kPa"]

def processNPY(file):
    vals = np.load(file)
    shape = vals.shape
    print shape
#    number of samples, data point, signal
    means = np.mean(vals,0)
    stds = np.std(vals,0,ddof=1)

    return file.replace(".npy",""), means,stds
    
def plotVibes(dicts,channel):
    ax = plt.subplot(111)
    ax.set_xscale("log", nonposx='clip')
    ax.set_yscale("log", nonposy='clip')


    for key in dicts.keys():
        (means,stds )= dicts[key]
        freq = means[:,6]
        storage_means = means[:,channel]
        storage_stds = stds[:,channel]
        #plt.loglog(freq,storage_means,'kx')
        #print freq
        #print storage_means
        print key
        plt.errorbar(freq, storage_means, yerr=storage_stds, fmt="s-",label = key)

    
    ax.grid(True, which='both',ls='--')
    #ax.grid(linestyle='--',linewidth=0.5)
    #plt.legend(bbox_to_anchor=(1.05,1),loc=2,borderaxespad=0.0)
    plt.legend(loc=2, borderaxespad=0.5)
    ax.set_xlim(0.9,110)
    ax.set_xlabel('Frequency (Hz)')
    ax.set_ylabel(Channels[channel]+" ("+Units[channel]+")")
    #ax.set_title(Channels[channel])

    plt.show()


if __name__ == "__main__":
    npfiles = [f for f in os.listdir('.') if '.np' and "I-" in f]
    toplots={}
    for npfile in npfiles:
        (name, means, stds) = processNPY(npfile)
        toplots[name] = (means,stds)
    plotVibes(toplots,2)
    