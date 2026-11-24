# DreamMachine - Specification

**Version:** 2.0.0 (rewrite, 2026-11-24; replaces the 2026-01-31 draft)
**Scope:** the reference model implemented in `dreammachine.spnet`, a replication of Izhikevich's `spnet.m` (2006 polychronization network, 2008 random-delay variant). Context and milestones: `docs/plan.md`. Test rules: `docs/testing.md`.

Verification names: `T:` a test in `tests/`, `S:` a script, `D:` a validation document. A requirement whose check is "none" is unverified. Anything marked **not implemented** does not exist in the code.

## 1. Model parameters (`SpnetParams` defaults)

| Parameter | Value | Meaning | Source |
|---|---|---|---|
| Ne, Ni | 800, 200 | excitatory, inhibitory neurons | `spnet.m` line 8 |
| M | 100 | outgoing synapses per neuron, distinct targets | `spnet.m` line 5 |
| D | 20 ms | maximal conduction delay | `spnet.m` line 6 |
| a, d (exc) | 0.02, 8 | regular spiking | `spnet.m` line 9-10 |
| a, d (inh) | 0.1, 2 | fast spiking | `spnet.m` line 9-10 |
| b, c | 0.2, -65 | all neurons | `spnet.m` line 46-47, 55, 72 |
| w_exc, w_inh | 6, -5 | initial weights | `spnet.m` line 29 |
| sm | 10 | excitatory weight upper bound (lower bound 0) | `spnet.m` line 11, 80 |
| input_current | 20 | one random neuron per ms | `spnet.m` line 53 |
| trace_amp, trace_decay | 0.1, 0.95 | postsynaptic/presynaptic trace set on a spike, decay per ms | `spnet.m` line 57, 73 |
| ltd_factor | 1.2 | LTD multiplier on the postsynaptic trace | `spnet.m` line 67 |
| sd_decay | 0.9 | derivative decay once per second | `spnet.m` line 81 |
| w_drift | 0.01 | added to excitatory weights once per second | `spnet.m` line 80 |
| time step | 1 ms | `v` in two 0.5 ms half-steps, `u` in one step; spike at v >= 30, reset at the start of the next step | `spnet.m` line 55, 70-72 |

## 2. Requirements

| ID | Requirement | Verification |
|---|---|---|---|
| SP-NET-01 | Each neuron has M synapses with distinct targets; inhibitory neurons target excitatory neurons only | T: `test_no_duplicate_targets_and_inhibitory_targets` |
| SP-NET-02 | Excitatory delays are integers in 1..D (varied); inhibitory delays are 1 | T: `test_delays_and_weights_and_params` |
| SP-NET-03 | Initial weights, a and d follow section 1 | T: `test_delays_and_weights_and_params` |
| SP-NET-04 | Array shapes and dtypes: indices int32, weights and parameters float64 | T: `test_default_shapes_dtypes` |
| SP-NET-05 | Network and input are reproducible from a `numpy.random.Generator` seed | T: `test_seed_determinism`, `test_make_inputs` |
| SP-SIM-01 | The kernel matches the oracle spike for spike and in final `s`, `sd`, `v`, `u`, bit for bit | T: `test_small_network_equivalence`, `test_default_network_equivalence_and_activity`, `test_small_equivalence_other_seeds` |
| SP-SIM-02 | Oracle and kernel match the original `spnet.m` under Octave (spike sequence, `s`), small network in the suite, 5 s and 20 s full network by script; skipped when Octave or the cached file is absent | T: `test_small_network_matches_original_spnet_m`; S: `scripts/crosscheck_original.py`; D: `docs/validation/crosscheck-original.md` |
| SP-SIM-03 | Runs are deterministic; the input network is not mutated | T: `test_weight_invariants_and_determinism` |
| SP-PLS-01 | Excitatory weights stay in [0, sm] after every update; inhibitory weights never change; plasticity changes excitatory weights | T: `test_weight_invariants_and_determinism` |
| SP-PLS-02 | STDP rule (traces, `sd`, once-per-second update) is as in `spnet.m` | covered by SP-SIM-01 and SP-SIM-02 only; no separate STDP-window test (TASK-020) |
| SP-VAL-01 | Long-run rates, weight distribution and spectra over 5 seeds, 3600 s each, compared with reported results | S: `scripts/validate_spnet.py`; D: `docs/validation/spnet-statistics.md` |
| SP-PER-01 | Reference network performance is recorded with machine details and every repeat | S: `scripts/bench.py spnet-reference`; D: `docs/validation/benchmarks.md` |
| SP-PER-02 | Scaling to 100,000 neurons (M=100) with time, peak RSS and bytes per synapse recorded | S: `scripts/bench.py spnet-scaling`; D: `docs/validation/benchmarks.md` |
| SP-PER-03 | Provisional target: reference network at least 20x realtime on one CPU thread (`docs/plan.md`) | D: `docs/validation/benchmarks.md` (measured on one machine; not the Apple M1) |
| SP-QUA-01 | Fast-path code is accepted only if SP-SIM-01 still passes | T: SP-SIM-01 tests; `docs/policies.md` |

## 3. Not implemented

- Polychronous group detection (TASK-014); GPU port (TASK-024).
- Comparison with `spnet.cpp`, MATLAB itself, or an independent simulator; MATLAB's random stream.
- Step sizes other than 1 ms, float32, or an accurate-integration mode (TASK-025); `fastmath` is off.
- Recording of membrane potentials or weight histories; only spike lists and final state are returned.
- Multi-threaded kernel: the kernel is serial.
- Pluggable plasticity rules, short-term plasticity, neuromodulation (TASK-019, -021, -022).
- Neuron types other than regular and fast spiking in `spnet`; Aplysia circuits; connectivity generators.
- CI, lint and type checks (TASK-005).
- Benchmarks on the Apple M1 (TASK-018).

## 4. Legacy prototype

`dreammachine.neurons`, `plasticity` and `network` implement a different, single-population model. They are not covered by this specification; their tests (`tests/test_neurons.py`, `test_plasticity.py`, `test_simulator.py`) check only their own behaviour.

## 5. References

Cited keys are in `references/manifest.jsonl`: `izhikevich2006_polychronization_page`, `izhikevich_spnet_m`, `pauli2018_reproducing`, `trensch2018_rigorous`.
