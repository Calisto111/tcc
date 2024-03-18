#!/usr/bin/env python
# -*- coding:utf-8 -*-

# File: net.py
# Description: Neural net class
# Version: 0.5


CONFIG_FILE = 'training_patterns'
CONFIG_FILE_SHORT = 'training_patterns_short'
N_BINARY_NEURON = 5
A_CHAR = 97

INPUT = 0
TARGET = 1

from copy import copy
from random import randint, random
from math import sqrt, pow

from neuron import BPNeuron
from training import BP
from config_file import ConfigFileFloat


class NeuralNet(object):
    def __init__(self, n_neurons):

        self.n_neurons = n_neurons
        self.neuron_list = []
        self.bias = 0
        self.theta = 0
        self.alpha = 1
        
        # Instantiate Adaline training algorithm
        self.adaline = Adaline()

        # Other initializations
        self.epoch = 0
        self.tolerance = 0
        self.patterns = []
        self.targets = []
        
        # Instatiate config file
        if (self.n_neurons == N_BINARY_NEURON):
            self.config_file = ConfigFileFloat(CONFIG_FILE_SHORT)
        else:
            self.config_file = ConfigFileFloat(CONFIG_FILE)

        self.patterns = copy(self.config_file.get_patterns())
        self.targets = copy(self.config_file.get_targets())

        # Plot data
        self.plot_data = []

# ------------------------------------------------------------

    # Update network parameters
    def update_parameters(self, new_alpha, new_tolerance):
        self.alpha = new_alpha
        self.tolerance = new_tolerance

# ------------------------------------------------------------

    # Get training patterns
    def get_patterns(self):
        return self.patterns

# ------------------------------------------------------------

    # Get training targets
    def get_targets(self):
        return self.targets

# ------------------------------------------------------------

    # Training method
    def training(self):
        # Re-init epoch number and plot data
        self.epoch = 0
        self.plot_data = []
        
        for i in range(self.n_neurons):
            self.create_training_list(i)

            self.adaline.update_parameters(self.training_list,
                                           self.alpha,
                                           self.tolerance)

            weights = self.adaline.training()
            bias = self.adaline.get_bias()
            self.epoch += self.adaline.get_epoch()
            self.error_data = self.adaline.get_error_data()

        
            # Add plot data
            self.plot_data.append(copy(self.error_data))

            # Instantiate neuron
            self.neuron_list.append(AdalineNeuron(weights, bias))

# ------------------------------------------------------------

    # Returns plot_data
    def get_plot_data(self):
        return self.plot_data

# ------------------------------------------------------------
    # Test network output for a given pattern
    def test_run(self):
        # Test in a different way for 4-neuron nets
        if self.n_neurons == N_BINARY_NEURON:
            self.test_run_short()
        else:
            for pattern in self.patterns:
                for neuron in self.neuron_list:
                    if neuron.act(pattern) == 1:
                        print (chr(A_CHAR + self.neuron_list.index(neuron)))

# ------------------------------------------------------------

    # Test network output for a given pattern
    def test_run_short(self):
        for pattern in self.patterns:
            output = ''
            for neuron in self.neuron_list:
                if neuron.act(pattern) == 1:
                    output += '1'
                else:
                    output += '0'
            
            print (int(output, 2) - 1)

# ------------------------------------------------------------

    # Test network output for a given pattern
    def run(self, pattern):
        # Test in a different way for 4-neuron nets
        if self.n_neurons == N_BINARY_NEURON:
            return self.run_short(pattern)
        else:
            rec_values = []
            for neuron in self.neuron_list:
                if neuron.act(pattern) == 1:
                    rec_values.append(self.neuron_list.index(neuron))

            return rec_values

# ------------------------------------------------------------

    # Test network output for a given pattern
    def run_short(self, pattern):
        output = ''
        rec_values = []
        for neuron in self.neuron_list:
            if neuron.act(pattern) == 1:
                output = '1' + output
            else:
                output = '0' + output

        value = int(output, 2) - 1
        if value < 10:
            rec_values.append(value)
        return rec_values

