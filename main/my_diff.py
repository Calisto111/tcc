#!/usr/bin/env python
# -*- coding:utf-8 -*-

# File: my_diff.py
# Description: Line by line diff
# Author: fmatt
# Date: 08/12/2010

from sys import argv, exit

if __name__ == "__main__":

    # Check correct usage
    if argv.__len__() < 3:
        print ('Usage: my_diff <file1> <file2>')
        exit(-1)

    # Read first file
    fid = open(argv[1], 'r')
    lines1 = fid.readlines()
    fid.close()

    # Read second file
    fid = open(argv[2], 'r')
    lines2 = fid.readlines()
    fid.close()

    for i in range(lines1.__len__()):
        if lines1[i] != lines2[i]:
            # Strip '\n' chars
            if lines1[i].endswith('\n'):
                lines1[i] = lines1[i].rstrip('\n')
            if lines2[i].endswith('\n'):
                lines2[i] = lines2[i].rstrip('\n')

            print (str(i + 1) + ': ' + lines1[i] + ' > ' + lines2[i])
            print ('--')


#    print 'args: ', argv[1], argv[2]
        
        
    
    
