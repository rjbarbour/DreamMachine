# DreamMachine - Architecture Document

**Version:** 1.0.0
**Date:** 2026-01-31
**Status:** Draft

## 1. Architecture Overview

### 1.1 Design Principles

1. **Vectorization First**: Use NumPy array operations for neuron state updates
2. **Sparse Connectivity**: CSR matrices for O(synapses) memory, not O(neurons²)
3. **JIT Compilation**: Numba for hot paths when vectorization insufficient
4. **Separation of Concerns**: Neurons, synapses, plasticity, and simulation are decoupled
5. **Immutable Configuration**: Neuron/synapse parameters set at construction

### 1.2 Technology Stack

| Layer | Technology | Rationale |
|-------|------------|-----------|
| Core Computation | NumPy 1.24+ | Vectorized array operations |
| JIT Acceleration | Numba 0.58+ | 10-100x speedup on loops |
| Sparse Matrices | SciPy.sparse | Memory-efficient connectivity |
| Testing | pytest 7.0+ | Industry standard, fixtures |
| Visualization | Matplotlib 3.7+ | Publication-quality plots |
| Type Checking | mypy | Static type verification |

## 2. Module Structure

```
dreammachine/
├── __init__.py           # Package exports
├── neurons/
│   ├── __init__.py
│   ├── base.py           # Abstract neuron interface
│   └── izhikevich.py     # Izhikevich implementation
├── synapses/
│   ├── __init__.py
│   └── synapse.py        # Synaptic connectivity and transmission
├── plasticity/
│   ├── __init__.py
│   ├── base.py           # Abstract plasticity interface
│   └── stdp.py           # STDP implementation
├── network/
│   ├── __init__.py
│   └── simulator.py      # Main simulation loop
├── io/
│   ├── __init__.py
│   └── monitors.py       # Spike/voltage recording
└── utils/
    ├── __init__.py
    └── connectivity.py   # Network topology generators
```

## 3. Core Components

### 3.1 Izhikevich Neuron Model

#### Mathematical Model

```
dv/dt = 0.04v² + 5v + 140 - u + I
du/dt = a(bv - u)

if v ≥ 30 mV:
    v ← c
    u ← u + d
    emit spike
```

#### Neuron Type Parameters

| Type | a | b | c | d | Description |
|------|---|---|---|---|-------------|
| RS | 0.02 | 0.2 | -65 | 8 | Regular Spiking (excitatory) |
| IB | 0.02 | 0.2 | -55 | 4 | Intrinsically Bursting |
| CH | 0.02 | 0.2 | -50 | 2 | Chattering |
| FS | 0.1 | 0.2 | -65 | 2 | Fast Spiking (inhibitory) |
| LTS | 0.02 | 0.25 | -65 | 2 | Low-Threshold Spiking |
| TC | 0.02 | 0.25 | -65 | 0.05 | Thalamocortical |
| RZ | 0.1 | 0.26 | -65 | 2 | Resonator |

#### Data Structure

```python
@dataclass
class IzhikevichParams:
    a: float  # Recovery time constant (smaller = slower)
    b: float  # Recovery sensitivity to subthreshold
    c: float  # Post-spike reset value (mV)
    d: float  # Post-spike recovery increment

class IzhikevichPopulation:
    """Vectorized population of Izhikevich neurons."""

    v: np.ndarray[np.float32]      # Membrane potential (N,)
    u: np.ndarray[np.float32]      # Recovery variable (N,)
    a: np.ndarray[np.float32]      # Parameters (N,) for heterogeneous populations
    b: np.ndarray[np.float32]
    c: np.ndarray[np.float32]
    d: np.ndarray[np.float32]
    I: np.ndarray[np.float32]      # Input current (N,)
```

#### Update Algorithm (Vectorized)

```python
def step(self, dt: float = 0.5) -> np.ndarray:
    """Advance one timestep, return spike mask."""
    # Euler integration (two half-steps for stability)
    self.v += dt/2 * (0.04*self.v**2 + 5*self.v + 140 - self.u + self.I)
    self.v += dt/2 * (0.04*self.v**2 + 5*self.v + 140 - self.u + self.I)
    self.u += dt * self.a * (self.b * self.v - self.u)

    # Spike detection and reset
    spikes = self.v >= 30.0
    self.v[spikes] = self.c[spikes]
    self.u[spikes] += self.d[spikes]

    return spikes
```

### 3.2 STDP Plasticity Model

#### Mathematical Model

Exponential STDP window:

```
Δw = {
    A+ · exp(-Δt/τ+)  if Δt > 0 (pre before post → LTP)
    A- · exp(Δt/τ-)   if Δt < 0 (post before pre → LTD)
}

where Δt = t_post - t_pre
```

#### Trace-Based Implementation

For computational efficiency O(1) per spike:

```
Pre-synaptic trace:  dx_pre/dt = -x_pre/τ+,  on pre-spike: x_pre += 1
Post-synaptic trace: dx_post/dt = -x_post/τ-, on post-spike: x_post += 1

Weight updates:
  On post-spike: Δw = A+ · x_pre   (LTP)
  On pre-spike:  Δw = A- · x_post  (LTD)
```

#### Data Structure

