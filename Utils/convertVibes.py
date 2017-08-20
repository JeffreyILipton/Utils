import sys
import csv
import re
import os

def processToCSV(file):
	f = open(file, 'r')
	outname= file.replace('.xls','.csv')
	fout = open(outname,'w')
	lines=[]
	for line in f:
		nl = line.replace('\0','').replace('\r','').replace('\n','').replace('\x00','')
		tabs = re.split(r'\t+',nl.rstrip('\t'))
		if len(tabs)>10:
			print tabs
			newline = ','.join(tabs)+'\n'
			lines.append(newline)
	for i in range(0,11):
		fout.write(lines[-11+i])

	print "done"

if __name__ == "__main__":
	xlsfiles = [f for f in os.listdir('.') if '.xls' in f]
	for xls in xlsfiles:
		processToCSV(xls)