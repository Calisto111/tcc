# -*- coding: iso-8859-1 -*-

set encoding iso_8859_1
set term postscript eps

# Performance - Alpha

 set terminal postscript enhanced font "Helvetica" 18
 set output 'performance_alpha.eps'
 set xrange [0.1:0.2]
 set yrange [0:100]

 set xlabel "Coeficiente de aprendizagem (alpha)" font "Helvetica,18"
 set title "Eficiência (E) da rede MLP para diferentes \n valores de Coeficiente de aprendizagem (alpha)" font "Helvetica,18"
 set ylabel "Eficiência da rede \n (%)" font "Helvetica,18"
set style fill solid 0.05 

 set style fill solid 0.05 
 plot './alpha/results_performance_alpha.dat'  using 1:($3*100):($4*100) w filledcu lc 3 notitle, '' using 1:($2*100) with lines lt 1 lc 3 lw 3 notitle, '' using 1:($3*100) w lines lt 1 lc 3 lw 1 notitle, '' using 1:($4*100) w lines lt 1 lc 3 lw 1 notitle
# ------------------------------------------------------------------------------

# Performance - Dec. Alpha
 set terminal postscript enhanced font "Helvetica" 18
# set output 'performance_dec_alpha.eps'
 set xrange [0.01:0.91]
 set yrange [80:90]

 set xlabel "Taxa de decaimento de alpha" font "Helvetica,18"
 set title "Eficiência (E) da rede MLP para diferentes \n valores de decaimento de alpha" font "Helvetica,18"
 set ylabel "Eficiência da rede \n (%)" font "Helvetica,18"

 set style fill solid 0.05 
 #plot './dec_alpha/results_performance_dec_alpha.dat' using 1:($3*100):($4*100) w filledcu lc 3 notitle, '' using 1:($2*100) with lines lt 1 lc 3 lw 3 notitle, '' using 1:($3*100) w lines lt 1 lc 3 lw 1 notitle, '' using 1:($4*100) w lines lt 1 lc 3 lw 1 notitle

# ------------------------------------------------------------------------------

# Execution time - Alpha

 set terminal postscript enhanced font "Helvetica" 18
 set output 'ex_time_alpha.eps'
 set xrange [0.1:0.2]
 set yrange [40:150]

set xlabel "Coeficiente de aprendizagem (alpha)" font "Helvetica,18"
set title "Treinamento da rede MLP para diferentes \n valores de Coeficiente de aprendizagem (alpha)" font "Helvetica,18"
set ylabel "Tempo de execução \n (s)" font "Helvetica,18"

# set grid
# set xtic offset 0.5

 plot './alpha/results_time_alpha.dat'  using 1:3:4 w filledcu lc 3 notitle, '' using 1:2 with lines lt 1 lc 3 lw 3 notitle, '' using 1:3 w lines lt 1 lc 3 lw 1 notitle, '' using 1:4 w lines lt 1 lc 3 lw 1 notitle

# ------------------------------------------------------------------------------

# Execution time - Dec. Alpha

 set terminal postscript enhanced font "Helvetica" 18
# set output 'ex_time_dec_alpha.eps'
 set xrange [0.01:0.91]
 set yrange [8:293]

 set xlabel "Decaimento de alpha" font "Helvetica,18"
 set title "Treinamento da rede MLP para diferentes \n valores de decaimento de alpha" font "Helvetica,18"
 set ylabel "Tempo de execução \n (ms)" font "Helvetica,18"

 #plot './dec_alpha/results_time_dec_alpha.dat' using 1:($2*1000) with lines lc 3 lw 3 notitle

# ------------------------------------------------------------------------------

# Performance - Tolerance

 set terminal postscript enhanced font "Helvetica" 18
 set output 'performance_tolerance.eps'
 set xrange [100:300]
 set yrange [0:75]

 set xlabel "Tolerância" font "Helvetica,18"
 set title "Eficiência (E) da rede MLP para diferentes \n valores de Tolerância" font "Helvetica,18"
 set ylabel "Eficiência da rede \n (%)" font "Helvetica,18"

 set style fill solid 0.05 

# Pre-processing

