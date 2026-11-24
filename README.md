# DreamMachine

**Spiking neural network simulator with Izhikevich neurons and STDP plasticity (early prototype)**

A biomimetic SNN framework intended for computational neuroscience research, Hebbian learning experiments, and as groundwork for simulating biological neural circuits like *Aplysia californica*.

> **Status: prototype.** The current code runs and is tested, but it does not yet
> replicate Izhikevich's reference network (no conduction delays, no inhibitory
> population) and it is not yet fast. See [docs/plan.md](docs/plan.md) for the audit,
> the revised milestones and the measured baseline. Work is tracked in `backlog/`
> ([Backlog.md](https://backlog.md), run `backlog board`).

## Features

- **Izhikevich Neuron Model**: 2-variable model with seven preset neuron types
- **STDP Plasticity**: Trace-based pair STDP with weight bounds
- **Computation**: NumPy, with the neuron update compiled by Numba (the plasticity and simulation loops are still Python)
- **Sparse Connectivity**: CSR weight matrix
- **Modular layout**: separate neuron, plasticity and simulator modules

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

Measured on 2026-11-24 in a 4-vCPU cloud container (Intel Xeon 2.1 GHz, 15 GB RAM),
Python 3.13, Numba 0.68, `dt = 0.5 ms`, no conduction delays:

| Network size | Synapses | Model time | Wall time | Realtime factor |
|--------------|----------|------------|-----------|-----------------|
| 1,000 neurons | 100,000 | 1.0 s | 4.4 s | 0.23x |

This is a single unrepeated run, recorded as the baseline to improve on. An earlier
version of this table contained estimates that had not been measured; they have been
removed. The performance target and method are in [docs/plan.md](docs/plan.md).

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

See [docs/plan.md](docs/plan.md). In short: replicate Izhikevich's reference network
correctly first, then make it fast on CPU, then add the plasticity rules that
Aplysia learning needs, then the Aplysia reflex circuit. GPU work is deferred until
a measured need exists.

## References

1. Izhikevich, E.M. (2003). "Simple model of spiking neurons." *IEEE Trans. Neural Networks*, 14(6):1569-1572.
2. Bi, G. & Poo, M. (1998). "Synaptic modifications in cultured hippocampal neurons." *J. Neurosci.*, 18:10464-10472.
3. Kandel, E.R. (2001). "The molecular biology of memory storage." *Science*, 294:1030-1038.

## License

MIT License
