import numpy as np
from electronic_circuits.circuits import MeasuringCircuit
from electronic_circuits.components import Diode

component = Diode()
# component = ZenerDiode()
# component = TunnelDiode()
# component = SchottkyDiode()
# component = LED()
circuit = MeasuringCircuit(component)

generator = circuit.generator
voltmeter = circuit.voltmeter
ammeter = circuit.ammeter

# Forward
for voltage in np.linspace(0, 1, 100):
    generator.set_voltage(voltage)

    measured_voltage = voltmeter.measure()
    measured_current = ammeter.measure()

    print(measured_voltage, measured_current)

# Backward
for voltage in np.arange(0, -20, step=-1):
    generator.set_voltage(voltage)

    measured_voltage = voltmeter.measure()
    measured_current = ammeter.measure()

    print(measured_voltage, measured_current)
