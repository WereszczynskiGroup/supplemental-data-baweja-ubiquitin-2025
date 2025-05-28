#!/bin/python
import os
import MDAnalysis as mda
from MDAnalysis.analysis import contacts
import numpy as np

def contacts_within_cutoff(u, group_a, group_b, radius=4.5, step=100):
    timeseries = []
    contact_map = np.zeros((len(group_a), len(group_b)))  # to store contacts for B-factor mapping
    for ts in u.trajectory[50000:150000:step]:  # Skip frames according to step
        # calculate distances between group_a and group_b
        dist = contacts.distance_array(group_a.positions, group_b.positions, box=u.dimensions)
        # determine which distances <= radius
        contact_matrix = contacts.contact_matrix(dist, radius)
        n_contacts = contact_matrix.sum()
        contact_map += contact_matrix  # accumulate contact map over time
        timeseries.append([ts.frame, n_contacts])
    # Normalize the contact map by the number of frames
    contact_map /= len(u.trajectory[50000:150000:step])
    return np.array(timeseries), contact_map

def write_complete_pdb_with_bfactors(u, group_a, group_b, contact_map, output_pdb):
    # Assign contact values to the B-factor of group_a atoms
    b_factors = np.zeros(len(u.atoms))  # Initialize B-factor array for all atoms
    
    # Assign contact values to group_a
    for i, atom in enumerate(group_a):
        b_factors[atom.index] = np.sum(contact_map[i])  # Sum contacts for each atom in group_a

    # Assign contact values to group_b
    for j, atom in enumerate(group_b):
        b_factors[atom.index] = np.sum(contact_map[:, j])  # Sum contacts for each atom in group_b

    # Assign the B-factors to the relevant atoms
    u.atoms.tempfactors = b_factors

    # Move to the last frame
    u.trajectory[-1]

    # Write out only the last frame (single snapshot) to the PDB file with updated B-factors for protein1 and protein2
    with mda.Writer(output_pdb, multiframe=False, bonds=None, n_atoms=len(u.atoms)) as W:
        W.write(u)  # Write only the last frame, keeping the TER records intact

# Function to aggregate contact maps from multiple trajectories
def aggregate_contacts_and_write_pdb(output_pdb, systems_data):
    aggregated_contact_map = None
    u_ref = None

    for system_data in systems_data:
        traj_dir, pdb_file, xtc_file, group_a_select, group_b_select = system_data
        os.chdir(traj_dir)
        u = mda.Universe(pdb_file, xtc_file)

        # Select the groups for contact analysis
        group_a = u.select_atoms(group_a_select)
        group_b = u.select_atoms(group_b_select)

        # Perform contact analysis on the current trajectory
        _, contact_map = contacts_within_cutoff(u, group_a, group_b, radius=4.5, step=100)

        # Initialize or accumulate the contact maps
        if aggregated_contact_map is None:
            aggregated_contact_map = contact_map
            u_ref = u  # Store a reference to the universe for final PDB writing
        else:
            aggregated_contact_map += contact_map

    # Average the contact map over the number of trajectories
    aggregated_contact_map /= len(systems_data)

    # Write the PDB file with the averaged contact map
    write_complete_pdb_with_bfactors(u_ref, group_a, group_b, aggregated_contact_map, output_pdb)

# Define the directories, PDB, and XTC files for each system
systems_data = [
    ("/home/lbaweja/canonical_nuc1", 'can_sim1.pdb', 'can_final_sim1.xtc', "resid 254:348 or resid 402:488 and not name H*", "resid 744:838 or resid 892:978 and not  name H*"),
    ("/home/lbaweja/canonical_nuc2", 'can_sim2.pdb', 'can_final_sim2.xtc', "resid 254:348 or resid 402:488 and not name H*", "resid 744:838 or resid 892:978 and not  name H*"),
    ("/home/lbaweja/canonical_nuc3", 'can_sim3.pdb', 'can_final_sim3.xtc', "resid 254:348 or resid 402:488 and not name H*", "resid 744:838 or resid 892:978 and not  name H*")
]

# Output PDB with averaged contacts
output_pdb = 'canonical_system_with_averaged_contacts.pdb'
aggregate_contacts_and_write_pdb(output_pdb, systems_data)
