# Prior art: spnet replications, SNN simulators, published speed figures

**Compiled:** 2026-11-24 by a research sub-agent (web search and page reads), saved
verbatim apart from this header. **Status:** not independently re-checked by a
second reader. The agent was instructed to report only what it found on pages it
opened and to list what it could not verify (end of file). Repository dates are
GitHub `pushedAt` values; release dates are from PyPI. Sources are recorded in
`references/manifest.jsonl` with `source_report` set to this file.

## 1. spnet re-implementations and validation studies

| Item | Licence / last activity | Use to us |
|---|---|---|
| Original `spnet.m`, `spnet.cpp`, `poly_spnet.cpp`, `polychron.m` (izhikevich.org, indexed by [ModelDB 115968](https://github.com/ModelDBRepository/115968)) | No licence shown | Ground truth. The README says the MATLAB and C versions are "similar but not equivalent". |
| [INM-6/reproducing-polychronization](https://github.com/INM-6/reproducing-polychronization) (NEST + Snakemake; needs a NEST fork) | MIT / 2022-11 | Validation reference. |
| [gtrensch/RigorousNeuralNetworkSimulations](https://github.com/gtrensch/RigorousNeuralNetworkSimulations) (C, PyNEST and SpiNNaker versions) | GPL-2.0 / 2023-07 | Readable C reference and validation statistics. |
| [chanokin/poly_genn](https://github.com/chanokin/poly_genn) (PyGeNN) | None shown / 2022-01 | Unvalidated; a glance only. |
| [HJLebbink/Spike-Izhi](https://github.com/HJLebbink/Spike-Izhi) (C++/MATLAB) | MIT / 2017 | No validation claims. |

**Pauli, Weidel, Kunkel & Morrison (2018)**, Front. Neuroinform. 12:46, doi:10.3389/fninf.2018.00046: citation verified ([PMC6085985](https://pmc.ncbi.nlm.nih.gov/articles/PMC6085985)). Their findings:

- **Code mismatch:** the downloadable C++ did not match the paper and differed from the MATLAB. The STDP buffer's 0.9 decay is applied before the weight update in C++ and after it in MATLAB.
- **Integration:** `v` advances in two 0.5 ms half-steps and `u` in one 1 ms step. Membrane potentials reach about 1,000 mV, and operation order alone eventually causes divergence.
- **Hidden details:** spikes are delivered at the start of a step, STDP is nearest-neighbour, weights change once per second with +0.01 added, and excitatory delays are hardwired at five synapses per delay value.
- **Results:** rates are about 2–5 Hz and weights are bimodal. Gamma peaks near 60 Hz in 87 of 100 seeds and near 40 Hz in 13, an unreported second mode.
- **Group counts:** these depend heavily on the analysis threshold (27,116, 4,305 or 608 groups). The paper reported 5,000–6,000.
- **Outcome:** bitwise reproduction was possible only after many fixes.

**Trensch et al. (2018)**, Front. Neuroinform. 12:81 ([PMC6275234](https://pmc.ncbi.nlm.nih.gov/articles/PMC6275234)), compares implementations by distributions of firing rate, local CV and pairwise cross-correlation, scored with effect sizes. They measured `v` up to about 1,700 in the original scheme.

**Paolucci et al. (2013)**, [arXiv:1310.8478](https://arxiv.org/abs/1310.8478), use a polychronous Izhikevich + STDP grid (DPSNN-STDP) as a distributed benchmark. A 3.2 G-synapse network on 128 cores took 10 wall-clock seconds per simulated second per Hz of mean firing rate. The abstract mentions no validation against spnet.

No Brian2 or NEST official example was found, and no Numba or Julia port.

## 2. General simulators

| Tool | Licence / latest | Izhikevich + STDP + delays | Backends | Layout notes |
|---|---|---|---|---|
| [Brian2](https://brian2.readthedocs.io/en/stable/user/synapses.html) | CeCILL-2.1 / 2.11.0, 2026-10 | Yes: equations, per-synapse presynaptic delay, event-driven traces | CPU (Cython, C++ standalone) | Sparse per-synapse `i`, `j` arrays |
| [Brian2CUDA](https://pmc.ncbi.nlm.nih.gov/articles/PMC9660315) | GPL-3.0 / 1.0b1, 2025-12 | Yes, including heterogeneous delays | CUDA | Pre-sorted CSR plus a post-sorted copy; circular list of spike queues; same-delay "bundles" |
| [Brian2GeNN](https://brian2genn.readthedocs.io/en/stable/introduction/exclusions.html) | GPL-2.0 / 1.7.0, 2023-07 | No heterogeneous delays | CUDA | n/a |
| [GeNN / PyGeNN](https://github.com/genn-team/genn) | LGPL-2.1 / 5.5.0 | Izhikevich built in; STDP as code snippets; [per-synapse dendritic delays](https://genn-team.github.io/genn/documentation/5/custom_models.html) | CUDA, AMD HIP; 5.3.0 fixed macOS builds | [Padded rows, column-major index for postsynaptic STDP, ring buffer of D_max × N_post](https://pmc.ncbi.nlm.nih.gov/articles/PMC6299048/) |
| [NEST GPU](https://nest-gpu.readthedocs.io/en/latest/models/index.html) | GPL-2.0 / 2026-11 | `izhikevich` and nearest-neighbour `stdp` | GPU + MPI | [Per-neuron spike buffer; connections sorted and grouped by delay](https://pmc.ncbi.nlm.nih.gov/articles/PMC7925400) |
| [CARLsim 6](https://github.com/UCI-CARL/CARLsim6) | MIT / 2025-11 | Izhikevich; E-, I- and DA-STDP; 1–20 ms delays in [the 2011 paper](https://pmc.ncbi.nlm.nih.gov/articles/PMC3172707) | x86 CPU, CUDA | 0.5 ms neuron step, 1 ms plasticity step |
| [BindsNET](https://github.com/BindsNET/bindsnet), [Norse](https://norse.github.io/norse/), [snnTorch](https://snntorch.readthedocs.io/en/latest/), [SpikingJelly](https://spikingjelly.readthedocs.io/zh-cn/latest/APIs/spikingjelly.activation_based.learning.html) | AGPL / LGPL / MIT / Apache | Partial: no delays on the pages opened | PyTorch | Layer-based |
| [Lava](https://lava-nc.org/), [Arbor](https://docs.arbor-sim.org/en/latest/) | BSD+LGPL / BSD-3 | Both have STDP; neither page mentions Izhikevich cells | CPU, Loihi / CPU, GPU | Not relevant |
| BrainPy, Spyx, jaxsnn | Releases in 2026 | Not verified (docs returned 404) | JAX | n/a |

## 3. Published performance numbers

| Source | Result | Hardware |
|---|---|---|
| [PyGeNN paper, 2021](https://pmc.ncbi.nlm.nih.gov/articles/PMC8100330) | 800 + 200 Izhikevich neurons with dopamine STDP: 62–72× real time; up to 31× on Jetson. PyGeNN adds about 31% overhead because per-step cost is so small. | Titan RTX and GTX 1650 (identical); Jetson Xavier NX |
| [GeNN, 2016](https://pmc.ncbi.nlm.nih.gov/articles/PMC4703976) | Izhikevich, 128,000 neurons × 1,000 synapses: 2.5× slower than real time (balanced regime); at most 10.8× faster than one CPU core | Tesla K40 |
| [Knight & Nowotny, 2018](https://pmc.ncbi.nlm.nih.gov/articles/PMC6299048/) | 77k-neuron, 0.3 billion-synapse microcircuit: about 0.45× real time. STDP network with 810 million plastic synapses ran over 10× faster on V100 than K40c. | Tesla V100 |
| [NeuronGPU, 2021](https://pmc.ncbi.nlm.nih.gov/articles/PMC7925400) | Microcircuit: 1.06 s per biological second. Izhikevich + STDP, 10⁶ neurons / 10⁸ synapses: 59% faster than CARLsim 4 (no absolute time given). | RTX 2080 Ti; Tesla K80 |
| [Richert et al., 2011](https://pmc.ncbi.nlm.nih.gov/articles/PMC3172707) | 110,000 Izhikevich neurons × 100 synapses: about 2 s per simulated second; GPU 12–18× faster than CPU | Tesla C1060 vs Core i7 920 |
| [Brian2CUDA, 2022](https://pmc.ncbi.nlm.nih.gov/articles/PMC9660315) | STDP speed-up of about 100× over single-thread C++ above 10⁶ neurons. Heterogeneous delays cost one to three orders of magnitude with STDP. | A100 |

No published single-core figure for spnet itself was found.

## 4. Apple Silicon GPUs

Nothing credible was found for this kind of network. [mlx-snn](https://arxiv.org/abs/2603.03529) has an Izhikevich neuron but is a surrogate-gradient training library benchmarked on MNIST (M3 Max), and its abstract mentions neither STDP nor delays. None of the simulators above lists a Metal or MPS backend.

## Recommendations for this project

- **Validation reference:** use Izhikevich's `spnet.cpp` for a same-seed, step-exact check, since C++ and MATLAB differ. Then compare against the Pauli statistics (rates, bimodal weights, 40/60 Hz gamma modes) and Trensch-style distribution tests across many seeds.
- **Fidelity:** build an "original-faithful" mode covering the half-step integration, delivery order, once-per-second update and 0.9 factor. Treat any 0.1 ms or exact-integration variant as a separate model.
- **Data layout:** fixed fan-out is the degenerate case of GeNN's padded rows. Use `[N, 100]` arrays for target, weight and delay, with rows sorted by delay, a 20-slot ring buffer, and a column-major incoming index for LTP.
- **CPU target (agent's inference):** at 1,000 neurons, well above the 62–72× real time GeNN reaches on a GPU, because GPUs are overhead-bound at this size.
- **GPU target (agent's inference):** real time at 10⁵ neurons and 10⁷ synapses or more on a modern card. 2011–2016 hardware was already within 2–2.5× of that.
- **Dependencies:** do not depend on a simulator for the core. GeNN documents per-synapse delays only as dendritic, and Brian2CUDA's heterogeneous delays are slow with STDP. Use Brian2 as an independent cross-check.

## Not verified

- modeldb.science returned 503 and izhikevich.org returned an empty page to the agent, so it used the ModelDB GitHub mirror. (The main session did retrieve `spnet.m` and the spnet page from izhikevich.org the same day; see the manifest.)
- CARLsim 6 benchmark numbers exist only in a figure.
- NeMo's performance figures could not be confirmed.
- The mlx-snn licence is MIT in the abstract but GPL-3.0 in GitHub metadata.
