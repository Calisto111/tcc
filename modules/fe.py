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

RECURSAO_AR_VECT = []
BUFFER_VECT = []
FILEYHAT = ''
CONT=0
FirstOp = 0
bufferAR = []

class FeatureExtractor(object):
    # Constructor
    # data_vector: data float list
    # segment_length: segment length (samples)
    def __init__(self, data_vector, segment_length,filterOrder,cteCng):
        self.data_vector = copy(data_vector) # Data vector initialization
        self.segment_length = segment_length # Segment length (samples)
        self.filterOrder = filterOrder
        self.cteCng = cteCng

        # Parameters initialization
        self.n_segments = 0
        self.segments = []

        # Other initializations
        self.zc_threshold = 1e-6

        # Segment signal
        self.segment_signal()

# ------------------------------------------------------------------------------

    # Signal segmentation
    def segment_signal(self):
        self.n_segments = self.data_vector.__len__() / self.segment_length
        print ("\n Entrou com ", self.n_segments, "segmentos")        
        # Remove not-used samples
        extra_samples = self.data_vector.__len__() % self.segment_length

        if extra_samples:
            if extra_samples % 2: # Odd number,
                for i in range(int(extra_samples / 2 + 1)): # Remove n/2 + 1 samples from the beginning
                    self.data_vector.__delitem__(0)
                for i in range(int(extra_samples / 2)): # Remove n/2 samples from the end
                    self.data_vector.__delitem__(-1)
            else:
                for i in range(int(extra_samples / 2)):
                    self.data_vector.__delitem__(0)
                    self.data_vector.__delitem__(-1)

        # Create signal segments
        for segment in range(int(self.n_segments)):
            self.segments.append( Segment(self.data_vector[segment * 40 : (segment + 1) * 40]) )
        #print "\nSaiu"
# ------------------------------------------------------------------------------

    # Segment feature extraction
    def calc_all(self):
        for i in range(int(self.n_segments)):
            if i > 0: # If not in first segment, set last mav
                self.segments[i].set_last_mav(self.segments[i - 1].get_mav())
            self.segments[i].calc_mav() # Calc mav
            self.segments[i].calc_mavs()
            self.segments[i].calc_zc(self.zc_threshold)
            self.segments[i].calc_ssc(self.zc_threshold)
            self.segments[i].calc_wl()

# ------------------------------------------------------------------------------

    # AR Segment feature extraction
    def calc_all_Ar(self):
        for i in range(int(self.n_segments)):
            if i == 0:
                self.segments[i].calc_AR(i,self.n_segments,self.filterOrder,self.cteCng)
            else:
                self.segments[i].calc_AR(i,self.n_segments,self.filterOrder,self.cteCng)

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

    # Returns AR feature vectors
    def get_feature_vectors_AR(self):
        feature_vectors_AR = []

        # If available samples less than segment size
        if self.segments.__len__() == 0:
            return []

        for segment in self.segments:
            feature_vectors_AR.append(segment.get_feature_vector_AR())

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
        self.segment_ARs = None
        self.yhat = []
        self.AR_vect = []
        self.temp_AR = []
        self.yhatfile = ''

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


