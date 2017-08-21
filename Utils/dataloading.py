import sys
import csv
import re
import os
import numpy as np
import codecs

def processCSVToData(file,index,maxlines,data):
    with open(file,'r') as csvfile:
        reader = csv.reader(csvfile,delimiter=',')
        i=0
        for row in reader:
            row = [f.replace('\xff','').replace('\xfe','') for f in row]
            #print row
            if len(row)>1 and i<maxlines:
                data[index,i,:] = row
            print i
            i+=1
    return data

if __name__ == "__main__":
    csvfiles = [f for f in os.listdir('.') if '.csv' in f]
    lines = 162-55
    shape = (len(csvfiles),lines,12)
    print shape
    data = np.zeros(shape)
    i=0
    for csvf in csvfiles:
        data = processCSVToData(csvf,i,lines,data)
        i+=1
    print data
    #np.save("data",data)