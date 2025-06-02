import re
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from fpdf import FPDF

# Function to calculate propagated standard error
def propagate_error(errors):
    return np.sqrt(np.sum(np.array(errors)**2))

# Define regex patterns to extract relevant sections and data
pattern_section = re.compile(r"Differences \(Complex - Receptor - Ligand\):\n(.*?)\n\n", re.DOTALL)
pattern_energy = re.compile(r"(VDWAALS|EGB|EEL|ESURF)\s+([-.\d]+)\s+([-.\d]+)\s+([-.\d]+)")

# Initialize lists to hold the extracted data from each file
evdw_means = []
evdw_errors = []
electro_means = []
electro_errors = []
total_means = []
total_errors = []

# List of files (assuming you have 3 files, replace with actual file paths)
files = ["file1.txt", "file2.txt", "file3.txt"]

for file in files:
    with open(file, 'r') as f:
        file_content = f.read()

    # Extract the "Differences" section
    match = re.search(pattern_section, file_content)
    if match:
        section_data = match.group(1)
        
        # Extract energy components
        energies = {}
        for energy_match in re.finditer(pattern_energy, section_data):
            component, avg, std_dev, std_err = energy_match.groups()
            energies[component] = {
                "Average": float(avg),
                "Std. Dev.": float(std_dev),
                "Std. Err. of Mean": float(std_err)
            }
        
        # Calculate Net VDW and Electrostatic energies and their errors
        evdw_avg = energies["VDWAALS"]["Average"] + energies["ESURF"]["Average"]
        evdw_err = propagate_error([energies["VDWAALS"]["Std. Err. of Mean"], energies["ESURF"]["Std. Err. of Mean"]])
        
        electro_avg = energies["EGB"]["Average"] + energies["EEL"]["Average"]
        electro_err = propagate_error([energies["EGB"]["Std. Err. of Mean"], energies["EEL"]["Std. Err. of Mean"]])
        
        total_avg = evdw_avg + electro_avg
        total_err = propagate_error([evdw_err, electro_err])
        
        # Append to the lists
        evdw_means.append(evdw_avg)
        evdw_errors.append(evdw_err)
        electro_means.append(electro_avg)
        electro_errors.append(electro_err)
        total_means.append(total_avg)
        total_errors.append(total_err)

# Convert the data to a DataFrame for easier handling
data = {
    "Evdw Mean": evdw_means,
    "Evdw Error": evdw_errors,
    "Electrostatics Mean": electro_means,
    "Electrostatics Error": electro_errors,
    "Total Energy Mean": total_means,
    "Total Energy Error": total_errors,
}

df = pd.DataFrame(data)

# Calculate overall means and standard errors
final_results = {
    "Evdw": [df["Evdw Mean"].mean(), propagate_error(df["Evdw Error"]) / len(files)],
    "Electrostatics": [df["Electrostatics Mean"].mean(), propagate_error(df["Electrostatics Error"]) / len(files)],
    "Total Energy": [df["Total Energy Mean"].mean(), propagate_error(df["Total Energy Error"]) / len(files)],
}

final_df = pd.DataFrame(final_results, index=["Mean", "Std Error"])

# Generate PDF with the final table
pdf = FPDF()
pdf.add_page()

# Set font for the PDF
pdf.set_font("Arial", size=12)

# Title
pdf.cell(200, 10, txt="Energy Calculation Results", ln=True, align='C')

# Table headers
pdf.cell(60, 10, "Component", border=1)
pdf.cell(60, 10, "Mean", border=1)
pdf.cell(60, 10, "Std Error", border=1)
pdf.ln()

# Table rows
for component, row in final_df.iterrows():
    pdf.cell(60, 10, component, border=1)
    pdf.cell(60, 10, f"{row['Mean']:.4f}", border=1)
    pdf.cell(60, 10, f"{row['Std Error']:.4f}", border=1)
    pdf.ln()

# Save the PDF
pdf.output("energy_results.pdf")

print("PDF generation complete!")

