#!/bin/bash
for i in {1..3}

do
	
cd ~/h2bk120_corrected$i/

mkdir dimdna1
mkdir dimdna2

cpptraj stripped.final_h2bk120_hmr_corrected.prmtop <<EOF
trajin h2bk120_final_sim$i.xtc 1 1
strip :1-1132 outprefix rec1 
trajout h2bk120_rec_sim$i.xtc
go
EOF


cpptraj stripped.final_h2bk120_hmr_corrected.prmtop <<EOF
trajin h2bk120_final_sim$i.xtc 1 1
strip !(:455-549,1044-1130) outprefix lig1
trajout h2bk120_lig_sim$i.xtc
go
EOF

cpptraj stripped.final_h2bk120_hmr_corrected.prmtop <<EOF
trajin h2bk120_final_sim$i.xtc 50000 200000 100
strip !(:455-549,1044-1130,1133-1426) outprefix com1 
trajout h2bk120_dimdna1_com1.xtc
go
EOF


cpptraj stripped.final_h2bk120_hmr_corrected.prmtop <<EOF
trajin h2bk120_final_sim$i.xtc 1 1
strip :1-1132 outprefix rec2
trajout h2bk120_rec_sim$i.xtc
go
EOF

cpptraj stripped.final_h2bk120_hmr_corrected.prmtop <<EOF
trajin h2bk120_final_sim$i.xtc 1 1
strip !(:113-199,820-914) outprefix lig2
trajout h2bk120_lig_sim$i.xtc
go
EOF

cpptraj stripped.final_h2bk120_hmr_corrected.prmtop <<EOF
trajin h2bk120_final_sim$i.xtc 50000 200000 100
strip !(:113-199,820-914,1133-1426) outprefix com2
trajout h2bk120_dimdna2_com2.xtc
go
EOF


cp  rec1* ./dimdna1/

cp ./dimerdna1/decomp.in ./dimdna1/

cp lig1* ./dimdna1/

cp com1.stripped.final_h2bk120_hmr_corrected.prmtop ./dimdna1/

cp h2bk120_dimdna1_com1.xtc  ./dimdna1/

cp rec2* ./dimdna2/

cp ./dimerdna2/decomp.in ./dimdna2/

cp lig2* ./dimdna2/

cp com2.stripped.final_h2bk120_hmr_corrected.prmtop ./dimdna2/

cp h2bk120_dimdna2_com2.xtc ./dimdna2/
cd ../

done
