#!/bin/bash

# Iterate through directories
for dir in ~/H2A119_corrected_sim{1..3}/ubq_dna{1,2}; do
    # Extract simulation number
    sim_number=$(basename $(dirname $dir))
    # Extract ubq_dna number
    ubq_dna_number=$(basename $dir)
    number1=$(echo "$ubq_dna_number" | grep -o '[0-9]\+')
    number="$((number1-0))"
    echo $number

    # Create sbatch file
    sbatch_file="$dir/run_dmmgbsa$number.sbatch"

    # Write sbatch directives to the file
    cat <<EOT >> $sbatch_file
#!/bin/bash
#SBATCH --time=24:00:00   # walltime limit (HH:MM:SS)
#SBATCH --nodes=1         # number of nodes
#SBATCH --ntasks-per-node=8  # 8 processor core(s) per node
#SBATCH --job-name="MMGBSA-H2A119-UBQ${sim_number}-${ubq_dna_number}"
#SBATCH --partition=normal
# Load necessary modules
source ~/amber22/amber.sh

# Move to the directory
cd $dir

# Run MMGBSA
mpirun -np 8 MMPBSA.py.MPI -O -i *.in -o h2a119_${ubq_dna_number}.sim${sim_number} -eo ${ubq_dna_number}.lig1 -sp com_ubq$number.stripped.final_explicit_hmr_corrected.prmtop -cp com_ubq$number.stripped.final_explicit_hmr_corrected.prmtop -rp rec_ubq$number.stripped.final_explicit_hmr_corrected.prmtop -lp lig_ubq$number.stripped.final_explicit_hmr_corrected.prmtop -y *.xtc
EOT

    # Submit the sbatch job
    sbatch $sbatch_file

done
