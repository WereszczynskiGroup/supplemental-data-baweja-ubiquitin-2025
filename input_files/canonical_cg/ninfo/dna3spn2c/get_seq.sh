cat 1kx5_dna.pdb | awk '{if($3=="C1'\''"&&$5=="I")print $4}' | sed 's/D//' | awk '{printf($1)}'
echo ""
