#!/bin/python
import os
import MDAnalysis as mda
from MDAnalysis.analysis import contacts
import numpy as np

def residue_contact_matrix(u_list, group_a_list, group_b_list, radius=4.5, step=100):
    n_res_a = len(group_a_list[0].residues)  # Assume same residues in all systems
    n_res_b = len(group_b_list[0].residues)
    
    contact_matrix = np.zeros((n_res_a, n_res_b))
    
    # Loop through all systems and aggregate contacts
    for u, group_a, group_b in zip(u_list, group_a_list, group_b_list):
        for ts in u.trajectory[50000:200000:step]:  # Adjust frame range as needed
            for i, res_a in enumerate(group_a.residues):
                for j, res_b in enumerate(group_b.residues):
                    # Calculate distances between residues
                    dist = contacts.distance_array(res_a.atoms.positions, res_b.atoms.positions, box=u.dimensions)
                    if np.any(dist <= radius):
                        contact_matrix[i, j] += 1
                    
    return contact_matrix

def save_contact_matrix(contact_matrix, filename):
    np.savetxt(filename, contact_matrix, fmt='%.6f')  # Save the matrix in .dat format with 6 decimal precision

# Lists to hold the universes and selection groups for all three systems
u_list = []
group_a_list = []
group_b_list = []

# Read and store universes and selections for all systems
for i in range(1, 4):
    new_directory = "/home/lbaweja/canonical_nuc" + str(i)
    os.chdir(new_directory)
    u = mda.Universe('can_sim' + str(i) + ".pdb", "can_final_sim" + str(i) + ".xtc")
    
    protein1 = u.select_atoms("resid 254:348 or resid 402:488 and not name H*")
    protein2 = u.select_atoms("resid 744:838 or resid 892:978 and not name H*")
    
    u_list.append(u)
    group_a_list.append(protein1)
    group_b_list.append(protein2)

# Calculate residue-wise contact matrix over all systems
contact_matrix = residue_contact_matrix(u_list, group_a_list, group_b_list, radius=4.5, step=100)

# Save the contact matrix as a .dat file
save_contact_matrix(contact_matrix, 'aggregated_residue_residue_contact_matrix.dat')
