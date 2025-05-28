#!/bin/python
import os
import MDAnalysis as mda
import numpy as np

def vector_between_residues(atomgroup, res1, res2):
    """
    Calculate the vector between two residues.
    """
    pos1 = atomgroup.select_atoms(f"resid {res1}").center_of_mass()
    pos2 = atomgroup.select_atoms(f"resid {res2}").center_of_mass()
    return pos2 - pos1


def super_helical(atomgroup, res1, res2):
    """
    Calculate the vector between two residues.
    """
    pos1 = atomgroup.select_atoms(f"{res1}").center_of_mass()
    pos2 = atomgroup.select_atoms(f"{res2}").center_of_mass()
    return pos2 - pos1


def calculate_angle(vector1, vector2):
    """
    Calculate the angle between two vectors.
    """
    cos_theta = np.dot(vector1, vector2) / (np.linalg.norm(vector1) * np.linalg.norm(vector2))
    angle = np.arccos(np.clip(cos_theta, -1.0, 1.0))
    return np.degrees(angle)

for i in range(1, 4):
    new_directory="/home/lbaweja/canonical_nuc"+str(i)
    os.chdir(new_directory)
    u = mda.Universe('can_sim' +str(i)+".pdb", "can_final_sim"+str(i)+".xtc")
    H3_1_2 = "resid 86:114 or resid 576:604"
    DNA_resid = "resid 1201 or resid 1054"
    H2A_1_start = 282
    H2A_1_end = 310
    H2A_2_start = 772
    H2A_2_end = 800

    with open('dimer1_can.helix_'+'sim'+str(i), 'w') as f:
        for ts in u.trajectory[::100]:
            vector1 = super_helical(u.atoms, H3_1_2, DNA_resid)
            vector2 = vector_between_residues(u.atoms, H2A_1_start, H2A_1_end)
            angle = calculate_angle(vector1, vector2)
            f.write(f"{ts.time}\t{angle}\n")

    with open('dimer2_can.helix_'+'sim'+str(i), 'w') as f:
        for ts in u.trajectory[::100]:
            vector1 = super_helical(u.atoms, H3_1_2, DNA_resid)
            vector2 = vector_between_residues(u.atoms, H2A_2_start, H2A_2_end)
            angle = calculate_angle(vector1, vector2)
            f.write(f"{ts.time}\t{angle}\n")









