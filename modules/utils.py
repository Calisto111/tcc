#!/usr/bin/env python
# -*- coding:utf-8 -*-

# File: utils.py
# Description: File processing utils
# Version: 0.1
# Date: 07/12/2010

from sys import argv, exit
from os import listdir, mkdir, rename
from shutil import move
from copy import copy

# ==============================================================================

# Truncate data files removing unused samples from the begining and from the end
def truncate_data_files(dir, seg_length):
    list_of_files = listdir(dir)

    # Check if backup dir exists
    if list_of_files.__contains__('bak'):
        backup_dir = True
    else:
        backup_dir = False

    # Remove non-data files from list
    for filename in list_of_files:
        if not filename.endswith('.dat'):
            list_of_files.remove(filename)

    # If no datafiles in directory, nothing to be done
    if list_of_files.__len__() < 1:
        print ('Nothing to be done in ' + dir + '.')
        exit(1)

    # Directory ends with '/'
    if not dir.endswith('/'):
        dir = dir + '/'

    # Truncate data files and backup old files
    if not backup_dir:
        mkdir(dir + 'bak')
    for filename in list_of_files:
        fid = open(dir + filename)
        lines = fid.readlines()
        fid.close()

        # Backup old file
        if not listdir(dir + 'bak').__contains__(filename):
            rename(dir + filename, dir + 'bak/' + filename)
        else:
            print (dir + 'bak/' + filename + ' already exists. Aborting...')
            exit(-1)

        # Remove not-used samples
        extra_samples = lines.__len__() % int(seg_length)

        if extra_samples:
            if extra_samples % 2: # Odd number,
                for i in range(extra_samples / 2 + 1): # Remove n/2 + 1 samples from the beginning
                    lines.__delitem__(0)
                for i in range(extra_samples / 2): # Remove n/2 samples from the end
                    lines.__delitem__(-1)
            else: # Even number, remove n/2 samples from the beginning and from the end
                for i in range(extra_samples / 2):
                    lines.__delitem__(0)
                    lines.__delitem__(-1)
        
        # Write new file
        fid = open(dir + filename, 'w')
        fid.writelines(lines)
        fid.close()

# ------------------------------------------------------------------------------

# Format lines (list of strings) in place
def format_lines(lines):
    # Auxiliary array
    to_be_removed = []

    # Config variables dictionary
    conf_var_dict = {}

    for i in range(lines.__len__()):
        lines[i] = lines[i].lstrip()
        # Comment or empty line
        if (lines[i].startswith('#')) or (lines[i].__len__() == 0):
            to_be_removed.append(lines[i])
        # Get config variables
        elif (lines[i].startswith('_')):
            name, value = lines[i].split()
            conf_var_dict[name[1:]] = value
            to_be_removed.append(lines[i])

    # Remove comments and empty lines
    for line in to_be_removed:
        lines.remove(line)

    # Returns config variables dictionary
    return copy(conf_var_dict)

# ==============================================================================

if __name__ == "__main__":
    # Test correct usage
    if (argv.__len__() < 2):
        print ('Function missing!')
        print ('Usage: utils <function_name> <function_args>')
        exit(-1)
        
    # Truncate data files
    if argv[1] == 'truncate_data_files':
        if (argv.__len__() != 4):
            print ('Function arguments missing!')
            print ('Usage: utils truncate_data_files <directory> <segment_length>')
            exit(-1)
        truncate_data_files(argv[2], argv[3])
