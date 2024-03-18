#!/usr/bin/env python
# -*- coding:utf-8 -*-

# File: gui.py
# Description: Application Gui
# Version: 1.0

# System imports
from sys import exit, stdout, path
from os import listdir
from numpy import average, std
from time import time
from math import sqrt

import gtk
import gtk.glade

import pygtk
pygtk.require('2.0')
#import gobject

# Global configurations
path.append('../modules')

# User imports
from training import Lvq

# Constants
SUB1 = 0
SUB2 = 1
SUB3 = 2
SUB4 = 3

LVQ = 0
BPNET =  1

HERLE = 0
AR = 1

SUB1_PREFIX = 'dan'
SUB2_PREFIX = 'fer'
SUB3_PREFIX = 'wed'
SUB4_PREFIX = 'adrisom1'
SUB41_PREFIX = 'adrisot1'

SUB1_FILE = 'res/dan_training_patterns'
SUB2_FILE = 'res/fer_training_patterns'
SUB3_FILE = 'res/wed_training_patterns'
SUB4_FILE = 'res/adrisom1_training_patterns.dat'
SUB41_FILE = 'res/adrisot1_training_patterns.dat'

SUB43_FILE = 'res/adrisom1AR3_training_patterns.dat'
SUB44_FILE = 'res/adrisom1AR4_training_patterns.dat'
SUB46_FILE = 'res/adrisom1AR6_training_patterns.dat'
SUB48_FILE = 'res/adrisom1AR8_training_patterns.dat'
SUB410_FILE = 'res/adrisom1AR10_training_patterns.dat'

SUB431_FILE = 'res/adrisot1AR3_training_patterns.dat'
SUB441_FILE = 'res/adrisot1AR4_training_patterns.dat'
SUB461_FILE = 'res/adrisot1AR6_training_patterns.dat'
SUB481_FILE = 'res/adrisot1AR8_training_patterns.dat'
SUB4101_FILE = 'res/adrisot1AR10_training_patterns.dat'

SUBDAR3_FILE = 'res/danAR3_training_patterns.dat'
SUBDAR4_FILE = 'res/danAR4_training_patterns.dat'
SUBDAR6_FILE = 'res/danAR6_training_patterns.dat'
SUBDAR8_FILE = 'res/danAR8_training_patterns.dat'
SUBDAR10_FILE = 'res/danAR10_training_patterns.dat'

MOVE = ['Hand Extension', 'Hand Flexion', 'Hand grasp', 'Hand Pronation']

PATTERNS_PATH = ['../patterns','../patterns/ARs/AR3','../patterns/ARs/AR4','../patterns/ARs/AR6','../patterns/ARs/AR8','../patterns/ARs/AR10','../patterns/ARs/Adriano/Isotonico/AR3/','../patterns/ARs/Adriano/Isotonico/AR4/','../patterns/ARs/Adriano/Isotonico/AR6/','../patterns/ARs/Adriano/Isotonico/AR8/','../patterns/ARs/Adriano/Isotonico/AR10/','../patterns/ARs/Adriano/Isometrico/AR3/','../patterns/ARs/Adriano/Isometrico/AR4/','../patterns/ARs/Adriano/Isometrico/AR6/','../patterns/ARs/Adriano/Isometrico/AR8/','../patterns/ARs/Adriano/Isometrico/AR10/']
DBG = False # Debugging flag

# ==============================================================================

# Main GUI class
class Gui(object):

    # Gui constructor
    def __init__(self):
        self.builder = gtk.Builder()
        self.builder.add_from_file( 'gui.glade' )

        self.window = self.builder.get_object( 'mainWindow' )
        self.window.set_size_request(650, 550)

        # Config labels
        self.alpha = self.builder.get_object( 'txtAlpha' )
        self.lblAlpha = self.builder.get_object( 'lblAlpha' )
        self.dec_alpha = self.builder.get_object( 'txtDecAlpha' )
        self.lblDecAlpha = self.builder.get_object( 'lblDecAlpha' )
        self.tolerance = self.builder.get_object( 'txtTolerance' )
        self.lblTolerance = self.builder.get_object( 'lblTolerance' )
        self.n_clusters = self.builder.get_object( 'txtNClusters' )
        self.lblNClusters = self.builder.get_object( 'lblNClusters' )
        self.n_classes = self.builder.get_object( 'txtNClasses' )
        self.lblNClasses = self.builder.get_object( 'lblNClasses' )
        self.lbNOrdem = self.builder.get_object('lbNOrdem')
        self.txtNOrdem = self.builder.get_object('txtNOrdem')
        self.lbConvcte = self.builder.get_object('lbConvcte')
        self.txtConvcte = self.builder.get_object('txtConvcte')
        self.lblHidneu = self.builder.get_object('lblhidneu')
        self.txtHidneu = self.builder.get_object('txthidneu')
        self.label6 = self.builder.get_object('label6')
        self.label7 = self.builder.get_object('label7')
        self.label2 = self.builder.get_object('label2')
        self.label4 = self.builder.get_object('label4')
        self.label5 = self.builder.get_object('label5')
        self.label10 = self.builder.get_object('label10')

        # txtNClasses
        self.img_file = self.builder.get_object( 'imgFile' )

        # RadioButtons
        self.rbIsometric = self.builder.get_object('rbIsometric')
        self.rbIsotonic = self.builder.get_object('rbIsotonic')

        # BtnFileChooser
        self.btn_file_chooser = self.builder.get_object( 'btnFileChooser' )

        #Console
        self.console = self.builder.get_object( 'lblconsole' )
        
        # Combobox
        self.cbTrainingPatterns = self.builder.get_object('cbTrainingPatterns')
        cell = gtk.CellRendererText()
        self.cbTrainingPatterns.pack_start(cell, True)
        self.cbTrainingPatterns.add_attribute(cell, 'text', 0)

        self.cbNeuralNets = self.builder.get_object('cbNeuralNets')
        cell1 = gtk.CellRendererText()
        self.cbNeuralNets.pack_start(cell1, True)
        self.cbNeuralNets.add_attribute(cell1, 'text', 0)

        self.cbFextration = self.builder.get_object('cbFextration')
        cell2 = gtk.CellRendererText()
        self.cbFextration.pack_start(cell2, True)
        self.cbFextration.add_attribute(cell2, 'text', 0)

        self.builder.connect_signals(self)

        # Instantiate hebb algorithm
        self.lvq = None

        # Default subject initialization
        self.subject = SUB1
        self.selectedNet = LVQ
        self.feExtration = HERLE
        self.on_cbNeuralNets_changed(self, data=None)

        #Welcome
        self.print_console('>> Welcome! Please, set the parameters of the neural net.')

