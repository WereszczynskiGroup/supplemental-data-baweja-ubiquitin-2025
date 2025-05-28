#!/usr/bin/python

import sys
#from sets import Set
import numpy as np
from numpy import linalg as LA

import MDAnalysis
import MDAnalysis.analysis.hbonds

class Hbond:
    pass

class Pdns_entry:
    pass

# define universe
uarray=[]
uarray.append(MDAnalysis.Universe('1kx5_model_charmm27.pdb'))
uarray.append(MDAnalysis.Universe('3lz0_adjust_resid_charmm27.pdb'))

# analyse hbonds
# tails edges essentially the same as those used in respac
selH3 =(44,134)
selH4 =(24,101)
selH2A=(16,116) # only exception 16 instead of 15, because of the non-symmetric residue
selH2B=(36,124)
harray=[]
for u in uarray:
  harray.append(MDAnalysis.analysis.hbonds.HydrogenBondAnalysis(u,selection1='(segid A and resid %d:%d) or (segid B and resid %d:%d) or (segid C and resid %d:%d) or (segid D and resid %d:%d) or (segid E and resid %d:%d) or (segid F and resid %d:%d) or (segid G and resid %d:%d) or (segid H and resid %d:%d)'%(selH3[0],selH3[1],selH4[0],selH4[1],selH2A[0],selH2A[1],selH2B[0],selH2B[1],selH3[0],selH3[1],selH4[0],selH4[1],selH2A[0],selH2A[1],selH2B[0],selH2B[1]),selection2='resname DA DT DC DG',acceptors=('O1P','O2P')))
  harray[-1].run()

chain2num={} # convert chain consistently with the go model, first dna, then proteins
chain2num["A"]=3
chain2num["B"]=4
chain2num["C"]=5
chain2num["D"]=6
chain2num["E"]=7
chain2num["F"]=8
chain2num["G"]=9
chain2num["H"]=10
chain2num["I"]=1
chain2num["J"]=2

# define set
bsets=[]
for h,u in zip(harray,uarray):
  bsets.append(set())
  for i in h.timeseries[0]:
    idonor=i[0] # donor
    iaccep=i[1] # acceptor
    b=Hbond()
    print (i)
    b.dsegid   =chain2num[u.atoms[idonor].segid]
    b.dresname =u.atoms[idonor].resname
    b.dresid   =u.atoms[idonor].resid
    b.asegid   =chain2num[u.atoms[iaccep].segid]
    #b.aresname =u.atoms[iaccep].resname
    b.aresid   =u.atoms[iaccep].resid
    b.true =1
    bsets[-1].add((b.dsegid,b.dresname,b.dresid,b.asegid,b.aresid,b.true))



print (bsets)
