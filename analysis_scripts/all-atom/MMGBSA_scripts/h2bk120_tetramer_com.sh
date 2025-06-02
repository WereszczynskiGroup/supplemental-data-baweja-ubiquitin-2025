#!/bin/bash
for i in {1..3}

do
	
cd ~/h2bk120_corrected$i/

mkdir dimer_dimer1

cpptraj stripped.final_h2bk120_hmr_corrected.prmtop <<EOF
trajin h2bk120_final_sim$i.xtc 1 1
strip !(:455-549,1044-1130) outprefix rec1 
trajout h2bk120_rec_sim$i.xtc
go
EOF


cpptraj stripped.final_h2bk120_hmr_corrected.prmtop <<EOF
trajin h2bk120_final_sim$i.xtc 1 1
strip !(:113-199,820-914) outprefix lig1
trajout h2bk120_lig_sim$i.xtc
go
EOF

cpptraj stripped.final_h2bk120_hmr_corrected.prmtop <<EOF
trajin h2bk120_final_sim$i.xtc 50000 200000 100
strip !(:113-199,455-549,820-914,1044-1130) outprefix com1 
trajout h2bk120_dimer_dimer1_com1.xtc
go
EOF


#cpptraj stripped.final_h2bk120_hmr_corrected.prmtop <<EOF
#trajin h2bk120_final_sim$i.xtc 1 1
#strip !(:113-199,202-438,567-803,820-914) outprefix rec2
#trajout h2bk120_rec_sim$i.xtc
#go
#EOF

#cpptraj stripped.final_h2bk120_hmr_corrected.prmtop <<EOF
#trajin h2bk120_final_sim$i.xtc 1 1
#strip !(:455-549,1044-1130) outprefix lig2
#trajout h2bk120_lig_sim$i.xtc
#go
#EOF

#cpptraj stripped.final_h2bk120_hmr_corrected.prmtop <<EOF
#trajin h2bk120_final_sim$i.xtc 50000 200000 100
#strip !(:113-199,202-438,455-549,567-803,820-914,1044-1130) outprefix com2
#trajout h2bk120_hexadna2_com2.xtc
#go
#EOF


cp  rec1* ./dimer_dimer1/

cp ../decomp1.in ./dimer_dimer1/

cp lig1* ./dimer_dimer1/

cp com1.stripped.final_h2bk120_hmr_corrected.prmtop ./dimer_dimer1/

cp h2bk120_dimer_dimer1_com1.xtc  ./dimer_dimer1/





cd ../

done
