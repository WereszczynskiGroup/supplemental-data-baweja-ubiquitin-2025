#!/bin/bash
for i in {1..3}

do
	
cd ~/canonical_nuc$i/

mkdir hexadna1
mkdir hexadna2

cpptraj stripped.final_canonical_hmr.prmtop <<EOF
trajin can_final_sim$i.xtc 1 1
strip !(:1-237,491-727,744-838,892-978) outprefix rec1 
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
strip !(:1-237,254-348,402-488,491-727,744-838,892-978) outprefix com1 
trajout canonical_hexadna1_com1.xtc
go
EOF


cpptraj stripped.final_canonical_hmr.prmtop <<EOF
trajin can_final_sim$i.xtc 1 1
strip !(:1-237,254-348,402-488,491-727) outprefix rec2
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
strip !(:1-237,254-348,402-488,491-727,744-838,892-978) outprefix com2
trajout canonical_hexadna2_com2.xtc
go
EOF


cp  rec1* ./hexadna1/

cp ../decomp.in ./hexadna1/

cp lig1* ./hexadna1/

cp com1.stripped.final_canonical_hmr.prmtop ./hexadna1/

cp canonical_hexadna1_com1.xtc  ./hexadna1/

cp rec2* ./hexadna2/

cp ../decomp.in ./hexadna2/

cp lig2* ./hexadna2/

cp com2.stripped.final_canonical_hmr.prmtop ./hexadna2/

cp canonical_hexadna2_com2.xtc ./hexadna2/
cd ../

done
