#!/bin/bash
for i in {1..3}

do
	
cd ~/H2A119_corrected_sim$i/

mkdir ubq_dna1
mkdir ubq_dna2

cpptraj stripped.final_explicit_hmr_corrected.prmtop <<EOF
trajin h2a119_final_sim$i.xtc 1 1
strip :1-1132 outprefix rec_ubq1 
trajout h2a119_rec_sim$i.xtc
go
EOF


cpptraj stripped.final_explicit_hmr_corrected.prmtop <<EOF
trajin h2a119_final_sim$i.xtc 1 1
strip !(:366-441) outprefix lig_ubq1
trajout h2a119_lig_sim$i.xtc
go
EOF

cpptraj stripped.final_explicit_hmr_corrected.prmtop <<EOF
trajin h2a119_final_sim$i.xtc 50000 200000 100
strip !(:366-441,1133-1426) outprefix com_ubq1
trajout h2a119_com1_sim$i.xtc
go
EOF


cpptraj stripped.final_explicit_hmr_corrected.prmtop <<EOF
trajin h2a119_final_sim$i.xtc 1 1
strip !(:932-1007) outprefix lig_ubq2
trajout h2a119_lig_sim$i.xtc
go
EOF


cpptraj stripped.final_explicit_hmr_corrected.prmtop <<EOF
trajin h2a119_final_sim$i.xtc 1 1
strip :1-1132 outprefix rec_ubq2
trajout h2a119_rec_sim$i.xtc
go
EOF


cpptraj stripped.final_explicit_hmr_corrected.prmtop <<EOF
trajin h2a119_final_sim$i.xtc 50000 200000 100
strip !(:932-1007,1133-1426) outprefix com_ubq2 
trajout h2a119_com2_sim$i.xtc
go
EOF

#cpptraj stripped.final_explicit_hmr_corrected.prmtop <<EOF
#trajin h2a119_sim$i.xtc 25000 100000 750
#trajout ubq1_sim$i.xtc
#go
#EOF

#cpptraj stripped.final_explicit_hmr_corrected.prmtop <<EOF
#trajin h2a119_sim$i.xtc 25000 100000 750
#trajout ubq2_sim$i.xtc
#go

#EOF


cp  rec_ubq1* ./ubq_dna1/

cp ../decomp_ubq1.in ./ubq_dna1/

cp lig_ubq1* ./ubq_dna1/

cp com_ubq1.stripped.final_explicit_hmr_corrected.prmtop ./ubq_dna1/

cp h2a119_com1_sim$i.xtc  ./ubq_dna1/

cp rec_ubq2* ./ubq_dna2/

cp ../decomp_ubq2.in ./ubq_dna2/

cp lig_ubq2* ./ubq_dna2/

cp com_ubq2.stripped.final_explicit_hmr_corrected.prmtop ./ubq_dna2/

cp h2a119_com2_sim$i.xtc ./ubq_dna2/
cd ../

done