# ------------------------------------------------------------

    # Creates a training list for one specific neuron
    def create_training_list(self, neuron_number):
        self.training_list = []
        
        for i in range(self.patterns.__len__()):
            self.training_list.append( (self.patterns[i], self.targets[neuron_number][i] )  )

# ------------------------------------------------------------

    # Return total epoch number
    def get_epoch(self):
        return self.epoch

# ------------------------------------------------------------

# Back propagation net
class BPNet(NeuralNet):
    
    def __init__(self, n_hidden_neurons, net_type='nw'):
        self.n_hidden_neurons = n_hidden_neurons
        self.n_output_neurons = 0
        self.hidden_neurons = []
        self.output_neurons = []
        self.bias = 0
        self.theta = 0
        self.alpha = 1
        
        # Instantiate Adaline training algorithm
#        self.adaline = Adaline()

        # Other initializations
        self.epoch = 0
        self.tolerance = 0
        self.patterns = []
        self.targets = []
        
        # Instatiate config file
        if (self.n_hidden_neurons == N_BINARY_NEURON):
            self.config_file = ConfigFileFloat(CONFIG_FILE_SHORT)
        else:
            self.config_file = ConfigFileFloat(CONFIG_FILE)

        self.patterns = copy(self.config_file.get_patterns())
        self.targets = copy(self.config_file.get_targets())

        # Plot data
        self.plot_data = []

 #       NeuralNet.__init__(self, n_hidden_neurons)
        self.net_type = net_type


# ------------------------------------------------------------

    # Training method
    def training(self):

        # Re-init epoch number and plot data
        self.epoch = 0
        self.plot_data = []

        self.create_training_list()

        # Weights initialization (hidden layer)
        beta = 0.7 * pow(self.n_hidden_neurons, 1.0/self.training_list[0][0].__len__())
        for i in range(self.n_hidden_neurons):
            weights = []
            for j in range(self.training_list[0][0].__len__()):
                weights.append(randint(-500,500)/1000.0)

            bias = randint(-500, 500)/1000.0

            if self.net_type == 'nw':
                norma_vj = 0
                for weight in weights:
                    norma_vj += pow(weight,2)
                norma_vj = sqrt(norma_vj)

                for j in range(weights.__len__()):
                    weights[j] = (beta * weights[j]) / norma_vj

                # -beta <= bias <= beta
                bias = (2 * beta) * random() - beta

            self.hidden_neurons.append(BPNeuron(weights, bias, 'bip'))

        # Weights initialization (output units)
        self.n_output_neurons = self.training_list[0][1].__len__()
        for i in range(self.n_output_neurons):
#        print 'training list [0]: ' + str(self.training_list[0])
            weights = []
            for j in range(self.n_hidden_neurons):
                weights.append(randint(-50,50)/100.0)
            bias = randint(-50,50)/100.0

            self.output_neurons.append(BPNeuron(weights, bias, 'bip'))

        self.back_propagation()

# ------------------------------------------------------------

    # Back propagation
    def back_propagation(self):

        # Error initialization
        self.error = 1000

        # Cycle number
        counter = 0

        while(self.error > self.tolerance):

            for training_tuple in self.training_list:
                # Attributes initialization
                self.delta_output = [0 for i in range(self.n_output_neurons)]
                self.delta_w = [[0 for i in range(self.n_output_neurons)] for i in range(self.n_hidden_neurons)]
                self.delta_w0 = [0 for i in range(self.n_output_neurons)]
                self.delta_in = [0 for i in range(self.n_hidden_neurons)]
                self.delta_hidden = [0 for i in range(self.n_hidden_neurons)]
                self.delta_v = [[0 for i in range(self.n_hidden_neurons)] for i in range(training_tuple[INPUT].__len__())]
                self.delta_v0 = [0 for i in range(self.n_hidden_neurons)]

                input_list = training_tuple[INPUT]
                target = training_tuple[TARGET]

                # Calculate output for output_neurons
                for k in range(self.n_output_neurons):
                    y = self.output_neurons[k].act(self.hidden_layer_act(input_list))
                    self.delta_output[k] = (target[k] - y) * self.output_neurons[k].derivative(self.hidden_layer_net(input_list))
                    print ('--- Delta output: --- ')
                    print (self.output_neurons[k].derivative(self.hidden_layer_net(input_list)))
                    print (self.output_neurons[k].get_weights())
                    print (input_list)

