# -*- coding: iso-8859-1 -*-

set encoding iso_8859_1
set term postscript eps

#--------------------------------------------------------------------------------------------------------------------------------
#Perfomance Clusters/AR Graphic 1

#set output 'com_perf_clusterAR1.eps'

set border 3 front linetype -1 linewidth 1.000
#set boxwidth 0.8 absolute
set style fill   solid 1.00 noborder
set grid nopolar
set grid noxtics nomxtics ytics nomytics noztics nomztics \
 nox2tics nomx2tics noy2tics nomy2tics nocbtics nomcbtics
set key bmargin center horizontal Left reverse enhanced autotitles columnhead nobox

set style histogram clustered gap 1 title  offset character 0, 0, 0
set style data histograms

set xtics border in scale 1,0.5 nomirror rotate by -45  offset character 0, 0, 0 
set xtics   ("80" 0.00000, "160" 1.00000, "240" 2.00000, "320" 3.00000, "400" 4.00000,"480" 5.0000, "560" 6.00000, "640" 7.00000, "720" 8.00000, "800" 9.00000)

#set title "Eficiencia da rede LVQ para diferentes ordens de AR \n em relacao a diferentes clusters" font "Times-Roman,18"
set title "Efficiency of the LVQ net for different orders of ARM \ n in relation to different output units numbers " font "Times-Roman,18"
set yrange [ 0.00000 : 100.0 ] noreverse nowriteback 
set ylabel "E(%)\n Efficiency" font "Helvetica,18"
set xlabel "Output units" font "Helvetica,18"

#plot './cluster/com_perf_clusterAR1.dat' using ($2*100):xtic(1) lc rgb "#66CDAA", '' u ($3*100) lc rgb "#BBFFFF", '' u ($4*100) lc rgb "#FF8C69", '' u ($5*100) lc rgb "#FFE7BA", '' u ($6*100) lc rgb "#87CEFF"


#--------------------------------------------------------------------------------------------------------------------------------
#Perfomance Clusters/AR Graphic 2
set output 'com_perf_clusterAR.eps'
set terminal postscript enhanced font "Helvetica" 18
set border 3 front linetype -1 linewidth 1.000
#set boxwidth 0.8 absolute
set style fill   solid 1.00 noborder
set grid nopolar
set grid noxtics nomxtics ytics nomytics noztics nomztics \
 nox2tics nomx2tics noy2tics nomy2tics nocbtics nomcbtics
set key bmargin center horizontal Left reverse enhanced autotitles columnhead nobox

set style histogram clustered gap 1 title  offset character 0, 0, 0
set style data histograms

set xtics border in scale 1,0.5 nomirror rotate by -0  offset character 0, 0, 0 
set xtics   ("AR3" 0.00000, "AR4" 1.00000, "AR6" 2.00000, "AR8" 3.00000, "AR10" 4.00000) 

set title "Eficiencia da rede LVQ para diferentes ordens de MAR \n em relacao a diferentes numeros de unidades de saida" font "Times-Roman,26"
#set title "Efficiency of the LVQ net for different orders of ARM \n in relation to different output units numbers " font "Times-Roman,26"
set yrange [ 0.000 : 100.0 ] noreverse nowriteback  
set ylabel "E(%)\n Eficiencia" font "Times-Roman,24"
set xlabel "Ordem MAR \n ---------------Quantidade de Unidades de Saida--------------" font "Times-Roman,20"

plot './cluster/com_perf_clusterAR.dat' using ($2*100):xtic(1) lc rgb "#BBFFFF", '' u ($3*100) lc rgb "#7FFFD4", '' u ($4*100) lc rgb "#66CDAA", '' u ($5*100) lc rgb "#FFFFE0", '' u ($6*100) lc rgb "#FFEC8B",'' u ($7*100) lc rgb "#FFFF00",'' u ($8*100) lc rgb "#FFC1C1",'' u ($9*100) lc rgb "#FF8C69",'' u ($10*100) lc rgb "#FF6A6A",'' u ($11*100) lc rgb "#FF0000"

#--------------------------------------------------------------------------------------------------------------------------------
#Comparative traning time process/AR 
set output 'com_traintime_AR.eps'
set terminal postscript enhanced font "Helvetica" 18

set border 3 front linetype -1 linewidth 1.000
#set boxwidth 0.8 absolute
set style fill   solid 1.00 noborder
set grid nopolar
set grid noxtics nomxtics ytics nomytics noztics nomztics \
 nox2tics nomx2tics noy2tics nomy2tics nocbtics nomcbtics
set key bmargin center horizontal Left reverse enhanced autotitles columnhead nobox

set style histogram clustered gap 1 title  offset character 0, 0, 0
set style data histograms

set xtics border in scale 1,0.5 nomirror rotate by -0  offset character 0, 0, 0 
set xtics   ("AR3" 0.00000, "AR4" 1.00000, "AR6" 2.00000, "AR8" 3.00000, "AR10" 4.00000)

#set title "Treinamento da rede LVQ para diferentes ordens de AR \n em relacao a diferentes clusters" 
set title "Treinamento da rede LVQ para diferentes ordens de MAR \n em relacao a diferentes numeros de unidades de saida" font "Times-Roman,26"
set yrange [ 0.00000 : 1000 ] noreverse nowriteback
set ylabel "Tempo (s)" font "Times-Roman,24"
set xlabel "Ordem MAR \n ---------------Quantidade de Unidades de Saida--------------" font "Times-Roman,20"

plot './cluster/com_traintime_AR.dat' using 2:xtic(1) lc rgb "#BBFFFF", '' u 3 lc rgb "#7FFFD4", '' u 4 lc rgb "#66CDAA", '' u 5 lc rgb "#FFFFE0", '' u 6 lc rgb "#FFEC8B",'' u 7 lc rgb "#FFFF00",'' u 8 lc rgb "#FFC1C1",'' u 9 lc rgb "#FF8C69",'' u 10 lc rgb "#FF6A6A",'' u 11 lc rgb "#FF0000"


