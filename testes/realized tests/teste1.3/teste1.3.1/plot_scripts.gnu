# -*- coding: iso-8859-1 -*-

set encoding iso_8859_1
set term postscript eps

# Plot filtered signal from Adriano

 set output 'window_original_tkeo_signal.eps'
 set xlabel 'Quantidade de Amostras'
 set ylabel 'Amplitude do Sinal'
 set title 'Janela do sinal original com tkeo'
 plot 'y.dat' with filledcurve

# ------------------------------------------------------------------------------

# Prediction Plot of Yhat from filtered signal Adriano

 set output 'window_yhat_tkeo_signal.eps'
 set xlabel 'Quantidade de Amostras'
 set ylabel 'Amplitude do Sinal'
 set title 'Janela da predição do sinal original com tkeo'
 plot 'yhat.dat' with filledcurve
