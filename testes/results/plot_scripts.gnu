# -*- coding: iso-8859-1 -*-

set encoding iso_8859_1
set term postscript eps

# Performance - Alpha

 set output 'performance_alpha.eps'
 set xrange [0.01:0.99]
 set yrange [0.8:1]
 set xlabel 'Coeficiente de aprendizagem (alpha)'
 set ylabel 'E (%)'
 set title 'Eficiência da rede - (E)'
 set style fill solid 0.05 
 plot 'results_performance_alpha.dat' using 1:3:4 w filledcu lc 3 notitle, '' using 1:2 with lines lt 1 lc 3 lw 3 notitle, '' using 1:3 w lines lt 1 lc 3 lw 1 notitle, '' using 1:4 w lines lt 1 lc 3 lw 1 notitle

# ------------------------------------------------------------------------------

# Performance - Dec. Alpha

# set output 'performance_dec_alpha.eps'
# set xrange [0.01:0.99]
# set yrange [0.7:0.9]
# set xlabel 'Taxa de decaimento de alpha'
# set ylabel 'E (%)'
# set title 'Eficiência da rede - (E)'
# set style fill solid 0.05 
# plot 'results_performance_dec_alpha.dat' using 1:3:4 w filledcu lc 3 notitle, '' using 1:2 with lines lt 1 lc 3 lw 3 notitle, '' using 1:3 w lines lt 1 lc 3 lw 1 notitle, '' using 1:4 w lines lt 1 lc 3 lw 1 notitle

# ------------------------------------------------------------------------------

# Execution time - Alpha

 set output 'ex_time_alpha.eps'
 set xrange [0.01:0.99]
 set yrange [30:80]
 set xlabel 'Coeficiente de aprendizagem (alpha)'
 set ylabel 'Tempo de execução (ms)'
 set title 'Treinamento da rede'
# set grid
 set xtic offset 0.5

plot 'results_time_alpha.dat' using 1:($2*1000) smooth bezier lc 3 lw 3 notitle

# ------------------------------------------------------------------------------

# Execution time - Dec. Alpha

# set output 'ex_time_dec_alpha.eps'
# set xrange [0.01:0.99]
# set yrange [0:2.5]
# set xlabel 'Decaimento de alpha'
# set ylabel 'Tempo de execução (s)'
# set title 'Treinamento da rede'

# plot './results_time_dec_alpha.dat' using 1:2 with lines lc 3 lw 3 notitle

# ------------------------------------------------------------------------------

# Performance - Tolerance

 set output 'performance_tolerance.eps'
 set xrange [0.001:0.099]
 set yrange [0.9:1]
 set xlabel 'Tolerância'
 set ylabel 'E (%)'
 set title 'Eficiência da rede - (E)'
 set style fill solid 0.05 

# Pre-processing

# set table 'tmp.dat'
# plot 'results_performance_tolerance.dat' using 1:2 smooth bezier notitle, '' using 1:3 smooth bezier notitle, '' using 1:4 smooth bezier notitle
# unset table

plot 'results_performance_tolerance.dat' using 1:3:4 w filledcu lc 3 notitle, '' using 1:2 with lines lt 1 lc 3 lw 3 notitle, '' using 1:3 w lines lt 1 lc 3 lw 1 notitle, '' using 1:4 w lines lt 1 lc 3 lw 1 notitle


# ------------------------------------------------------------------------------

# Execution time - Tolerance

 set output 'ex_time_tolerance.eps'
 set xrange [0.001:0.099]
 set yrange [0:60]
 set xlabel 'Tolerância'
 set ylabel 'Tempo de execução (ms)'
 set title 'Treinamento da rede'

 plot 'results_time_tolerance.dat' using 1:($2*1000) smooth bezier  lc 3 lw 3 notitle

# ------------------------------------------------------------------------------

# Performance - N. clusters

# set output 'performance_clusters.eps'
# set xrange [4:60]
# set yrange [0.3:1]
# set xlabel 'Número de unidades de classificação'
# set ylabel 'E (%)'
# set title 'Eficiência da rede - (E)'
# set style fill solid 0.05 

# plot 'results_performance_clusters.dat' using 1:3:4 w filledcu lc 3 notitle, '' using 1:2 with lines lt 1 lc 3 lw 3 notitle, '' using 1:3 w lines lt 1 lc 3 lw 1 notitle, '' using 1:4 w lines lt 1 lc 3 lw 1 notitle

# ------------------------------------------------------------------------------
# Execution time - Training N. clusters

 set output 'time_training_clusters.eps'
 set xrange [200:1600]
 set yrange [0.3:100]
 set xlabel 'Número de unidades de classificação'
 set ylabel 'Tempo de execução (s)'
 set title 'Treinamento da rede'
 set style fill solid 0.05 

 plot 'results_time_clusters.dat' using 1:3:4 w filledcu lc 3 notitle, '' using 1:2 with lines lt 1 lc 3 lw 3 notitle, '' using 1:3 w lines lt 1 lc 3 lw 1 notitle, '' using 1:4 w lines lt 1 lc 3 lw 1 notitle

# ------------------------------------------------------------------------------

# Execution time - Hidden units

#set output 'mlp_hidden_time.eps'
#set xrange [2:30]
#set yrange [0:700]
#set xlabel 'Número de neurônios na camada escondida'
#set ylabel 'Tempo de execução (s)'
#set title 'Treinamento da rede'

#plot './result_n_hidden_time.dat' using 1:($2) with lines lc 3 lw 3 notitle


# ------------------------------------------------------------------------------


# Performance - Hidden units

#set output 'mlp_hidden_acc.eps'
#set xrange [2:30]
#set yrange [0.3:1]
#set xlabel 'Número de neurônios na camada escondida'
#set ylabel 'E (%)'
#set title 'Eficiência da rede - (E)'
#set style fill solid 0.05 

#plot 'result_n_hidden_acc.dat' using 1:3:4 w filledcu lc 3 notitle, '' using 1:2 with lines lt 1 lc 3 lw 3 notitle, '' using 1:3 w lines lt 1 lc 3 lw 1 notitle, '' using 1:4 w lines lt 1 lc 3 lw 1 notitle

# ------------------------------------------------------------------------------


