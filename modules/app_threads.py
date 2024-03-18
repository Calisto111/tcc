#!/usr/bin/env python
# -*- coding:utf-8 -*-

# File: app_threads.py
# Description: Application threads
# Author: fmatt
# Date: 02/12/2010

# System imports
from threading import Thread
from copy import copy
from socket import error
from math import pow

# User imports
from fe import FeatureExtractor
from training import Lvq

# Module constants
SEGMENT_LENGTH = 40
MIN_WINDOW_SIZE = 100 # Minimum window size (at least 100 samples)
# ==============================================================================

# Data aquisition thread
class ProducerThread(Thread):
    def __init__(self, data_buffer, socket):
        # Class constants
        self.SIG = 0 # Signal flag
        self.SIG_BEGIN = 1 # Begin of signal flag
        self.SIG_END = 2 # End of signal flag
        self.NOISE = 3 # Noise flag
        self.TKEO_THRESHOLD = 1e6 # TKEO Threshold
        self.NOISE_COUNTER_START = 5 # Noise counter init value

        # Class attributes
        self.data_buffer = data_buffer # Data storage
        self.socket = socket # Communication
        self.local_segment = [] # Local data storage
        self.is_signal = False # Signal flag for TKEO
        self.noise_counter = self.NOISE_COUNTER_START # Noise counter for TKEO
        self.last_data = 0
        self.last_sample = 0
        self.current_sample = 0
        
        
        # Base class constructor
        Thread.__init__(self)

# ------------------------------------------------------------------------------

    # Thread's main function
    def run(self):
        # Thread running
        print ('AcqThread running...')

        # Always keep signal samples
        # Bugfix: must keep NOISE_COUNTER_START + 2 to ignore last element
        noise_before_signal = [0 for i in range(self.NOISE_COUNTER_START + 2)]
        
        try:
            # Thread main loop
            while True:
                # Get data until window is full
                data = self.socket.recv(1024)
                data = data.decode()
                data = data.split('\n')
                data.pop(-1) # Remove last element ('') from data 

                # No data in socket buffer (connection closed)
                if data.__len__() == 0:
                    break

                # Copy data into local storage
                for d in data:
                    # Store current sample
                    noise_before_signal.pop(0)
                    noise_before_signal.append(float(d))
                    
                    td = self.test_data(float(d))
                    if td == self.SIG: # Signal
                        self.local_segment.append(self.last_data) # Append single data (d) to segment
                    elif td == self.SIG_BEGIN: # Signal begin
                        self.local_segment = noise_before_signal[0:self.NOISE_COUNTER_START+1] + self.local_segment
                    elif td == self.SIG_END: # End of signal
                        # Test if ready to send data to buffer
                        if self.local_segment.__len__() >= MIN_WINDOW_SIZE:

                            # DBG
#                            print 'local_segment: ', self.local_segment
#                            print 'local_segment length: ', self.local_segment.__len__()
                            #

                            # Atomic operation: write data to buffer
                            self.data_buffer.lock()
                            self.data_buffer.write(copy(self.local_segment))
                            self.data_buffer.unlock()
                        self.local_segment = [] # Clear local segment
                    else:
                        pass
                    # Update last data
                    self.last_data = float(d)

        except error: # Socket error
            print ('Socket error caught!')
            self.socket.close()
        finally:
            # Atomic operation: close data buffer
            self.data_buffer.lock()
            self.data_buffer.close()
            self.data_buffer.unlock()

# ------------------------------------------------------------------------------

    # Apply TKEO and test data
    def test_data(self, d):
        # Calculate TKEO
        tkeo = pow(self.current_sample, 2) - self.last_sample * d

        # Update samples
        self.last_sample = self.current_sample
        self.current_sample = d

#        print 'tkeo: ', tkeo
        if abs(tkeo) > self.TKEO_THRESHOLD:
            # Reset noise counter
            self.noise_counter = self.NOISE_COUNTER_START

            # Return flag
            if self.is_signal:
                return self.SIG
            else:
                self.is_signal = True
                return self.SIG_BEGIN
        else:
            if self.is_signal:
                if self.noise_counter > 0:
                    self.noise_counter -= 1
                    return self.SIG
                else:
                    self.noise_counter = self.NOISE_COUNTER_START
                    self.is_signal = False
                    return self.SIG_END
            return self.NOISE
        
