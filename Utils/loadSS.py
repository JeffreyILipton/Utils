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
			row = [f.replace('\xff','').replace('\xfe','').replace('\0','') for f in row]
			print row
			if len(row)>1 and i<maxlines:
				data[index,i,:] = row
			#print i
			i+=1
	return data

if __name__ == "__main__":

	for leter in ['H','I']:
		for val in ["5","10","15","20","25"]:
			name = leter+"-25-"+val
			print name
			csvfiles = [f for f in os.listdir('.') if name in f]
			lines = 107
			shape = (len(csvfiles),lines,12)
			print shape
			data = np.zeros(shape)
			i=0
			for csvf in csvfiles:
				print csvf
				data = processCSVToData(csvf,i,lines,data)
				i+=1
			#print data
			np.save(name,data)