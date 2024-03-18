#!/usr/bin/env python
# -*- coding:utf-8 -*-

# File: teste.py
# Description: Server side
# Author: fmatt
# Date: 19/11/2010

# System imports
from sys import path
from os import listdir

PATTERNS_PATH=['../patterns/ARs/AR10']
SUB4_PREFIX = 'adrisot'
SUB41_PREFIX = 'adrisom'
SUB1=0

# Test if file must be included in test files list
def is_test_file(file):
    if SUB1 == 1:
        prefix = SUB4_PREFIX
    else:
        prefix = SUB41_PREFIX

    # Check correct prefix
    if file.startswith(prefix) and file.endswith('.pat'):
        return True
    else:
        return False

list_of_files = listdir(PATTERNS_PATH[0])
#print list_of_files
#print 'list_of_files len():',len(list_of_files)
test_files = filter(is_test_file, list_of_files)
print ('list files',test_files.sort())
print ('test_files len():',test_files)


# Init training list
new_file = ''
CONT=51

for filename in test_files:
#    print '\nFile: ', filename
#    print '-------------------------'
    fid = open(PATTERNS_PATH[0] + '/' + filename, 'r')
    lines = fid.readlines()
    fid.close()


    if filename.__contains__('extensao'):
        correct_class = 0
    elif filename.__contains__('flexao'):
        correct_class = 1
    elif filename.__contains__('grasp'):
        correct_class = 2
    elif filename.__contains__('torcao'):
        correct_class = 3

    for line in lines:
        temp = line.split('\n')
        new_file=new_file+str(temp[0])+'\t'+str(correct_class)+'\t'+str(CONT)+'\n'
    
    CONT=CONT+1
#print 'New_file',new_file
fid = open('patternsbracoAR10isom','a')
fid.writelines(new_file)
fid.close
        