# ------------------------------------------------------------------------------

    # Callbacks
    # Quit application if window is closed
    def on_mainWindow_destroy(self, widget, data=None):
        stdout.write('0\n')
        stdout.flush()
        gtk.main_quit()
        exit(0)

# ------------------------------------------------------------------------------
    def print_console (self, message):
        self.console.set_text(message)

# ------------------------------------------------------------------------------

    # BntTraining callback
    def on_btnTraining_clicked(self, widget, data=None):

       # Get training patterns
        self.subject = self.cbTrainingPatterns.get_active()
        self.feExtration = self.cbFextration.get_active()
        self.selectedNet  = self.cbNeuralNets.get_active()
        nOrdem = int(self.txtNOrdem.get_text())


        #Setting way of network training and if LVQ was selected
        if self.selectedNet == LVQ:
            #Get training patterns if HERLE selected        
            if self.feExtration == HERLE:
                if self.subject == SUB1:
                    fid = open(SUB1_FILE, 'r')
                if self.subject == SUB2:
                    fid = open(SUB2_FILE, 'r')
                if self.subject == SUB3:
                    fid = open(SUB3_FILE, 'r')
                if self.subject == SUB4:
                    if self.rbIsometric.get_active()== True:
                        fid = open(SUB4_FILE, 'r')
                    else:
                        fid = open(SUB41_FILE,'r')
                    
            #Get training patterns if AR selected
            if self.feExtration == AR and nOrdem == 3:
                if self.subject == SUB1 :
                    fid = open(SUBDAR3_FILE , 'r')
                elif self.subject == SUB2:
                    print ("TODO: Gerar arquivos do SUB2")
                elif self.subject == SUB3:
                    print ("TODO: Gerar arquivos do SUB3")
                elif self.subject == SUB4:
                    if self.rbIsometric.get_active()== True:
                        fid = open(SUB43_FILE, 'r')
                    else:
                        fid = open(SUB431_FILE,'r')
            if self.feExtration == AR and nOrdem == 4:
                if self.subject == SUB1 :
                    fid = open(SUBDAR4_FILE , 'r')
                elif self.subject == SUB2:
                    print ("TODO: Gerar arquivos do SUB2")
                elif self.subject == SUB3:
                    print ("TODO: Gerar arquivos do SUB3")
                elif self.subject == SUB4:
                    if self.rbIsometric.get_active()== True:
                        fid = open(SUB44_FILE, 'r')
                    else:
                        fid = open(SUB441_FILE,'r')
            if self.feExtration == AR and nOrdem == 6:
                if self.subject == SUB1 :
                    fid = open(SUBDAR6_FILE , 'r')
                elif self.subject == SUB2:
                    print ("TODO: Gerar arquivos do SUB2")
                elif self.subject == SUB3:
                    print ("TODO: Gerar arquivos do SUB3")
                elif self.subject == SUB4:
                    if self.rbIsometric.get_active()== True:
                        fid = open(SUB46_FILE, 'r')
                    else:
                        fid = open(SUB461_FILE,'r')
            if self.feExtration == AR and nOrdem == 8:
                if self.subject == SUB1 :
                    fid = open(SUBDAR8_FILE , 'r')
                elif self.subject == SUB2:
                    print ("TODO: Gerar arquivos do SUB2")
                elif self.subject == SUB3:
                    print ("TODO: Gerar arquivos do SUB3")
                elif self.subject == SUB4:
                    if self.rbIsometric.get_active()== True:
                        fid = open(SUB48_FILE, 'r')
                    else:
                        fid = open(SUB481_FILE,'r')
            if self.feExtration == AR and nOrdem == 10:
                if self.subject == SUB1 :
                    fid = open(SUBDAR10_FILE , 'r')
                elif self.subject == SUB2:
                    print ("TODO: Gerar arquivos do SUB2")
                elif self.subject == SUB3:
                    print ("TODO: Gerar arquivos do SUB3")
                elif self.subject == SUB4:
                    if self.rbIsometric.get_active()== True:
                        fid = open(SUB410_FILE, 'r')
                    else:
                        fid = open(SUB4101_FILE,'r')

            #Reading patterns for each LVQ paramenter           
            lines = fid.readlines()
            fid.close()

            # Get Lvq parameters
            n_clusters = int(self.n_clusters.get_text())
            alpha = float(self.alpha.get_text())
            tolerance = float(self.tolerance.get_text())
            n_classes = int(self.n_classes.get_text())
            dec_alpha = float(self.dec_alpha.get_text())

            # Init training list
            training_list = []
            for line in lines:
                # Ignore comments and blanklines
                if not ( line.startswith('#') or line.isspace() ):
                    patterns = line.split()
                    #print "Padroes\n", patterns
                    training_list.append( (map(float, patterns[0:-1]), int(patterns[-1]) ) )
            #print "Lista de Padroes",training_list

            if self.feExtration == HERLE:
                print ("Feature Extration HERLE")
                self.lvq = Lvq(training_list=training_list, n_clusters=n_clusters, alpha=alpha, mult_alpha=dec_alpha, tolerance=tolerance, n_classes=n_classes)
                training_status = self.lvq.training()

                # Problem instantiating Lvq
                if training_status != self.lvq.TRAINING_OK:
                    self.print_console('>> Problem training network. Check console/terminal for more information.')
                    return
                self.print_console('>> Network was trained. Ready to run!')
                # Create configuration file for neural network
                self.create_config_file(self.lvq.get_weights())
            else:
                print ("Feature Extration AR")
                self.lvq = Lvq(training_list=training_list, n_clusters=n_clusters, alpha=alpha, mult_alpha=dec_alpha, tolerance=tolerance, n_classes=n_classes)
                training_status = self.lvq.training()

                # Problem instantiating Lvq
                if training_status != self.lvq.TRAINING_OK:
                    self.print_console('>> Problem training network. Check console/terminal for more information.')
                    return
                self.print_console('>> Network was trained. Ready to run!')
                # Create configuration file for neural network
                self.create_config_file(self.lvq.get_weights())

        #Otherwise BpNet was selected then
        else:
            #Get training patterns if HERLE selected
            #Get training patterns if AR selected    
            print ("TODO: Create read patterns files for Bpnet")
            # Get BpNet parameters
            print ("Rede para Treinamento: BpNet")

            if self.feExtration == HERLE:            
                print ("TODO: Implementar Treinamento BpNet-HERLE")
                self.print_console('>> TODO: Implementar Treinamento BpNet-HERLE')
            else:
                print ("TODO: Implementar Treinamento BpNet-AR")
                self.print_console('>> TODO: Implementar Treinamento BpNet-AR')