# ------------------------------------------------------------------------------

    # Calculate Regression of each 
    def calc_AR(self,rightsegment,n_segments,filterOrder,cteCng):

        self.filterOrder = filterOrder
        self.cteCng = cteCng
        self.rightsegment = rightsegment
        self.n_segments = n_segments
        global FirstOp
        global bufferAR
        global BUFFER_VECT
        global CONT
        ind = 0

        #Inicializando os coeficientes do filtro AR
        if FirstOp == 0:
            for j in range(self.filterOrder):
                self.temp_AR.append(0.0)
            self.AR_vect.append(self.temp_AR)
            self.yhatfille = ''
            self.y = ''
            self.featurefile = ''
            FirstOp = 1
            self.All_AR_vect = []
            self.All_yhat = []
            self.BufferTemp=[]
        else:             
            self.yhatfille = ''
            self.y = ''
            self.featurefile = ''
            self.All_AR_vect = []
            self.All_yhat = []

        #print "############ Segmento Atual:",self.rightsegment
        for i in range (self.length):
            somaYhat = 0.0
            #Calculando o yhat
            #Calcs for first segment doesn't need recursive
            if self.rightsegment == 0 and self.rightsegment < self.n_segments:
                #print "Valor de I antes da recursao", i
                for j in range(1,self.filterOrder+1):
                    if i == 0:
                        somaYhat+= 0.0
                    if i == 1 and j <=1 :
                        somaYhat+=self.AR_vect[i][j-1]*(float(self.data_vector[i-j])/10000)
                    if i == 2 and j <= 2:
                        somaYhat+=self.AR_vect[i][j-1]*(float(self.data_vector[i-j])/10000)
                    if i == 3 and j <= 3:
                        somaYhat+=self.AR_vect[i][j-1]*(float(self.data_vector[i-j])/10000)
                    if i == 4 and j <= 4:
                        somaYhat+=self.AR_vect[i][j-1]*(float(self.data_vector[i-j])/10000)
                    if i == 5 and j <= 5:
                        somaYhat+=self.AR_vect[i][j-1]*(float(self.data_vector[i-j])/10000)
                    if i == 6 and j <= 6:
                        somaYhat+=self.AR_vect[i][j-1]*(float(self.data_vector[i-j])/10000)
                    if i == 7 and j <= 7:
                        somaYhat+=self.AR_vect[i][j-1]*(float(self.data_vector[i-j])/10000)
                    if i == 8 and j <= 8:
                        somaYhat+=self.AR_vect[i][j-1]*(float(self.data_vector[i-j])/10000)
                    if i >= 9:
                        somaYhat+=self.AR_vect[i][j-1]*(float(self.data_vector[i-j])/10000)
                self.yhat.append(-1*somaYhat)

                self.yhatfile=self.yhatfile+str(self.yhat[i])+'\n'
                self.y = self.y + str(self.data_vector[i])+'\n'

                erro = 0.0
                #Calculando o Erro de Estimação e(n)
                erro = float(self.data_vector[i])/10000-self.yhat[i]

                #Starting temporary temp_AR
                self.temp_AR = []
                for l in range(self.filterOrder):
                    self.temp_AR.append(0.0)

                #Atualizando os coeficientes do modelo AR:
                for k in range(1,self.filterOrder+1):
                    if i == 0:
                        self.temp_AR[k-1]=self.AR_vect[i][k-1]-2*self.cteCng*erro*(float(self.data_vector[i-k])/10000)
                    if i == 1 and k <=1 :
                        self.temp_AR[k-1]=self.AR_vect[i][k-1]-2*self.cteCng*erro*(float(self.data_vector[i-k])/10000)
                    if i == 2 and k <= 2:
                        self.temp_AR[k-1]=self.AR_vect[i][k-1]-2*self.cteCng*erro*(float(self.data_vector[i-k])/10000)
                    if i == 3 and k <= 3:
                        self.temp_AR[k-1]=self.AR_vect[i][k-1]-2*self.cteCng*erro*(float(self.data_vector[i-k])/10000)
                    if i == 4 and k <= 4:
                        self.temp_AR[k-1]=self.AR_vect[i][k-1]-2*self.cteCng*erro*(float(self.data_vector[i-k])/10000)
                    if i == 5 and k <= 5:
                        self.temp_AR[k-1]=self.AR_vect[i][k-1]-2*self.cteCng*erro*(float(self.data_vector[i-k])/10000)
                    if i == 6 and k <= 6:
                        self.temp_AR[k-1]=self.AR_vect[i][k-1]-2*self.cteCng*erro*(float(self.data_vector[i-k])/10000)
                    if i == 7 and k <= 7:
                        self.temp_AR[k-1]=self.AR_vect[i][k-1]-2*self.cteCng*erro*(float(self.data_vector[i-k])/10000)
                    if i == 8 and k <= 8:
                        self.temp_AR[k-1]=self.AR_vect[i][k-1]-2*self.cteCng*erro*(float(self.data_vector[i-k])/10000)
                    if i >= 9:
                        self.temp_AR[k-1]=self.AR_vect[i][k-1]-2*self.cteCng*erro*(float(self.data_vector[i-k])/10000)
                if (self.length-1) != i:
                    self.AR_vect.append(self.temp_AR)
                else:
                    #Buffering All AR and last AR
                    self.All_AR_vect.append(self.AR_vect)
                    bufferAR=copy(self.temp_AR)
                    self.AR_vect = [] 
                    #print "Valores do Buffer AR", bufferAR, "do segmento", self.rightsegment
                    #print "Vect AR",self.AR_vect
                    BUFFER_VECT = []
                    ind = self.length -  self.filterOrder
                    for ind in range(self.length):
                        BUFFER_VECT.append(self.data_vector[ind])

                #Buffering All yhat
                self.All_yhat.append(self.yhat)
           
            #for others segments using recurssive
            else:
                #print "Valor de I na Recurssao", i
                if i == 0:
                    self.AR_vect = copy([bufferAR])
                #print "Recursive AR_vect",self.AR_vect
                #print "Tamanho Recursive AR_vect",len(self.AR_vect[0])
                self.BufferTemp = copy(BUFFER_VECT)
                for j in range(1,self.filterOrder+1):                    
                    if i - j >= 0:
                        somaYhat+=self.AR_vect[i][j-1]*(float(self.data_vector[i-j])/10000)
                    else:
                        somaYhat+=self.AR_vect[i][j-1]*(float(self.BufferTemp[i-j])/10000)
                self.yhat.append(-1*somaYhat)
                self.yhatfile=self.yhatfile+str(self.yhat[i])+'\n'
                self.y = self.y + str(self.data_vector[i])+'\n'

                erro = 0.0
                #Calculando o Erro de Estimação e(n)
                erro = float(self.data_vector[i])/10000-self.yhat[i]

                #Starting temporary temp_AR
                self.temp_AR = []
                for l in range(self.filterOrder):
                    self.temp_AR.append(0.0)

                #Atualizando os coeficientes do modelo AR:
                for k in range(1,self.filterOrder+1):
                    if i - k >= 0:
                        self.temp_AR[k-1]=self.AR_vect[i][k-1]-2*self.cteCng*erro*(float(self.data_vector[i-k])/10000)
                    else:
                        self.temp_AR[k-1]=self.AR_vect[i][k-1]-2*self.cteCng*erro*(float(self.BufferTemp[i-k])/10000)
                if (self.length-1) != i:
                    #print "Passando arqui"
                    self.AR_vect.append(self.temp_AR)
                else:
                    #Buffering all AR and last AR
                    self.All_AR_vect.append(self.AR_vect)
                    bufferAR=copy(self.temp_AR)
                    BUFFER_VECT = []
                    ind = self.length -  self.filterOrder
                    for ind in range(self.length):
                        BUFFER_VECT.append(self.data_vector[ind])
        #print "Vetor de Caracterísitcas", self.All_AR_vect[0][1]
        #print "Quantidade de pontos do vetor de características", len(self.All_AR_vect[0])


        #Exporting yhat segment
        #path = 'yhat0'+str(CONT)+'.dat'
        #fid = open(path,'w')
        #fid.writelines(self.yhatfile)
        #fid.close
        #Exporting y of segment
        #path = 'y0'+str(CONT)+'.dat'
        #fid = open(path,'w')
        #fid.writelines(self.y)
        #fid.close

        #Exporting ar coeficient of segment
        #for feature_vector in self.All_AR_vect:
            #for each_feature_vector in feature_vector:
                #for each_values in each_feature_vector:
                    #self.featurefile= self.featurefile+str(each_values)+'\t'
                #self.featurefile=self.featurefile+'\n'
        #path = 'PAT0'+str(CONT)+'.dat'
        #fid = open(path,'w')
        #fid.writelines(self.featurefile)
        #fid.close                
        
        #CONT+=1
        
        #print "Segmento Atual: ",self.n_segments,"N segmentos - 1: ",self.n_segments -1
        if self.rightsegment == (self.n_segments -1):
            FirstOp = 0

        #print "File yhat:",self.yhatfile        
        #print "Quantidade de Valores: ",len(self.data_vector)
        #print "Yhat",self.yhat

        #print "Recurssive Vector:", RECURSAO_AR_VECT
        #print "Quantidade de pontos: ", self.length
        #print "Quantidade de pontos do data vector:",len(self.data_vector)

# ------------------------------------------------------------------------------
    def get_feature_vector_AR(self):
        return self.All_AR_vect

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
    filterOrder = 4
    cteCng = 0.025
    fe = FeatureExtractor(data, SEG_LENGTH,filterOrder,cteCng)
    fe.calc_all_Ar()
    fv = fe.get_feature_vectors_AR()
    print ("Vetor de Caracteristicas por segmento: ", fv)
    #print "Tamanho vetor de características", len(fv[0][1])