```python
@dataclass
class STDPParams:
    tau_plus: float = 20.0   # LTP time constant (ms)
    tau_minus: float = 20.0  # LTD time constant (ms)
    A_plus: float = 0.01     # LTP amplitude
    A_minus: float = -0.012  # LTD amplitude (negative)
    w_min: float = 0.0       # Minimum weight
    w_max: float = 1.0       # Maximum weight

class STDPSynapses:
    """Trace-based STDP implementation."""

    weights: scipy.sparse.csr_matrix  # (pre, post) sparse connectivity
    pre_trace: np.ndarray             # Pre-synaptic eligibility trace
    post_trace: np.ndarray            # Post-synaptic eligibility trace
```

### 3.3 Network Simulator

#### Simulation Loop

```python
def run(self, duration_ms: float, dt: float = 0.5) -> SimulationResult:
    n_steps = int(duration_ms / dt)

    for step in range(n_steps):
        t = step * dt

        # 1. Compute synaptic input
        I_syn = self.synapses.compute_input(prev_spikes)
        self.neurons.I = I_external[step] + I_syn

        # 2. Update neuron states
        spikes = self.neurons.step(dt)

        # 3. Update plasticity traces
        self.plasticity.update_traces(dt)

        # 4. Apply STDP on spikes
        if spikes.any():
            self.plasticity.on_spikes(spikes, self.synapses)

        # 5. Record
        self.monitor.record(t, spikes, self.neurons.v)

        prev_spikes = spikes
```

## 4. Performance Optimizations

### 4.1 Vectorization Strategy

| Operation | Naive O() | Vectorized O() | Speedup |
|-----------|-----------|----------------|---------|
| Neuron update | O(N) loop | O(N) SIMD | 10-50x |
| Synaptic input | O(S) loop | O(S) sparse matmul | 5-20x |
| Trace decay | O(N) loop | O(N) SIMD | 10-50x |

### 4.2 Memory Layout

```
Neurons: Struct of Arrays (SoA)
    v: [v0, v1, v2, ...] contiguous float32
    u: [u0, u1, u2, ...] contiguous float32

Synapses: Compressed Sparse Row (CSR)
    For N=10000 with 1% connectivity:
    Dense: 10000² × 4 bytes = 400 MB
    Sparse: 10000² × 0.01 × 12 bytes ≈ 12 MB (33x reduction)
```

### 4.3 Numba JIT Targets

```python
@numba.jit(nopython=True, parallel=True, cache=True)
def _izhikevich_step_numba(v, u, a, b, c, d, I, dt):
    """JIT-compiled neuron update for maximum performance."""
    for i in numba.prange(len(v)):
        # ... update equations ...
```

## 5. Data Flow

```
                    ┌──────────────┐
                    │ External I(t)│
                    └──────┬───────┘
                           ▼
┌────────────┐      ┌──────────────┐      ┌─────────────┐
│ Spike t-1  │─────▶│   Synapses   │─────▶│  I_synaptic │
└────────────┘      └──────────────┘      └──────┬──────┘
                                                  ▼
                                          ┌──────────────┐
                                          │   Neurons    │
                                          │ v' = f(v,u,I)│
                                          └──────┬───────┘
                                                  ▼
                                          ┌──────────────┐
                                          │ Spike t      │
                                          └──────┬───────┘
                           ┌──────────────────────┼───────────────────────┐
                           ▼                      ▼                       ▼
                    ┌──────────────┐      ┌──────────────┐      ┌──────────────┐
                    │   Monitor    │      │    STDP      │      │  Next Step   │
                    │   (record)   │      │  (update w)  │      │              │
                    └──────────────┘      └──────────────┘      └──────────────┘
```

## 6. Extension Points

### 6.1 Custom Neuron Models

```python
class CustomNeuron(NeuronBase):
    def step(self, dt: float) -> np.ndarray:
        """Override with custom dynamics."""
        ...
```

### 6.2 Custom Plasticity Rules

```python
class CustomPlasticity(PlasticityBase):
    def on_pre_spike(self, neuron_idx: int): ...
    def on_post_spike(self, neuron_idx: int): ...
    def update_traces(self, dt: float): ...
```

## 7. Testing Strategy

### 7.1 Unit Tests

| Module | Test Focus |
|--------|------------|
| neurons/izhikevich | Firing patterns match literature |
| plasticity/stdp | Weight changes correct for known Δt |
| network/simulator | Energy conservation, spike propagation |

### 7.2 Integration Tests

- 1000-neuron random network runs to completion
- STDP produces expected weight distribution after training

### 7.3 Validation Tests

- Compare RS neuron output to Izhikevich (2003) Figure 1
- Compare STDP curve to Bi & Poo (1998) Figure 1

## 8. Future Architecture (Aplysia Phase)

```
┌─────────────────────────────────────────────────────────────────┐
│                     Aplysia Circuit Model                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   Siphon Touch ───▶ [Sensory Neurons] ───▶ [Motor Neurons]     │
│                            │                     │              │
│                            │     (glutamate)     │              │
│                            ▼                     ▼              │
│                     [Interneurons]         Gill Withdrawal      │
│                            │                                    │
│   Tail Shock ────▶ [Modulatory Neurons] ──── 5-HT ───┐         │
│                    (serotonergic)                     │         │
│                                                       ▼         │
│                                            Synaptic Facilitation│
│                                            (sensitization)      │
└─────────────────────────────────────────────────────────────────┘
```

## 9. Revision History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0.0 | 2026-01-31 | Claude | Initial architecture |
