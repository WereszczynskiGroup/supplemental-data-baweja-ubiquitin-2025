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

def calculate_perpendicular_axis(atomgroup, H3_resid, DNA_resid):
    """
    Calculate the perpendicular axis to the plane defined by the vectors between the H3 residues and DNA.
    """
    # Split H3 into two parts
    pos_H3_1 = atomgroup.select_atoms("resid 86:114").center_of_mass()
    pos_H3_2 = atomgroup.select_atoms("resid 652:680").center_of_mass()
    
    # DNA COM
    pos_DNA = atomgroup.select_atoms(f"{DNA_resid}").center_of_mass()
    
    # Vector between two H3 parts and DNA
    vector_H3 = pos_H3_2 - pos_H3_1
    vector_DNA = pos_DNA - pos_H3_1
    
    # Cross product to get the perpendicular axis
    perpendicular_axis = np.cross(vector_H3, vector_DNA)
    return perpendicular_axis

def calculate_angle(vector1, vector2):
    """
    Calculate the angle between two vectors.
    """
    cos_theta = np.dot(vector1, vector2) / (np.linalg.norm(vector1) * np.linalg.norm(vector2))
    angle = np.arccos(np.clip(cos_theta, -1.0, 1.0))
    return np.degrees(angle)

def calculate_COM(atomgroup, res1, res2):
    """
    Calculate the center of mass of a base pair using the C1' atoms from each residue.
    """
    pos1 = atomgroup.select_atoms(f"resid {res1} and name C1'").center_of_mass()
    pos2 = atomgroup.select_atoms(f"resid {res2} and name C1'").center_of_mass()
    return (pos1 + pos2) / 2

def calculate_radial_distance(COM, nucleosome_axis_vector, nucleosome_point):
    """
    Calculate the radial distance from the COM of the base pair to the nucleosome axis.
    """
    vector_from_axis = COM - nucleosome_point  # Vector from axis to COM
    projection_on_axis = np.dot(vector_from_axis, nucleosome_axis_vector) * nucleosome_axis_vector
    radial_vector = vector_from_axis - projection_on_axis
    return np.linalg.norm(radial_vector)  # Radial distance

# Threshold for unwrapping (in Ångstroms)
threshold_radius = 7.0

for i in range(1, 4):
    new_directory = "/home/lbaweja/canonical_nuc" + str(i)
    os.chdir(new_directory)
    
    u = mda.Universe('can_sim' + str(i) + ".pdb", "can_final_sim" + str(i) + ".xtc")
    
    H3_1_2 = "resid 86:114 or resid 576:604"  # H3 residues for nucleosome axis
    DNA_resid = "resid 1201 or resid 1054"    # DNA residues for axis definition
    
    # DNA base pair residue ranges for both strands
    strand1_residues = list(range(981, 1054))  # First strand
    strand2_residues = list(range(1274, 1201, -1))  # Complementary strand (reverse order)
    strand3_residues = list(range(1127, 1054, -1))  # First strand
    strand4_residues = list(range(1128, 1201))  # Complementary strand (reverse order)
    # Calculate the superhelical axis using the cross product (perpendicular to the H3-DNA plane)
    nucleosome_axis_vector = calculate_perpendicular_axis(u.atoms, H3_1_2, DNA_resid)
    nucleosome_axis_vector /= np.linalg.norm(nucleosome_axis_vector)  # Normalize
    
    nucleosome_point = u.atoms.select_atoms(f"resid 86:114").center_of_mass()  # A point on the nucleosome axis
    
    with open('dimer1_can.unwrap_'+'side1_sim'+str(i), 'w') as f:
        for ts in u.trajectory[::100]:
            wrapped_bp_count = 0
            total_bp = len(strand1_residues)
            
            # Iterate through base pairs
            for res1, res2 in zip(strand1_residues, strand2_residues):
                # Calculate the COM of the base pair
                COM_bp = calculate_COM(u.atoms, res1, res2)
                
                # Calculate radial distance from nucleosome axis
                radial_distance = calculate_radial_distance(COM_bp, nucleosome_axis_vector, nucleosome_point)
                
                # Check if the base pair is wrapped or unwrapped
                if radial_distance <= threshold_radius:
                    wrapped_bp_count += 1
            
            unwrapped_bp_count = total_bp - wrapped_bp_count
            f.write(f"{ts.time}\t{wrapped_bp_count}\t{unwrapped_bp_count}\n")
    
    with open('dimer1_can.unwrap_'+'side2_sim'+str(i), 'w') as f:
        for ts in u.trajectory[::100]:
            wrapped_bp_count = 0
            total_bp = len(strand1_residues)
            
            # Iterate through base pairs
            for res1, res2 in zip(strand3_residues, strand4_residues):
                # Calculate the COM of the base pair
                COM_bp = calculate_COM(u.atoms, res1, res2)
                
                # Calculate radial distance from nucleosome axis
                radial_distance = calculate_radial_distance(COM_bp, nucleosome_axis_vector, nucleosome_point)
                
                # Check if the base pair is wrapped or unwrapped
                if radial_distance <= threshold_radius:
                    wrapped_bp_count += 1
            
            unwrapped_bp_count = total_bp - wrapped_bp_count
            f.write(f"{ts.time}\t{wrapped_bp_count}\t{unwrapped_bp_count}\n")
