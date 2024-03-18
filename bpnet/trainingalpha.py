#!/usr/bin/env python
# -*- coding:utf-8 -*-

# File: training.py
# Description: BP training algorithm
# Version: 0.5

INPUT = 0
TARGET = 1

from copy import copy, deepcopy
from random import random, seed, randint, shuffle
from sys import exit
from math import pow, exp, sqrt
from time import time


# Back propagation training
class BP(object):

    # Constructor
    def __init__(self, alpha=0.01, tolerance=0.1):
        
        # Constructor arguments
        self.training_set = None
        self.alpha = alpha
        
        # Other initializations
        self.net = 0
        self.type = 'bip'
        self.inc_error = 0
        self.delta_wjk = []
        self.delta_vij = []
        self.mu = 0.5 # Momentum

        # Number of inputs
        self.n_inputs = 0

        # Number of hidden/output neurons
        self.n_hidden_neurons = 0
        self.n_output_neurons = 0

        # Epoch number
        self.epoch = 1
        self.last_epoch = 1 # Needed for epoch initialization

        # Tolerance
        self.tolerance = tolerance

        # Random number generator initialization
        seed()

        # Bias
#        self.bias = random()

        # Error and error data
        self.error =  0
        self.last_error = 0
# ------------------------------------------------------------------------------

    # Update parameters
    def update_parameters(self, training_set, alpha, tolerance, n_hidden_neurons, n_output_neurons, type):
        self.training_set = training_set
        self.alpha = alpha
        self.tolerance = tolerance
        self.n_hidden_neurons = n_hidden_neurons
        self.n_output_neurons = n_output_neurons
        self.type = type

        self.n_inputs = self.training_set[0][0].__len__()

        # Re-init error data
        self.error_data = []

        self.init_weights()

# ------------------------------------------------------------

    # Initialize weights
    def init_weights(self):
        self.v = []
        self.w = []
        self.v0 = []
        self.w0 = []

        # Scale factor (Nguyen-Widrow initialization)
        beta = 0.7 * pow(self.n_hidden_neurons, (1.0/self.n_inputs))

        # Hidden neurons
        for i in range(self.n_inputs):
            self.v.append([])

            # Input -> hidden neurons weights and bias
            for j in range(self.n_hidden_neurons):
                self.v0.append(float(randint(-50,50))/100)
                

                self.v[i].append((float(randint(-10,10)) * beta)/10.0)

        # Nguyen-Widrow Initialization
        for j in range(self.n_hidden_neurons):
            norma_vj = 0
            for i in range(self.n_inputs):
                norma_vj += pow(self.v[i][j], 2)

            norma_vj = sqrt(norma_vj)

            for i in range(self.n_inputs):
                self.v[i][j] = (beta * self.v[i][j]) /norma_vj

        # Output neurons
        for j in range(self.n_hidden_neurons):
            self.w.append([])

            for k in range(self.n_output_neurons):
                self.w0.append(float(randint(-50,50))/100)
#                self.w[j].append(0)
                self.w[j].append(float(randint(-50,50))/100)
                #self.w[j].append(1)

# ------------------------------------------------------------------------------

    # Calculate net
    def calc_net(self, xs):

        self.z_in = []

        for j in range(self.n_hidden_neurons):
            # Reset net to 0
            self.net = 0

            # net = bias + xi * wi
            for i in range(xs.__len__()):
                try:
                    self.net += xs[i] * self.v[i][j]
                except(IndexError):
                    print 'IndexError exception caught!'
                    print 'xs, self.v = ', xs, self.v
                    exit(-1)
                self.net += self.v0[j]

            self.z_in.append(self.net)

#        print 'z_in: ', self.z_in
            
        self.activation_function()


# ------------------------------------------------------------------------------

    # Activation function
    def activation_function(self):
        self.z = []
        for i in range(self.n_hidden_neurons):
            try:
                if self.type == 'bin':
                    self.z.append(1.0/(1.0 + exp(-self.z_in[i])))
                else:
                    self.z.append(2.0/(1.0 + exp(-self.z_in[i])) - 1.0)
            except OverflowError:
#                if z_in[i] < 500:
#                    return -1.0
#                else:
                print 'OverflowError exception reached. Execution aborted.'
                exit(-1)