# ==============================================================================

# Feature extraction thread
class FEThread(Thread):
    def __init__(self, data_buffer, feature_buffer,feExtract,filterOrder,cteCng):
        self.data_buffer = data_buffer # Data buffer
        self.feature_buffer = feature_buffer # Feature buffer
        self.feExtract = feExtract # Type of Feature Extration Herle/AR
        self.filterOrder = filterOrder # Filter order
        self.cteCng = cteCng # Convergence Constant

#        self.segment = Segment([None for i in range(SEGMENT_LENGTH)]) # Data segment

        # Base class constructor
        Thread.__init__(self)

# ------------------------------------------------------------------------------

    # Main method for FEThread
    def run(self):
        # Local variables initialization
        seg_grp = 0 # Segment group

        pathpatterns = ['../patterns/','../patterns/ARs/Adriano/Isotonico/AR3/','../patterns/ARs/Adriano/Isotonico/AR4/','../patterns/ARs/Adriano/Isotonico/AR6/','../patterns/ARs/Adriano/Isotonico/AR8/','../patterns/ARs/Adriano/Isotonico/AR10/']
        pathtrainingpatt = '../gui/res/'

        while True:
            # Check if buffer is closed
            self.data_buffer.lock()
            if self.data_buffer.is_closed():
                # Unlock data buffer
                self.data_buffer.unlock()
                # Close feature buffer
                self.feature_buffer.lock()
                self.feature_buffer.close()
                self.feature_buffer.unlock()
                break
            # If not, check if there is data to be read
            if self.data_buffer.get_length() != 0:
                # Update data in ring buffer
                data_tmp = self.data_buffer.read()
                self.data_buffer.unlock()
                newfiletrainingp = ''
                newfilepaterns = ''

                ### DBG
                #print 'data_tmp: ', data_tmp
                #print 'data_tmp length: ', data_tmp.__len__()
                ###
                
                #Extract Method Herle was selected
                if self.feExtract == 1:
                    fe = FeatureExtractor(data_tmp, SEGMENT_LENGTH,0,0)
                    fe.calc_all()
                    fv = fe.get_feature_vectors()

                    ### DBG
                    #print 'feature vectors: ', fv
                    #print 'Tamanho do feature vectors: ', len(fv)
                    ###

                    # Write feature vector in feature buffer
                    self.feature_buffer.lock()
                    for feature_vector in fv:
                        self.feature_buffer.write((copy(feature_vector), seg_grp))
                        #for each_feature_vector in feature_vector:
                            #Traning patterns                            
                            #newfiletrainingp= newfiletrainingp+str(each_feature_vector)+'\t'
                            #Patterns                            
                            #newfilepaterns=newfilepaterns+str(each_feature_vector)+'\t'
                        #Traning patterns, dont forget to change ind of string: 0, 1, 2 e 3
                        #newfiletrainingp=newfiletrainingp+str(3)+'\n'
                        #Patterns
                        #newfilepaterns=newfilepaterns+'\n'

                    self.feature_buffer.unlock()

                    #Saving Traning patterns: Example file name: adrisom1_training_patterns.dat
                    #Name patterns file: adrisom1_, adrisot1_
                    # adrisom1_ adrisot1_, dan_:               
                    #fid=open(pathtrainingpatt+'adrisot1_training_patterns.dat','a')
                    #fid.writelines(newfiletrainingp)
                    #fid.close

                    #Saving patterns: Example file name: adrisom1_extensao_03
                    #Name patterns file: adrisom1_, adrisot1_
                    # adrisom1_ adrisot1_, dan_: extensao, flexao, grasp, e torcao                    
                    #fid=open(pathpatterns[0]+'adrisot1_torcao_0'+str(seg_grp+1)+'.pat','w')
                    #fid.writelines(newfilepaterns)
                    #fid.close

    #                 for i in range (data_tmp.__len__()/SEGMENT_LENGTH):
    #                     # Copy SEGMENT_LENGTH samples each time
    #                     self.segment.update_data(data_tmp[SEGMENT_LENGTH * i : SEGMENT_LENGTH * (i + 1)])

    #                     ### DBG
    #                     #print 'segment: '
    #                     #self.segment.print_data_vector()
    #                     ###

    #                     # Extract features from segment
    #                     self.segment.calc_all(threshold=1e-6)

    #                     ### DBG
    #                     print 'feature vector, seg_grp: ', self.segment.get_feature_vector(), seg_grp
    #                     ###

                        
    #                     # Write feature vector in feature buffer
    #                     self.feature_buffer.lock()
    #                     self.feature_buffer.write((copy(self.segment.get_feature_vector()), seg_grp))
    #                     self.feature_buffer.unlock()

                    # Update segment group
                    if seg_grp == 9:
                        seg_grp = 0
                    else:
                        seg_grp += 1
                    
                    ### DBG
    #                print 'Thread 2, feature vector: '
    #                print self.segment.get_feature_vector()
    #                print 'Feature buffer: '
    #                print self.feature_buffer.get_data()
                    ### 
                else: # Extract Method selected was AR
                    print ("TODO: Implementar o Método de Extração AR")
                    #print "Tamanho dos buffer de dados temporários:", len(data_tmp)
                    fe = FeatureExtractor(data_tmp, SEGMENT_LENGTH,self.filterOrder,self.cteCng) 
                    fe.calc_all_Ar()
                    fv = fe.get_feature_vectors_AR()
                    #print 'feature vectors: ', fv
                    #print 'Tamanho do feature vector: ',len(fv)
                    
                    # Write feature vector in feature buffer
                    self.feature_buffer.lock()

                    for feature_vector in fv:
                        #print "Segmento : ", feature_vector
                        #print "Tamanho de cada vetor",len(feature_vector[0])
                        for each_feature_vector in feature_vector:
                            #print "Each segmento: ", each_feature_vector
                            for am_feature_vector in each_feature_vector:
                                #print "Each segmento: ", am_feature_vector
                                self.feature_buffer.write((copy(am_feature_vector), seg_grp))
                                #for am_feature_vecto_value in am_feature_vector:
                                    #Traning patterns                            
                                    #newfiletrainingp= newfiletrainingp+str(am_feature_vecto_value)+'\t'
                                    #Patterns                            
                                    #newfilepaterns=newfilepaterns+str(am_feature_vecto_value)+'\t'
                                #Traning patterns, dont forget to change ind of string: 0, 1, 2 e 3
                                #newfiletrainingp=newfiletrainingp+str(3)+'\n'
                                #Patterns
                                #newfilepaterns=newfilepaterns+'\n'


                    self.feature_buffer.unlock()
                    #Saving Traning patterns: Example file name: danAR3_training_patterns.dat
                    #Name patterns file: danAR3, danAR4, danAR6, danAR8 e danAR10
                    # danAR#_traning_patterns:                 
                    #fid=open(pathtrainingpatt+'adrisot1AR10_traning_patterns.dat','a')
                    #fid.writelines(newfiletrainingp)
                    #fid.close

                    #Saving patterns: Example file name: adrisom1_extensao_03
                    #Name patterns file: dan_extensao_01
                    # adrisom1_ adrisot1_, dan_: extensao, flexao, grasp, e torcao                    


                    #if (self.filterOrder == 3):
                        #fid=open(pathpatterns[1]+'adrisot1_torcao_0'+str(seg_grp+1)+'.pat','w')
                    #if self.filterOrder == 4:
                        #fid=open(pathpatterns[2]+'adrisot1_torcao_0'+str(seg_grp+1)+'.pat','w')
                    #if self.filterOrder == 6:
                        #fid=open(pathpatterns[3]+'adrisot1_torcao_0'+str(seg_grp+1)+'.pat','w')
                    #if self.filterOrder == 8:
                        #fid=open(pathpatterns[4]+'adrisot1_torcao_0'+str(seg_grp+1)+'.pat','w')
                    #if self.filterOrder == 10:
                        #fid=open(pathpatterns[5]+'adrisot1_torcao_0'+str(seg_grp+1)+'.pat','w')
                    #fid.writelines(newfilepaterns)
                    #fid.close

                    # Update segment group
                    if seg_grp == 9:
                        seg_grp = 0
                    else:
                        seg_grp += 1
            else:
                self.data_buffer.unlock()

