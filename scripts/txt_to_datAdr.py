#!/usr/bin/env python
# -*- coding:utf-8 -*-

# File: txt_to_dat.py
# Description: Create data file from txt
# Author: fmatt
# Date: 03/03/2011
# Version: 0.1

# System imports
from sys import argv, exit

# Check correct usage
if argv.__len__() < 2:
    print ('Usage: txt_to_dat.py <datafile.txt>')
    exit(-1)

# Parse filename
filename = argv[1]

if filename.endswith('.txt'):
    output_filename = filename.replace('.txt', '.dat')
else:
    output_filename = filename + '.dat'

# Read input file
fid = open(filename, 'r')
lines = fid.readlines()
fid.close()

new_lines = []

for line in lines:
    if line.__contains__('"'):
        line = line.replace('"', '') # Remove double quotes from line
    new_line = line.replace(',','')
    new_line = line.replace(' ','\n')
    new_lines.append(new_line)

# Write output file
fid = open(output_filename, 'w')
fid.writelines(new_lines)
fid.close()

#Normalization of each sample *10.000
new_lines=[]
fid = open(output_filename,'r',)
data = fid.readlines()
fid.close()
for eachsample in data:
    eachsample = eachsample.replace(',','.')
    #print 'Each sample', eachsample
    new_lines.append(str(int(float(eachsample)*10000))+'\n')

fid = open(output_filename,'w')
fid.writelines(new_lines)
fid.close

print ("Tamanho quantidade de pontos: ", len(data))
print ('Dat file written.')
