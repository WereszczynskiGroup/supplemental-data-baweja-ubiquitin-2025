#!/bin/bash
for i in {1..3}

do
	
cd ~/canonical_nuc$i/

mkdir dimdna1
mkdir dimdna2

cpptraj stripped.final_canonical_hmr.prmtop <<EOF
trajin can_final_sim$i.xtc 1 1
strip :1-980 outprefix rec1 
trajout canonical_rec_sim$i.xtc
go
EOF


cpptraj stripped.final_canonical_hmr.prmtop <<EOF
trajin can_final_sim$i.xtc 1 1
strip !(:254-348,402-488) outprefix lig1
trajout canonical_lig_sim$i.xtc
go
EOF

cpptraj stripped.final_canonical_hmr.prmtop <<EOF
trajin can_final_sim$i.xtc 50000 200000 100
strip !(:254-348,402-488,981-1274) outprefix com1 
trajout canonical_dimdna1_com1.xtc
go
EOF


cpptraj stripped.final_canonical_hmr.prmtop <<EOF
trajin can_final_sim$i.xtc 1 1
strip :1-980 outprefix rec2
trajout canonical_rec_sim$i.xtc
go
EOF

cpptraj stripped.final_canonical_hmr.prmtop <<EOF
trajin can_final_sim$i.xtc 1 1
strip !(:744-838,892-978) outprefix lig2
trajout canonical_lig_sim$i.xtc
go
EOF

cpptraj stripped.final_canonical_hmr.prmtop <<EOF
trajin can_final_sim$i.xtc 50000 200000 100
strip !(:744-838,892-978,981-1274) outprefix com2
trajout canonical_dimdna2_com2.xtc
go
EOF


cp  rec1* ./dimdna1/

cp ./dimerdna1/decomp.in ./dimdna1/

cp lig1* ./dimdna1/

cp com1.stripped.final_canonical_hmr.prmtop ./dimdna1/

cp canonical_dimdna1_com1.xtc  ./dimdna1/

cp rec2* ./dimdna2/

cp ./dimerdna2/decomp.in ./dimdna2/

cp lig2* ./dimdna2/

cp com2.stripped.final_canonical_hmr.prmtop ./dimdna2/

cp canonical_dimdna2_com2.xtc ./dimdna2/
cd ../

done
