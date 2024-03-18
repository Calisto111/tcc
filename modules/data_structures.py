#!/usr/bin/env python
# -*- coding:utf-8 -*-

# File: data_structures.py
# Description: Data structures for main application
# Author: fmatt
# Date: 01/12/2010

# Imports
from threading import RLock

# ==============================================================================

# Ring buffer
class RingBuffer:
    def __init__(self, max_length):
        self.max_length = max_length # Buffer size
        self.data = [] # Data array
        self.closed = False # Buffer closed flag
        self.buffer_lock = RLock() # Mutex

# ------------------------------------------------------------------------------

    # Write x to buffer (and removes first element)
    def write(self, x):
        if self.data.__len__() == self.max_length: # Buffer is full, overwrite
            self.data.pop(0)
        # Append x to data
        self.data.append(x)

# ------------------------------------------------------------------------------

    # Read data in read pointer
    def read(self):
        return self.data.pop(0)

# ------------------------------------------------------------------------------

    # Open ring buffer
    def open(self):
        self.closed = False

# ------------------------------------------------------------------------------

    # Close ring buffer
    def close(self):
        self.closed = True

# ------------------------------------------------------------------------------

    # Return buffer status (true for buffer closed)
    def is_closed(self):
        return self.closed

# ------------------------------------------------------------------------------

    # Return buffer data
    def get_data(self):
        return self.data

# ------------------------------------------------------------------------------

    # Return current buffer length
    def get_length(self):
        return self.data.__len__()

# ------------------------------------------------------------------------------

    # Lock buffer (get buffer's mutex)
    def lock(self):
        self.buffer_lock.acquire()

# ------------------------------------------------------------------------------

    # Unlock buffer (release buffer mutex)
    def unlock(self):
        self.buffer_lock.release()
        
# ==============================================================================

if __name__ == "__main__":

    # Create ring buffer with length 5
    rb = RingBuffer(5)

    
