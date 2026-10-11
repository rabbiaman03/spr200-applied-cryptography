set terminal png size 1400,900

set output 'ecc_keygen_performance.png'

set title 'ECC Key Generation Performance'

set style data histograms

set style histogram rowstacked

set style fill solid 1.0 border -1

set boxwidth 0.8

set bmargin 8

set lmargin 10

set rmargin 10

set xtics rotate by -30 offset -1.5,-1

set key below

set ylabel "Time (seconds)"



# Create a temporary data file that splits each row into private and public measurements

system("awk 'NR>1 {print $1\"_priv\",$2,$3,$4; print $1\"_pub\",$5,$6,$7}' ecc_keygen_perf.dat > temp.dat")



# Create labels for each curve's private and public keys

set xtics ("secp256k1 Private" 0, "secp256k1 Public" 1, "prime256v1 Private" 2, "prime256v1 Public" 3, \

          "secp384r1 Private" 4, "secp384r1 Public" 5, "brainpoolP512t1 Private" 6, "brainpoolP512t1 Public" 7)



# Set new colors for better visual appeal

set style fill solid 0.8 border -1

set boxwidth 0.6



# Plot stacked bars showing real, user, and sys times with better color choices

plot 'temp.dat' using 2:xticlabels(1) title "Real" lc rgb "skyblue", \
     '' using 3 title "User" lc rgb "lightgreen", \
     '' using 4 title "Sys" lc rgb "lightpink"