# set table 'tmp.dat'
# plot 'results_performance_tolerance.dat' using 1:2 smooth bezier notitle, '' using 1:3 smooth bezier notitle, '' using 1:4 smooth bezier notitle
# unset table

 plot './tolerance/results_performance_tolerance.dat' using 1:($3*100):($4*100) w filledcu lc 3 notitle, '' using 1:($2*100) with lines lt 1 lc 3 lw 3 notitle, '' using 1:($3*100) w lines lt 1 lc 3 lw 1 notitle, '' using 1:($4*100) w lines lt 1 lc 3 lw 1 notitle


# ------------------------------------------------------------------------------

# Execution time - Tolerance

 set terminal postscript enhanced font "Helvetica" 18
 set output 'ex_time_tolerance.eps'
 set xrange [100:300]
 set yrange [0:130]

 set xlabel "Tolerância" font "Helvetica,18"
 set title "Treinamento da rede MLP para diferentes \n valores de Tolerância" font "Helvetica,18"
 set ylabel "Tempo de execução \n (s)" font "Helvetica,18"

 plot './tolerance/results_time_tolerance.dat' using 1:2 smooth bezier  lc 3 lw 3 notitle

# ------------------------------------------------------------------------------

# Performance - N. clusters

 set terminal postscript enhanced font "Helvetica" 18
# set output 'performance_clusters.eps'
 set xrange [7:70]
 set yrange [35:100]

 set xlabel "Número de unidades de classificação" font "Helvetica,18"
 set title "Eficiência (E) da rede MLP para diferentes \n números de unidades de classificação" font "Helvetica,18"
 set ylabel "Eficiência da rede \n (%)" font "Helvetica,18"
 set style fill solid 0.05 

# plot './clusters/results_performance_clusters.dat' using 1:($3*100):($4*100) w filledcu lc 3 notitle, '' using 1:($2*100) with lines lt 1 lc 3 lw 3 notitle, '' using 1:($3*100) w lines lt 1 lc 3 lw 1 notitle, '' using 1:($4*100) w lines lt 1 lc 3 lw 1 notitle

# ------------------------------------------------------------------------------

# Execution time - Training N. clusters

 set terminal postscript enhanced font "Helvetica" 18
# set output 'time_training_clusters.eps'
 set xrange [7:70]
 set yrange [9:63]

 set xlabel "Número de unidades de classificação" font "Helvetica,18"
 set title "Treinamento da rede MLP para diferentes \n números de unidades de classificação" font "Helvetica,18"
 set ylabel "Tempo de execução \n (ms)" font "Helvetica,18"

 set style fill solid 0.05 

# plot './clusters/results_time_clusters.dat' using 1:($2*1000) smooth bezier  lc 3 lw 3 notitle

# ------------------------------------------------------------------------------


# Execution time - Hidden units

set output 'mlp_hidden_time.eps'
set xrange [4:30]
set yrange [0:500]
set xlabel "Número de neurônios na camada escondida" font "Helvetica,18"
set title "Treinamento da rede MLP para diferentes \n números de neurônios na camada escondida" font "Helvetica,18"
set ylabel "Tempo de execução \n (s)" font "Helvetica,18"

plot './hidden_layers/results_time_n_clusters.dat' using 1:($2) with lines lc 3 lw 3 notitle


# ------------------------------------------------------------------------------


# Performance - Hidden units

set output 'mlp_hidden_acc.eps'
set xrange [4:30]
set yrange [0:100]
 set xlabel "Número de unidades de classificação" font "Helvetica,18"
 set title "Eficiência (E) da rede MLP para diferentes \n números de unidades de classificação" font "Helvetica,18"
 set ylabel "Eficiência da rede \n (%)" font "Helvetica,18"
set style fill solid 0.05 

plot './hidden_layers/results_performance_n_clusters.dat' using 1:($3*100):($4*100) w filledcu lc 3 notitle, '' using 1:($2*100) with lines lt 1 lc 3 lw 3 notitle, '' using 1:($3*100) w lines lt 1 lc 3 lw 1 notitle, '' using 1:($4*100) w lines lt 1 lc 3 lw 1 notitle

# ------------------------------------------------------------------------------


