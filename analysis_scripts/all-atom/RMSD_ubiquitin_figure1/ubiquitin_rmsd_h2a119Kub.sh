#!/bin/sh 

for i in {1..3}

do

cd ./H2A119_corrected_sim$i/



cpptraj <<EOF

parm stripped.final_explicit_hmr_corrected.prmtop
trajin h2a119_final_sim$i.xtc 1 200000 20
rms "(:45-132, 161-229, 611-697, 726-795)&(@CA,C,N,O)" 
rmsd  :366-441@CA,C,N,O  out rmsd_core_aligned_ubq$i.ubq1 nofit
rmsd  :932-1007@CA,C,N,O  out rmsd_core_aligned_ubq$i.ubq2 nofit
EOF

cd ../

done
