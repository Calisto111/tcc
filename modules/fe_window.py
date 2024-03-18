#!/usr/bin/env python
# -*- coding:utf-8 -*-

# File: fe.py
# Description: Feature extraction module
# Version: 0.5
# Date: 14/06/2010

# System imports
from copy import copy
from sys import argv, exit

# User imports
from utils import format_lines

class FeatureExtractor(object):
    # Constructor
    # data_vector: data float list
    # segment_length: segment length (samples)
    def __init__(self, data_vector, segment_length,filterOrder,cteCng):
        self.data_vector = copy(data_vector) # Data vector initialization
        self.segment_length = segment_length # Segment length (samples)
        self.filterOrder = filterOrder
        self.cteCng = cteCng
        self.regression_vec = None
        self.FirstOp = 0
        self.yhat = []
        self.AR_vect = []
        self.temp_AR = []

        # Parameters initialization
        self.n_segments = 0
        self.segments = []

        # Other initializations
        self.zc_threshold = 1e-6

        if self.filterOrder == 0 and self.cteCng == 0 :
            # Segment signal
            self.segment_signal()

        # Window AR feature extraction
        self.calc_AR()


# ------------------------------------------------------------------------------

    # Signal segmentation
    def segment_signal(self):
        self.n_segments = self.data_vector.__len__() / self.segment_length
        print ("\n Entrou com ", self.n_segments, "segmentos")        
        # Remove not-used samples
        extra_samples = self.data_vector.__len__() % self.segment_length

        if extra_samples:
            if extra_samples % 2: # Odd number,
                for i in range(extra_samples / 2 + 1): # Remove n/2 + 1 samples from the beginning
                    self.data_vector.__delitem__(0)
                for i in range(extra_samples / 2): # Remove n/2 samples from the end
                    self.data_vector.__delitem__(-1)
            else:
                for i in range(extra_samples / 2):
                    self.data_vector.__delitem__(0)
                    self.data_vector.__delitem__(-1)

        # Create signal segments
        for segment in range(self.n_segments):
            self.segments.append( Segment(self.data_vector[segment * 40 : (segment + 1) * 40]) )
        #print "\nSaiu"
# ------------------------------------------------------------------------------

    # Segment feature extraction
    def calc_all(self):
        for i in range(self.n_segments):
            if i > 0:  # If not in first segment, set last mav
                self.segments[i].set_last_mav(self.segments[i - 1].get_mav())
            self.segments[i].calc_mav()  # Calc mav
            self.segments[i].calc_mavs()
            self.segments[i].calc_zc(self.zc_threshold)
            self.segments[i].calc_ssc(self.zc_threshold)
            self.segments[i].calc_wl()

# ------------------------------------------------------------------------------

    # Returns feature vectors Herle
    def get_feature_vectors(self, virtual_vector_flag=False):
        feature_vectors = []

        # If available samples less than segment size
        if self.segments.__len__() == 0:
            return []

        for segment in self.segments:
            feature_vectors.append(segment.get_feature_vector())

        # Create virtual segment using current segments
        # Initialize feature vector
        if virtual_vector_flag:
            virtual_feature_vector = []
            for i in range(feature_vectors[0].__len__()):
                virtual_feature_vector.append(0)

            for feature_vector in feature_vectors:
                for i in range(feature_vector.__len__()):
                    virtual_feature_vector[i] += feature_vector[i]

            # Calculate average values
            for i in range(virtual_feature_vector.__len__()):
                virtual_feature_vector[i] = virtual_feature_vector[i] / float(feature_vectors.__len__())

            # Append virtual feature vector to feature vectors
            feature_vectors.append(virtual_feature_vector)

        return feature_vectors

# ------------------------------------------------------------------------------

