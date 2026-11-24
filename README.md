# DreamMachine

**Spiking neural network simulator with Izhikevich neurons and STDP plasticity (early prototype)**

A biomimetic SNN framework intended for computational neuroscience research, Hebbian learning experiments, and as groundwork for simulating biological neural circuits like *Aplysia californica*.

> **Status: early research code.** `dreammachine.spnet` is a replication of
> Izhikevich's `spnet.m` (800 excitatory and 200 inhibitory neurons, 100 synapses
> per neuron, 1-20 ms delays, STDP with once-a-second weight updates). A compiled
> kernel is bit-identical to a plain NumPy transcription and was cross-checked
> against the original `spnet.m` under Octave
> ([docs/validation/crosscheck-original.md](docs/validation/crosscheck-original.md));
> long-run statistics are in
> [docs/validation/spnet-statistics.md](docs/validation/spnet-statistics.md).
> The older modules (`neurons`, `plasticity`, `network`) are a legacy prototype and
> do not implement that model. Nothing for Aplysia exists yet. See
> [docs/plan.md](docs/plan.md) for the milestones. Work is tracked in `backlog/`
> ([Backlog.md](https://backlog.md), run `backlog board`).

## Features

- **`dreammachine.spnet`**: replication of `spnet.m` with per-synapse conduction delays, an inhibitory population, and STDP through a decaying weight derivative.
- **Oracle and kernel**: `run_oracle` (slow, obviously correct) and `run_kernel` (Numba) agree spike for spike; see [docs/testing.md](docs/testing.md).
- **Own random numbers**: networks and inputs come from `numpy.random.Generator`, not MATLAB's stream.
- **Legacy prototype**: single-population Izhikevich network with pair STDP (`dreammachine.network`), kept for reference only.

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
import numpy as np
from dreammachine.spnet import SpnetParams, build_network, make_inputs, run_kernel

params = SpnetParams()                      # 800 exc + 200 inh, M=100, D=20
rng = np.random.default_rng(1)
net = build_network(params, rng)
inputs = make_inputs(params, 10, rng)       # 10 s of model time
res = run_kernel(net, inputs, params)       # first call includes JIT compilation

print(f"spikes: {res.spike_time.size}")
print(f"mean weight (exc): {res.s[:params.Ne].mean():.2f}")
```

Statistics scripts: `scripts/validate_spnet.py`, benchmarks: `scripts/bench.py`.

## Legacy prototype

The `neurons`, `plasticity` and `network` modules (seven neuron presets, pair STDP
with weight bounds, CSR connectivity, no conduction delays) are the first
iteration. They are superseded by `dreammachine.spnet` and are described in
[docs/architecture.md](docs/architecture.md) only as legacy.

## Performance

Reference network (1000 neurons, 100k synapses, delays and STDP), compiled kernel,
10 s of model time, 7 repeats on a 4-vCPU Xeon 2.1 GHz cloud container:
**81.5-89.9x realtime** (min-max; record
`benchmarks/records/bench-spnet-reference-20261124T010156Z.json`). Scaling,
memory use, the legacy baseline and caveats are in
[docs/validation/benchmarks.md](docs/validation/benchmarks.md).

## Project Structure

```
DreamMachine/
├── docs/                 # plan, spec, architecture, testing, policies, validation/
├── src/dreammachine/
│   ├── spnet/            # spnet.m replication: network, oracle, kernel
│   └── neurons/ plasticity/ network/   # legacy prototype
├── scripts/              # bench.py, validate_spnet.py, crosscheck_original.py
├── benchmarks/records/   # JSON records written by the scripts
├── tests/                # pytest test suite
└── examples/             # legacy prototype example
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
