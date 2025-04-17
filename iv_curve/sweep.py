from argparse import ArgumentParser

import numpy as np
from electronic_circuits.circuits import MeasuringCircuit
from electronic_circuits.components import Diode, Resistor

circuit_configuration_dict = {
    "resistor": {
        "component": Resistor(),
        "sweeps": [{"start_v": -5, "stop_v": 5, "num_points": 11}],
    },
    "diode": {
        "component": Diode(),
        "sweeps": [
            {"start_v": 0, "stop_v": 1, "num_points": 100},
            {"start_v": -1, "stop_v": -5, "num_points": 5},
        ],
    },
}


def sweep_voltage(
    circuit: MeasuringCircuit, start_v: float, stop_v: float, num_points: int
) -> np.array:
    voltages = []
    currents = []

    for voltage in np.linspace(start=start_v, stop=stop_v, num=num_points):
        circuit.generator.set_voltage(voltage)

        measured_voltage = circuit.voltmeter.measure()
        measured_current = circuit.ammeter.measure()

        voltages.append(measured_voltage)
        currents.append(measured_current)

    return np.array([voltages, currents])


if __name__ == "__main__":
    # Parse arguments
    parser = ArgumentParser()
    parser.add_argument(
        "--component", type=str, choices=set(circuit_configuration_dict)
    )
    args = parser.parse_args()

    # Configure the circuit
    config = circuit_configuration_dict[args.component]

    component = config["component"]
    circuit = MeasuringCircuit(component)

    # Run the experiment
    results = [
        sweep_voltage(
            circuit,
            start_v=sweep["start_v"],
            stop_v=sweep["stop_v"],
            num_points=sweep["num_points"],
        )
        for sweep in config["sweeps"]
    ]

    # Save results
    output_array = np.concatenate(results, axis=-1)
    print(output_array)
