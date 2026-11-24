# Benchmarks

Harness: `scripts/bench.py` (`PYTHONPATH=src python scripts/bench.py <subcommand>`). Records are in `benchmarks/records/`. Machine: 4-vCPU Intel Xeon 2.10 GHz cloud container, Python 3.13.18, NumPy 2.5.3, Numba 0.68.1 (4 Numba threads available; the spnet kernel is serial). Git SHA is stored in each record. One benchmark ran at a time.

| Benchmark | Record | Setup | Result |
|---|---|---|---|
| spnet reference | `bench-spnet-reference-20261124T010156Z.json` | 1000 neurons, 100k synapses, 10 s model time, kernel only, 7 repeats after JIT warm-up | wall 0.111-0.123 s (median 0.114 s): 81.5-89.9x realtime (min-max), 46,291 spikes each repeat |
| Prototype baseline | `bench-prototype-baseline-20261124T010209Z.json` | `dreammachine.network.simulator`, 1000 neurons, density 0.1, dt 0.5 ms, 1 s model time, 3 repeats | wall 0.203-0.213 s (median 0.213 s): 4.7-4.9x realtime |
| spnet scaling, 1k | `bench-spnet-scaling-20261124T010600Z.json` | 20 s model time, single run | 127x realtime, peak RSS 177 MB |
| spnet scaling, 10k | same | 20 s | 17.4x, 328 MB, 344 bytes/synapse |
| spnet scaling, 100k | same | 20 s | 1.46x, 1416 MB, 148 bytes/synapse |

## Reading the numbers

- No size fell below realtime: the largest measured (100,000 neurons, 10 million synapses) ran at 1.46x. The crossover lies beyond the sizes measured.
- The reference figure exceeds the provisional 20x target in `docs/plan.md` on this machine. The Apple M1 has not been measured (TASK-018).
- Activity differs between sizes. The input is one 20-unit pulse per millisecond to a random neuron, so larger networks are close to silent: mean rates were 3.3 Hz (1k), 0.099 Hz (10k) and 0.010 Hz (100k) over the 20 s run. The scaling figures therefore measure a nearly quiescent network and flatter the larger sizes. Weights had no time to evolve.
- Bytes per synapse is peak process RSS (including interpreter, JIT and index arrays) divided by synapses; the 1k figure is dominated by fixed overhead.
- Building the 100k network took 101 s (Python loop in `build_network`), not included in the run times.
- The prototype baseline in `docs/plan.md` (0.23x, one run) is not reproduced here: that run is not recorded and its conditions are unknown. The new figure uses constant drive to 20 neurons (519-524 spikes per second of model time), after a JIT warm-up.
- Single run per scaling size; no repeat variance is available for them.
