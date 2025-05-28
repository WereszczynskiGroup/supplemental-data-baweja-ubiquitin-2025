import os
import matplotlib.pyplot as plt

# Function to read RMSD data and skip header lines starting with #
def read_rmsd_data(folder, file_name):
    file_path = os.path.join(folder, file_name)
    time, rmsd = [], []
    try:
        with open(file_path, 'r') as f:
            for line in f:
                if line.startswith('#'):  # Skip header lines
                    continue
                if line.strip():
                    t, r = map(float, line.split())
                    time.append(t / 5000)  # Convert time to microseconds
                    rmsd.append(r)
    except FileNotFoundError:
        print(f'File not found: {file_path}')
    return time, rmsd

# Define folder names and filenames
folders = ['h2ak119ub', 'h2bk120ub']  # Folders for the two systems
systems = ['ubq1', 'ubq2']  # Filenames prefixes for the two systems
dimers = ['ubq1', 'ubq2']  # Dimers to iterate over
copies = ['1', '2', '3']  # Run copies

# Set up figure with 2x2 subplots, sharing x-axis between rows
fig, axs = plt.subplots(2, 2, figsize=(8, 6), sharex=True)

# Labels for subplots
labels = ['(a)', '(b)', '(c)', '(d)']

# Initialize a list to hold labels for the legend (for the first subsystem only)
legend_labels = []

# Plotting RMSD data for each system
for i, folder in enumerate(folders):  # Loop over folder (system) indices
    for j, dimer in enumerate(dimers):  # Loop over dimer indices
        ax = axs[i, j]
        
        # Aggregate data from the 3 copies for each folder and dimer
        for copy_num in copies:
            # Construct file name correctly for each system and copy
            file_name = f'rmsd_core_aligned_ubq{copy_num}.{dimers[j]}'
            print(folder, file_name)
            time, rmsd_data = read_rmsd_data(folder, file_name)
            if time and rmsd_data:  # Ensure data was read successfully
                ax.plot(time, rmsd_data, label=f'Run {copy_num}')
                
                # Collect legend labels only for the first subsystem (h2a119)
                if folder == 'h2a119':
                    legend_labels.append(f'Run {copy_num}')
        
        # Customize plot
        ax.set_ylim(0, 60)  # Set y limits
        ax.set_xlim(0, 2)  # Set x limits
        ax.text(0.1, 0.9, labels[i * 2 + j], transform=ax.transAxes, fontsize=14, fontweight='bold')
        
        # Set axis labels with bold font
        ax.set_ylabel('RMSD (Å)', fontsize=12, fontweight='bold')

# Set x-axis label for the bottom row
axs[1, 0].set_xlabel('Time (µs)', fontsize=12, fontweight='bold')

# Create a single legend for the first subsystem (h2a119), outside the plot area
axs[0, 0].legend(legend_labels, fontsize=10, loc='upper left', frameon=False, title='Runs', title_fontsize='10', bbox_to_anchor=(1, 1))

# Overall title
# plt.suptitle('RMSD of Ubiquitin1 and Ubiquitin2 in H2A119 and H2BK120 Systems', fontsize=16, fontweight='bold')

# Adjust layout to make room for the legend
plt.subplots_adjust(right=0.75)

# Save the plot as a PDF with tight layout
plt.savefig('Figure2_rmsd.pdf', format='pdf', dpi=300, bbox_inches='tight')

# Display the plot
plt.show()
