# Useful additional packages
import matplotlib.pyplot as plt
import numpy as np
from math import pi
from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister, transpile
from qiskit.tools.visualization import circuit_drawer
from qiskit.quantum_info import state_fidelity, Pauli, Operator
from qiskit import Aer
from qiskit.visualization import plot_histogram


# %%

backend = Aer.get_backend('statevector_simulator')

quantum_registers = QuantumRegister(2, name='q')

classical_registers = ClassicalRegister(2, name='c')

XX = Operator(Pauli(label='XX'))

# Create a Quantum Circuit acting on the q register
circuit = QuantumCircuit(quantum_registers, classical_registers)
# In Qiskit we give you access to the general unitary using the 𝑢3 gate
#circuit.u(pi / 2, pi / 2, pi / 2, q)
circuit.append(XX, quantum_registers)
circuit.measure(quantum_registers, classical_registers)

circuit.draw('mpl')
plt.show()

# %%
job = backend.run(transpile(circuit, backend))
result = job.result()

# %%

# Plot a histogram
plot_histogram(result)
plt.show()

print("\nresult:\n", result)
