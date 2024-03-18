# -*- coding: iso-8859-1 -*-

set encoding iso_8859_1
set term postscript eps

#Time line comparative traning time process
 set output 'tl_comp_traintime_AR.eps'
 set xrange [120:1200]
 set yrange [47:982]
 set xlabel 'Numero de clusters'
 set ylabel 'Tempo de execucao (s)'
 set title 'Treinamento da rede LVQ'
# set style fill solid 0.05 

set key inside left top vertical Right noreverse enhanced autotitles 

 plot './cluster/AR3results_time_clusters.dat' u 1:2 w lines lc 1 title "AR3", './cluster/AR4results_time_clusters.dat' u 1:2 w lines lc 2 title "AR4", './cluster/AR6results_time_clusters.dat' u 1:2 w lines lc 3 title "AR6", './cluster/AR8results_time_clusters.dat' u 1:2 w lines lc 4 title "AR8", './cluster/AR10results_time_clusters.dat' u 1:2 w lines lc 5 title "AR10"

#--------------------------------------------------------------------------------------------------------------------------------
#Time line comparative training time alpha
 set output 'tl_comptime_alpha_AR.eps'
 set xrange [0.01:0.911]
 set yrange [21:130]
 set xlabel 'Alpha'
 set ylabel "Tempo (s)"
 set title 'Treinamento da rede LVQ'
# set style fill solid 0.05 

 plot './alpha/AR3results_time_alpha.dat' u 1:2 w lines lc 1 title "AR3", './alpha/AR4results_time_alpha.dat' u 1:2 w lines lc 2 title "AR4", './alpha/AR6results_time_alpha.dat' u 1:2 w lines lc 3 title "AR6", './alpha/AR8results_time_alpha.dat' u 1:2 w lines lc 4 title "AR8", './alpha/AR10results_time_alpha.dat' u 1:2 w lines lc 5 title "AR10"

#--------------------------------------------------------------------------------------------------------------------------------

#Traning Time Process Cluster/AR
 set output 'tl_comptime_dec_alpha_AR.eps'
 set xrange [0.01:0.911]
 set yrange [5:1908]
 set xlabel 'Decaimento de alpha'
 set ylabel "Tempo (s)"
 set title 'Treinamento da rede LVQ'
# set style fill solid 0.05 

 plot './dec_alpha/AR3results_time_dec_alpha.dat' u 1:2 w lines lc 1 title "AR3", './dec_alpha/AR4results_time_dec_alpha.dat' u 1:2 w lines lc 2 title "AR4", './dec_alpha/AR6results_time_dec_alpha.dat' u 1:2 w lines lc 3 title "AR6", './dec_alpha/AR8results_time_dec_alpha.dat' u 1:2 w lines lc 4 title "AR8", './dec_alpha/AR10results_time_dec_alpha.dat' u 1:2 w lines lc 5 title "AR10"


#--------------------------------------------------------------------------------------------------------------------------------
