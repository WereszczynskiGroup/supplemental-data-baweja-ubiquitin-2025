import numpy as np
import matplotlib.pyplot as plt
from collections import defaultdict

def parse_pdb(pdb_file):
    residue_contacts = defaultdict(float)  # Store sum of contacts for each residue
    residue_names = {}  # Store residue names
    with open(pdb_file, 'r') as f:
        for line in f:
            if line.startswith("ATOM") or line.startswith("HETATM"):
                res_num = int(line[22:26].strip())
                b_factor = float(line[60:66].strip())  # Contact value stored in B-factor column
                res_name = line[17:20].strip()  # Residue name
                
                # Sum B-factor (contact) for the corresponding residue number
                residue_contacts[res_num] += b_factor
                residue_names[res_num] = res_name  # Store residue name for the residue number
    
    return residue_contacts, residue_names

def filter_residues(residue_contacts, residue_names, region_ranges):
    filtered_residues = {}
    filtered_names = []
    for start, end in region_ranges:
        for res_num in range(start, end + 1):
            if res_num in residue_contacts:
                filtered_residues[res_num] = residue_contacts[res_num]
                filtered_names.append(residue_names[res_num])  # Add residue name to filtered list
            else:
                filtered_residues[res_num] = 0.0  # No contact
                filtered_names.append(residue_names.get(res_num, 'UNK'))  # Add 'UNK' for unknown residues
    return filtered_residues, filtered_names

def generate_contact_map(region1_contacts, region2_contacts):
    contact_map = np.zeros((len(region1_contacts), len(region2_contacts)))

    region1_names = list(region1_contacts.keys())
    region2_names = list(region2_contacts.keys())
    
    for i, res1 in enumerate(region1_names):
        print (region1_names)
        for j, res2 in enumerate(region2_names):
            contact_map[i, j] = region1_contacts[res1] * region2_contacts[res2]
    
    return contact_map, region1_names, region2_names

def plot_contact_maps(contact_maps, region1_names_all, region2_names_all, colors, labels):
    fig, axs = plt.subplots(1, len(contact_maps), figsize=(10, 3), sharey=False)  # Increased figure size
    norm = plt.Normalize(vmin=1, vmax=100)  # Normalizing values for colormap
    cmap = plt.cm.Greens

    for ax, contact_map, region1_names, region2_names, color, label in zip(axs, contact_maps, region1_names_all, region2_names_all, colors, labels):
        x_coords, y_coords, values = [], [], []
        for i in range(contact_map.shape[0]):
            for j in range(contact_map.shape[1]):
                if contact_map[i, j] > 0:
                    x_coords.append(j)
                    y_coords.append(i)
                    values.append(contact_map[i, j])

        hexbin = ax.hexbin(x_coords, y_coords, C=values, gridsize=30, cmap=cmap, norm=norm)
        ax.set_title(label, fontsize=13, fontweight='bold')  # Adjust title font size and weight
         
        twin_ax = ax.twiny()
        twin_ax.set_xlim(ax.get_xlim())
        twin_ax.set_xticks(np.arange(0, len(region2_names), 3))  # Every second residue
        twin_ax.set_xticklabels(region2_names[::3], fontsize=6, rotation=90, fontweight='bold')  # 90-degree rotation for residue names
        twin_ax.xaxis.set_ticks_position('top')
        twin_ax.xaxis.set_label_position('top')

        ax.set_xticks([])  # Remove x-axis ticks
        ax.set_yticks([])  # Remove y-axis ticks

        #ranges = [(0, 10), (10, 19), (19, 29), (29, 32), (56, 68), (68, 76), (76, 104), (104, 111)]
        #ranges = [(0, 10), (10, 19), (19, 29), (29, 32), (32, 33), (33, 34), (34, 52), (52, 60)]
        
        ranges = [(0, 9), (9, 19), (19, 22), (22, 40), (40, 48)]
        region_labels = ['H2A-α1', 'H2A-L1', 'H2A-α2', 'H2B-α2', 'H2B-L2']
        label_positions = [(x + y) / 2 for x, y in ranges]  # Midpoints of ranges
     
        tick_positions = list(set([item for sublist in ranges for item in sublist]))
        tick_spacing_x = 5
        tick_spacing_y = 5
        ax.set_xticks(np.arange(0, len(region2_names), tick_spacing_x))
        #ax.set_yticks(np.arange(0, len(region1_names), tick_spacing_y))

        #ax.set_yticks(tick_positions, labels=None)
        #ax.set_yticklabels([])
        #ax.set_yticks(label_positions, minor=True)
        #ax.set_yticklabels(region_labels, minor=True, fontweight="bold")

        ax.set_yticks(np.arange(0, len(region2_names), 3))  # Every second residue
        ax.set_yticklabels(region2_names[::3], fontsize=6, rotation=0, fontweight='bold')  # 90-degree rotation for residue names
        ax.set_xticks(tick_positions, labels=None)
        ax.set_xticklabels([])
        ax.set_xticks(label_positions, minor=True)
        ax.set_xticklabels(region_labels, minor=True, fontweight="bold", rotation=90)

    plt.subplots_adjust(left=0.1, right=0.9, bottom=0.2)  # Adjust margins

    cbar = fig.colorbar(hexbin, ax=axs, orientation='vertical')
    cbar.set_ticks([1, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100])  # Set ticks to integers
    cbar.set_label('No. of Contacts', fontsize=12)

    plt.savefig("combined_contact_maps.svg", bbox_inches='tight')
    plt.show()

# Define separate region ranges for each system
region1_ranges = {
    "Canonical": [(264, 286), (432, 458)],
    "H2A119ub": [(264, 286), (508, 534)],
    "H2BK120ub": [(465, 487), (1074, 1100)],
}
region2_ranges = {
    "Canonical": [(754, 776), (922, 948)],
    "H2A119ub": [(830, 852), (1074, 1100)],  # Update with actual ranges
    "H2BK120ub": [(830, 852), (143, 169)],  # Update with actual ranges
}

# PDB file paths
pdb_files = {
    "Canonical": 'canonical_withchain_bfac.pdb',       # Replace with actual filenames
    "H2A119ub": 'h2a119_withchain_bfac.pdb',         # Replace with actual filenames
    "H2BK120ub": 'h2bk120_withchain_bfac.pdb',       # Replace with actual filenames
}

contact_maps = []
region1_names_all = []
region2_names_all = []
colors = ['blue', 'orange', 'green']  # Different colors for each system
labels = ['Canonical', 'H2AK119ub', 'H2BK120ub']

for system, pdb_file in pdb_files.items():
    residue_contacts, residue_names = parse_pdb(pdb_file)
    
    # Process first region
    region1_contacts, region1_names = filter_residues(residue_contacts, residue_names, region1_ranges[system])
    
    # Process second region
    region2_contacts, region2_names = filter_residues(residue_contacts, residue_names, region2_ranges[system])

    # Generate contact map
    contact_map, _, _ = generate_contact_map(region1_contacts, region2_contacts)

    contact_maps.append(contact_map)
    region1_names_all.append(region1_names)
    region2_names_all.append(region2_names)

# Plot the contact maps for all systems
plot_contact_maps(contact_maps, region1_names_all, region2_names_all, colors, labels)

