#!/bin/bash
for i in {1..3}

do
	
cd ~/canonical_nuc$i/

mkdir dimer_dimer1

cpptraj stripped.final_canonical_hmr.prmtop <<EOF
trajin can_final_sim$i.xtc 1 1
strip !(:744-838,892-978) outprefix rec1 
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
strip !(:254-348,402-488,744-838,892-978) outprefix com1 
trajout canonical_dimer_dimer1_com1.xtc
go
EOF


cp  rec1* ./dimer_dimer1/

cp ../decomp.in ./dimer_dimer1/

cp lig1* ./dimer_dimer1/

cp com1.stripped.final_canonical_hmr.prmtop ./dimer_dimer1/

cp canonical_dimer_dimer1_com1.xtc  ./dimer_dimer1/

cd ../

done
