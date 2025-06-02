#!/bin/sh 

for i in {1..3}

do

cd ./canonical_nuc$i/

j=$(($i+6))

cpptraj <<EOF

parm stripped.final_canonical_hmr.prmtop
trajin can_final_sim$i.xtc 50000 200000 

#trajout can_final_sim$i.pdb

#rms first

# Calculate the center of mass for the first base pair
#vector V1 :982@C1',N9,C4,C5,C6,C8 :1272@C1',N9,C4,C5,C6,C8 corrframe com1_1425 out com1.dat

# Calculate the center of mass for the second base pair
#vector V2 :1126@C1',N9,C4,C5,C6,C8 :1129@C1',N9,C4,C5,C6,C8 corrframe com2_1281 out com2.dat

# Calculate the distance between the COMs of the two base pairs
#distance BP_COM_Distance com1_1425 com2_1281 out can_dist$j.dist


#distance x_a :1014,1015,1016,1017,1238,1239,1240,1241@C1' :1163,1164,1165,1166,1092,1093,1094,1095@C1' out nuc_dist$j.dist1

distance x_a :982,1273@C1' :1055,1200@C1' out nuc_dist$j.dist1_entry
distance x_a1 :1126,1129@C1' :1055,1200@C1' out nuc_dist$j.dist1_exit
#atomicfluct out strand1_sim$j.dat :981-1127@C1'
#atomicfluct out strand2_sim$j.dat :1128-1274@C1'

#rmsd :366-441 
#rmsd :366-441@CA first out 1UBQ_run1.dat
#rmsd :932-1007
#rmsd :932-1007 first out 2UBQ_run1.dat
go
EOF

cd ../

done
