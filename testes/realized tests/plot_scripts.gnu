# -*- coding: iso-8859-1 -*-

set encoding iso_8859_1
set term postscript eps

 set output 'performance_alpha.eps'

set bar 1.000000
set boxwidth 0.9 absolute
set style fill  solid 1.00 border -1
set style rectangle back fc lt -3 fillstyle  solid 1.00 border -1
set key inside right top vertical Right noreverse enhanced autotitles columnhead nobox
set style histogram clustered gap 1 title  offset character 0, 0, 0
#set datafile missing '-'
set style data histograms
set xtics border in scale 1,0.5 nomirror rotate by -45  offset character 0, 0, 0
set xtics  norangelimit
set xtics   ("80" 0.00000 -1, "160" 1.00000 -1, "240" 2.00000 -1, "320" 3.00000 -1, "400" 4.00000 -1, "480" 5.00000 -1, "560" 6.00000 -1, "640" 7.00000 -1, "720" 8.00000 -1, "800" 9.00000 -1)
set title "US immigration from Northern Europe\nPlot selected data columns as histogram of clustered boxes" 
#set rrange [ * : * ] noreverse nowriteback  # (currently [0.00000:10.0000] )
#set trange [ * : * ] noreverse nowriteback  # (currently [-5.00000:5.00000] )
#set urange [ * : * ] noreverse nowriteback  # (currently [-5.00000:5.00000] )
#set vrange [ * : * ] noreverse nowriteback  # (currently [-5.00000:5.00000] )
set ylabel  offset character 0, 0, 0 font "" textcolor lt -1 rotate by 90
set y2label  offset character 0, 0, 0 font "" textcolor lt -1 rotate by 90
set yrange [ 0.00000 : 300000. ] noreverse nowriteback
set cblabel  offset character 0, 0, 0 font "" textcolor lt -1 rotate by 90
set locale "C"
plot 'AR3results_performance_clusters.dat' using 1:xtic(1) ti col, 'AR4results_performance_clusters.dat' u 12 ti col, 'AR6results_performance_clusters.dat' u 12 ti col, 'AR8results_performance_clusters.dat' u 12 ti col,'AR10results_performance_clusters.dat' u 12 ti col
