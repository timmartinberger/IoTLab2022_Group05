#
# Gnuplot starten
#
gnuplot << EOF
#
# \"andern des default plotting style + postscript Einstellung f\"ur eps
#
set terminal postscript eps color
# Achsenbeschriftung
set xlabel "time (seconds)"
set ylabel "packets"
# Dateiname der Abbildung (Output)
set output "gnuplot_output.eps"
# Separator festlegen f\"ur die Inputdatei
# benutze "," f\"ur csv
set datafile separator " "
# Plot aus Dateien datei_1.log und datei_2.log
# datei_1: Spalte 1 f\"ur die x-Achse und Spalte 7 f\"ur die y-Achse
# datei_2: Zahlen 1 bis n f\"ur die x-Achse und Spalte 2 f\"ur die y-Achse
plot "sequence_numbers.log" using 1:2 with lines title " test 1" , \
# plot "report.log" using :2 with lines title " test 2"
EOF