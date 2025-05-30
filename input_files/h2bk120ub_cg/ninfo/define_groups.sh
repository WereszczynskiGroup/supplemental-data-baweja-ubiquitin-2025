# **DEL_LGO_ADD_FLP(1199-1287)
# chains A and E (H3)    Nresidues: 135 
# chains B and F (H4)    Nresidues: 102 
# chain  C and G (H2A.1) Nresidues: 128 
# chain  D and H (H2B.2) Nresidues: 125 
awk '
 BEGIN{

  Nchains=8
  Nbp=147      # number of base pairs
  Ndna=Nbp*6-2 # number of dna beads
  # number of residues in each protein
  Nres["H3"]=135
  Nres["H4"]=102
  Nres["H2A"]=128
  Nres["H2B"]=125
  # type of molecules, id refers to the chain in the pdb file
  mol[1]=mol[5]="H3"
  mol[2]=mol[6]="H4"
  mol[3]=mol[7]="H2A"
  mol[4]=mol[8]="H2B"
  # end of flexible N-tails
  Ntail["H3"]=32   # occupancy convention
  Ntail["H4"]=23   # occupancy convention
  Ntail["H2A"]=14  # occupancy convention
  Ntail["H2B"]=26  # occupancy convention
  # start of flexible C-tails
  Ctail["H3"]=Nres["H3"]+1   # no Ctail
  Ctail["H4"]=Nres["H4"]+1   # no Ctail
  Ctail["H2A"]=121           # occupancy convention
  Ctail["H2B"]=Nres["H2B"]+1 # no Ctail
  # define shifts to apply to chains
  for(i=1;i<=Nchains;i=i+1) Nres[i]=Nres[mol[i]]
  ridshift[1]=Ndna
  for(i=2;i<=Nchains;i=i+1) ridshift[i]=ridshift[i-1]+Nres[i-1]

  # delete long-range go interactions
  print "<<<< del_interaction"
  for(i=1;i<=Nchains;i=i+1) {
   if(ridshift[i]+Ntail[mol[i]]>ridshift[i]+1)            {
    print "** "mol[i]" Ntail chain "i
    print "DEL_GO("ridshift[i]+1"-"ridshift[i]+Ntail[mol[i]]"/"ridshift[1]+1"-"ridshift[Nchains]+Nres[mol[Nchains]]")"
   }
   if(ridshift[i]+Nres[mol[i]]>ridshift[i]+Ctail[mol[i]]) {
    print "** "mol[i]" Ctail chain "i
    print "DEL_GO("ridshift[i]+Ctail[mol[i]]"-"ridshift[i]+Nres[mol[i]]"/"ridshift[1]+1"-"ridshift[Nchains]+Nres[mol[Nchains]]")"
   }
  }
  print ">>>>"
  print ""

  # define flexible regions and delete local go contacts
  print "<<<< flexible_local"
  print "k_dih = 1.00000"
  print "k_ang = 1.00000"
  for(i=1;i<=Nchains;i=i+1) {
   if(ridshift[i]+Ntail[mol[i]]>ridshift[i]+1)            {
    print "** "mol[i]" Ntail chain "i
    print "DEL_LGO_ADD_FLP("ridshift[i]+1"-"ridshift[i]+Ntail[mol[i]]")"
   }
   if(ridshift[i]+Nres[mol[i]]>ridshift[i]+Ctail[mol[i]]) {
    print "** "mol[i]" Ctail chain "i
    print "DEL_LGO_ADD_FLP("ridshift[i]+Ctail[mol[i]]"-"ridshift[i]+Nres[mol[i]]")"
   }
  }
  print ">>>>"
  print ""

 }
'