# ------------------------------------------------------------------------------

    # btnClear callback
    def on_btnClear_clicked(self, widget, data=None):
        
        # Clear config labels
        self.alpha.set_text('')
        self.dec_alpha.set_text('')
        self.tolerance.set_text('')
        self.n_clusters.set_text('')
        self.n_classes.set_text('')
        self.txtNOrdem.set_text('')
        self.txtConvcte.set_text('')
        self.txtHidneu.set_text('')

        self.cbTrainingPatterns.set_active(0)
        self.cbFextration.set_active(0)
        self.cbNeuralNets.set_active(0)
        self.subject = SUB1

        self.print_console('>> Data cleared. Start over!')

# ------------------------------------------------------------------------------

    # btnRun callback
    def on_btnRun_clicked(self, widget, data=None):

       # Get training patterns
        self.subject = self.cbTrainingPatterns.get_active()
        self.feExtration = self.cbFextration.get_active()
        self.selectedNet  = self.cbNeuralNets.get_active()
        nOrdem = int(self.txtNOrdem.get_text())

        #If NeuralNet selected was LVQ:
        if self.selectedNet == LVQ:
            path = self.btn_file_chooser.get_filename()
            filename = path.split('/')[-1]
            filename = filename.replace('jpg', 'pat')

            if self.feExtration == HERLE:
                filename = '../patterns/' + filename

            #Get training patterns if AR selected
            if self.feExtration == AR and nOrdem == 3:
                filename = '../patterns/ARs/AR3/' + filename

            if self.feExtration == AR and nOrdem == 4:
                filename = '../patterns/ARs/AR4/' + filename

            if self.feExtration == AR and nOrdem == 6:
                filename = '../patterns/ARs/AR6/' + filename

            if self.feExtration == AR and nOrdem == 8:
                filename = '../patterns/ARs/AR8/' + filename

            if self.feExtration == AR and nOrdem == 10:
                filename = '../patterns/ARs/AR10/' + filename

            fid = open(filename, 'r')
            lines = fid.readlines()
            fid.close()
            #print "Arquivo Lido: ", filename
             # Init training list
            test_run_list = []
            for line in lines:
                # Ignore comments and blanklines
                if not ( line.startswith('#') or line.isspace() ):
                    patterns = line.split()
                    test_run_list.append( (map(float, patterns) ) )

            # Counter for classes 0, 1, 2 and 3
            result_counter = [0, 0, 0, 0]

            if self.lvq:

                if self.subject == 0:
                    for test_run in test_run_list:
                        rec_class = self.lvq.run(test_run)
                        if DBG:
                            print ('Recognized as ' + str(rec_class))
                    result_counter[rec_class] += 1

                    # Test recognized classes
                    if result_counter.count(max(result_counter)) == 1:
                        result = result_counter.index(max(result_counter))

                        # Send result to stdout
                        stdout.write(str(result + 1) + '\n')
                        stdout.flush()

                        self.print_console('>> Recognized move as ' + MOVE[result])
                        return result
                    else:
                        self.print_console('>> Could not recognize move...')
                if self.subject == 3:
                    for test_run in test_run_list:
                        rec_class = self.lvq.run(test_run)
                        if DBG:
                            print ('Recognized as ' + str(rec_class))
                    result_counter[rec_class] += 1

                    # Test recognized classes
                    if result_counter.count(max(result_counter)) == 1:
                        result = result_counter.index(max(result_counter))

                        # Send result to stdout
                        if result == 0:
                            stdout.write(str(result + 5) + '\n')
                            stdout.flush()
                            self.print_console('>> Recognized move as Elbol Extension')
                        if result == 1:
                            stdout.write(str(result + 5) + '\n')
                            stdout.flush()
                            self.print_console('>> Recognized move as Elbol Flexion')
                        if result == 2:
                            stdout.write(str(result + 5) + '\n')
                            stdout.flush()
                            self.print_console('>> Recognized move as Forearm Supination')
                        if result == 3:
                            stdout.write(str(result + 1) + '\n')
                            stdout.flush()
                            self.print_console('>> Recognized move as Forearm Pronation')
                        return result
                    else:
                        self.print_console('>> Could not recognize move...')
                    
            else:
                self.print_console('>> Error: Network not trained!!')
        else:
            print ("TODO: Implementar Run BpNet")
            if self.feExtraction == HERLE:
                print ("TODO: Implementar Run BpNet-HERLE")
                self.print_console('>> TODO: Implementar Run BpNet-HERLE')
            if self.feExtraction == AR:
                print ("TODO: Implementar Run BpNet-AR")
                self.print_console('>> TODO: Implementar Run BpNet-AR')                

