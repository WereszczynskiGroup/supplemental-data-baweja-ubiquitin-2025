# calculate_kcl_ions.py

# Constants
AVOGADRO = 6.022e23       # mol⁻¹
MOLARITY = 0.15            # mol/L
ANGSTROM3_TO_LITERS = 1e-27  # conversion factor

# Input: final box volume in Å³
# Replace this with your actual volume from LEaP or cpptraj output
final_volume_angstrom3 = 4801601.89  # Example volume

# Convert volume to liters
volume_liters = final_volume_angstrom3 * ANGSTROM3_TO_LITERS

# Calculate number of ions
num_ions = int(MOLARITY * AVOGADRO * volume_liters)

print(f"Final volume: {final_volume_angstrom3:.2e} Å³")
print(f"Volume in liters: {volume_liters:.3e} L")
print(f"To achieve 0.15 M KCl, add:")
print(f"  K+ ions : {num_ions}")
print(f"  Cl- ions: {num_ions}")
