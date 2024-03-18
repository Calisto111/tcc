#!/usr/bin/env python
# -*- coding:utf-8 -*-

# File: neuron.py
# Description: Neuron class
# Version: 0.4

from math import exp
from copy import copy

class Neuron(object):
    def __init__(self, weights, bias, theta, type='bin'):
        self.weights = []
        self.bias = bias
        self.theta = theta
        self.type = type

        for i in range(weights.__len__()):
            self.weights.append(weights[i])

# ------------------------------------------------------------

    def act(self, xs):
        sum = 0

        for i in range(xs.__len__()):
            sum += xs[i] * self.weights[i]
        sum += self.bias
            
        return self.output(sum)

# ------------------------------------------------------------

    def output(self, sum):
        if (sum >= self.theta):
            return 1
        else:
            if self.type == 'bin':
                return 0
            else:
                return -1

# ------------------------------------------------------------

class AdalineNeuron(Neuron):
    
    # Constructor
    def __init__(self, weights, bias):
        Neuron.__init__(self, weights, bias, 0, 'bip')

# ------------------------------------------------------------

class TriStateNeuron(Neuron):

    def __init__(self, weights, bias, theta):
        self.weights = []        
        self.bias = bias
        self.theta = theta
        
        for i in range(weights.__len__()):
            self.weights.append(weights[i])

# ------------------------------------------------------------

    def output(self, sum):
        if (sum > self.theta):
            return 1
        elif (sum < self.theta):
            return -1
        else:
            return 0

# ------------------------------------------------------------

class PerceptronNeuron(TriStateNeuron):

    # Output function
    def output(self, sum):
        if (sum > self.theta):
            return 1
        elif (sum < -self.theta):
            return -1
        else:
            return 0

# ------------------------------------------------------------

# Back propagation neuron
class BPNeuron(Neuron):

    def __init__(self, weights, bias, type='bin'):
        Neuron.__init__(self, weights, bias, None, type)

# ------------------------------------------------------------

    def output(self, sum):
        try:
            if self.type == 'bin':
                return 1.0/(1.0 + exp(-sum))
            else:
                return (2.0/(1.0 + exp(-sum))) - 1.0
        except OverflowError:
            if sum < 500:
                return -1.0
            else:
                print ('OverflowError exception reached. Execution aborted.')
                exit(-1)


# ------------------------------------------------------------

    def derivative(self, xs):
        sum = 0

        for i in range(xs.__len__()):
            sum += xs[i] * self.weights[i]
        sum += self.bias
            
        if self.type == 'bin':
            return self.output(sum) * (1.0  - self.output(sum))
        else:
            return 0.5 * (1.0 + self.output(sum)) * (1 - self.output(sum))

# ------------------------------------------------------------

    # Return weights list
    def get_weights(self):
        return self.weights

# ------------------------------------------------------------

    # Return bias
    def get_bias(self):
        return self.bias


# ------------------------------------------------------------

    # Updates weights and bias
    def update(self, weights, bias):
        self.weights = copy(weights)
        self.bias = bias

# ------------------------------------------------------------
    
    # Return net output
    def net(self, xs):
        sum = 0

        for i in range(xs.__len__()):
            sum += xs[i] * self.weights[i]
        sum += self.bias
            
        return sum

# ------------------------------------------------------------

if __name__ == "__main__":

    test_neuron = BPNeuron([1.0, 1.0], 1.0, 'bip')

    print (test_neuron.act([2.0, 3.0]))
