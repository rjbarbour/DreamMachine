# DreamMachine - Architecture

**Version:** 2.0.0 (2026-11-24). Describes the code as it is. Requirements: `docs/spec.md`.

## 1. Layout

```
src/dreammachine/
├── spnet/            # current: replication of spnet.m
│   ├── network.py    # SpnetParams, build_network, make_inputs, result types
│   ├── oracle.py     # run_oracle: slow, obviously correct transcription
│   └── kernel.py     # run_kernel: Numba, bit-identical to the oracle
└── neurons/ plasticity/ network/   # LEGACY prototype
```

**Legacy:** `neurons`, `plasticity` and `network` (single population, pair STDP with bounds, CSR connectivity, no delays, Python loop) predate the spnet work. They are kept for reference, are not part of the reference model, and may be removed. Do not extend them.

## 2. spnet data layout

Zero-based indices. Neurons 0..Ne-1 are excitatory, the rest inhibitory.

| Array | Shape, dtype | Content |
|---|---|---|
| `post` | (N, M) int32 | target of synapse `[i, slot]` |
| `delay` | (N, M) int32 | delay 1..D ms |
| `s` | (N, M) float64 | weight (updated in place on a copy) |
| `sd` | (N, M) float64 | weight derivative, zero at start |
| `v`, `u`, `a`, `d` | (N,) float64 | neuron state and parameters |
| `trace` | (1001 + D, N) float64 | postsynaptic traces for the current second plus D steps of history, copied back after each second |
| `inputs` | (seconds, 1000) int32 | neuron receiving `input_current` each ms |
| spike list | growing int64 time, int32 neuron | global ms index, detection order |

Kernel indices, built once by `_build_indices` as flat CSR arrays: incoming excitatory synapses grouped by target neuron (`in_ptr`, `in_pre`, `in_slot`, `in_delay`), and outgoing synapses grouped by (neuron, delay) (`out_ptr`, `out_slot`). There is no delay ring buffer: arriving spikes are found by scanning the global spike list back over the last D ms.

## 3. Step order (one millisecond `t`)

1. Set input current: 0 everywhere, `input_current` on `inputs[sec, t-1]`.
2. Detect neurons with `v >= 30`; reset `v = c`, `u += d`; set their trace to `trace_amp`.
3. For each spiking neuron (postsynaptic), for each incoming excitatory synapse: `sd += trace of the presynaptic neuron` at the time the delayed spike arrived (LTP).
4. Append spikes to the spike list.
5. Walk the spike list backwards over the last D ms; for each spike, take the synapses whose delay equals its age: add `s` to the target's current, and `sd -= ltd_factor * trace[target]` (LTD).
6. Update `v` (two 0.5 ms half-steps) and `u` (one step); decay all traces by `trace_decay`.

After 1000 steps: copy the last D+1 trace columns to the start; excitatory `s = clip(w_drift + s + sd, 0, sm)`; all `sd *= sd_decay`.

## 4. Verification of the layout

`run_oracle` and `run_kernel` use the same step order with different data structures; their agreement is tested bit for bit (`tests/test_spnet_equivalence.py`). Equality with the original `spnet.m` is in `docs/validation/crosscheck-original.md`.

## 5. Measured cost

See `docs/validation/benchmarks.md` for time and memory; those figures include the arrays above (about 148 bytes per synapse at 100,000 neurons, peak RSS).
