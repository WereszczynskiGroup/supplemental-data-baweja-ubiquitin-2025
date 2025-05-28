#!/bin/sh 

for i in {1..3}
do

j=$(($i+3))
cd ./h2bk120_corrected$i/



cpptraj <<EOF

parm stripped.final_h2bk120_hmr_corrected.prmtop
trajin h2bk120_final_sim$i.xtc 1 200000 20 

rms  "(:246-331, 362-430, 611-697, 726-795)&(@CA,C,N,O)" 

rmsd  :1-76@CA,C,N,O  out rmsd_core_aligned_ubq$i.ubq1 nofit

rmsd  :932-1007@CA,C,N,O  out rmsd_core_aligned_ubq$i.ubq2 nofit

EOF

cd ../

done
