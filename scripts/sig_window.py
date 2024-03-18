#!/usr/bin/env python
# -*- coding:utf-8 -*-

# File: sig_window.py
# Description: Create signal windows from tkeo
# Author: fmatt
# Date: 07/01/2011
# Version: 0.2

# System imports
from sys import argv, exit
from shutil import copy

# Local imports
import calc_teo

# Script constants
NOISE_COUNTER_START = 5
SEGMENT_SIZE = 40
THRESHOLD = 1e6
MIN_WINDOW_SIZE = 100 # Minimum window size (at least 100 samples)

SIG = 0 # Signal flag
NOI = 1 # Noise flag
SIG_END = 2 # End of signal flag
SIG_BEGIN = 3 # Begining of signal flag

TKEO_FILE_PATH = '../data/tkeo.dat'

# Flags
is_signal = False
noise_counter = NOISE_COUNTER_START

def test_data(d):
    global is_signal, noise_counter
    if abs(d) > THRESHOLD:
        # Reset noise counter
        noise_counter = NOISE_COUNTER_START

        # Return flag
        if is_signal:
            return SIG
        else:
            is_signal = True
            return SIG_BEGIN
    else:
        if is_signal:
            if noise_counter > 0:
                noise_counter -= 1
                return SIG
            else:
                noise_counter = NOISE_COUNTER_START
                is_signal = False
                return SIG_END
        return NOI

def print_usage():
    print ('Usage: sig_window.py <data_file>')

# Check for correct usage
if argv.__len__() < 2:
    print_usage()
    exit(-1)

file_path_name = argv[1]
filename = file_path_name.split('/')[-1]
filepath = file_path_name.replace(filename, '')

copy(file_path_name, filepath + 'sample.dat')

# Call calc_teo script
calc_teo.main()

# Read tkeo file
fid = open(TKEO_FILE_PATH, 'r')
lines = fid.readlines()
fid.close()

# Read data file
fid2 = open(filepath + 'sample.dat', 'r')
data_lines = fid2.readlines()
fid2.close()

lines2 = []

# Noise data buffer (before signal is detected, keep n samples)
noise_before_signal = [0 for i in range(NOISE_COUNTER_START + 1)]

base_index = 1

for i in range(lines.__len__()):
    # Stock data for future use (last n samples used when signal detected)
    noise_before_signal.pop(0)
    noise_before_signal.append(i)
    
    td = test_data(int(lines[i]))
    if td == SIG: # Signal
        lines2.append(i)
    elif td == SIG_BEGIN:
        lines2 = noise_before_signal + lines2
    elif td == SIG_END: # Signal end
        if lines2.__len__() > 100:
#             print 'sig: ', lines2[0] + 1, lines2[-1] + 1
#             print 'lines: ', data_lines[lines2[0]], data_lines[lines2[-1]]
#             print 'length: ', lines2.__len__()
            
#             print '####### Window ######'
#             print data_lines[lines2[0]:lines2[-1] + 1]
#             print '### Window End ###'
            
            # Write output file (window file)
            window_filename = file_path_name.replace('.dat', '_0' + str(base_index) + '.dat')
            fid = open(window_filename, 'w')
            fid.writelines(data_lines[lines2[0]:lines2[-1] + 1])
            fid.close()

            # Output message
            print ('File ' + window_filename + ' created.')
          
            # Update base_index
            base_index += 1

        lines2 = []
