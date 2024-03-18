#!/usr/bin/env python
# -*- coding:utf-8 -*-

# File: traininga.py
# Description: Training algorithms
# Version: 0.5

# System imports
from copy import copy, deepcopy
from random import randint, shuffle
from os import system
from math import sqrt
from sys import argv

# Module constants
DBG = True

class Neuron(object):
    def __init__(self, weights, theta, function='bin', training='A'):
        self.theta = theta
        self.weights = []
        self.function = function
        self.training_type = training

    
        for i in range(weights.__len__()):
            self.weights.append(weights[i])

# ------------------------------------------------------------

    def act(self, xs):
        sum = 0
        # Input is always 1 for bias
#        xs.append(1)
        
        if self.training_type == 'A':
            for i in range(xs.__len__()):
                sum += xs[i] * self.weights[i]
            return self.output(sum)
        else:
            sum = []
            for i in range(self.weights.__len__()):
                sum_tmp = 0
                for j in range(self.weights[0].__len__()):
                    sum_tmp += xs[j] * self.weights[i][j]
                sum.append(sum_tmp)
            return self.output(sum)


# ------------------------------------------------------------

    def output(self, sum):
        if self.training_type == 'A':
            if (sum > self.theta):
                return 1
            else:
                if self.function == 'bin':
                    return 0
                else:
                    return -1
        else:
            result = []
            for i in range (self.weights.__len__()):
                if (sum[i] > self.theta):
                    result.append(1)
                else:
                    if self.function == 'bin':
                        result.append(0)
                    else:
                        result.append(-1)
            return result

# ------------------------------------------------------------

class TriStateNeuron(Neuron):

    def __init__(self, weights, theta):
        self.theta = theta
        self.weights = []

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

class Hebb(object):
    def __init__(self):
        pass

    def train(self, training_set):
        n_input = training_set[0][0].__len__()
        w = []

        # Weights initialization
        for i in range(n_input):
            w.append(0)

        for training_tuple in training_set:
            input_list = training_tuple[0]

            # Append bias to input list
#            input_list.append(1)

            target=  training_tuple[1]
            
            for i in range(w.__len__()):
                w[i] = w[i] + input_list[i] * target
    
           # print 'weights: ', w
        return w

# ------------------------------------------------------------

class HebbOuterProduct(object):
    def __init__(self):
        pass

    def train(self, training_set):
        n_input = training_set[0][0].__len__()
        n_output = training_set[0][1].__len__()
        
        w = []

        # Weights initialization
        for i in range(n_output):
            w_tmp = []
            for j in range(n_input):
                w_tmp.append(0)
            w.append(w_tmp)

        for training_tuple in training_set:
            input_list = training_tuple[0]
            target_list = training_tuple[1]

            for i in range(input_list.__len__()):
                for j in range(target_list.__len__()):
                    w[j][i] += input_list[i] * target_list[j]

    
        print ('weights: ', w)
        return w

# ------------------------------------------------------------

class Som(object):
    def __init__(self, training_list, n_clusters, alpha, tolerance, n_neighbors, weights=None):

        # Parameters initialization
        self.training_list = copy(training_list)
        self.n_clusters = n_clusters
        self.alpha = alpha
        self.n_inputs = self.training_list[0].__len__()
        self.tolerance = tolerance
        self.n_neighbors = n_neighbors
        
        # Weights initialization
        self.weights = []
        for i in range(self.n_clusters): # For each cluster, init weights
            tmp_weights = []
            if (weights): # Init values
                for j in range(weights[i].__len__()):
                    tmp_weights.append(weights[i][j])
            else: # No init values, init with 0
                for j in range(self.training_list[0].__len__()):
                    tmp_weights.append(0)
            self.weights.append(copy(tmp_weights))

        self.plot_data()

        self.training() # Network training