#        print 'z: ', self.z
# ------------------------------------------------------------------------------

    # Calculate net
    def calc_output_net(self):

        self.y_in = []

        for k in range(self.n_output_neurons):

            # Reset net to 0
            self.net = 0

            # net = bias + xi * wi
            for j in range(self.n_hidden_neurons):
                try:
                    self.net += self.z[j] * self.w[j][k]
                except(IndexError):
                    print 'IndexError exception caught!'
                    exit(-1)
                self.net += self.w0[k]

            self.y_in.append(self.net)

#        print 'y_in: ', self.y_in
            
        self.output_activation_function()

# ------------------------------------------------------------------------------


    # Activation function
    def output_activation_function(self):
        self.y = []
        for i in range(self.n_output_neurons):
            try:
                if self.type == 'bin':
                    self.y.append(1.0/(1.0 + exp(-self.y_in[i])))
                else:
                    self.y.append(2.0/(1.0 + exp(-self.y_in[i])) - 1.0)
            except OverflowError:
#                if z_in[i] < 500:
#                    return -1.0
#                else:
                print 'OverflowError exception reached. Execution aborted.'
                exit(-1)

#        print 'y: ', self.y

# ------------------------------------------------------------------------------

    # Output backpropagation
    def bp_output(self, targets):

        self.delta_wjk_old = deepcopy(self.delta_wjk) 

        self.delta_k = []
        self.delta_wjk = []
        self.delta_w0k = []

        # Calculate delta_k
        for k in range(self.n_output_neurons):

            if self.type == 'bin':
                derivative = self.y[k] * (1 - self.y[k])
            else:
                derivative = 0.5 * (1.0 + self.y[k]) * (1.0 - self.y[k])

            self.delta_k.append((targets[k] - self.y[k]) * derivative)

        # Calculate delta_wjk and delta_w0k
        for j in range(self.n_hidden_neurons):
            self.delta_wjk.append([])
            for k in range(self.n_output_neurons):
                if (self.delta_wjk_old.__len__() == 0):
                    self.delta_wjk[j].append(self.alpha * self.delta_k[k] * self.z[j])
                else:
                    self.delta_wjk[j].append(self.alpha * self.delta_k[k] * self.z[j] + self.mu * self.delta_wjk_old[j][k])

        # Calculate delta_w0k
        for k in range(self.n_output_neurons):
            self.delta_w0k.append(self.alpha * self.delta_k[k])

#        print 'dwjk, dw0k = ', self.delta_wjk, self.delta_w0k

# ------------------------------------------------------------------------------

    # Derivative
    def bp_hidden(self, input):

        self.delta_vij_old = deepcopy(self.delta_vij)

        self.delta_in_j = []
        self.delta_j = []
        self.delta_vij = []
        self.delta_v0j = []

        for j in range(self.n_hidden_neurons):
            self.delta_in_j.append(0)

            # Calculate delta_in_j
            for k in range(self.n_output_neurons):
                self.delta_in_j[j] += self.delta_k[k] * self.w[j][k]

            if self.type == 'bin':
                derivative = self.z[j] * (1 - self.z[j])
            else:
                derivative = 0.5 * (1.0 + self.z[j]) * (1.0 - self.z[j])

            # Calculate delta_j
            self.delta_j.append(self.delta_in_j[j] * derivative)
        
        # Calculate delta_vij
        for i in range(input.__len__()):
            self.delta_vij.append([])        
            for j in range(self.n_hidden_neurons):
                if (self.delta_vij_old.__len__() == 0):
                    self.delta_vij[i].append(self.alpha * self.delta_j[j] * input[i])
                else:
                    self.delta_vij[i].append(self.alpha * self.delta_j[j] * input[i] + self.mu * self.delta_vij_old[i][j])
                
        # Calculate delta_v0j
        for j in range(self.n_hidden_neurons):
            self.delta_v0j.append(self.alpha * self.delta_j[j])
            
#        print 'dvij, dv0j: ', self.delta_vij, self.delta_v0j    


# ------------------------------------------------------------------------------

    # Update weights from output neurons
    def output_update(self):
        for k in range(self.n_output_neurons):
            self.w0[k] += self.delta_w0k[k]
            for j in range(self.n_hidden_neurons):
                self.w[j][k] += self.delta_wjk[j][k]