# ------------------------------------------------------------------------------

    # btnTestRun callback
    def on_btnTestRun_clicked(self, widget, data=None):
      # Statistical variables
        correct_segments = 0
        correct_windows = 0
        total_segments = 0
        total_windows = 0

        self.feExtration = self.cbFextration.get_active()
        nOrdem = int(self.txtNOrdem.get_text()) 
        self.selectedNet  = self.cbNeuralNets.get_active()

        #If LVQ Network was selected then
        if self.selectedNet == LVQ:        
            #If featureExtraction is HERLE
            if self.feExtration == HERLE:
                list_of_files = listdir(PATTERNS_PATH[0])
                PATH=PATTERNS_PATH[0]

            if self.feExtration == AR and nOrdem == 3:
                list_of_files = listdir(PATTERNS_PATH[1])
                PATH=PATTERNS_PATH[1]   
            

            #If featureExtraction is AR
            if self.feExtration == AR and nOrdem == 4:
                list_of_files = listdir(PATTERNS_PATH[2])
                PATH=PATTERNS_PATH[2]   

            if self.feExtration == AR and nOrdem == 6:
                list_of_files = listdir(PATTERNS_PATH[3])
                PATH=PATTERNS_PATH[3]   

            if self.feExtration == AR and nOrdem == 8:
                list_of_files = listdir(PATTERNS_PATH[4])
                PATH=PATTERNS_PATH[4]   

            if self.feExtration == AR and nOrdem == 10:
                list_of_files = listdir(PATTERNS_PATH[5])
                PATH=PATTERNS_PATH[5]   

            test_files = filter(self.is_test_file, list_of_files)
            test_files.sort()
        
            for filename in test_files:
                print ('\nFile: ', filename)
                print ('-------------------------')
                fid = open(PATH + '/' + filename, 'r')
                lines = fid.readlines()
                fid.close()

                if DBG:
                    # Statistical analysis
                    if filename.__contains__('extensao'):
                        correct_class = 0
                    elif filename.__contains__('flexao'):
                        correct_class = 1
                    elif filename.__contains__('grasp'):
                        correct_class = 2
                    elif filename.__contains__('torcao'):
                        correct_class = 3
                    else:
                        print ('Error detecting correct classification.')
                        exit(-1)

                # Init training list
                test_run_list = []
                for line in lines:
                    # Ignore comments and blanklines
                    if not ( line.startswith('#') or line.isspace() ):
                        patterns = line.split()
                        test_run_list.append( (map(float, patterns) ) )

                # Counter for classes 0, 1, 2 and 3
                result_counter = [0, 0, 0, 0]

                if self.lvq:
                    for test_run in test_run_list:
                        rec_class = self.lvq.run(test_run)
		
                        if DBG:
                            if rec_class == correct_class:
                                correct_segments += 1
                            total_segments += 1
                                
                            print ('Segment classification: ' + str(rec_class))
			
                        result_counter[rec_class] += 1

                    # Test recognized classes
                    if result_counter.count(max(result_counter)) == 1:
                        result = result_counter.index(max(result_counter))
                        self.print_console('>> Recognized move as ' + MOVE[result])
                        
                        if DBG:
                            if result == correct_class:
                                correct_windows +=1
                            
                            print ('-------------------------')
                            print ('Window classification: ' + str(result) + '\n')

                    else:
                        self.print_console('>> Could not recognize move...')
                    if DBG:
                        total_windows += 1
                    
                else:
                    self.print_console('>> Error: Network not trained!!')
            if DBG:
                print ('\n-----------------------------------')
                print ('Segment classification performance: ' + str(correct_segments) + '/' + str(total_segments))
                print ('Window classification performance: ' + str(correct_windows) + '/' + str(total_windows))
                print ('-----------------------------------')

            result_dict = {'correct_segments': correct_segments,
            'total_segments':total_segments, 'correct_windows':
            correct_windows, 'total_windows':total_windows}

            return result_dict
        #Otherwise BpNet
        else:
            print ("TODO: Implementar TestRun BpNet")
            self.print_console('>> Implementar TestRun BpNet')

