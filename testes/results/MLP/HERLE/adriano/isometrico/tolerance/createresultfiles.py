#!/usr/bin/env python
# -*- coding:utf-8 -*-

# File: teste.py
# Description: Server side
# Author: fmatt
# Date: 19/11/2010

# System imports
from sys import path
from os import listdir
from numpy import average, std
from math import sqrt

PATTERNS_PATH=['/home/dantutu/Documents/Mestrado/ProjetoFinal/netscompair/Mattioli/netComp_src/testes/results/MLP/HERLE/adriano/isometrico/tolerance']

list_of_files = listdir(PATTERNS_PATH[0])
print list_of_files
print 'list_of_files len():',len(list_of_files)


# Init training list
new_list = []
new_file = ''
CONT=0
results = []
ex_time = []

for filename in list_of_files:
    if filename.__contains__('_20_'):
        new_list.append(filename)

new_list.sort()
print 'new_list',new_list
print PATTERNS_PATH[0]+'/'+filename

for filename in new_list:
    fid = open(PATTERNS_PATH[0]+'/'+filename, 'r')
    lines = fid.readlines()
    fid.close()
    results = []
    ex_time = []
    for line in lines:
        temp=line.split('\t')
        temp[2]=temp[2].strip('\n')
        results.append(float(temp[1]))
        ex_time.append(float(temp[2]))
    temp=filename.split('_')
    temp1=temp[2].split('.')
    tolerance=int(temp1[0])
    print 'tolerance',tolerance
    mean = average(results)  # Mean
    st_dev = std(results)       # Standard deviation
    c1 = mean - 1.96 * st_dev / sqrt(len(results))
    c2 = mean + 1.96 * st_dev / sqrt(len(results))

    fid = open('results_performance_n_clusters.dat', 'a')
    fid.write(str(tolerance) + '\t' + str(mean) + '\t' + str(c1) +
    '\t' + str(c2) + '\n')
    fid.close()

    mean_time = average(ex_time)
    std_time = std(ex_time)
    c1_time = mean_time - 1.96 * std_time / sqrt(len(ex_time))
    c2_time = mean_time + 1.96 * std_time / sqrt(len(ex_time))

    fid = open('results_time_n_clusters.dat', 'a')
    fid.write(str(tolerance) + '\t' + str(mean_time) + '\t' + str(c1_time) +
    '\t' + str(c2_time) + '\n')
    fid.close()

