from qiskit import Aer
from qiskit_nature.drivers import UnitsType, Molecule
from qiskit_nature.drivers.second_quantization import (
    ElectronicStructureDriverType,
    ElectronicStructureMoleculeDriver,
)
from qiskit_nature.problems.second_quantization import ElectronicStructureProblem
from qiskit_nature.converters.second_quantization import QubitConverter
from qiskit_nature.mappers.second_quantization import JordanWignerMapper, ParityMapper
from qiskit.algorithms import NumPyMinimumEigensolver
from qiskit.providers.aer import StatevectorSimulator
from qiskit import Aer
from qiskit.utils import QuantumInstance
from qiskit_nature.algorithms import VQEUCCFactory
from qiskit.algorithms import VQE
from qiskit.circuit.library import TwoLocal
from qiskit_nature.algorithms import GroundStateEigensolver
from qiskit_nature.drivers.second_quantization import GaussianForcesDriver
from qiskit_nature.algorithms import NumPyMinimumEigensolverFactory
from qiskit_nature.problems.second_quantization import VibrationalStructureProblem
from qiskit_nature.mappers.second_quantization import DirectMapper

molecule = Molecule(
    geometry=[["H", [0.0, 0.0, 0.0]], ["H", [0.0, 0.0, 0.735]]], charge=0, multiplicity=1
)
driver = ElectronicStructureMoleculeDriver(
    molecule, basis="sto3g", driver_type=ElectronicStructureDriverType.PYSCF
)

# %%

es_problem = ElectronicStructureProblem(driver)
#qubit_converter = QubitConverter(JordanWignerMapper())
qubit_converter = QubitConverter(mapper=ParityMapper(), two_qubit_reduction=True)

numpy_solver = NumPyMinimumEigensolver()

quantum_instance = QuantumInstance(backend=Aer.get_backend("aer_simulator_statevector"))
vqe_solver = VQEUCCFactory(quantum_instance)

tl_circuit = TwoLocal(
    rotation_blocks=["h", "rx"],
    entanglement_blocks="cz",
    entanglement="full",
    reps=2,
    parameter_prefix="y",
)

another_solver = VQE(
    ansatz=tl_circuit,
    quantum_instance=QuantumInstance(Aer.get_backend("aer_simulator_statevector")),
)


calc = GroundStateEigensolver(qubit_converter, vqe_solver)
res = calc.solve(es_problem)

print(res)

calc = GroundStateEigensolver(qubit_converter, numpy_solver)
res = calc.solve(es_problem)
print(res)

driver = GaussianForcesDriver(logfile="aux_files/CO2_freq_B3LYP_631g.log")

vib_problem = VibrationalStructureProblem(driver, num_modals=2, truncation_order=2)

qubit_covnerter = QubitConverter(DirectMapper())

solver_without_filter = NumPyMinimumEigensolverFactory(use_default_filter_criterion=False)
solver_with_filter = NumPyMinimumEigensolverFactory(use_default_filter_criterion=True)

gsc_wo = GroundStateEigensolver(qubit_converter, solver_without_filter)
result_wo = gsc_wo.solve(vib_problem)

gsc_w = GroundStateEigensolver(qubit_converter, solver_with_filter)
result_w = gsc_w.solve(vib_problem)

print(result_wo)
print("\n\n")
print(result_w)