#                print '##### Delta k ####'
#                print self.delta_output

                # Update output neuron weights
                for k in range(self.n_output_neurons):
                    for j in range(self.n_hidden_neurons):
                        self.delta_w[j][k] = self.alpha * self.delta_output[k] * self.hidden_neurons[j].act(input_list)

                    self.delta_w0[k] = self.alpha * self.delta_output[k]


                print ('##### Delta w ####')
                print (self.delta_w)

                # Calculate delta in
                for j in range(self.n_hidden_neurons): # For each hidden neuron
                    for k in range(self.output_neurons.__len__()):
                        # weights = self.output_neurons[k].get_weights()
                        self.delta_in[j] += self.delta_output[k] * self.output_neurons[k].get_weights()[j]
                    # for i in range(self.n_hidden_neurons):
                    self.delta_hidden[j] = self.delta_in[j] * self.hidden_neurons[j].derivative(input_list)

                    # Calculate delta v_ij
                    for i in range(input_list.__len__()):
                        self.delta_v[i][j] = self.alpha * self.delta_hidden[j] * input_list[i]
            
                    # Calculate delta v_0j
                    self.delta_v0[j] = self.alpha * self.delta_hidden[j]

                # Initialize delta_v_old
                #delta_v_old = []
                #delta_v0_j_old = []
#                 for j in range(self.n_hidden_neurons):
#                     for i in range
#                     self.delta_v[][]
#                     delta_v_old_tmp = []
#                     for j in range(input_list.__len__()):
#                         delta_v_old_tmp.append(0)
#                     delta_v_old.append(delta_v_old_tmp)
#                     delta_v0_j_old.append(0)

                # Update weights and biases (output neurons)
                for k in range(self.n_output_neurons):
                    weights = copy(self.output_neurons[k].get_weights())
                    bias = self.output_neurons[k].get_bias()

                    for j in range(self.n_hidden_neurons):
                        weights[j] += self.delta_w[j][k]

                    bias += self.delta_w0[k]
                    self.output_neurons[k].update(weights, bias)

                # Update weights and biases (hidden layer neurons)
                for j in range(self.n_hidden_neurons):
                    weights = copy(self.hidden_neurons[j].get_weights())
                    bias = self.hidden_neurons[j].get_bias()
                                   
                    for i in range(input_list.__len__()):
                        weights[i] += self.delta_v[i][j]

                    bias += self.delta_v0[j]
                    self.hidden_neurons[j].update(weights, bias)

#                     tmp_weights = []
#                     for j in range(input_list.__len__()):
#                         delta_v_old[i][j] = self.alpha * self.delta_j[i] * input_list[j] + mu * delta_v_old[i][j]
#                         tmp_weights.append(delta_v_old[i][j])
#                     self.delta_v.append(tmp_weights)
#                     delta_v0_j_old[i] = self.alpha * self.delta_j[i] + mu * delta_v0_j_old[i]
#                     self.delta_v0_j.append(delta_v0_j_old[i])

                # Update weights and biases
                # Output unit
#                 weights = copy(self.output_neuron.get_weights())
#                 for i in range(weights.__len__()):
#                     weights[i] += self.delta_w[i]


#                 bias = self.output_neuron.get_bias()
#                 bias += self.delta_w0_j

