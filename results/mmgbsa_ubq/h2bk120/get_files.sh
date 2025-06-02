#!/bin/sh


for i in {1..3}; 


do 

rsync -aurP lbaweja@condo.tbc.iit.edu:~/h2bk120_corrected$i/dimer_dimer1/*.simh2bk120_corrected$i ./dimer_dimer1
#rsync -aurP lbaweja@condo.tbc.iit.edu:~/h2bk120_corrected$i/ubiquitin2/*.simh2bk120_corrected$i ./dimer2


done


