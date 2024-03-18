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
            if i > 0: # If not in first segment, set last mav
                self.segments[i].set_last_mav(self.segments[i - 1].get_mav())
            self.segments[i].calc_mav() # Calc mav
            self.segments[i].calc_mavs()
            self.segments[i].calc_zc(self.zc_threshold)
            self.segments[i].calc_ssc(self.zc_threshold)
            self.segments[i].calc_wl()

# ------------------------------------------------------------------------------

    # Segment AR feature extraction
    def calc_all_Ar(self):
        for i in range(self.n_segments):
            self.segments[i].calc_regression(self.filterOrder,self.cteCng)
            #print "-------Segmento: ", i

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
    
    # Returns feature vectors AR
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
        self.regression_vec = None
        self.FirstOp = 0

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

    # Calculate Regression of each 
    def calc_regression(self,filterOrder,cteCng):
        self.filterOrder = filterOrder
        self.cteCng = cteCng
        #inicialization of regression vector        
        self.regression_vec = []
        #print "Quantidade de pontos: ", self.length
        #print "Quantidade de pontos do data vector:",len(self.data_vector)
        for i in range (self.length):
            if i == 0:
                self.regression_vec.append(int(self.data_vector[i])/10000)
            if i == 1:
                self.regression_vec.append((int(self.data_vector[i]) + 0.5*self.regression_vec[i-1])/10000)
            if i == 2:
                self.regression_vec.append((int(self.data_vector[i]) + 0.5*self.regression_vec[i-1]-0.4*self.regression_vec[i-2])/10000)
            if i == 3:
                self.regression_vec.append((int(self.data_vector[i]) + 0.5*self.regression_vec[i-1]-0.4*self.regression_vec[i-2]+0.23*self.regression_vec[i-3])/10000)
            if i >= 4:
                self.regression_vec.append((int(self.data_vector[i])+ 0.5*self.regression_vec[i-1]-0.4*self.regression_vec[i-2]+0.23*self.regression_vec[i-3]-0.4*self.regression_vec[i-4])/10000)
            #print "Tamanho do vetor de regressao", len(self.regression_vec)  
            #print "Valor :(",i+1,"): ",self.regression_vec[i] 
            #print "Valor original: ",self.data_vector[i]            
       
        self.calc_AR(self.filterOrder,self.cteCng,self.regression_vec)


    # Calculate Error_Ar 
    def calc_AR(self,filterOrder,cteCng,regression_vec):
        self.regression_vec = regression_vec
        self.cteCng = cteCng
        self.filterOrder = filterOrder
        self.AR_vect = []
        e = 0
        #self.firstOp = 0 
        w = []
        a = []
        #print "Tamanho do vetor de regressao",len(self.regression_vec)
        for i in range(len(self.regression_vec)):
            temp_Ar = []
            if self.FirstOp == 0:
                #print "Entrou na inicialização: ",self.FirstOp
                for j in range(self.filterOrder+1):
                    w.append(0)
                    a.append(0)
            #print "W original",len(w)
            a[0]=1.0
            w[0]=self.regression_vec[i]
            e = self.calc_erro_Ar(a,w,self.filterOrder)
            for j in range(self.filterOrder-1):
                #print "Valor do J no cálculo do Ar: ", j+1
                a[j+1]-=2.0*self.cteCng*e*w[j+1]
                temp_Ar.append(a[j+1])
            self.AR_vect.append(temp_Ar)
            self.FirstOp = 1
            #print "Entrou na inicialização: ",self.FirstOp
            j = self.filterOrder
            #print "W antes do while",w
            while j > 0:
                w[j] = w[j-1]
                j-=1
            #print "W depois do while",w            
            #print "ValorRegressão:(",i,"):",self.regression_vec[i]
        #print "Quantidade de Coeficientes: ", len(self.AR_vect)
        #print "Vetor de AR's: ", self.AR_vect


    # Calculate Error_Ar 
    def calc_erro_Ar(self,a,w,filterOrder):
        erro = 0
        erro_list = []
        for i in range(filterOrder):
            erro+=a[i]*w[i]
        erro_list.append(erro)
        #print "Erro: ",erro
        return erro

    def get_feature_vector_AR(self):
        return self.AR_vect

# ==============================================================================
    

if __name__ == "__main__":

    #Mattioli---------------------------------------
    # Module constants
    SEG_LENGTH = 40

    # Test correct usage
    if (argv.__len__() != 3):
        print ('Config file or virtual_segment_flag missing!')
        print ('Usage: fe <config_file> virtual_segment_flag')
        exit(-1)

    # Get file name from input parameters
    filename = argv[1]

    # Virtual segment flag
    if (argv[2] == '1'):
        vs_flag = True
    else:
        vs_flag = False

    # Read config file
    fid = open(filename, 'r')
    config_lines = fid.readlines()
    fid.close()

    # Format lines
    var_dict = format_lines(config_lines)

    # Stock training file lines for further use
    training_file_lines = []
    
    # Process each data file
    for config_line in config_lines:
        filename = config_line.split()[0]
        class_id = config_line.split()[1]

        # Create data vector from file <filename>
        fid = open(filename, 'r')
        lines = fid.readlines()
        fid.close()

        # Get 2nd column from input file
        data_vector = [] # Initialize data vector
        for line in lines:
            data_vector.append( float(line.split()[1])  )
 
        fe = FeatureExtractor(data_vector, SEG_LENGTH)

        fe.calc_all()

        fv = fe.get_feature_vectors()

        # Save lines for further pattern file writing
        pattern_lines = []

        for v in fv:
            line = ''
            for i in range(v.__len__()):
                if i < (v.__len__() - 1):
                    line += str(v[i]) + '\t'
                else:
                    line += str(v[i]) + '\t' + class_id

            # Output do stdout
            if not var_dict.__contains__('OUTPUT_FILE'):
                print (line)

            pattern_lines.append(line[0:-2] + '\n')
            training_file_lines.append(line + '\n')

        # If requested in configuration file, update patterns in pattern dir
        if var_dict.__contains__('PATTERNS_DIR'):
            patterns_dir = var_dict['PATTERNS_DIR']

            # Check patterns directory format
            if not patterns_dir.endswith('/'):
                patterns_dir += '/'

            only_name = filename.split('/')[-1]
            only_name = only_name[0:-4]
            only_name += '.pat'

            # Write pattern file
            fid = open(patterns_dir + only_name, 'w')
            fid.writelines(pattern_lines)
            fid.close()
            
            # Status message
            print ('File ' + patterns_dir + only_name + ' written.')

    # If requested in config file, write training patterns file
    if var_dict.__contains__('OUTPUT_FILE'):
        output_file = var_dict['OUTPUT_FILE']

        # Write training file
        fid = open(output_file, 'w')
        fid.writelines(training_file_lines)
        fid.close()

        # Status message
        print ('File ' + output_file + ' written.')

    #Daniel-----------------------------------------
    # Module constants
#    SEG_LENGTH = 40
#    DATA_FILE = '../data/sample.dat'

    # Load data from file
#    fid = open(DATA_FILE, 'r')
#    data = fid.readlines()
#    fid.close()
#    filterOrder = 4
#    cteCng = 0.0025
#    fe = FeatureExtractor(data, SEG_LENGTH,filterOrder,cteCng)
#    fe.calc_all_Ar()

#    fv = fe.get_feature_vectors_AR()
#    print "Vetor de Caracteristicas por segmento: ", fv