# ==============================================================================

# Classification Thread
class ClassificationThread(Thread):
    def __init__(self, feature_buffer,netChoice):
        # Class constants
        self.N_CLASSES = 4 # Classes of movement
        self.config_file = '../res/cfg_network'
#        self.NOISE_CLASS = 4 # Index of noise class

        self.feature_buffer = feature_buffer # Feature buffer
        self.feature_vector = [] # Feature vector
        self.netChoice = netChoice #Rede Selecionada

        #After had trained, choose Neural Net to create weights
        
        if self.netChoice == 1:
            weights = self.read_config_file()
    #        print 't3: weights = ', weights

            self.neural_network = Lvq(weights=weights, n_classes=self.N_CLASSES) # LVQ Neural network
            print ("Aqui")
        else:
            print ("TODO: Chamar método BpNet para gerar os pesos")
            pass
        # Base class constructor
        Thread.__init__(self)

# ------------------------------------------------------------------------------

    # Get neural network weigths from configuration file
    def read_config_file(self):
        weights = []
        
        # Read config file
        fid = open(self.config_file, 'r')
        lines = fid.readlines()
        fid.close()

        # Get network weights
        for line in lines:
            weight_vector = line.split()
            weight_vector = map(float, weight_vector) # Convert weigts to float
            weights.append(weight_vector)

        return weights

