# -*- coding: iso-8859-1 -*-

set encoding iso_8859_1
set term postscript eps

# Plot original signal from Adriano

 set output 'original_signal.eps'
 set xlabel 'Quantidade de Amostras'
 set ylabel 'Amplitude do Sinal'
 set title 'Sinal original sem tkeo'
 plot 'sample.dat' with filledcurve

# ------------------------------------------------------------------------------

# Prediction Plot of Yhat from original signal Adriano

 set output 'yhat_original_signal.eps'
 set xlabel 'Quantidade de Amostras'
 set ylabel 'Amplitude do Sinal'
 set title 'Predi��o do sinal original sem tkeo'
 plot 'yhatsample.dat' with filledcurve

# ------------------------------------------------------------------------------

# Plot filtered signal from Adriano

 set output 'tkeo_signal.eps'
 set xlabel 'Quantidade de Amostras'
 set ylabel 'Amplitude do Sinal'
 set title 'Sinal original ap�s tkeo'
 plot 'file.dat' with filledcurve

# ------------------------------------------------------------------------------

# Prediction Plot of Yhat from filtered signal Adriano

 set output 'yhat_tkeo_signal.eps'
 set xlabel 'Quantidade de Amostras'
 set ylabel 'Amplitude do Sinal'
 set title 'Predi��o do sinal ap�s tkeo'
 plot 'yhatfile.dat' with filledcurve
