# %%
# Imports
import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

from iv_curve.storage import IV_CURVE_PATH, timestamp

# %%
# Display list of available sweeps
sweep_paths = list(IV_CURVE_PATH.glob("sweep_resistor*txt"))
print("Available sweeps:")
for path in sweep_paths:
    print(f"  - {path.stem}")

# %%
# Load the data
path = sweep_paths[0]

component_type = path.stem.split("_")[1]
voltages, currents = np.loadtxt(path)

# %%
# Load the measured parameters of the resistor
analysis_path = path.parent / f"analysis_resistor_{timestamp(path)}.json"
with Path.open(analysis_path) as f:
    measure_dict = json.load(f)
resistance = measure_dict["resistance"]
resistance_std = measure_dict["resistance_std"]
bias = measure_dict["bias"]
bias_std = measure_dict["bias_std"]

# %%
# Useful parameters for clean plot

min_v = min(voltages)
max_v = max(voltages)
amp_v = max_v - min_v

min_x = min_v - 0.1 * amp_v
max_x = max_v + 0.1 * amp_v
plot_x_limits = [min_x, max_x]
abscissa = np.arange(min_x, max_x)

min_c = min(currents)
max_c = max(currents)
amp_c = max_c - min_c
plot_y_limits = [min_c - 0.1 * amp_c, max_c + 0.1 * amp_c]

# %%
# Plot the measurements
plt.errorbar(voltages, currents, yerr=5e-4 * np.ones(len(currents)), fmt="o")

# Plot the regression
plt.plot(abscissa, (abscissa - bias) / resistance, zorder=0)
plt.fill_between(
    abscissa,
    y1=(abscissa - bias) / (resistance - resistance_std),
    y2=(abscissa - bias) / (resistance + resistance_std),
    zorder=0,
    alpha=0.5,
    color="tab:orange",
)

# Configure display
plt.title(f"I-C curve of the resistor (R = {resistance:.1f})")
plt.xlabel("Voltage (V)")
plt.ylabel("Current (A)")
plt.xlim(plot_x_limits)
plt.ylim(plot_y_limits)

# Tell python to show the figure
plt.show()

# %%
