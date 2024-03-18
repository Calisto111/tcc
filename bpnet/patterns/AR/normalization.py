#!/usr/bin/env python
# -*- coding:utf-8 -*-

# File: normalization.py
# Description: Data normalization script
# Version: 0.1

INPUT_FILE = 'patternsbracoAR10isom'
OUTPUT_FILE = 'patterns_all_bracoAR10isom'

if __name__ == '__main__':
    fid = open(INPUT_FILE, 'r')
    lines = fid.readlines()
    fid.close()

    f1 = []
    f1x = []
    f2 = []
    f2x=[]
    f3 = []
    f3x=[]
    f4 = []
    f4x=[]
    f5 = []
    f5x=[]
    f6 = []
    f6x=[]
    f7 = []
    f7x=[]
    f8 = []
    f8x=[]
    f9 = []
    f9x=[]
    f10 = []
    f10x=[]
    classification = []
    segment_index = []

    for line in lines:
        parsed_line = line.split()
        f1.append(float(parsed_line[0]))
        f1x.append(abs(float(parsed_line[0])))
        f2.append(float(parsed_line[1]))
        f2x.append(abs(float(parsed_line[1])))
        f3.append(float(parsed_line[2]))
        f3x.append(abs(float(parsed_line[2])))
        f4.append(float(parsed_line[3]))
        f4x.append(abs(float(parsed_line[3])))
        f5.append(float(parsed_line[4]))
        f5x.append(abs(float(parsed_line[4])))
        f6.append(float(parsed_line[5]))
        f6x.append(abs(float(parsed_line[5])))
        f7.append(float(parsed_line[6]))
        f7x.append(abs(float(parsed_line[6])))
        f8.append(float(parsed_line[7]))
        f8x.append(abs(float(parsed_line[7])))
        f9.append(float(parsed_line[8]))
        f9x.append(abs(float(parsed_line[8])))
        f10.append(float(parsed_line[9]))
        f10x.append(abs(float(parsed_line[9])))
        classification.append(parsed_line[10])
        segment_index.append(parsed_line[11])
        
    print 'f1',f1
    max_f1 = max(f1)
    max_f1x = max(f1x)
    max_f2 = max(f2)
    max_f2x = max(f2x)
    max_f3 = max(f3)
    max_f3x = max(f3x)
    max_f4 = max(f4)
    max_f4x = max(f4x)
    max_f5 = max(f5)
    max_f5x = max(f5x)
    max_f6 = max(f6)
    max_f6x = max(f6x)
    max_f7 = max(f7)
    max_f7x = max(f7x)
    max_f8 = max(f8)
    max_f8x = max(f8x)
    max_f9 = max(f9)
    max_f9x = max(f9x)
    max_f10 = max(f10)
    max_f10x = max(f10x)

    new_lines = []

    for i in range(len(f1)):
        # 4 output neurons needed to represent the 4 hand moves
        if classification[i] == '0':
            clss = '1\t-1\t-1\t-1'
        elif classification[i] == '1':
            clss = '-1\t1\t-1\t-1'
        elif classification[i] == '2':
            clss = '-1\t-1\t1\t-1'
        else:
            clss = '-1\t-1\t-1\t1'

        new_lines.append(str(f1[i]/max_f1x) + '\t' +
                         str(f2[i]/max_f2x) + '\t' +
                         str(f3[i]/max_f3x) + '\t' +
                         str(f4[i]/max_f4x) + '\t' +
                         str(f5[i]/max_f5x) + '\t' +
                         str(f6[i]/max_f6x) + '\t' +
                         str(f7[i]/max_f7x) + '\t' +
                         str(f8[i]/max_f8x) + '\t' +
                         str(f9[i]/max_f9x) + '\t' +
                         str(f10[i]/max_f10x) + '\t' +
                         clss + '\t' +
                         segment_index[i] + '\n')

    fid = open(OUTPUT_FILE, 'a')
    fid.writelines(new_lines)
    fid.close()

# ------------------------------------------------------------------------------
    

        
