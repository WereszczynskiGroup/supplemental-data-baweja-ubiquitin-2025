#!/bin/sh


for i in {1..3}; 


do 

rsync -aurP lbaweja@condo.tbc.iit.edu:~/H2A119_corrected_sim$i/dimer_dimer1/*.simH2A119_corrected_sim$i ./dimer_dimer/

#rsync -aurP lbaweja@condo.tbc.iit.edu:~/H2A119_corrected_sim$i/ubq_dna2/*.simH2A119_corrected_sim$i ./dimer2
#rsync -aurP lbaweja@condo.tbc.iit.edu:~/H2A119_corrected_sim$i/dimerdna2/file$i.txt ./dimer2

done