# ------------------------------------------------------------------------------

    # Update weights from hidden neurons
    def hidden_update(self):
        for j in range(self.n_hidden_neurons):
            self.v0[j] += self.delta_v0j[j]
            for i in range(self.n_inputs):
                self.v[i][j] += self.delta_vij[i][j]

# ------------------------------------------------------------------------------

    # Test stopping condition
    def test_stop(self):

        # Re-init error
        self.last_error = self.error
        self.error = 0

        # Iterate through training set
        for training_tuple in self.training_set:

            input_list = training_tuple[INPUT]
            target = training_tuple[TARGET]

            # Calculate net
            self.calc_net(input_list)
            self.calc_output_net()

            # Update error
            for k in range(self.n_output_neurons):
                try:
                    self.error += pow((target[k] - self.y[k]), 2)
                except(OverflowError):
                    print 'Math overflow!!'
                    print 'target, self.net = ', target, self.net
                    exit(-1)

        # Update error data
                #self.error_data.append(self.error)

        # Test if error is acceptable
        if self.error >= self.tolerance:
#            print self.error
            return False
        else:
            # If error < tolerance
            return True

# ------------------------------------------------------------------------------

    # Print error
    def print_error(self):
        print self.error

# ------------------------------------------------------------------------------

    # Print last epoch number
    def print_epoch(self):
        print self.last_epoch

# ------------------------------------------------------------------------------

    # Returns bias
#    def get_bias(self):
#        return self.bias

# ------------------------------------------------------------------------------

    # Training 
    def training(self):
        try:
            # Initialize old weights
            old_v = deepcopy(self.v)
            old_v0 = copy(self.v0)

            self.z = []

            # Iterate through training set
            for training_tuple in self.training_set:

 #               print 'v, w: ', self.v, self.w
#                raw_input('TEST')

                input_list = training_tuple[INPUT]
                target = training_tuple[TARGET]

                # Calculate net
                self.calc_net(input_list)

                # Calculate output net
                self.calc_output_net()

                # Output error backpropagation
                self.bp_output(target)

                # Hidden layer backpropagation
                self.bp_hidden(input_list)

                # Update weights and bias: output neurons
                self.output_update()

                # Update weights and bias: hidden neurons
                self.hidden_update()

                

#                 for i in range(self.n_inputs):
#                     self.delta[i] = target - self.net
#                     self.weights[i] = self.weights[i] + self.alpha * self.delta[i] * input_list[i]
#                 # Update bias
#                 self.bias = self.bias + self.alpha * (target - self.net)
            
            # Test stopping condition
            if self.test_stop():
                self.last_epoch = self.epoch
                self.epoch = 1
                return self.w
            else:
                # Prevent infinit loop from ocurring
                #if (old_v == self.v) and (old_v0 == self.v0):
                #    print 'Error: infinite loop reached after ' + str(self.epoch) + ' cycles!!'
                #    print 'Minimum error reached = ' + str(self.error) + '.'
                #    exit(-1)
                if ((self.error - self.last_error) > 0):
                    if (self.inc_error > 100):
                        self.inc_error = 0
                        print 'Small error decrement or increasing error: aborting traininig.'
                        print 'Minimum error reached = ' + str(self.error)
                        self.last_epoch = self.epoch
                        self.epoch = 1
                        return None
                    else:
                        self.inc_error += 1
                elif (self.epoch == 10000):
                    print 'Maximum epoch number reached! Aborting...'
                    return None
                else:
                    self.inc_error = 0
                    self.epoch += 1
#                    print 'Epoch, error: ', self.epoch, self.error
                return self.training()
        # Catch maximum recursion limit
        except(RuntimeError):
            print 'Maximum recursion depth reached. Aborting!!!'
            print 'Epoch = ', self.epoch
            exit(-1)

# ------------------------------------------------------------------------------

    # Network run method
    def run(self, pattern):
        self.calc_net(pattern)
        self.calc_output_net()
        return self.y

# ------------------------------------------------------------------------------

