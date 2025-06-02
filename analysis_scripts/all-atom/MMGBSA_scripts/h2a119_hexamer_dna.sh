#!/bin/bash
for i in {1..3}

do
	
cd ~/H2A119_corrected_sim$i/

mkdir hexadna1
mkdir hexadna2

cpptraj stripped.final_explicit_hmr_corrected.prmtop <<EOF
trajin h2a119_final_sim$i.xtc 1 1
strip !(:1-237,567-803,820-914,1044-1130) outprefix rec1 
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
strip !(:1-237,254-348,478-564,567-803,820-914,1044-1130) outprefix com1 
trajout h2a119_hexadna1_com1.xtc
go
EOF


cpptraj stripped.final_explicit_hmr_corrected.prmtop <<EOF
trajin h2a119_final_sim$i.xtc 1 1
strip !(:1-237,254-348,478-564,567-803) outprefix rec2
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
strip !(:1-237,254-348,478-564,567-803,820-914,1044-1130) outprefix com2
trajout h2a119_hexadna2_com2.xtc
go
EOF


cp  rec1* ./hexadna1/

#cp ../decomp.in ./hexadna1/

cp lig1* ./hexadna1/

cp com1.stripped.final_explicit_hmr_corrected.prmtop ./hexadna1/

cp h2a119_hexadna1_com1.xtc  ./hexadna1/

cp rec2* ./hexadna2/

#cp ../decomp.in ./hexadna2/

cp lig2* ./hexadna2/

cp com2.stripped.final_explicit_hmr_corrected.prmtop ./hexadna2/

cp h2a119_hexadna2_com2.xtc ./hexadna2/
cd ../

done
