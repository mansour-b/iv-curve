import json
from pathlib import Path

import numpy as np
from scipy.stats import linregress

from iv_curve.storage import IV_CURVE_PATH, timestamp


def measure_resistance(voltages: np.array, currents: np.array) -> float:
    result = linregress(x=currents, y=voltages)
    return {
        "resistance": result.slope,
        "resistance_std": result.stderr,
        "bias": result.intercept,
        "bias_std": result.stderr,
        "rvalue": result.rvalue,
        "pvalue": result.pvalue,
    }


if __name__ == "__main__":
    sweep_paths = IV_CURVE_PATH.glob("sweep_resistor*")
    analysis_paths = IV_CURVE_PATH.glob("analysis_resistor*")

    already_analysed_timestamps = {timestamp(path) for path in analysis_paths}

    to_be_analysed = [
        path
        for path in sweep_paths
        if timestamp(path) not in already_analysed_timestamps
    ]

    print(f"Found {len(to_be_analysed)} file(s) to be analysed:")
    for path in to_be_analysed:
        print(f"    - {path.stem}")

    print("Fitting...")
    for path in to_be_analysed:
        voltages, currents = np.loadtxt(path)
        output_dict = measure_resistance(voltages, currents)

        output_path = (
            IV_CURVE_PATH / f"analysis_resistor_{timestamp(path)}.json"
        )

        with Path.open(output_path, "w") as f:
            json.dump(output_dict, f, indent=2)
    print("Done!")