# ==============================================================================

    # Calculate Regression of each 
    def calc_AR(self):

        #inicialization of regression vector        
        erro = 0.0
        yhatfile = ''
        for i in range (len(self.data_vector)):
            somaYhat = 0.0
            #Inicializando os coeficientes do filtro AR
            if self.FirstOp == 0:
                for j in range(self.filterOrder):
                    self.temp_AR.append(0.0)
                self.AR_vect.append(self.temp_AR)
                self.FirstOp = 1
            #print "Valor de I:", i
            #print self.AR_vect
            #Calculando o yhat
            for j in range(self.filterOrder):
                #print "I, J:", i, j
                    if i == 0:
                        somaYhat+=0.0
                    if i == 1 and j <=1 :
                        somaYhat+=self.AR_vect[i][j]*(float(self.data_vector[i-j])/10000)
                    if i == 2 and j <= 2:
                        somaYhat+=self.AR_vect[i][j]*(float(self.data_vector[i-j])/10000)
                    if i == 3 and j <= 3:
                        somaYhat+=self.AR_vect[i][j]*(float(self.data_vector[i-j])/10000)
                    if i == 4 and j <= 4:
                        somaYhat+=self.AR_vect[i][j]*(float(self.data_vector[i-j])/10000)
                    if i == 5 and j <= 5:
                        somaYhat+=self.AR_vect[i][j]*(float(self.data_vector[i-j])/10000)
                    if i == 6 and j <= 6:
                        somaYhat+=self.AR_vect[i][j]*(float(self.data_vector[i-j])/10000)
                    if i == 7 and j <= 7:
                        somaYhat+=self.AR_vect[i][j]*(float(self.data_vector[i-j])/10000)
                    if i == 8 and j <= 8:
                        somaYhat+=self.AR_vect[i][j]*(float(self.data_vector[i-j])/10000)
                    if i >= 9:
                        somaYhat+=self.AR_vect[i][j]*(float(self.data_vector[i-j])/10000)
            self.yhat.append(-1*somaYhat)
            yhatfile+=str(self.yhat[i])+'\n'
            #print "Valor de Yhat:", self.yhat[i]
            #Calculando o Erro de Estimação e(n)
            erro = float(self.data_vector[i])/10000-self.yhat[i]
            #print "Valor do Erro: ", erro
            #Starting temporary temp_AR
            self.temp_AR = []
            for l in range(self.filterOrder):
                self.temp_AR.append(0.0)
            #Atualizando os coeficientes do modelo AR:
            for k in range(self.filterOrder):
                    if i == 0:
                        self.temp_AR[k]=self.AR_vect[i][k]-2*self.cteCng*erro*(float(self.data_vector[i-k])/10000)
                    if i == 1 and k <=1 :
                        self.temp_AR[k]=self.AR_vect[i][k]-2*self.cteCng*erro*(float(self.data_vector[i-k])/10000)
                    if i == 2 and k <= 2:
                        self.temp_AR[k]=self.AR_vect[i][k]-2*self.cteCng*erro*(float(self.data_vector[i-k])/10000)
                    if i == 3 and j <= 3:
                        self.temp_AR[k]=self.AR_vect[i][k]-2*self.cteCng*erro*(float(self.data_vector[i-k])/10000)
                    if i == 4 and j <= 4:
                        self.temp_AR[k]=self.AR_vect[i][k]-2*self.cteCng*erro*(float(self.data_vector[i-k])/10000)
                    if i == 5 and j <= 5:
                        self.temp_AR[k]=self.AR_vect[i][k]-2*self.cteCng*erro*(float(self.data_vector[i-k])/10000)
                    if i == 6 and j <= 6:
                        self.temp_AR[k]=self.AR_vect[i][k]-2*self.cteCng*erro*(float(self.data_vector[i-k])/10000)
                    if i == 7 and j <= 7:
                        self.temp_AR[k]=self.AR_vect[i][k]-2*self.cteCng*erro*(float(self.data_vector[i-k])/10000)
                    if i == 8 and j <= 8:
                        self.temp_AR[k]=self.AR_vect[i][k]-2*self.cteCng*erro*(float(self.data_vector[i-k])/10000)
                    if i >= 9:
                        self.temp_AR[k]=self.AR_vect[i][k]-2*self.cteCng*erro*(float(self.data_vector[i-k])/10000)
            if (len(self.data_vector)-1) != i:
                self.AR_vect.append(self.temp_AR)

        fid = open('yhat.dat','w')
        fid.writelines(yhatfile)        
        fid.close
        print ("Quantidade de Valores: ",len(self.data_vector))
        #print "Vetor de Caracterísitcas", self.AR_vect
        #print "Quantidade de pontos do vetor de características", len(self.AR_vect)
        #print "Quantidade de pontos: ", self.length
        #print "Quantidade de pontos do data vector:",len(self.data_vector)
# ------------------------------------------------------------------------------
    
    # Returns feature vectors AR
    def get_feature_vectors_AR(self):
        feature_vectors_AR = []

        # If available samples less than segment size
        if self.data_vector.__len__() == 0:
            return []
        
        else:
            feature_vectors_AR.append(self.AR_vect)

        return feature_vectors_AR