# ------------------------------------------------------------

    # Training algorithm
    def training(self):
        # Initialization
        stopping_condition = False
        epoch = 0
        d = []
        for cluster in range(self.n_clusters):
            d.append(0)

        while not stopping_condition:
            for input_vector in self.training_list:
                
                for j in range(self.n_clusters):
                    # Re-init d
                    d[j] = 0
                    for i in range(input_vector.__len__()):
                        d[j] += pow(self.weights[j][i] - input_vector[i], 2)
                
                # Find index J
                j_index = d.index(min(d))

                # Update weights
                for i in range(self.n_inputs):

                    for offset in range(self.n_neighbors + 1):
                        # Update left neighbor
                        tmp_index = j_index - offset
                        if (tmp_index) >= 0:
                            self.weights[tmp_index][i] = self.weights[tmp_index][i] + self.alpha * (input_vector[i] - self.weights[tmp_index][i])

                        tmp_index = j_index + offset
                        # Update right neighbor
                        if tmp_index < d.__len__():
                            self.weights[tmp_index][i] = self.weights[tmp_index][i] + self.alpha * (input_vector[i] - self.weights[tmp_index][i])

            self.alpha = self.alpha - 0.0049

            epoch += 1
            if not (epoch % 10):
                self.plot_data()

            if self.alpha <= self.tolerance:
                stopping_condition = True
                
                # If data not yet plotted, last plot
                if (epoch % 10):
                    self.plot_data()

# ------------------------------------------------------------

    def plot_data(self):
        # Common initializations
        lines = []

        # Write data to file
        for weights in self.weights:
            line = str(weights[0]) + '\t' + str(weights[1]) + '\n'
            lines.append(line)

        fid = open('data', 'w')
        fid.writelines(lines)
        fid.close()

        cmd = "gnuplot -persist -e 'plot" + '"data" with linespoints 2, ' + '"training_patterns" with points 1' + "'"
        system(cmd)

# ------------------------------------------------------------

    # Print network weights
    def print_weights(self):
        print (self.weights)

# ==============================================================================

class Lvq(object):
    def __init__(self, *args, **kwargs):
        # Class constants
        self.TRAINING_ERROR = -1
        self.TRAINING_OK = 0

        # Test correct usage
        # Lvq(training_list, n_clusters, alpha, mult_alpha, tolerance, n_classes)
        if kwargs.__len__() == 6:
            # Parameters initialization
            self.training_list = kwargs.get('training_list')
            self.n_clusters = kwargs.get('n_clusters')
            self.alpha = kwargs.get('alpha')
            self.mult_alpha = kwargs.get('mult_alpha') # Alpha reducing factor
            self.tolerance = kwargs.get('tolerance')
            self.n_classes = kwargs.get('n_classes')
            self.n_inputs = self.training_list[0][0].__len__()       

            ### DBG
            print ('self.training_list: ', self.training_list.__len__())
            #print "Lista de training", self.training_list
            ###

            # Shuffle training list
            shuffle(self.training_list)

            # Weights initialization
            self.weights = []

            # Test if enough training patterns
            if self.n_clusters > self.training_list.__len__():
                return
            for i in range(self.n_clusters): # For each cluster, init weights
                tmp_weights = []
                for training_tuple in self.training_list:
                    if training_tuple[1] == (i % self.n_classes):
                        for weight in training_tuple[0]:
                            tmp_weights.append(weight)
                        self.training_list.pop(self.training_list.index(training_tuple))
                        break

                # No more training patterns for this class, append last pattern (nevermind the class) at this place
                if tmp_weights.__len__() == 0:
                    for weight in self.training_list[-1][0]:
                        tmp_weights.append(weight)
                    self.training_list.pop()
                
                self.weights.append(copy(tmp_weights))
            #print "Pesos", self.weights
            #print "Tamanho dos pesos", len(self.weights)

        # Lvq(weights, n_classes)
        elif kwargs.__len__() == 2:
            self.weights = deepcopy(kwargs.get('weights'))
            self.n_classes = kwargs.get('n_classes')
            self.n_clusters = self.weights.__len__()

        # Incorrect usage
        else:
            print ('Incorrect usage: Lvq constructor takes 6 or 2 arguments.')
            
