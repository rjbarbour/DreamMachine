# DreamMachine

**High-performance spiking neural network simulator with Izhikevich neurons and STDP plasticity**

A biomimetic SNN framework designed for computational neuroscience research, Hebbian learning experiments, and as groundwork for simulating biological neural circuits like *Aplysia californica*.

## Features

- **Izhikevich Neuron Model**: Efficient 2-variable model reproducing 20+ firing patterns
- **STDP Plasticity**: Trace-based spike-timing-dependent plasticity with O(1) complexity per spike
- **Vectorized Computation**: NumPy + Numba JIT for near-native performance
- **Sparse Connectivity**: Memory-efficient CSR matrices for large-scale networks
- **Modular Architecture**: Extensible design for custom neuron and plasticity models

## Installation

```bash
# Clone repository
git clone https://github.com/rjbarbour/DreamMachine.git
cd DreamMachine

# Install in development mode
pip install -e ".[all]"
```

## Quick Start

```python
from dreammachine import (
    IzhikevichPopulation,
    NeuronType,
    NetworkSimulator,
)
from dreammachine.network.simulator import create_network
import numpy as np

# Create a 100-neuron network with 10% connectivity
neurons, synapses, sim = create_network(
    n_neurons=100,
    neuron_type=NeuronType.RS,  # Regular Spiking
    connectivity_density=0.1,
)

# Define external input (drive first 20 neurons)
def external_input(t):
    I = np.zeros(100, dtype=np.float32)
    I[:20] = 15.0
    return I

# Run 1 second simulation
result = sim.run(1000.0, dt=0.5, I_ext=external_input)

print(f"Total spikes: {result.n_spikes}")
print(f"Mean firing rate: {result.mean_firing_rate:.1f} Hz")
```

## Neuron Types

| Type | Description | Use Case |
|------|-------------|----------|
| RS | Regular Spiking | Excitatory pyramidal neurons |
| FS | Fast Spiking | Inhibitory interneurons |
| IB | Intrinsically Bursting | Layer 5 pyramidal |
| CH | Chattering | Fast rhythmic bursting |
| LTS | Low-Threshold Spiking | Inhibitory interneurons |
| TC | Thalamocortical | Thalamic relay neurons |
| RZ | Resonator | Subthreshold oscillations |

## STDP Learning

The simulator implements exponential STDP:

```
Δw = A+ × exp(-Δt/τ+)  if pre fires before post (LTP)
Δw = A- × exp(Δt/τ-)   if post fires before pre (LTD)
```

Configure via `STDPParams`:

```python
from dreammachine import STDPParams

params = STDPParams(
    tau_plus=20.0,   # LTP time constant (ms)
    tau_minus=20.0,  # LTD time constant (ms)
    A_plus=0.01,     # LTP amplitude
    A_minus=-0.012,  # LTD amplitude
    w_min=0.0,       # Weight bounds
    w_max=1.0,
)
```

## Performance

Benchmark on typical hardware (Intel i7, 16GB RAM):

| Network Size | Synapses | 100ms Simulation | Realtime Factor |
|--------------|----------|------------------|-----------------|
| 100 neurons  | 1,000    | ~5ms            | 20x             |
| 1,000 neurons| 10,000   | ~50ms           | 2x              |
| 10,000 neurons| 100,000 | ~500ms          | 0.2x            |

Performance scales linearly with neuron count and synapse count.

## Project Structure

```
DreamMachine/
├── docs/
│   ├── spec.md           # Requirements specification
│   └── architecture.md   # System design
├── src/dreammachine/
│   ├── neurons/          # Neuron models
│   ├── plasticity/       # STDP and learning rules
│   └── network/          # Simulation engine
├── tests/                # pytest test suite
└── examples/             # Usage examples
```

## Running Tests

```bash
pytest tests/ -v
```

## Roadmap

1. **Phase 1** (Current): Core Izhikevich + STDP
2. **Phase 2**: GPU acceleration (CuPy/CUDA)
3. **Phase 3**: Aplysia gill-withdrawal circuit model
4. **Phase 4**: Kandel's learning experiments *in silico*

## References

1. Izhikevich, E.M. (2003). "Simple model of spiking neurons." *IEEE Trans. Neural Networks*, 14(6):1569-1572.
2. Bi, G. & Poo, M. (1998). "Synaptic modifications in cultured hippocampal neurons." *J. Neurosci.*, 18:10464-10472.
3. Kandel, E.R. (2001). "The molecular biology of memory storage." *Science*, 294:1030-1038.

## License

MIT License
