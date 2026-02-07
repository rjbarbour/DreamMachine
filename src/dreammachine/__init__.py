"""DreamMachine: High-performance spiking neural network simulator.

A biomimetic SNN framework implementing Izhikevich neurons with STDP plasticity.
Designed for computational neuroscience research and Hebbian learning experiments.
"""

from dreammachine.neurons.izhikevich import IzhikevichPopulation, NeuronType
from dreammachine.plasticity.stdp import STDPSynapses, STDPParams
from dreammachine.network.simulator import NetworkSimulator, SimulationResult

__version__ = "0.1.0"
__all__ = [
    "IzhikevichPopulation",
    "NeuronType",
    "STDPSynapses",
    "STDPParams",
    "NetworkSimulator",
    "SimulationResult",
]