# ------------------------------------------------------------------------------

    # Training algorithm
    def training(self):
        # Initialization
        stopping_condition = False
        epoch = 0
        d = []

        # Test if enough training patterns

        ### DBG
        print ('n_clusters: ', self.n_clusters)
        #print 'weights: ', self.weights[72:]
        ###

        if self.n_clusters > self.weights.__len__():
            print ('Error: not enough training patterns.')
            print ('Number of clusters and number of training patterns must be at least the same length')
            return self.TRAINING_ERROR

        # Clusters initialization
        for cluster in range(self.n_clusters):
            d.append(0)

        while not stopping_condition:
            for training_tuple in self.training_list:
                input_vector = training_tuple[0]
                
                for j in range(self.n_clusters):
                    # Re-init d
                    d[j] = 0
                    for i in range(input_vector.__len__()):
                        
                        # DBG
                       # print 'i, j: ', i, j
#                        print 'weights[]: ', self.weights[j][0]
#                        print 'input vector: ', input_vector
                        #

                        d[j] += pow(self.weights[j][i] - input_vector[i], 2)
                        
                    d[j] = sqrt(d[j])

                # Find index J
                j_index = d.index(min(d))

                # Bugfix: compare target with classification, not with cluster index
                classif = j_index % 4

                # Update weights
                for i in range(self.n_inputs):
                    # Target matches cluster
                    if classif == training_tuple[1]:
                        self.weights[j_index][i] = self.weights[j_index][i] + self.alpha * (input_vector[i] - self.weights[j_index][i])
                    else:
                        self.weights[j_index][i] = self.weights[j_index][i] - self.alpha * (input_vector[i] - self.weights[j_index][i])

            # Update alpha
            self.alpha = self.alpha * self.mult_alpha

            epoch += 1

#            self.plot_data()

            if self.alpha <= self.tolerance:
                stopping_condition = True

        # Debug
        if DBG:
            print ('Epoch = ', epoch)

        return self.TRAINING_OK

# ------------------------------------------------------------------------------

    # Run network
    # pattern: float list corresponding to the pattern to be classified
    def run(self, pattern):
        d = [] # Distance vector

        # Initialize distance vector
        for cluster in range(self.n_clusters):
            d.append(0)

        for i in range(self.n_clusters):
            for j in range(len(list(pattern))):
                print(f"Pattern list: {pattern}")
                d[i] += pow(self.weights[i][j] - list(pattern)[j], 2)
            d[i] = sqrt(d[i])

        # Find J index (minimum distance)
        j_index = d.index(min(d))

        if j_index > (self.n_classes - 1):
            class_found = j_index % self.n_classes
        else:
            class_found = j_index

        return class_found

# ------------------------------------------------------------------------------

    def plot_data(self):
        # Common initializations
        lines = []

        # Write data to file
        for weights in self.weights:
            line = str(weights[0]) + '\t' + str(weights[1]) + '\n'
            lines.append(line)

        fid = open('data', 'w')
        fid.writelines(lines)
        fid.close()

        cmd = "gnuplot -persist -e 'set nokey; set term postscript eps enhanced color; set output" + '"../img/output.eps"; plot "data" with points 3 ' + "'"
#        cmd = "gnuplot -persist -e 'plot" + '"data" with points 3 ' + "'"
        system(cmd)

# ------------------------------------------------------------------------------

    def print_weights(self):
        print ('Weights:')
        for i in range(self.n_clusters):
            print (self.weights[i])

# ------------------------------------------------------------------------------
    
    # Returns network weights
    def get_weights(self):
        return deepcopy(self.weights)

# ------------------------------------------------------------------------------

    # Update network weights
    def update_weights(self, new_weights):
        self.weights = deepcopy(new_weights)

# ==============================================================================