# ------------------------------------------------------------------------------

    # btnStatTest callback
    def on_btnStatTest_clicked(self, widget, data=None):
        alpha = 0.1
        dec_alpha = 0.5
        tolerance = 0.001
        n_clusters = 100

       # Get training patterns
        self.subject = self.cbTrainingPatterns.get_active()
        self.feExtration = self.cbFextration.get_active()
        nOrdem = int(self.txtNOrdem.get_text())
        self.selectedNet  = self.cbNeuralNets.get_active()
        FILE = None

        #If LVQ Neural Net was selected then
        if self.selectedNet == LVQ:
            #Get training patterns if HERLE selected        
            if self.feExtration == HERLE:
                if self.subject == SUB1:
                    FILE = SUB1_FILE
                elif self.subject == SUB2:
                    FILE = SUB2_FILE
                elif self.subject == SUB3:
                    FILE = SUB3_FILE
                elif self.subject == SUB4:
                    if self.rbIsometric.get_active()== True:
                        FILE = SUB4_FILE
                    else:
                        FILE = SUB41_FILE

            #Get training patterns if AR selected
            if self.feExtration == AR and nOrdem == 3:
                if self.subject == SUB1 :
                    FILE = SUBDAR3_FILE
                if self.subject == SUB4:
                    if self.rbIsometric.get_active()== True:
                        FILE = SUB43_FILE
                    if self.rbIsotonic.get_active() == True:
                        FILE = SUB431_FILE

            if self.feExtration == AR and nOrdem == 4:
                if self.subject == SUB1 :
                    FILE = SUBDAR4_FILE
                if self.subject == SUB4:
                    if self.rbIsometric.get_active()== True:
                        FILE = SUB44_FILE
                    if self.rbIsotonic.get_active() == True:
                        FILE = SUB441_FILE

            if self.feExtration == AR and nOrdem == 6:
                if self.subject == SUB1 :
                    FILE = SUBDAR6_FILE
                if self.subject == SUB4:
                    if self.rbIsometric.get_active()== True:
                        FILE = SUB46_FILE
                    if self.rbIsotonic.get_active() == True:
                        FILE = SUB461_FILE

            if self.feExtration == AR and nOrdem == 8:
                if self.subject == SUB1 :
                    FILE = SUBDAR8_FILE
                if self.subject == SUB4:
                    if self.rbIsometric.get_active()== True:
                        FILE = SUB48_FILE
                    if self.rbIsotonic.get_active() == True:
                        FILE = SUB481_FILE

            if self.feExtration == AR and nOrdem == 10:
                if self.subject == SUB1 :
                    FILE = SUBDAR10_FILE
                if self.subject == SUB4:
                    if self.rbIsometric.get_active()== True:
                        FILE = SUB410_FILE
                    if self.rbIsotonic.get_active() == True:
                        FILE = SUB4101_FILE
           
            #Start training if HERLE was selected
            if self.feExtration == HERLE:
                #If want test performance and time changing cluster:  for j in range(0,401,25):
                #If want test performance and time changing alpha, dec alpha and tolerance:  for j in range(10):
                #If test alpha uncoment next line
                #alpha = 0.011  #ranging of de_alpha+= 0.1
                #If test dec_alpha uncoment next line
                #dec_alpha = 0.011  #ranging of de_alpha+= 0.1
                #If test tolerance uncoment next line
                #tolerance = 0.001 #ranging of tolerance+= 0.01
                for j in range(1,11,1):
                    #To test alpha, dec alpha and tolerance do n_clusters = best cluster setting
                    n_clusters = 40
                    #n_clusters = 150

                    results = []
                    ex_time = []
                    resultseg = []

                    # 100 test for each class
                    for i in range(100):
                        t1 = time()
                        self.parameters_test(alpha, dec_alpha, tolerance,
                    n_clusters,FILE,self.selectedNet)
                        t2 = time()
                        delta_t = t2 - t1
                        ex_time.append(delta_t)
                        result = self.on_btnTestRun_clicked(self, widget)
                        results.append(float(result['correct_windows'])/float(result['total_windows']))
                        resultseg.append(float(result['correct_segments'])/float(result['total_segments']))
                        print ("Actual Test", i)

                    # Save test results to file
                    test_id = str(tolerance)
                    if len(test_id) < 2:
                        test_id = '0' + test_id

                    mean = average(results)  # Mean
                    st_dev = std(results)       # Standard deviation
                    c1 = mean - 1.96 * st_dev / sqrt(len(results))
                    c2 = mean + 1.96 * st_dev / sqrt(len(results))
                    
                    #If you are testing clusters:fid = open('res/results_clusters_' + test_id, 'w')
                    #If you are testing alpha: fid = open('res/results_alpha_' + test_id, 'w')
                    #If you are testing dec_alpha: fid = open('res/results_dec_alpha_' + test_id, 'w')
                    #If you are testing tolerance: fid = open('res/results_tolerance_' + test_id, 'w')
                    #fid = open('res/results_clusters_' + test_id, 'w')
                    #fid = open('res/results_alpha_' + test_id, 'w')
                    fid = open('res/results_n_clusters_' + test_id, 'w')
                    fid.write('-----\n')
                    fid.write('Stats\n')
                    fid.write('-----\n')
                    fid.write('Mean = ' + str(mean) + '\n')
                    fid.write('Std = ' + str(st_dev) + '\n')
                    fid.write('----\n')
                    fid.write('Data begin\n')
                    fid.write('----\n')
                    for r in results:
                        fid.write(str(r) + '\n')
                    fid.write('--------\n')
                    fid.write('Data end\n')
                    fid.write('--------\n')
                    fid.close()

                    meanseg = average(resultseg)  # Mean
                    st_devseg = std(resultseg)       # Standard deviation
                    c1seg = meanseg - 1.96 * st_devseg / sqrt(len(resultseg))
                    c2seg = meanseg + 1.96 * st_devseg / sqrt(len(resultseg))

                    fid = open('res/results_seg_n_clusters_' + test_id, 'w')
                    fid.write('-----\n')
                    fid.write('Stats\n')
                    fid.write('-----\n')
                    fid.write('Mean = ' + str(meanseg) + '\n')
                    fid.write('Std = ' + str(st_devseg) + '\n')
                    fid.write('----\n')
                    fid.write('Data begin\n')
                    fid.write('----\n')
                    for r in resultseg:
                        fid.write(str(r) + '\n')
                    fid.write('--------\n')
                    fid.write('Data end\n')
                    fid.write('--------\n')
                    fid.close()

                    fid = open('res/results_seg_performance_n_clusters.dat', 'a')
                    fid.write(str(tolerance) + '\t' + str(meanseg) + '\t' + str(c1seg) +
                    '\t' + str(c2seg) + '\n')
                    fid.close()


                    #If you are testing clusters: fid = open('res/results_performance_clusters.dat', 'a') and fid.write(str(n_clusters)
                    #If you are testing alpha: fid = open('res/results_performance_alpha.dat', 'a') and fid.write(str(alpha)
                    #If you are testing dec_alpha: fid = open('res/results_performance_dec_alpha.dat', 'a') and fid.write(str(dec_alpha)
                    #If you are testing tolerance: fid = open('res/results_performance_tolerance.dat', 'a') and fid.write(str(tolerance)
                    #fid = open('res/results_performance_clusters.dat', 'a')
                    #fid = open('res/results_performance_alpha.dat', 'a')
                    fid = open('res/results_performance_n_clusters.dat', 'a')
                    fid.write(str(tolerance) + '\t' + str(mean) + '\t' + str(c1) +
                    '\t' + str(c2) + '\n')
                    fid.close()

                    mean_time = average(ex_time)
                    std_time = std(ex_time)
                    c1_time = mean_time - 1.96 * std_time / sqrt(len(ex_time))
                    c2_time = mean_time + 1.96 * std_time / sqrt(len(ex_time))
                    
                    #If you are testing clusters:fid = open('res/results_time_clusters.dat', 'a') and fid.write(str(n_clusters)
                    #If you are testing alpha: fid = open('res/results_time_alpha.dat', 'a') and fid.write(str(alpha)
                    #If you are testing dec_alpha: fid = open('res/results_time_dec_alpha.dat', 'a') and fid.write(str(dec_alpha)
                    #If you are testing tolerance: fid = open('res/results_time_tolerance.dat', 'a') and fid.write(str(tolerance)
                    #fid = open('res/results_time_clusters.dat', 'a')
                    #fid = open('res/results_time_alpha.dat', 'a')
                    fid = open('res/results_time_n_clusters.dat', 'a')
                    fid.write(str(tolerance) + '\t' + str(mean_time) + '\t' + str(c1_time) +
                    '\t' + str(c2_time) + '\n')
                    fid.close()
                    #alpha+=0.1
                    #dec_alpha+=0.1
                    #tolerance+= 0.01

            if self.feExtration == AR:  
                #If want test performance and time changing cluster:  for j in range(0,401,25):
                #If want test performance and time changing alpha, dec alpha and tolerance:  for j in range(10):
                #If test alpha uncoment next line
                #alpha = 0.011  #ranging of alpha+= 0.1
                #If test dec_alpha uncoment next line
                #dec_alpha = 0.011  #ranging of de_alpha+= 0.1
                #If test tolerance uncoment next line
                #tolerance = 0.001 #ranging of 

          
                for j in range(1,11,1):
                    #n_clusters = 40
                    n_clusters = 150

                    results = []
                    ex_time = []
                    resultseg = []

                    # Perform 100 performance tests
                    for i in range(25):
                        t1 = time()
                        self.parameters_test(alpha, dec_alpha, tolerance,
                    n_clusters,FILE,self.selectedNet)
                        t2 = time()
                        delta_t = t2 - t1
                        ex_time.append(delta_t)
                        result = self.on_btnTestRun_clicked(self, widget)
                        results.append(float(result['correct_windows'])/float(result['total_windows']))
                        resultseg.append(float(result['correct_segments'])/float(result['total_segments']))
                        print ("Actual Test", i)

                    # Save test results to file
                    test_id = str(tolerance)
                    if len(test_id) < 2:
                        test_id = '0' + test_id

                    mean = average(results)  # Mean
                    st_dev = std(results)       # Standard deviation
                    c1 = mean - 1.96 * st_dev / sqrt(len(results))
                    c2 = mean + 1.96 * st_dev / sqrt(len(results))


                    #If you are testing clusters:fid = open('res/results_clusters_' + test_id, 'w')
                    #If you are testing alpha: fid = open('res/results_alpha_' + test_id, 'w')
                    #If you are testing dec_alpha: fid = open('res/results_dec_alpha_' + test_id, 'w')
                    #If you are testing tolerance: fid = open('res/results_tolerance_' + test_id, 'w')
                    #fid = open('res/results_clusters_' + test_id, 'w')
                    #fid = open('res/results_alpha_' + test_id, 'w')
                    #fid = open('res/results_clusters_' + test_id, 'w')
                    fid = open('res/results_n_clusters_' + test_id, 'w')
                    fid.write('-----\n')
                    fid.write('Stats\n')
                    fid.write('-----\n')
                    fid.write('Mean = ' + str(mean) + '\n')
                    fid.write('Std = ' + str(st_dev) + '\n')
                    fid.write('----\n')
                    fid.write('Data begin\n')
                    fid.write('----\n')
                    for r in results:
                        fid.write(str(r) + '\n')
                    fid.write('--------\n')
                    fid.write('Data end\n')
                    fid.write('--------\n')
                    fid.close()


                    #If you are testing clusters: fid = open('res/results_performance_clusters.dat', 'a') and fid.write(str(n_clusters)
                    #If you are testing alpha: fid = open('res/results_performance_alpha.dat', 'a') and fid.write(str(alpha)
                    #If you are testing dec_alpha: fid = open('res/results_performance_dec_alpha.dat', 'a') and fid.write(str(dec_alpha)
                    #If you are testing tolerance: fid = open('res/results_performance_tolerance.dat', 'a') and fid.write(str(tolerance)
                    #fid = open('res/results_performance_clusters.dat', 'a')
                    #fid = open('res/results_performance_alpha.dat', 'a')
                    #fid = open('res/results_performance_clusters.dat', 'a')
                    fid = open('res/results_performance_n_clusters.dat', 'a')
                    fid.write(str(tolerance) + '\t' + str(mean) + '\t' + str(c1) +
                    '\t' + str(c2) + '\n')
                    fid.close()

                    #meanseg = average(resultseg)  # Mean
                    #st_devseg = std(resultseg)       # Standard deviation
                    #c1 = meanseg - 1.96 * st_devseg / sqrt(len(resultseg))
                    #c2 = meanseg + 1.96 * st_devseg / sqrt(len(resultseg))

                    #fid = open('res/results_seg_clusters_' + test_id, 'w')
                    #fid.write('-----\n')
                    #fid.write('Stats\n')
                    #fid.write('-----\n')
                    #fid.write('Mean = ' + str(meanseg) + '\n')
                    #fid.write('Std = ' + str(st_devseg) + '\n')
                    #fid.write('----\n')
                    #fid.write('Data begin\n')
                    #fid.write('----\n')
                    #for r in resultseg:
                        #fid.write(str(r) + '\n')
                    #fid.write('--------\n')
                    #fid.write('Data end\n')
                    #fid.write('--------\n')
                    #fid.close()

                    #fid = open('res/results_seg_performance_clusters.dat', 'a')
                    #fid.write(str(n_clusters) + '\t' + str(meanseg) + '\t' + str(c1) +
                    #'\t' + str(c2) + '\n')
                    #fid.close()

                    mean_time = average(ex_time)
                    std_time = std(ex_time)
                    c1_time = mean_time - 1.96 * std_time / sqrt(len(ex_time))
                    c2_time = mean_time + 1.96 * std_time / sqrt(len(ex_time))

                    fid = open('res/results_time_n_clusters.dat', 'a')
                    fid.write(str(tolerance) + '\t' + str(mean_time) + '\t' + str(c1_time) +
                    '\t' + str(c2_time) + '\n')
                    fid.close()
                    #alpha+= 0.1
                    #dec_alpha+= 0.1
                    #tolerance+= 0.01

        #Otherwise Bpnet was selected
        else:
            print ("TODO: Implementar Statistical Test for Bpnet")
            self.print_console('>> Implementar Statistical Test for Bpnet')
