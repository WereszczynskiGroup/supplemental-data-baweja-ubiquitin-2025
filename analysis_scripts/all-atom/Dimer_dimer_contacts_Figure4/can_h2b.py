#!/bin/python
import os
import MDAnalysis as mda
from MDAnalysis.analysis import contacts
import numpy as np
def contacts_within_cutoff(u, group_a, group_b, radius=4.5, step=100):
    timeseries = []
    for ts in u.trajectory[1:150000:step]:  # Skip frames according to step
        # calculate distances between group_a and group_b
        dist = contacts.distance_array(group_a.positions, group_b.positions, box=u.dimensions)
        # determine which distances <= radius
        n_contacts = contacts.contact_matrix(dist, radius).sum()
        timeseries.append([ts.frame, n_contacts])
    return np.array(timeseries)

for i in range(1, 4):
    new_directory = "/home/lbaweja/h2bk120_corrected" + str(i)
    os.chdir(new_directory)
    u = mda.Universe('k120_sim' + str(i) + ".pdb", "h2bk120_final_sim" + str(i) + ".xtc")
    
    protein1 = u.select_atoms("resid 455:549 or resid 1044:1130 and not name H*")
    protein2 = u.select_atoms("resid 820:914 or resid 113:199 and  not name H*")
    DNA = u.select_atoms("resid 202:438 or resid 567:803 and not name H*")

    # Calculate contacts between protein selections and DNA
    contacts_protein1_DNA = contacts_within_cutoff(u, protein1, DNA, radius=4.5, step=100)
    contacts_protein2_DNA = contacts_within_cutoff(u, protein2, DNA, radius=4.5, step=100)

    np.savetxt('contacts_dimer1_sys' + str(i) + '.con', contacts_protein1_DNA, header="Time Contacts")
    np.savetxt('contacts_dimer2_sys' + str(i) + '.con', contacts_protein2_DNA, header="Time Contacts")
