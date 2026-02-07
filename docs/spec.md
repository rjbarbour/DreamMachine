# DreamMachine - Requirements Specification

**Version:** 1.0.0
**Date:** 2026-01-31
**Status:** Draft

## 1. Executive Summary

DreamMachine is a high-performance, scalable spiking neural network (SNN) simulator implementing biologically plausible Izhikevich neurons with spike-timing-dependent plasticity (STDP). The system provides a foundation for Hebbian learning research and computational neuroscience experiments, with an architectural roadmap toward simulating Aplysia californica neural circuits.

## 2. Background and Motivation

### 2.1 Scientific Context

- **Izhikevich Model (2003)**: Combines computational efficiency of integrate-and-fire models with biological plausibility of Hodgkin-Huxley dynamics
- **STDP (Bi & Poo, 1998)**: Hebbian learning rule where synaptic strength changes based on precise spike timing
- **Kandel's Aplysia Research**: Demonstrated cellular mechanisms of habituation, sensitization, and classical conditioning

### 2.2 References

1. Izhikevich, E.M. (2003). "Simple model of spiking neurons." IEEE Trans. Neural Networks, 14(6):1569-1572.
2. Izhikevich, E.M. (2007). "Dynamical Systems in Neuroscience." MIT Press.
3. Bi, G. & Poo, M. (1998). "Synaptic modifications in cultured hippocampal neurons." J. Neurosci., 18:10464-10472.
4. Kandel, E.R. (2001). "The molecular biology of memory storage." Science, 294:1030-1038.

## 3. Functional Requirements

### 3.1 Neuron Model (FR-NEU)

| ID | Requirement | Priority |
|----|-------------|----------|
| FR-NEU-01 | Implement Izhikevich neuron model with equations: v' = 0.04v² + 5v + 140 - u + I; u' = a(bv - u) | P0 |
| FR-NEU-02 | Support configurable parameters (a, b, c, d) for different neuron types | P0 |
| FR-NEU-03 | Implement spike detection at v ≥ 30mV with reset v←c, u←u+d | P0 |
| FR-NEU-04 | Support neuron types: RS, IB, CH, FS, LTS, TC, RZ | P1 |
| FR-NEU-05 | Support external current injection I(t) | P0 |

### 3.2 Synaptic Model (FR-SYN)

| ID | Requirement | Priority |
|----|-------------|----------|
| FR-SYN-01 | Implement weighted synaptic connections with conductance-based or current-based transmission | P0 |
| FR-SYN-02 | Support axonal delay (1-20ms configurable) | P1 |
| FR-SYN-03 | Implement excitatory (AMPA/NMDA-like) and inhibitory (GABA-like) synapses | P1 |

### 3.3 Plasticity Model (FR-PLS)

| ID | Requirement | Priority |
|----|-------------|----------|
| FR-PLS-01 | Implement exponential STDP window: Δw = A±·exp(-|Δt|/τ±) | P0 |
| FR-PLS-02 | Support configurable time constants τ+ (LTP) and τ- (LTD), typical 10-30ms | P0 |
| FR-PLS-03 | Support configurable amplitude A+ (positive) and A- (negative) | P0 |
| FR-PLS-04 | Implement trace-based STDP for O(1) computational complexity per spike | P0 |
| FR-PLS-05 | Support weight bounds [w_min, w_max] to prevent runaway potentiation/depression | P0 |
| FR-PLS-06 | Support both all-to-all and nearest-neighbor spike pairing modes | P1 |

### 3.4 Network Model (FR-NET)

| ID | Requirement | Priority |
|----|-------------|----------|
| FR-NET-01 | Support arbitrary network topologies via adjacency specification | P0 |
| FR-NET-02 | Support populations of neurons with configurable connectivity patterns | P1 |
| FR-NET-03 | Support random, small-world, and scale-free connectivity generators | P2 |

### 3.5 Simulation Engine (FR-SIM)

