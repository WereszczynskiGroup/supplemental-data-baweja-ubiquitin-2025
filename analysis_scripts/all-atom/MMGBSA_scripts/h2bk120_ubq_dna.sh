#!/bin/bash

for i in {1..3}

do
	
cd ~/h2bk120_corrected$i/


mkdir ubiquitin1

mkdir ubiquitin2

cpptraj stripped.final_h2bk120_hmr_corrected.prmtop <<EOF
trajin h2bk120_final_sim$i.xtc 1 1
strip !(:1133-1426) outprefix rec_ubq1 
trajout h2bk120_rec_sim$i.xtc
go
EOF


cpptraj stripped.final_h2bk120_hmr_corrected.prmtop <<EOF
trajin h2bk120_final_sim$i.xtc 1 1
strip :1-931,1008-1426 outprefix lig_ubq1
trajout h2bk120_lig_sim$i.xtc
go
EOF


cpptraj stripped.final_h2bk120_hmr_corrected.prmtop <<EOF
trajin h2bk120_final_sim$i.xtc 50000 200000 100
strip !(:932-1007,1133-1426) outprefix com_ubq1
trajout h2bk120_com1_mmgbsa.xtc
go
EOF



cpptraj stripped.final_h2bk120_hmr_corrected.prmtop <<EOF
trajin h2bk120_final_sim$i.xtc
strip !(:1133-1426) outprefix rec_ubq2 
trajout h2bk120_rec_sim$i.xtc
go
EOF


cpptraj stripped.final_h2bk120_hmr_corrected.prmtop <<EOF
trajin h2bk120_final_sim$i.xtc 
strip :77-1426 outprefix lig_ubq2
trajout h2bk120_lig_sim$i.xtc
go
EOF


cpptraj stripped.final_h2bk120_hmr_corrected.prmtop <<EOF
trajin h2bk120_final_sim$i.xtc 50000 200000 100
strip !(:1-76,1133-1426) outprefix com_ubq2
trajout h2bk120_com2_mmgbsa.xtc

go
EOF


cp rec_ubq1* ./ubiquitin1/

cp ../decomp_ubq1.in ./ubiquitin1/

cp lig_ubq1* ./ubiquitin1/

cp com_ubq1.stripped.final_h2bk120_hmr_corrected.prmtop ./ubiquitin1/

cp h2bk120_com1_mmgbsa.xtc  ./ubiquitin1/

cp rec_ubq2* ./ubiquitin2/

cp ../decomp_ubq2.in ./ubiquitin2/

cp lig_ubq2* ./ubiquitin2/

cp com_ubq2.stripped.final_h2bk120_hmr_corrected.prmtop ./ubiquitin2/

cp h2bk120_com2_mmgbsa.xtc ./ubiquitin2/
cd ../

done