#                 self.output_neuron.update(weights, bias)

#                 # Hidden units
#                 for i in range(self.n_hidden_neurons):
#                     weights = copy(self.hidden_neurons[i].get_weights())
#                     bias = self.hidden_neurons[i].get_bias()

#                     for j in range(weights.__len__()):
#                         weights[j] += self.delta_v[i][j]

#                     bias += self.delta_v0_j[i]

#                     self.hidden_neurons[i].update(weights, bias)

            # Re-init error
            self.error = 0

            # Iterate through training set
            for training_tuple in self.training_list:
                input_list = training_tuple[INPUT]
                target = training_tuple[TARGET]

                # Update error
                self.z = []
                for neuron in self.hidden_neurons:
                    self.z.append(neuron.act(input_list))

                # Calculate output for output_neurons
                for k in range(self.n_output_neurons):
                    y = self.output_neurons[k].act(self.z)
#                    print 'Target: ', target[k]
#                    print 'y: ', y
                    print ('Error: ')
                    print (pow((target[k]-y),2))
                    self.error += pow((target[k] - y), 2)
#                    print 'error: ', self.error
                
            counter += 1
#            print 'Counter: ', counter
            print ('Error: ', self.error)

        print ('Counter: ', counter)
        

# ------------------------------------------------------------

    # Calculates output for all the hidden neurons
    def hidden_layer_act(self, input_list):
        output_list = []
        for hidden_neuron in self.hidden_neurons:
            output_list.append(hidden_neuron.act(input_list))

        return copy(output_list)

# ------------------------------------------------------------

    # Calculates net output for all hidden neurons
    def hidden_layer_net(self, input_list):
        output_list = []
        for hidden_neuron in self.hidden_neurons:
            output_list.append(hidden_neuron.net(input_list))

        return copy(output_list)

# ------------------------------------------------------------

    # Creates a training list for one specific neuron
    def create_training_list(self, neuron_number=None):
        self.training_list = []
        
        if neuron_number: # Creates a training list for a specific neuron
            for i in range(self.patterns.__len__()):
                self.training_list.append( (self.patterns[i], self.targets[i][neuron_number] )  )
        else:
            for i in range(self.patterns.__len__()):
                self.training_list.append( (self.patterns[i], self.targets[i] )  )

# ------------------------------------------------------------

    # Run network with input pattern
    def run(self, pattern):
        
        z = []
        for neuron in self.hidden_neurons:
            z.append(neuron.act(pattern))

        y = []
        for neuron in self.output_neurons:
            y.append(neuron.act(z))

        return copy(y)

# ------------------------------------------------------------

    # Print network weights
    def print_weights(self):
        for neuron in self.hidden_neurons:
            print (neuron.get_weights())

        # Print output neuron weights
        print ('-*- Output neuron -*-')
        print (self.output_neuron.get_weights())

# ------------------------------------------------------------

if __name__ == "__main__":
    myNet = BPNet(3, 'rand')

    alpha = 0.5
    tolerance = 4.5

    myNet.update_parameters(alpha, tolerance)

#    print 'Patterns: ' + str(myNet.patterns)
#    print 'Targets: ' + str(myNet.targets)
    
    myNet.training()
#    print myNet.training_list
#    print myNet.targets

    print ('###########')
    print ('test run')
    print ('###########')

    print ('alpha: ', myNet.alpha)

    print (myNet.run([-1, -1]))
    print (myNet.run([-1, 1]))
    print (myNet.run([1, -1]))
    print (myNet.run([1, 1]))

#    value = -3.14
#    for i in range(51):
#        print myNet.run([value + i * 6.2832/50.0])
#    print myNet.run([2.35])
#    print myNet.run([3.14])
#    print myNet.run([3.92])
#    print myNet.run([4.71])
#    print myNet.run([5.49])
#    print myNet.run([6.28])


#    print '### Network weights ###'
#    myNet.print_weights()

    #myNet.test_run()