| ID | Requirement | Priority |
|----|-------------|----------|
| FR-SIM-01 | Time-stepped simulation with configurable dt (default 0.5ms for accuracy, 1ms for speed) | P0 |
| FR-SIM-02 | Record spike times for all neurons | P0 |
| FR-SIM-03 | Record membrane potential traces (optional, configurable) | P0 |
| FR-SIM-04 | Record synaptic weight evolution over time | P1 |

## 4. Non-Functional Requirements

### 4.1 Performance (NFR-PER)

| ID | Requirement | Target |
|----|-------------|--------|
| NFR-PER-01 | Simulate 1000 neurons with 100K synapses in real-time or faster | ≤1s per 1s simulated |
| NFR-PER-02 | Scale to 10,000+ neurons with sparse connectivity | Linear time complexity |
| NFR-PER-03 | Memory-efficient sparse weight matrix representation | O(synapses), not O(neurons²) |

### 4.2 Code Quality (NFR-QUA)

| ID | Requirement |
|----|-------------|
| NFR-QUA-01 | Type hints throughout codebase (PEP 484) |
| NFR-QUA-02 | Docstrings for all public functions (NumPy style) |
| NFR-QUA-03 | Unit test coverage ≥80% for core modules |
| NFR-QUA-04 | Linting compliance (ruff/flake8) |

### 4.3 Extensibility (NFR-EXT)

| ID | Requirement |
|----|-------------|
| NFR-EXT-01 | Modular architecture allowing custom neuron models |
| NFR-EXT-02 | Pluggable plasticity rules |
| NFR-EXT-03 | Event hooks for monitoring and intervention |

## 5. System Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                      DreamMachine                           │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐  │
│  │   Neurons   │  │  Synapses   │  │    Plasticity       │  │
│  │  (Izhikevich)│  │ (Weighted)  │  │    (STDP)          │  │
│  └──────┬──────┘  └──────┬──────┘  └──────────┬──────────┘  │
│         │                │                     │             │
│         └────────────────┼─────────────────────┘             │
│                          │                                   │
│                  ┌───────▼───────┐                          │
│                  │    Network    │                          │
│                  │   Simulator   │                          │
│                  └───────┬───────┘                          │
│                          │                                   │
│         ┌────────────────┼────────────────┐                 │
│         ▼                ▼                ▼                 │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐         │
│  │   Monitors  │  │  Analysis   │  │Visualization│         │
│  └─────────────┘  └─────────────┘  └─────────────┘         │
└─────────────────────────────────────────────────────────────┘
```

## 6. Use Cases

### UC-01: Basic Network Simulation

**Actor:** Researcher
**Preconditions:** Network configuration defined
**Flow:**
1. Create neurons with specified parameters
2. Define synaptic connections with weights and delays
3. Run simulation for specified duration
4. Retrieve spike times and weight changes
5. Analyze/visualize results

### UC-02: Aplysia Gill-Withdrawal Circuit (Future)

**Actor:** Researcher
**Preconditions:** Aplysia circuit template available
**Flow:**
1. Instantiate sensory, motor, and interneuron populations
2. Apply tactile stimulus (current injection to sensory neurons)
3. Observe motor neuron response
4. Repeat stimulus to observe habituation
5. Apply modulatory signal (simulated serotonin) for sensitization

## 7. Acceptance Criteria

### Phase 1 MVP Acceptance

- [ ] Single Izhikevich neuron produces correct firing patterns for RS, FS types
- [ ] Network of 100 neurons with random connectivity runs without error
- [ ] STDP modifies weights according to spike timing
- [ ] Spike raster plot can be generated from simulation output
- [ ] Unit tests pass with ≥80% coverage

## 8. Glossary

| Term | Definition |
|------|------------|
| **SNN** | Spiking Neural Network - neural network using discrete spike events |
| **STDP** | Spike-Timing-Dependent Plasticity - Hebbian learning based on spike timing |
| **LTP** | Long-Term Potentiation - strengthening of synaptic connection |
| **LTD** | Long-Term Depression - weakening of synaptic connection |
| **RS** | Regular Spiking - excitatory cortical neuron type |
| **FS** | Fast Spiking - inhibitory interneuron type |
| **Aplysia** | Sea slug used in foundational memory research by Kandel |
