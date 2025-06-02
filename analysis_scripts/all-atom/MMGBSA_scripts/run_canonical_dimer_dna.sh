#!/bin/bash

# Iterate through directories
for dir in ~/canonical_nuc{1..3}/dimdna{1,2}; do
    # Extract simulation number
    sim_number=$(basename $(dirname $dir))
    # Extract ubiquitin number
    dimdna_number=$(basename $dir)
    number1=$(echo "$dimdna_number" | grep -o '[0-9]\+')
    number="$((number1-0))"
    echo $number

    # Create sbatch file
    sbatch_file="$dir/run_smmgbsa$number.sbatch"

    # Write sbatch directives to the file
    cat <<EOT >> $sbatch_file
#!/bin/bash
#SBATCH --time=24:00:00   # walltime limit (HH:MM:SS)
#SBATCH --nodes=1         # number of nodes
#SBATCH --ntasks-per-node=8  # 8 processor core(s) per node
#SBATCH --job-name="MMGBSA-H2A119-UBQ${sim_number}-${dimdna_number}"
#SBATCH --partition=normal
# Load necessary modules
source ~/amber22/amber.sh

# Move to the directory
cd $dir

# Run MMGBSA
mpirun -np 8 MMPBSA.py.MPI -O -i *.in -o canonical_${dimdna_number}.sim${sim_number} -eo ${dimdna_number}.lig1 -sp com$number.stripped.final_canonical_hmr.prmtop -cp com$number.stripped.final_canonical_hmr.prmtop -rp ../dimdna1/rec1.stripped.final_canonical_hmr.prmtop -lp lig$number.stripped.final_canonical_hmr.prmtop -y canonical_dimdna$number"_"com$number.xtc
EOT

    # Submit the sbatch job
    sbatch $sbatch_file

done
