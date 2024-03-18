#!/usr/bin/env python
# -*- coding:utf-8 -*-

# File: calc_teo.py
# Description: Calculates TKEO from an input file
# Author: fmatt
# Date: 07/01/2011
# Version: 0.3

def main():
    # Script constants
    INPUT_DATA = "../data/sample.dat"
    OUTPUT_FILE = "../res/tkeo.dat"

    # Read input file
    fid = open(INPUT_DATA, 'r')
    lines = fid.readlines()
    fid.close()

    # Remove index from line
    for i in range(lines.__len__()):
        lines[i] = lines[i].split()[1]

    # Calculate TKEO
    tkeo = []
    for i in range(1, lines.__len__() - 1):
        tkeo.append( str( pow(int(lines[i]),2) - int(lines[i-1]) * int(lines[i+1])) + '\n')
    # Insert 0 in the begining and end of tkeo (first and last element)
    tkeo.insert(0,'0\n')
    tkeo.append('0\n')

    # Write output file
    fid = open(OUTPUT_FILE, 'w')
    fid.writelines(tkeo)
    fid.close()
    
    print ('tkeo.dat written.')

if __name__ == '__main__':
    main()