# ------------------------------------------------------------------------------

    # Main method for ClassificationThread
    def run(self):
        # Local initializations
        # Store last 3 recognized moves
        rec_moves_queue = [None, None, None] 
        
        # Store last segment group
        last_seg_grp = None

        while True:
            # Check if buffer is closed
            self.feature_buffer.lock()
            if self.feature_buffer.is_closed():
                self.feature_buffer.unlock()
                break
            # If not, check if there is data to be read
            if self.feature_buffer.get_length() != 0:
                #If NeuralNet selected was LVQ:
                if self.netChoice == 1:

                    # Update feature vector
                    self.feature_vector, seg_grp = copy(self.feature_buffer.read())
                    self.feature_buffer.unlock()
                    #print 't3: vector = ', self.feature_vector , 'seg_grp:', seg_grp
    #                print 't3: class = ', self.neural_network.run(self.feature_vector)
    #                print 'recognized_move: ', self.neural_network.run(self.feature_vector)

                    # Need to compare recognized moves from the same segment group (consecutive segments)
                    if last_seg_grp != seg_grp:
                        # Clear last recognized moves
                        rec_moves_queue = [None, None, None]
                        
                        # Update segment group
                        last_seg_grp = seg_grp

                    # Pop first element and appends new recognized move
                    del rec_moves_queue[0]
                    rec_moves_queue.append(self.neural_network.run(self.feature_vector))

                    # DBG
                    #print 'rec_moves_queue, seg_grp:', rec_moves_queue, seg_grp

                    # Two consecutive segments recognized = move recognized
    #                if (rec_moves_queue[-1] == rec_moves_queue[-2]) and (rec_moves_queue[-1] == rec_moves_queue[-3]):
                    if (rec_moves_queue[-1] == rec_moves_queue[-2]):
                        #print 't3: class = ', rec_moves_queue[-1]
                        pass

    #                print 'Thread 3, feature vector: ', self.feature_vector
               #Otherwise, NeuralNet selected was BpNet
                else: 
                    print ("TODO: Implementar BpNet para classificar sinais")
                    self.feature_buffer.unlock()
            else:
                # Don't forget to release lock
                self.feature_buffer.unlock()

# ==============================================================================

        


