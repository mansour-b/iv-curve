import numpy as np
from electronic_circuits.circuits import MeasuringCircuit
from electronic_circuits.components import Resistor

component = Resistor()
circuit = MeasuringCircuit(component)


for voltage in np.arange(-5, 6):
    circuit.generator.set_voltage(voltage)

    measured_voltage = circuit.voltmeter.measure()
    measured_current = circuit.ammeter.measure()

    print(measured_voltage, measured_current)
