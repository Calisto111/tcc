#!/usr/bin/env python
# -*- coding:utf-8 -*-

# File: config_file.py
# Description: Configuration file class
# Version: 0.1


class ConfigFile(object):
    def __init__(self, file_name):

        self.file_name = file_name

        self.patterns = []
        self.targets = []

        # Parse config file
        self.parse_config_file()

# ------------------------------------------------------------
    
    # Update config file
    def update(self, file_name):
        self.file_name = file_name

        # Reset patterns and targets
        self.patterns = []
        self.targets = []

        # Parse config file
        self.parse_config_file()

# ------------------------------------------------------------

    # Update network parameters
    def parse_config_file(self):
        fid = open(self.file_name)

        self.patterns = []

        # Get training patterns
        line = fid.readline()
        while not line.startswith('#'):
            # Don't get blank lines
            if line != '\n':
                self.patterns.append(line)
            line = fid.readline()

        self.targets = fid.readlines()

        fid.close()

        # Parse patterns and targets
        self.parse_patterns()
        self.parse_targets()

# ------------------------------------------------------------

    # Create patterns list
    def parse_patterns(self):
        for i in range(self.patterns.__len__()):
            # Remove end line char
            self.patterns[i] = self.patterns[i].rstrip('\n')

            # Create list from string
            self.patterns[i] = list(self.patterns[i])

            # Remove space chars from list
            while self.patterns[i].__contains__(' '):
                self.patterns[i].remove(' ')
            
            # Convert patterns from str ('0', '1') to int (-1, 1)
            for j in range(self.patterns[i].__len__()):
                if self.patterns[i][j] == '0':
                    self.patterns[i][j] = -1
                else:
                    self.patterns[i][j] = int(self.patterns[i][j])

# ------------------------------------------------------------

    # Create targets list
    def parse_targets(self):
        for i in range(self.patterns.__len__()):
            # Remove end line char
            self.targets[i] = self.targets[i].rstrip('\n')

            # Create list from string
            self.targets[i] = list(self.targets[i])

            # Remove space chars from list
            while self.targets[i].__contains__(' '):
                self.targets[i].remove(' ')
            
            # Convert targets from str ('0', '1') to int (-1, 1)
            for j in range(self.targets[i].__len__()):
                if self.targets[i][j] == '0':
                    self.targets[i][j] = -1
                else:
                    self.targets[i][j] = int(self.targets[i][j])

# ------------------------------------------------------------

    # Return patterns list
    def get_patterns(self):
        return self.patterns

# ------------------------------------------------------------

    # Return targets list
    def get_targets(self):
        return self.targets

# ============================================================

class ConfigFileFloat(ConfigFile):
    # Create patterns list
    def parse_patterns(self):
        for i in range(self.patterns.__len__()):
            # Remove end line char
            self.patterns[i] = self.patterns[i].rstrip('\n')

            # Create list from string
            self.patterns[i] = map(float, self.patterns[i].split())

# ------------------------------------------------------------

    # Create targets list
    def parse_targets(self):
        for i in range(self.targets.__len__()):
            # Remove end line char
            self.targets[i] = self.targets[i].rstrip('\n')

            # Create list from string
            self.targets[i] = map(float, self.targets[i].split())

# ------------------------------------------------------------

