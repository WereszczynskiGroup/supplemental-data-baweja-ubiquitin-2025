#!/bin/sh


for i in {1..3}; 


do 

rsync -aurP lbaweja@condo.tbc.iit.edu:~/canonical_nuc$i/dimer_dimer1/*.simcanonical_nuc$i ./dimer_dimer1



#rsync -aurP lbaweja@condo.tbc.iit.edu:~/canonical_nuc$i/hexadna2/*.simcanonical_nuc$i ./dim_tet2
#rsync -aurP lbaweja@condo.tbc.iit.edu:~/H2A119_corrected_sim$i/dimerdna2/file$i.txt ./dimer2

done