# ------------------------------------------------------------------------------
    
    # Prints segment
    def print_segment(self, segment):
        self.segments[segment].print_data_vector()

# ==============================================================================

class Segment(object):
    # Constructor
    # data: data float list
    def __init__(self, data):
        self.data_vector = copy(data) # Data vector initialization
        self.length = self.data_vector.__len__() # Data vector length

        # Parameters initialization
        self.mav = None
        self.last_mav = None # Used to calculate MAVS
        self.mavs = None
        self.zc = None
        self.ssc = None
        self.wl = None

# ------------------------------------------------------------------------------

    # Calculate mean absolute value of segment
    def calc_mav(self):
        sum = 0.0
        for data in self.data_vector:
            sum += abs(data)
        self.mav = sum / float(self.length)

# ------------------------------------------------------------------------------

    # Calculate mean absolute value slope
    def calc_mavs(self):
        if self.last_mav:
            self.mavs = self.mav - self.last_mav
        else:
            self.mavs = 0

# ------------------------------------------------------------------------------
            
    # Calculate zero crossing
    # threshold: threshold to reduce noise-inducted zero crossing
    def calc_zc(self, threshold=None):
        # zc initialization
        self.zc = 0

        # Threshold initialization
        if not threshold:
            threshold = 0

        for i in range (self.length):
            if (i + 1) < self.length:
                if ( ( self.data_vector[i] > 0 ) and ( self.data_vector[i + 1] < 0 ) )\
                        or ( ( self.data_vector[i] < 0 ) and ( self.data_vector[i + 1] > 0 ) )\
                        and abs(self.data_vector[i] - self.data_vector[i + 1]) > threshold:
                    self.zc += 1

# ------------------------------------------------------------------------------

    # Calculate slop sign changes
    def calc_ssc(self, threshold):
        # ssc initialization
        self.ssc = 0

        for i in range (self.length):
            if ( (i - 1) >= 0 ) and ( (i + 1) < self.length):
                xa = self.data_vector[i - 1]
                xb = self.data_vector[i]
                xc = self.data_vector[i + 1]

                if ( (xb > xa) and (xb > xc) ) or\
                   ( (xb < xa) and (xb < xc) ) and\
                   ( ( abs(xb - xa) >= threshold ) and ( abs(xb - xc) >= threshold ) ):
                    self.ssc += 1

# ------------------------------------------------------------------------------

    # Calculate waveform complexity
    def calc_wl(self):
        self.wl = 0 # Waveform length initialization
        
        for i in range (self.length):
            if (i - 1) >= 0:
                xa = self.data_vector[i - 1]
                xb = self.data_vector[i]
                self.wl += abs(xb - xa)

# ------------------------------------------------------------------------------

    def get_feature_vector(self):
        return [self.mav, self.mavs, self.zc, self.ssc, self.wl]

# ------------------------------------------------------------------------------

    # Calculate all parameters
    def calc_all(self, threshold):
        self.calc_mav() # calc_mav MUST be called before calc_mavs (updating issues)
        self.calc_mavs()
        self.calc_zc(threshold)
        self.calc_ssc(threshold)
        self.calc_wl()
# ------------------------------------------------------------------------------

    def get_mav(self):
        return self.mav
        
# ------------------------------------------------------------------------------

    # Prints data vector
    def print_data_vector(self):
        print (self.data_vector)

# ------------------------------------------------------------------------------

    # Update data
    def update_data(self, data):
        self.data_vector = copy(data)

# ------------------------------------------------------------------------------

    # Update last mav
    def set_last_mav(self, last_mav):
        self.last_mav = last_mav

# ==============================================================================
    

if __name__ == "__main__":


    #Daniel-----------------------------------------
    # Module constants
    SEG_LENGTH = 40
    DATA_FILE = '../data/sample.dat'

    # Load data from file
    fid = open(DATA_FILE, 'r')
    data = fid.readlines()
    fid.close()
    filterOrder = 10
    cteCng = 0.0025
    fe = FeatureExtractor(data, SEG_LENGTH,filterOrder,cteCng)
    fv = fe.get_feature_vectors_AR()
    print ("Vetor de Caracteristicas por segmento: ", fv)
    #print "Tamanho vetor de características", len(fv[0][1])


