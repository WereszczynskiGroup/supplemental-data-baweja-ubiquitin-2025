import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# File details
files_dimer1 = {
    'Canonical': ['dimer1_can.helix_sim1', 'dimer1_can.helix_sim2', 'dimer1_can.helix_sim3'],
    'H2AK119ub': ['dimer1_h2a.helix_sim1', 'dimer1_h2a.helix_sim2', 'dimer1_h2a.helix_sim3'],
    'H2BK120ub': ['dimer2_h2b.helix_sim1', 'dimer2_h2b.helix_sim2', 'dimer2_h2b.helix_sim3']
}
files_dimer2 = {
    'Canonical': ['dimer2_can.helix_sim1', 'dimer2_can.helix_sim2', 'dimer2_can.helix_sim3'],
    'H2AK119ub': ['dimer2_h2a.helix_sim1', 'dimer2_h2a.helix_sim2', 'dimer2_h2a.helix_sim3'],
    'H2BK120ub': ['dimer1_h2b.helix_sim1', 'dimer1_h2b.helix_sim2', 'dimer1_h2b.helix_sim3']
}

# Colors for each system
colors = {'Canonical': 'red', 'H2AK119ub': 'black', 'H2BK120ub': 'blue'}

# Function to read second column (angles) from files, skipping non-numeric rows
def read_data(files):
    all_angles = []
    for file in files:
        with open(file, 'r') as f:
            lines = f.readlines()[500:2000]  # Read only lines 501 to 2000
            angles = []
            for line in lines:
                try:
                    # Split the line and extract the second column (angles)
                    angle = float(line.split()[1])
                    angles.append(angle)
                except (IndexError, ValueError):
                    # Skip the line if it's malformed or non-numeric
                    continue
            all_angles.append(np.array(angles))
    return all_angles  # Return list of arrays, each corresponding to a file

# Function to plot smooth KDE curves using Seaborn and add mean and SEM to legend
def plot_distributions(ax, data, label, color):
    # Concatenate all angle data across files
    concatenated_data = np.concatenate(data)
    
    # Calculate mean and standard error of the mean (SEM)
    mean_val = np.mean(concatenated_data)
    std_val = np.std(concatenated_data)
    sem_val = std_val / np.sqrt(len(concatenated_data))
    
    # Plot KDE using seaborn
    sns.kdeplot(concatenated_data, ax=ax, color=color, fill=True, label=f'{label} ({mean_val:.2f} ± {sem_val:.2f})', linewidth=2)

# Create subplots for dimer1 and dimer2
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 6))

# Plot dimer1 (DNA entry side dimer)
for system, files in files_dimer1.items():
    data = read_data(files)
    plot_distributions(ax1, data, system, colors[system])

ax1.set_title('DNA Entry Side Dimer', fontsize=14)
ax1.set_xlabel('H2A-Dyad axis angle θ (°)', fontsize=14, fontweight='bold')  # Bold x-axis label
ax1.set_ylabel('Probability Density', fontsize=14, fontweight='bold')  # Bold y-axis label
ax1.set_xlim(25.0, 45.0)  # Set x-axis limits
ax1.legend(fontsize=12, loc='upper left')  # Place legend in upper left with font size 12
#ax1.text(25.5, 0.05, '(a)', fontsize=14, fontweight='bold')  # Label subplot

# Plot dimer2 (DNA exit side AT-rich dimer)
for system, files in files_dimer2.items():
    data = read_data(files)
    plot_distributions(ax2, data, system, colors[system])

ax2.set_title('DNA Exit Side Dimer', fontsize=14)
ax2.set_xlabel('H2A-Dyad axis angle θ (°)', fontsize=14, fontweight='bold')  # Bold x-axis label
ax2.set_ylabel('Probability Density', fontsize=14, fontweight='bold')  # Bold y-axis label
ax2.set_xlim(25.0, 45.0)  # Set x-axis limits
ax2.legend(fontsize=12, loc='upper left')  # Place legend in upper left with font size 12
#ax2.text(25.5, 0.05, '(b)', fontsize=12, fontweight='bold')  # Label subplot
ax1.tick_params(axis='both', labelsize=12)
ax2.tick_params(axis='both', labelsize=12)
# Adjust layout
plt.tight_layout(pad=1.0)  # Adjust padding to compress the plot
plt.savefig('dimer_probability_distributions.pdf', format='pdf')
plt.show()
