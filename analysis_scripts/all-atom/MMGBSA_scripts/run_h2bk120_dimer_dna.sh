#!/bin/bash

# Iterate through directories
for dir in ~/h2bk120_corrected{1..3}/dimdna{1,2}; do
    # Extract simulation number
    sim_number=$(basename $(dirname $dir))
    # Extract ubiquitin number
    dimdna_number=$(basename $dir)
    number1=$(echo "$dimdna_number" | grep -o '[0-9]\+')
    number="$((number1-0))"
    echo $number

    # Create sbatch file
    sbatch_file="$dir/run_nmgbsa$number.sbatch"

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
mpirun -np 8 MMPBSA.py.MPI -O -i *.in -o h2bk120_${dimdna_number}.sim${sim_number} -eo ${dimdna_number}.lig1 -sp com$number.stripped.final_h2bk120_hmr_corrected.prmtop -cp com$number.stripped.final_h2bk120_hmr_corrected.prmtop -rp rec$number.stripped.final_h2bk120_hmr_corrected.prmtop -lp lig$number.stripped.final_h2bk120_hmr_corrected.prmtop -y h2bk120_dimdna$number"_"com$number.xtc
EOT

    # Submit the sbatch job
    sbatch $sbatch_file

done