# ------------------------------------------------------------------------------

#     # btnStatTest callback
#     def on_btnStatTest_clicked(self, widget, data=None):
        
#         results = []

#         # Perform 100 performance tests
#         for i in range(100):
#             self.on_btnTraining_clicked(self, widget)
#             result = self.on_btnTestRun_clicked(self, widget)
#             results.append(float(result['correct_windows'])/float(result['total_windows']))

#         # Save test results to file
#         fid = open('res/results.txt', 'w')
#         fid.write('-----\n')
#         fid.write('Stats\n')
#         fid.write('-----\n')
#         fid.write('Average = ' + str(average(results)) + '\n')
#         fid.write('Std = ' + str(std(results)) + '\n')
#         fid.write('----\n')
#         fid.write('Data\n')
#         fid.write('----\n')
#         for r in results:
#             fid.write(str(r) + '\n')
#         fid.write('--------\n')
#         fid.write('Data end\n')
#         fid.write('--------\n')
#         fid.close()

# ------------------------------------------------------------------------------

    # BntTraining callback
    def parameters_test(self, alpha, dec_alpha, tolerance, n_clusters,FILE,selectedNet):

        # Local variables initialization
        n_classes = 4
            
        fid = open(FILE, 'r')            
        lines = fid.readlines()
        fid.close()
        
        #If NeuralNet selected was LVQ then
        if selectedNet == LVQ:
            # Init training list
            training_list = []
            for line in lines:
                # Ignore comments and blanklines
                if not ( line.startswith('#') or line.isspace() ):
                    patterns = line.split()
                    training_list.append( (map(float, patterns[0:-1]), int(patterns[-1]) ) )

            self.lvq = Lvq(training_list=training_list, n_clusters=n_clusters, alpha=alpha, mult_alpha=dec_alpha, tolerance=tolerance, n_classes=n_classes)
            training_status = self.lvq.training()

            # Problem instantiating Lvq
            if training_status != self.lvq.TRAINING_OK:
                self.print_console('>> Problem training network. Check console/terminal for more information.')
                return

            # Create configuration file for neural network
            self.create_config_file(self.lvq.get_weights())

            self.print_console('>> Network was trained. Ready to run!')
        else:
            print ("TODO: Implementar parameters_test para Bpnet")
            self.print_console('>> Implementar parameters_test para Bpnet')

