#!/usr/bin/env python
# -*- coding:utf-8 -*-

# File: client.py
# Description: Sockets test
# Author: fmatt
# Date: 19/11/2010

# Echo client program
import socket
from time import sleep

# Local constants
HOST = 'localhost'    # Server is in localhost
PORT = 2727           # The same port as used by the server
DATA_FILE = '../data/sample.dat' # Data file

# ------------------------------------------------------------------------------

# Data pre-processing function
def data_pre_processing(raw_data):
    return raw_data.rstrip('\r\n')

# ------------------------------------------------------------------------------

# Main
if __name__ == "__main__":

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))

    # Load data from file
    fid = open(DATA_FILE, 'r')
    data = fid.readlines()
    fid.close()

    # Data pre-processing
#    data = map(data_pre_processing, data)

    # Send data to server
    try:
        for d in data:
            print ('Sending ', d)
            s.send(d.encode())
#            sleep(0.0002) # Simulating a 5 kHz sample rate
            sleep(0.0025) # Simulating a 400 Hz sample rate
    except KeyboardInterrupt:
        print ('Keyboard interrupt reached!')
        s.close()

