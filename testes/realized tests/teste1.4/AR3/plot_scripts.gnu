# -*- coding: iso-8859-1 -*-

set encoding iso_8859_1
set term postscript eps

# Performance - Alpha

 set output 'performance_alpha.eps'
 set xrange [0.01:0.91]
 set yrange [0.22:0.89]
 set xlabel 'Coeficiente de aprendizagem (alpha)'
 set ylabel 'E (%)'
 set title 'Efici�ncia da rede LVQ com AR3 - (E)'
 set style fill solid 0.05 
 plot 'results_performance_alpha.dat' using 1:3:4 w filledcu lc 3 notitle, '' using 1:2 with lines lt 1 lc 3 lw 3 notitle, '' using 1:3 w lines lt 1 lc 3 lw 1 notitle, '' using 1:4 w lines lt 1 lc 3 lw 1 notitle

# ------------------------------------------------------------------------------

# Performance - Dec. Alpha

 set output 'performance_dec_alpha.eps'
 set xrange [0.01:0.91]
 set yrange [0.23:0.72]
 set xlabel 'Taxa de decaimento de alpha'
 set ylabel 'E (%)'
 set title 'Efici�ncia da rede LVQ com AR3 - (E)'
 set style fill solid 0.05 
 plot 'results_performance_dec_alpha.dat' using 1:3:4 w filledcu lc 3 notitle, '' using 1:2 with lines lt 1 lc 3 lw 3 notitle, '' using 1:3 w lines lt 1 lc 3 lw 1 notitle, '' using 1:4 w lines lt 1 lc 3 lw 1 notitle

# ------------------------------------------------------------------------------

# Execution time - Alpha

 set output 'ex_time_alpha.eps'
 set xrange [0.01:0.91]
 set yrange [4.53:12]
 set xlabel 'Coeficiente de aprendizagem (alpha)'
 set ylabel 'Tempo de execu��o (s)'
 set title 'Treinamento da rede LVQ com AR3'
# set grid
 set xtic offset 0.5

plot 'results_time_alpha.dat' using 1:2 smooth bezier lc 3 lw 3 notitle

# ------------------------------------------------------------------------------

# Execution time - Dec. Alpha

 set output 'ex_time_dec_alpha.eps'
 set xrange [0.1:0.92]
 set yrange [2.75:56]
 set xlabel 'Decaimento de alpha'
 set ylabel 'Tempo de execu��o (s)'
 set title 'Treinamento da rede LVQ com AR3'

 plot 'results_time_dec_alpha.dat' using 1:2 with lines lc 3 lw 3 notitle

# ------------------------------------------------------------------------------

# Performance - Tolerance

 set output 'performance_tolerance.eps'
 set xrange [0.001:0.091]
 set yrange [0.4:0.69]
 set xlabel 'Toler�ncia'
 set ylabel 'E (%)'
 set title 'Efici�ncia da rede LVQ com AR3- (E)'
  set style fill solid 0.05 

# Pre-processing

# set table 'tmp.dat'
# plot 'results_performance_tolerance.dat' using 1:2 smooth bezier notitle, '' using 1:3 smooth bezier notitle, '' using 1:4 smooth bezier notitle
# unset table

plot 'results_performance_tolerance.dat' using 1:3:4 w filledcu lc 3 notitle, '' using 1:2 with lines lt 1 lc 3 lw 3 notitle, '' using 1:3 w lines lt 1 lc 3 lw 1 notitle, '' using 1:4 w lines lt 1 lc 3 lw 1 notitle


# ------------------------------------------------------------------------------

# Execution time - Tolerance

 set output 'ex_time_tolerance.eps'
 set xrange [0.001:0.091]
 set yrange [1.13:8]
 set xlabel 'Toler�ncia'
 set ylabel 'Tempo de execu��o (s)'
 set title 'Treinamento da rede LVQ com AR3'

 plot 'results_time_tolerance.dat' using 1:2 smooth bezier  lc 3 lw 3 notitle

# ------------------------------------------------------------------------------

# Performance - N. clusters

 set output 'performance_clusters.eps'
 set xrange [80:800]
 set yrange [0.43:1.01]
 set xlabel 'N�mero de unidades de classifica��o'
 set ylabel 'E (%)'
 set title 'Efici�ncia da rede LVQ com AR3 - (E)'
 set style fill solid 0.05 

 plot 'results_performance_clusters.dat' using 1:3:4 w filledcu lc 3 notitle, '' using 1:2 with lines lt 1 lc 3 lw 3 notitle, '' using 1:3 w lines lt 1 lc 3 lw 1 notitle, '' using 1:4 w lines lt 1 lc 3 lw 1 notitle

# ------------------------------------------------------------------------------

# Execution time - Training N. clusters

 set output 'time_training_clusters.eps'
 set xrange [80:800]
 set yrange [6.25:49]
 set xlabel 'N�mero de unidades de classifica��o'
 set ylabel 'Tempo de execu��o (s)'
 set title 'Treinamento da rede LVQ com AR3'
 set style fill solid 0.05 

 plot 'results_time_clusters.dat' using 1:3:4 w filledcu lc 3 notitle, '' using 1:2 with lines lt 1 lc 3 lw 3 notitle, '' using 1:3 w lines lt 1 lc 3 lw 1 notitle, '' using 1:4 w lines lt 1 lc 3 lw 1 notitle

# ------------------------------------------------------------------------------


# Execution time - Hidden units

#set output 'mlp_hidden_time.eps'
#set xrange [2:30]
#set yrange [0:700]
#set xlabel 'N�mero de neur�nios na camada escondida'
#set ylabel 'Tempo de execu��o (s)'
#set title 'Treinamento da rede'

#plot './result_n_hidden_time.dat' using 1:($2) with lines lc 3 lw 3 notitle


# ------------------------------------------------------------------------------


# Performance - Hidden units

#set output 'mlp_hidden_acc.eps'
#set xrange [2:30]
#set yrange [0.3:1]
#set xlabel 'N�mero de neur�nios na camada escondida'
#set ylabel 'E (%)'
#set title 'Efici�ncia da rede - (E)'
#set style fill solid 0.05 

#plot 'result_n_hidden_acc.dat' using 1:3:4 w filledcu lc 3 notitle, '' using 1:2 with lines lt 1 lc 3 lw 3 notitle, '' using 1:3 w lines lt 1 lc 3 lw 1 notitle, '' using 1:4 w lines lt 1 lc 3 lw 1 notitle

# ------------------------------------------------------------------------------


