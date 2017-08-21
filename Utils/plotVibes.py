import os
import numpy as np
import matplotlib.pyplot as plt
import scipy
from scipy import optimize

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

powerlaw = lambda x, amp, index: amp * (x**index)
fitfunc = lambda p, x: p[0] + p[1] * x
errfunc = lambda p, x, y, err: (y - fitfunc(p, x)) / err

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

        logx = np.log10(freq)
        logy = np.log10(storage_means)
        logyerr = storage_stds/storage_means


        pinit = [1.0, -1.0]
        out = optimize.leastsq(errfunc, pinit,
                               args=(logx, logy, logyerr), full_output=1)

        pfinal = out[0]
        covar = out[1]
        print pfinal
        print covar

        index = pfinal[1]
        amp = 10.0**pfinal[0]

        indexErr = np.sqrt( covar[1][1] )
        ampErr = np.sqrt( covar[0][0] ) * amp

        #curve = scipy.optimize.curve_fit(lambda w,E,n: E*w**n,freq,storage_means)
        #E = curve[0][0]
        #n = curve[0][1]
        #x = np.logspace(0,2,50)
        #y = E*x**n
        
        #plt.loglog(freq,storage_means,'kx')
        #print freq
        #print storage_means
        print key
        p = plt.errorbar(freq, storage_means, yerr=storage_stds, fmt="s",label = key)
        mark = p[0].get_color()
        plt.plot(freq,powerlaw(freq,amp,index),mark+'-')
        #plt.loglog(x,y,mark+'-')
        

    
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
    