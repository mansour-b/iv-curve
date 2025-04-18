# %%
# Imports
import matplotlib.pyplot as plt
import numpy as np

from iv_curve.storage import IV_CURVE_PATH

# %%
# Display list of available sweeps
sweep_paths = list(IV_CURVE_PATH.glob("*txt"))
print("Available sweeps:")
for path in sweep_paths:
    print(f"  - {path.stem}")

# %%
# Load the data
path = sweep_paths[0]

component_type = path.stem.split("_")[1]
voltages, currents = np.loadtxt(path)

# %%
# Plot the measurements
plt.errorbar(voltages, currents, yerr=5e-4 * np.ones(len(currents)), fmt="o")

# Configure display
plt.title(f"I-C curve of the {component_type}")
plt.xlabel("Voltage (V)")
plt.ylabel("Current (A)")

# Tell python to show the figure
plt.show()

# %%