# ------------------------------------------------------------------------------

    # Test if file must be included in test files list
    def is_test_file(self, file):
        if self.subject == SUB1:
            prefix = SUB1_PREFIX
        elif self.subject == SUB2:
            prefix = SUB2_PREFIX
        elif self.subject == SUB3:
            prefix = SUB3_PREFIX
        elif self.subject == SUB4:
            if self.rbIsometric.get_active()== True:
                prefix = SUB4_PREFIX
            else:
                prefix = SUB41_PREFIX
        else:
            print ('Wrong subject id. Execution aborted.')
            exit(-1)

        # Check correct prefix
        if file.startswith(prefix) and file.endswith('.pat'):
            return True
        else:
            return False

# ------------------------------------------------------------------------------

    def on_cbTrainingPatterns_changed(self, widget, data=None):
        self.subject =  self.cbTrainingPatterns.get_active()
        if self.subject == 3:
            self.rbIsometric.set_visible(True)
            self.rbIsotonic.set_visible(True)
        else:
            self.rbIsometric.set_visible(False)
            self.rbIsotonic.set_visible(False)

# ------------------------------------------------------------------------------

    def on_cbNeuralNets_changed(self, widget, data=None):
        self.selectedNet =  self.cbNeuralNets.get_active()
        if self.selectedNet == 0:
            self.lblAlpha.set_visible(True)
            self.alpha.set_visible(True)
            self.lblDecAlpha.set_visible(True)
            self.dec_alpha.set_visible(True)
            self.lblTolerance.set_visible(True)
            self.tolerance.set_visible(True)
            self.lblNClusters.set_visible(True)
            self.n_clusters.set_visible(True)
            self.lblNClasses.set_visible(True)
            self.n_classes.set_visible(True)
            self.lblHidneu.set_visible(False)
            self.txtHidneu.set_visible(False)
            self.label6.set_visible(True)
            self.label7.set_visible(True)
            self.label2.set_visible(True)
            self.label4.set_visible(True)
            self.label5.set_visible(False)
            self.label10.set_visible(False)
        else:
            self.lblAlpha.set_visible(True)
            self.alpha.set_visible(True)
            self.lblDecAlpha.set_visible(False)
            self.dec_alpha.set_visible(False)
            self.lblTolerance.set_visible(True)
            self.tolerance.set_visible(True)
            self.tolerance.set_text('150')
            self.lblNClusters.set_visible(False)
            self.n_clusters.set_visible(False)
            self.lblNClasses.set_visible(False)
            self.n_classes.set_visible(False)
            self.lblHidneu.set_visible(True)
            self.txtHidneu.set_visible(True)
            self.label6.set_visible(False)
            self.label7.set_visible(False)
            self.label2.set_visible(False)
            self.label4.set_visible(False)
            self.label5.set_visible(True)
            self.label10.set_visible(True)
        #print "Rede Selecionada", self.selectedNet

