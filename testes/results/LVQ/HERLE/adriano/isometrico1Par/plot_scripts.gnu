# -*- coding: iso-8859-1 -*-

set encoding iso_8859_1
set term postscript eps

# Performance - Alpha

 set terminal postscript enhanced font "Helvetica" 18
 set output 'isom1par_performance_alpha.eps'
 set xrange [0.01:0.91]
 set yrange [64:81]

 set xlabel "Coeficiente de aprendizagem (alpha)" font "Helvetica,18"
 set title "Eficiência (E) da rede LVQ para diferentes \n valores de coeficiente de aprendizagem (alpha)" font "Helvetica,18"
 set ylabel "Eficiência da rede \n (%)" font "Helvetica,18"

 set style fill solid 0.05 
 plot './alpha/results_performance_alpha.dat'  using 1:($3*100):($4*100) w filledcu lc 3 notitle, '' using 1:($2*100) with lines lt 1 lc 3 lw 3 notitle, '' using 1:($3*100) w lines lt 1 lc 3 lw 1 notitle, '' using 1:($4*100) w lines lt 1 lc 3 lw 1 notitle
# ------------------------------------------------------------------------------

# Performance - Dec. Alpha
 set terminal postscript enhanced font "Helvetica" 18
 set output 'isom1par_performance_dec_alpha.eps'
 set xrange [0.01:0.91]
 set yrange [66:80]

 set xlabel "Taxa de decaimento de alpha" font "Helvetica,18"
 set title "Eficiência (E) da rede LVQ para diferentes \n valores de decaimento de alpha" font "Helvetica,18"
 set ylabel "Eficiência da rede \n (%)" font "Helvetica,18"

 set style fill solid 0.05 
 plot './dec_alpha/results_performance_dec_alpha.dat' using 1:($3*100):($4*100) w filledcu lc 3 notitle, '' using 1:($2*100) with lines lt 1 lc 3 lw 3 notitle, '' using 1:($3*100) w lines lt 1 lc 3 lw 1 notitle, '' using 1:($4*100) w lines lt 1 lc 3 lw 1 notitle

# ------------------------------------------------------------------------------

# Execution time - Alpha

 set terminal postscript enhanced font "Helvetica" 18
 set output 'isom1par_ex_time_alpha.eps'
 set xrange [0.01:0.91]
 set yrange [350:900]

 set xlabel "Coeficiente de aprendizagem (alpha)" font "Helvetica,18"
 set title "Treinamento da rede LVQ para diferentes \n valores de coeficiente de aprendizagem (alpha)" font "Helvetica,18"
 set ylabel "Tempo de execução \n (ms)" font "Helvetica,18"

# set grid
# set xtic offset 0.5

 plot './alpha/results_time_alpha.dat'  using 1:($2*1000) smooth bezier lc 3 lw 3 notitle

# ------------------------------------------------------------------------------

# Execution time - Dec. Alpha

 set terminal postscript enhanced font "Helvetica" 18
 set output 'isom1par_ex_time_dec_alpha.eps'
 set xrange [0.01:0.91]
 set yrange [180:4280]

 set xlabel "Decaimento de alpha" font "Helvetica,18"
 set title "Treinamento da rede LVQ para diferentes \n valores de decaimento de alpha" font "Helvetica,18"
 set ylabel "Tempo de execução \n (ms)" font "Helvetica,18"

 plot './dec_alpha/results_time_dec_alpha.dat' using 1:($2*1000) with lines lc 3 lw 3 notitle

# ------------------------------------------------------------------------------

# Performance - Tolerance

 set terminal postscript enhanced font "Helvetica" 18
 set output 'isom1par_performance_tolerance.eps'
 set xrange [0.001:0.091]
 set yrange [67:73]

 set xlabel "Tolerância" font "Helvetica,18"
 set title "Eficiência (E) da rede LVQ para diferentes \n valores de Tolerância" font "Helvetica,18"
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
 set output 'isom1par_ex_time_tolerance.eps'
 set xrange [0.001:0.091]
 set yrange [90:620]

 set xlabel "Tolerância" font "Helvetica,18"
 set title "Treinamento da rede LVQ para diferentes \n valores de Tolerância" font "Helvetica,18"
 set ylabel "Tempo de execução \n (ms)" font "Helvetica,18"

 plot './tolerance/results_time_tolerance.dat' using 1:($2*1000) smooth bezier  lc 3 lw 3 notitle

# ------------------------------------------------------------------------------

# Performance - N. clusters

 set terminal postscript enhanced font "Helvetica" 18
 set output 'isom1par_performance_clusters.eps'
 set xrange [25:250]
 set yrange [60:73]

 set xlabel "Número de unidades de classificação" font "Helvetica,18"
 set title "Eficiência (E) da rede LVQ para diferentes \n número de unidades de classificação" font "Helvetica,18"
 set ylabel "Eficiência da rede \n (%)" font "Helvetica,18"
 set style fill solid 0.05 

 plot './clusters/results_performance_clusters.dat' using 1:($3*100):($4*100) w filledcu lc 3 notitle, '' using 1:($2*100) with lines lt 1 lc 3 lw 3 notitle, '' using 1:($3*100) w lines lt 1 lc 3 lw 1 notitle, '' using 1:($4*100) w lines lt 1 lc 3 lw 1 notitle

# ------------------------------------------------------------------------------

# Execution time - Training N. clusters

 set terminal postscript enhanced font "Helvetica" 18
 set output 'isom1par_time_training_clusters.eps'
 set xrange [25:250]
 set yrange [200:620]

 set xlabel "Número de unidades de classificação" font "Helvetica,18"
 set title "Treinamento da rede LVQ para diferentes \n número de unidades de classificação" font "Helvetica,18"
 set ylabel "Tempo de execução \n (ms)" font "Helvetica,18"

 set style fill solid 0.05 

 plot './clusters/results_time_clusters.dat' using 1:($2*1000) smooth bezier  lc 3 lw 3 notitle

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


