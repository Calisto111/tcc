# -*- coding: iso-8859-1 -*-

set encoding iso_8859_1
set term postscript eps

# Plot original signal from Adriano

 set output 'original_signal.eps'
 set xlabel 'Quantidade de Amostras'
 set ylabel 'Amplitude do Sinal'
 set title 'Exemplo de sinal antes da Normalização'
 plot 'sample.dat' with filledcurve

# ------------------------------------------------------------------------------

# Plot filtered signal from Adriano Tkeo

 set output 'normalized_signal.eps'
 set xlabel 'Quantidade de Amostras'
 set ylabel 'Amplitude do Sinal'
 set title 'Exemplo de sinal após filtro tkeo'
 plot 'file.dat' with filledcurve

