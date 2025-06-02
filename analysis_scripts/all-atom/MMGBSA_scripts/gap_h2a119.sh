#!/bin/sh 

for i in {1..3}

do

cd ./H2A119_corrected_sim$i/



cpptraj <<EOF

parm stripped.final_explicit_hmr_corrected.prmtop
trajin h2a119_final_sim$i.xtc 50000 200000 

#trajout h2a119_final_sim$i.pdb
#rms first

#atomicfluct out strand1_sim$i.dat :1133-1279@C1'
#atomicfluct out strand2_sim$i.dat :1280-1426@C1'

# Calculate the center of mass for the first base pair
#vector V1 :1134@C1',N9,C4,C5,C6,C8 :1425@C1',N9,C4,C5,C6,C8 corrframe com1_1425 out com1.dat

# Calculate the center of mass for the second base pair
#vector V2 :1278@C1',N9,C4,C5,C6,C8 :1281@C1',N9,C4,C5,C6,C8 corrframe com2_1281 out com2.dat

# Calculate the distance between the COMs of the two base pairs
#distance BP_COM_Distance com1_1425 com2_1281 out h2a119_dist$i.dist

#distance x_a :1166,1167,1168,1169,1390,1391,1392,1393@C1' :1312,1313,1314,1315,1244,1245,1246,1247@C1' out h2a119_dist$i.dist1

distance x_a :1134,1425@C1' :1207,1352@C1' out h2a119_dist$i.dist1_entry
distance x_a1 :1278,1281@C1' :1207,1352@C1' out h2a119_dist$i.dist1_exit
#rmsd :366-441 
#rmsd :366-441@CA first out 1UBQ_run1.dat
#rmsd :932-1007
#rmsd :932-1007 first out 2UBQ_run1.dat
go
EOF

cd ../

done
