import matplotlib.pyplot as plt
import numpy as np

# Rearranged file paths for each system in the desired order
files = {
    "Canonical": {
        "side1_sim1": "dimer1_can.unwrap_side1_sim1",
        "side2_sim1": "dimer1_can.unwrap_side2_sim1",
        "side1_sim2": "dimer1_can.unwrap_side1_sim2",
        "side2_sim2": "dimer1_can.unwrap_side2_sim2",
        "side1_sim3": "dimer1_can.unwrap_side1_sim3",
        "side2_sim3": "dimer1_can.unwrap_side2_sim3",
    },
    "H2AK119ub": {
        "side1_sim1": "dimer1_h2a.unwrap_side1_sim1",
        "side2_sim1": "dimer1_h2a.unwrap_side2_sim1",
        "side1_sim2": "dimer1_h2a.unwrap_side1_sim2",
        "side2_sim2": "dimer1_h2a.unwrap_side2_sim2",
        "side1_sim3": "dimer1_h2a.unwrap_side1_sim3",
        "side2_sim3": "dimer1_h2a.unwrap_side2_sim3",
    },
    "H2BK120ub": {
        "side1_sim1": "dimer1_h2b.unwrap_side1_sim1",
        "side2_sim1": "dimer1_h2b.unwrap_side2_sim1",
        "side1_sim2": "dimer1_h2b.unwrap_side1_sim2",
        "side2_sim2": "dimer1_h2b.unwrap_side2_sim2",
        "side1_sim3": "dimer1_h2b.unwrap_side1_sim3",
        "side2_sim3": "dimer1_h2b.unwrap_side2_sim3",
    }
}

# Color scheme for each simulation
colors = {
    "Run 1": 'blue',
    "Run 2": 'orange',
    "Run 3": 'green',
}

# Function to read data from a file (time, base pairs unwrapped)
def read_data(file):
    data = np.loadtxt(file)
    time = data[:, 0]
    unwrapped = data[:, 1]
    
    # Filter time and unwrapped data to include only time <= 2 * 10^6
    valid_indices = time <= 2e6  # time threshold of 2 * 10^6 ps
    time = time[valid_indices]
    unwrapped = unwrapped[valid_indices]
    
    return time, unwrapped

# Plotting function
def plot_system_data(ax, system_name, data, side, title):
    ax.set_title(title, fontsize=14)
    ax.set_xlabel("Time (µs)", fontsize=12)  # Update label to show microseconds
    ax.set_ylabel("DNA Base Pairs", fontsize=12)
    
    # Plot each simulation for the given side
    for run_num, (sim_key, file) in enumerate(data.items()):
        time, unwrapped = read_data(file)
        time_in_us = time / 1e6  # Convert time to microseconds (divide by 1000)
        run_label = f"Run {run_num + 1}"
        ax.plot(time_in_us, unwrapped, label=run_label, color=colors[f"Run {run_num + 1}"], linestyle='-')
    
    ax.legend(fontsize=14)
    ax.set_xlim(0.0, 2.0)

# Create figure and axes (1 row, 6 columns: 2 per system)
fig, axes = plt.subplots(3, 2, figsize=(12, 9), sharey=True)

# Plot data for each system (one row per system)
for idx, (system_name, system_data) in enumerate(files.items()):
    # Plot for side1 and side2
    plot_system_data(axes[idx, 0], system_name, {key: system_data[key] for key in system_data if 'side1' in key}, side="side1", title=f"{system_name} - DNA-entry")
    plot_system_data(axes[idx, 1], system_name, {key: system_data[key] for key in system_data if 'side2' in key}, side="side2", title=f"{system_name} - DNA-exit")

# Adjust layout
plt.tight_layout()
plt.savefig("dna_unwrapping.pdf")
plt.show()