# ------------------------------------------------------------------------------

    def on_cbFextration_changed(self, widget, data=None):
        self.feExtration =  self.cbFextration.get_active()
        if self.feExtration == 1:
            self.lbNOrdem.set_visible(True)
            self.txtNOrdem.set_visible(True)
            self.lbConvcte.set_visible(True)
            self.txtConvcte.set_visible(True)
        else:
            self.lbNOrdem.set_visible(False)
            self.txtNOrdem.set_visible(False)
            self.lbConvcte.set_visible(False)
            self.txtConvcte.set_visible(False)          
        #print "Extração de Caracteristica", self.feExtration

# ------------------------------------------------------------------------------

    def print_weights(self):
        h = 0
        f = 0
        for i in range(self.weights.__len__()):
            for j in range(self.weights[0].__len__()): 
                self.weights_matrix[h].set_text(str(self.weights[i][j]))
                h = h + 10
            f += 1
            h = f
            
# ------------------------------------------------------------------------------

    def on_btnFileChooser_file_set(self, widget, data=None):
        self.img_file.set_from_file(widget.get_filename())
        
# ------------------------------------------------------------------------------

    # Write configuration file with current configuration
    def create_config_file(self, weights):
        # weights = [[x1,y1,z1], [x2,y2,z2], ..., [xn,yn,zn]] 
        lines = [] # File lines
        for wv in weights: # For each weight vector
            line = ''
            for i in range(wv.__len__() - 1):
                line += str(wv[i]) + '\t'
            line += str(wv[i + 1]) + '\n' # Append last weight, without '\t'    
            lines.append(line)

        fid = open('../res/cfg_network', 'w')
        fid.writelines(lines)
        fid.close()
        
# ==============================================================================

if __name__ == "__main__":
    my_gui = Gui()
    my_gui.window.show()
    gtk.main()
    

# ==============================================================================
