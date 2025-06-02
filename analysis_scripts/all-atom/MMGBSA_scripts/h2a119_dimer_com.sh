#!/bin/bash
for i in {1..3}

do
	
cd ~/H2A119_corrected_sim$i/

mkdir dimdna1
mkdir dimdna2

cpptraj stripped.final_explicit_hmr_corrected.prmtop <<EOF
trajin h2a119_final_sim$i.xtc 1 1
strip :1-1132 outprefix rec1 
trajout h2a119_rec_sim$i.xtc
go
EOF


cpptraj stripped.final_explicit_hmr_corrected.prmtop <<EOF
trajin h2a119_final_sim$i.xtc 1 1
strip !(:254-348,478-564) outprefix lig1
trajout h2a119_lig_sim$i.xtc
go
EOF

cpptraj stripped.final_explicit_hmr_corrected.prmtop <<EOF
trajin h2a119_final_sim$i.xtc 50000 200000 100
strip !(:254-348,478-564,1133-1426) outprefix com1 
trajout h2a119_dimdna1_com1.xtc
go
EOF


cpptraj stripped.final_explicit_hmr_corrected.prmtop <<EOF
trajin h2a119_final_sim$i.xtc 1 1
strip :1-1132 outprefix rec2
trajout h2a119_rec_sim$i.xtc
go
EOF

cpptraj stripped.final_explicit_hmr_corrected.prmtop <<EOF
trajin h2a119_final_sim$i.xtc 1 1
strip !(:820-914,1044-1130) outprefix lig2
trajout h2a119_lig_sim$i.xtc
go
EOF

cpptraj stripped.final_explicit_hmr_corrected.prmtop <<EOF
trajin h2a119_final_sim$i.xtc 50000 200000 100
strip !(:820-914,1044-1130,1133-1426) outprefix com2
trajout h2a119_dimdna2_com2.xtc
go
EOF


cp  rec1* ./dimdna1/

cp ../decomp.in ./dimdna1/

cp lig1* ./dimdna1/

cp com1.stripped.final_explicit_hmr_corrected.prmtop ./dimdna1/

cp h2a119_dimdna1_com1.xtc  ./dimdna1/

cp rec2* ./dimdna2/

cp ../decomp.in ./dimdna2/

cp lig2* ./dimdna2/

cp com2.stripped.final_explicit_hmr_corrected.prmtop ./dimdna2/

cp h2a119_dimdna2_com2.xtc ./dimdna2/
cd ../

done