if __name__ == "__main__":
    from neuron import BPNeuron
    from sys import exit, setrecursionlimit, getrecursionlimit

    PATTERNS = 'patterns/AR/patterns_all_maoAR3'
    fid = open(PATTERNS, 'r')
    lines = fid.readlines()
    fid.close()
    alpha = 0.1
    n_output_neurons = 4
    tolerance = 150
    setrecursionlimit(10000000)
    test_numbers = []

    training_set = []
    training_setx = []

    for line in lines:
        patterns = line.split()

############### Sempre alterar aqui também
        patterns = line.split()
        training_set.append( ([float(patterns[0]), float(patterns[1]), float(patterns[2])], [int(patterns[3]), int(patterns[4]), int(patterns[5]), int(patterns[6]), int(patterns[7])]))

    for n in range(20,21,1):
        n_hidden_neurons = n

        for alpha in range(1,8,1):
            shuffle(training_set)
            test_numbers = []
            training_setx = []
############### Sempre alterar aqui também
            # 36, 72, 108, 144, 18
            for i in range(36):
                training_setx.append(training_set[i])

            print '-----------'
            print 'Test header'
            print '-----------'
            alpha = alpha/10.0

            print 'alpha\ttolerance\thidden_neurons\toutput_neurons'
            print str(alpha) + '\t' + str(tolerance) + '\t' + str(n_hidden_neurons) + '\t' + str(n_output_neurons)
            
            # Perform 100 tests
            while len(test_numbers) < 100:

                print '---------'
                print 'Test ', len(test_numbers)
                print '---------'

                a1 = BP()
                a1.update_parameters(training_setx, alpha, tolerance, n_hidden_neurons, n_output_neurons, 'bip')

                # Compute training time
                t1 = time()
                weights = a1.training()
                t2 = time()

                delta_t = t2 - t1

                if not weights:
                    print 'Failed.'
                    continue

                fid = open(PATTERNS, 'r')
                lines = fid.readlines()
                fid.close()

                test_set = []
                result_set = []

    ############### Sempre alterar aqui também
                for line in lines:
                    patterns = line.split()
                    test_set.append([float(patterns[0]), float(patterns[1]), float(patterns[2])])
                    result_set.append([int(patterns[3]), int(patterns[4]), int(patterns[5]), int(patterns[6]), int(patterns[7])])

                correct = 0
                total = 0
    ############### Sempre alterar aqui também            
                correct_vector = [0 for i in range(23)]
                total_vector =[0 for i in range(23)]

                for i in range(test_set.__len__()):
                    result = a1.run(test_set[i])

                    # Segment index initialization
                    segment_index = int(result_set[i][4])

                    # Rounding results
                    for j in range(n_output_neurons):
                        if result[j] < 0:
                            result[j] = -1
                        else:
                            result[j] = 1

                    # Test patterns
                    failed = False

                    for j in range(n_output_neurons):
                        if (result[j] != result_set[i][j]):
                            failed = True
                            break
                        #if (result[0] == result_set[i][0]) and (result[1] == result_set[i][1]):

                    if not failed:
                        correct += 1
                        correct_vector[segment_index] += 1
                    
                    total += 1
                    total_vector[segment_index] += 1


                    #print 'dbg ', correct_vector, total_vector


            #            print 'Correct = ', float(correct)
            #            print 'Total = ', float(total)
            #            print 'Performance = ', float(correct)/float(total)

            #            print 'Correct vector: ', correct_vector 
            #            print 'Total vector: ', total_vector

                # Calculate window classification performance
                window_correct = 0
                for i in range(correct_vector.__len__()):
                    if ((float(correct_vector[i])/total_vector[i]) > 0.5):
                        window_correct += 1
                print 'Window performance = ', float(window_correct)/correct_vector.__len__()
                print 'Execution time = ', delta_t
                fid = open('results/res_'+str(n_hidden_neurons)+'_'+str(alpha)+'.dat','a')
                fid.write(str(alpha) + '\t' + str(float(window_correct)/correct_vector.__len__()) + '\t' + str(delta_t) + '\n')
                fid.close()

                #Checking if achieve 100 tests results on file
                fid = open('results/res_'+str(n_hidden_neurons)+'_'+str(alpha)+'.dat','r')
                test_numbers =  fid.readlines()
                fid.close()


