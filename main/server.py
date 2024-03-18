#!/usr/bin/env python
# -*- coding:utf-8 -*-

# File: server.py
# Description: Server side
# Author: fmatt
# Date: 19/11/2010

# System imports
import socket
from sys import path

# Global configurations
path.append('../modules')

# User imports
from data_structures import RingBuffer
from app_threads import ProducerThread, FEThread, ClassificationThread

# ==============================================================================

if __name__ == "__main__":
    HOST = ''      # Symbolic name meaning all available interfaces
    PORT = 2727    # Arbitrary non-privileged port
    BUFFER_SIZE = 100
    netOption = input("Selecione a Rede a ser inicializada: (1) - LVQ; (2) - BpNet: ")
    netChoice = int(netOption)
    feOption = input("Selecione a Extração de Característica a ser inicializada: (1) - Herle; 2 - AR: ")
    feExtract = int(feOption)
    # Debug Option
    DBG = False
    
    # Verificar se for LVQ ou BpNet
    # Se for LVQ: Verificar inicializacao com FeExtraction Herle ou AR
    if netChoice == 1: # Verificar se é LVQ
        if feExtract == 1: # Herle Extraction
            pass
            filterOrder = 0
            cteCng = 0
            # Ativa/Desativa Debug
            if DBG:
                print("Rede selecionada LVQ")
                print("Depug Extração Caractecterística Herle")
        else: # Se for AR Extraction solicitar os demais dados
            m = input("Digite a ordem do Filtro: ")
            filterOrder = int(m)
            mu = input("Digite o valor da constante de convergência(0-1): ")
            cteCng = float(mu)

            # Ativa/Desativa Debug
            if DBG:
                print("Depug Rede selecionada LVQ")
                print("Depug Extração Caractecterística AR")
                print("Debug filterOrder:", filterOrder)
                print("Debug cteCng:", cteCng)
    # Se não for LVQ, ou seja, é BpNet: 
    # Se for BpNet: Verificar inicializacao com FeExtraction Herle ou AR
    else: # Senão é BpNet
        if feExtract == 1: # Herle Extraction
            pass
            filterOrder = 0
            cteCng = 0
            # Ativa/Desativa Debug
            if DBG:
                print("Rede selecionada BpNet")
                print("Depug Extração Caractecterística Herle")
        else: # Se for AR Extraction solicitar os demais dados
            m = input("Digite a ordem do Filtro: ")
            filterOrder = int(m)
            mu = input("Digite o valor da constante de convergência(0-1): ")
            cteCng = float(mu)

            # Ativa/Desativa Debug
            if DBG:
                print("Depug Rede selecionada BpNet")
                print("Depug Extração Caractecterística AR")
                print("Debug filterOrder:", filterOrder)
                print("Debug cteCng:", cteCng)

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT))
    s.listen(1)
    conn, addr = s.accept()

    # Create ring buffer with length 10 * window size
    data_buffer = RingBuffer(BUFFER_SIZE)
    feature_buffer = RingBuffer(BUFFER_SIZE)
    if DBG:
        print('Connected by', addr)

    at = ProducerThread(data_buffer, conn)
    pt = FEThread(data_buffer, feature_buffer, feExtract, filterOrder, cteCng)
    ct = ClassificationThread(feature_buffer, netChoice)

    at.start()
    pt.start()
    ct.start()