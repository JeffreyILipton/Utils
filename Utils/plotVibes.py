
import numpy as np
import matplotlib.pyplot as plt

'''
1 time(min)
2 temp (C)
3 storage modulus (MPa)
4 Loss modulus (MPa)
5 stress (MPa)
6 Tan Delta
7 Freq (Hz)
8 Drive Froce (N)
9 Amplitude (um)
10 Strain (%)
11 Displacement (um)
12 Static Force (N)
13 Position (mm)
14 Length (mm)
15 Force (N)
16 Stiffness (N/m)
17 GCA Pressure (kPa)
'''

def processNPY(file):
    vals = np.load(file)
    shape = vals.shape
    print shape

if __name__ == "__main__":
	npfiles = [f for f in os.listdir('.') if '.np' in f]
	for xls in npfiles:
		processToCSV(xls)