if __name__ == "__main__":

    # Test correct usage
    if (argv.__len__() != 3):
        print ('Arguments missing!')
        print ('Usage: training.py <training_file> test_flag')
        exit(-1)

    # Get file name from input parameters
    filename = argv[1] 
    test_flag = int(argv[2])

    # Get patterns from file
    fid = open(filename, 'r')
    lines = fid.readlines()
    fid.close()

    # Init training list
    training_list = []
    for line in lines:
        # Ignore comments and blanklines
        if not ( line.startswith('#') or line.isspace() ):
            patterns = line.split()
            training_list.append((map(float, patterns[0:-1]), int(patterns[-1]) ) )

#    print training_list

#     training_list = [([0.2, 0.2], 0),
#                      ([0.2, 0.4], 0),
#                      ([0.4, 0.2], 0),
#                      ([0.4, 0.4], 0),
#                      ([0.6, 0.2], 1),
#                      ([0.8, 0.2], 1),
#                      ([0.6, 0.4], 1),
#                      ([0.8, 0.4], 1),
#                      ([0.2, 0.6], 2),
#                      ([0.4, 0.6], 2),
#                      ([0.2, 0.8], 2),
#                      ([0.4, 0.8], 2),
#                      ([0.6, 0.6], 3),
#                      ([0.6, 0.8], 3),
#                      ([0.8, 0.6], 3),
#                      ([0.8, 0.8], 3),
#                      ([0.25, 0.25], 3)]

    n_clusters = 80
    alpha = 0.5
    tolerance = 0.01
    n_classes = 4
    mult_alpha = 0.95

    # Test patterns
    test_class_0 = [2276.0, 446.4, 23, 26, 136160.0]
    test_class_1 = [1994.0, 0, 24, 27, 116816.0]
    test_class_2 = [2798.0, 1487.2, 17, 26, 161008.0]
    test_class_3 = [2549.3, -617.6, 25.25, 28.75, 167880.0]
    test_class_4 = [3666.0, -11.4666666667, 20.1666666667, 23.1666666667, 214936.0]
    test_class_5 = [2827.06666667, -198.8, 22.3333333333, 28.5, 180538.666667]
    test_class_6 = [2830.4, -677.7, 23.75, 26.75, 180892.0]
    test_class_7 = [1319.2, -79.0666666667, 20.0, 24.3333333333, 73728.0]
    test_class_8 = [5320.8, 12.0, 21.0, 25.6666666667, 320853.333333]
    test_class_9 = [2794.33333333, -611.533333333, 22.0, 27.3333333333, 168546.666667]
    test_class_10 = [3921.06666667, -1655.46666667, 22.0, 27.0, 247845.333333]

    my_lvq = Lvq(training_list, n_clusters, alpha, mult_alpha, tolerance, n_classes)

#     print 'Running test 1: '
#     my_lvq.run(test_class_0)

#     print 'Running test 2: '
#     my_lvq.run(test_class_1)

#     print 'Running test 3: '
#     my_lvq.run(test_class_2)

#     print 'Running test 4: '
#     my_lvq.run(test_class_4)

#     print 'Running test 5: '
#     my_lvq.run(test_class_5)

#     print 'Running test 6: '
#     my_lvq.run(test_class_6)

#     print 'Running test 7: '
#     my_lvq.run(test_class_7)

#     print 'Running test 8: '
#     my_lvq.run(test_class_8)

#     print 'Running test 9: '
#     my_lvq.run(test_class_9)

#     print 'Running test 10: '
#     my_lvq.run(test_class_10)


    print ('Testing...')

    # Testing: correct and wrong flags
    correct = 0
    wrong = 0

    for training_tuple in training_list:
        if training_tuple[1] == test_flag:
            if my_lvq.run(training_tuple[0]) == test_flag:
                correct += 1
            else:
                wrong += 1

    print ('Correct: ', correct)
    print ('Wrong: ', wrong)
    print ('Accuracy: ', round(float(correct) / (correct + wrong) * 100))


#    my_lvq.print_weights()
