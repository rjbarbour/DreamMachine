# DreamMachine — Plan and Milestones

**Revised:** 2026-11-24. Supersedes the four-phase roadmap of 2026-01-31.
**Work tracking:** `backlog/` (Backlog.md). Run `backlog board` or `backlog task list --plain`.
**Sources:** every citation is a key in `references/manifest.jsonl`; prior-art notes are in `references/notes/`.

## 1. Why the plan changed

The first iteration was written without the source material (the fetch of
izhikevich.org failed) and was reported more favourably than the evidence allowed.
An audit on 2026-11-24 found the following.

| # | Finding | Evidence |
|---|---------|----------|
| 1 | The code does not implement Izhikevich's STDP network. It has one all-excitatory population, random sparse connectivity, no conduction delays, and applies STDP to weights immediately. | `spnet.m` (`izhikevich_spnet_m`) has 800 RS + 200 FS neurons, 100 synapses per neuron, 1–20 ms delays, and changes weights once per second through a decaying derivative. |
| 2 | The example's "STDP" result is a clamping artefact. | `STDPParams.w_max` defaults to 1.0 while the example starts weights at 15; mean weight falls 15.0 → 1.12. TASK-007. |
| 3 | Reported speed was wrong by a factor of 1000. | The example printed `duration_ms / elapsed`; "2080x realtime" was 2.08x. The first commit message repeats the wrong figure and cannot be changed without rewriting history. |
| 4 | The README performance table was never measured. | Removed; replaced by one recorded measurement. |
| 5 | The simulator is slow at reference scale. | 1000 neurons, 100k synapses, no delays: 1.0 s of model time takes 4.4 s (0.23x realtime), single run, 4-vCPU Xeon container. |
| 6 | Two failing tests were made to pass by loosening tolerances, with no root cause. | `tests/test_neurons.py`, tolerance 1e-5 → 1e-3. TASK-006. |
| 7 | Process documents requested in the brief were not written: testing principles, policies, recorded and analysed execution. | TASK-002, TASK-003, TASK-004. |
| 8 | The roadmap put GPU acceleration ahead of the science and assumed pair STDP is the learning rule for Aplysia. | See section 3. |

What is sound and kept: the package layout, the Izhikevich neuron update (two
half-steps for `v`), the trace-based pair-STDP rule as one rule among several, and
the 57 existing tests as a starting point.

## 2. What the linked page actually describes

The page in the brief (`izhikevich_blue_brain_page`) covers three things:

1. The simple spiking neuron model.
2. A 10^11-neuron, ~10^15-synapse thalamocortical simulation finished in October
   2005, where one second of model time took 50 days on 27 processors.
3. The 2008 large-scale model, with multi-compartment neurons, 21 firing types,
   short-term plasticity, dendritic STDP and dopamine modulation of plasticity.

None of these is a small runnable program. The runnable "Izhikevich STDP model" is
`spnet` from the 2006 polychronization paper (`izhikevich2006_polychronization_page`),
for which he published MATLAB and C++ code. **That is the reference for M1.** The
2008 model matters later: its plasticity ingredients (short-term plasticity,
neuromodulated STDP) are the ones M3 adds.

### Reference model parameters (from `spnet.m`)

| Quantity | Value |
|----------|-------|
| Neurons | 800 excitatory (a=0.02, d=8) and 200 inhibitory (a=0.1, d=2); b=0.2, c=−65 for all |
| Synapses | 100 per neuron, no duplicate targets; inhibitory neurons target excitatory only |
| Delays | Excitatory: random integer 1–20 ms. Inhibitory: 1 ms |
| Weights | Excitatory start at 6, bounded to [0, 10], plastic. Inhibitory fixed at −5 |
| Input | Each millisecond one randomly chosen neuron receives 20 |
| Integration | 1 ms step; `v` advanced in two 0.5 ms half-steps, `u` in one 1 ms step; spikes detected at `v ≥ 30` and reset at the start of the next step |
| STDP | Each neuron has a trace set (not added) to 0.1 when it fires and multiplied by 0.95 each ms. When a neuron fires, the derivative `sd` of each incoming excitatory synapse gains the presynaptic trace as it stood when that synapse's delayed spike arrived. When a presynaptic spike arrives, `sd` loses 1.2 × the postsynaptic trace |
| Weight update | Once per second: `s = clip(0.01 + s + sd, 0, 10)`, then `sd = 0.9 · sd` |

## 3. Principles for the revised plan

1. **Correct before fast.** A transcription of the original that is obviously right
   comes first; the fast kernel must match it exactly.
2. **Nothing is claimed that was not measured.** Numbers come from recorded runs.
3. **CPU first.** A network of this size is bound by overhead on a GPU. GPU work is
   gated on a measured need.
4. **Aplysia needs different plasticity, not more neurons.** The reflex circuit is
   small; the work is in the synaptic mechanisms and in validating against
   published measurements.
5. **Reuse prior art.** Existing replication studies and simulators supply the
   validation method and the data layout. See `references/notes/`.

## 4. Milestones

Each milestone has an exit criterion that can be checked. Sizes are relative
(S/M/L), not dates: nothing has been measured that would support a schedule.

| Milestone | Goal | Exit criterion | Size |
|-----------|------|----------------|------|
| **M0** Honest baseline and foundations | Repo says only true things; process docs exist; results are recorded by a script; CI runs | No unmeasured claim in README or docs; CI green; baseline re-recorded through the harness | S |
| **M1** Replicate `spnet` | Reproduce the 2006 network | Kernel matches the transcription spike for spike; long-run statistics compared with the paper and with the published replication study | L |
| **M2** CPU performance and scaling | Make M1 fast; show how it scales | Recorded results for the reference network and a scaling curve to ≥100k neurons, on the cloud container and the Apple M1 | M |
| **M3** Plasticity framework | Rules beyond pair STDP behind one interface | Short-term plasticity and a neuromodulator-gated rule each reproduce a published result | M |
| **M4** Aplysia withdrawal reflex v0 | Minimal circuit; habituation, sensitization, classical conditioning as scripted protocols | Each protocol compared against published measurements, with differences stated | L |
| **M5** GPU scale-out (gated) | Port the kernel | Started only when an M2 benchmark shows a required network size misses its target on CPU | M |

Dependencies: M0 → M1 → M2. M3 needs the M1 kernel. M4 needs M3. M5 needs M2 and
its gate. M2 and M3 can proceed in parallel.

### Performance target

Provisional, for the reference network (1000 neurons, 100k synapses, with delays
and STDP): **at least 20x realtime on one CPU thread.** This is a planning figure
to be replaced after the first profile of the M1 kernel. The prior-art search found
no published single-core figure for this network; the nearest published number is
a GPU result for a similar 1000-neuron network (see `references/notes/`), and at
this size a GPU is limited by per-step overhead.

## 5. Risks

| Risk | Mitigation |
|------|------------|
| The original MATLAB and C++ programs are not equivalent, and the published code differs from the paper | Pick one as the reference explicitly (TASK-010) and follow the published replication study's findings |
| Network activity is chaotic: tiny numerical differences diverge | Exact comparison only against our own transcription with identical arithmetic; statistical comparison against everything else |
| The model's headline result may depend on its coarse integration: the techniques survey reports, citing Pauli et al. 2018, that polychronous group counts fell from about 4,300 to 151 at a 0.1 ms step | Keep an original-faithful mode and a separately named accurate mode; measure which results survive (TASK-025) before M3 and M4 build on the neuron update |
| Aplysia validation data may be sparse or only in figures | M4 tasks record the source and extraction method for every target; where no number exists the comparison is qualitative and labelled so |
| Benchmarks on a shared cloud VM are noisy and do not transfer to the M1 | Repeated runs recorded with machine details; M1 runs recorded separately (TASK-018) |
| Scope creep toward a general simulator | Mature simulators already exist; this project implements only what its milestones need |

## 6. Environment

| | Cloud session | Owner's machine |
|---|---|---|
| CPU | 4 vCPU Intel Xeon 2.1 GHz (x86-64, AVX-512), KVM guest | Apple M1 (ARM) |
| Memory | 15 GB | not recorded |
| GPU | none | Apple GPU (unused by this plan) |
| Persistence | Ephemeral: the container was rebuilt during the 2026-11-24 session and installed packages were lost | persistent |

M0 and M1 are machine-independent and fine to do in the cloud. M2 timings must also
be taken on the M1.

## 7. Prior art in brief

Three searches were run on 2026-11-24. The full reports are in `references/notes/`
and were compiled by research sub-agents; they have not been re-read by a second
reader, and many papers were read as abstracts only. Manifest records marked
`opened: false` are leads, not evidence.

**Replications of `spnet`** (`notes/2026-11-24-spnet-replications-and-simulators.md`)

- A dedicated replication study exists (`pauli2018_reproducing`) with open code
  (`inm6_reproducing_polychronization`, MIT), and a second study supplies a
  statistical comparison method and a C implementation (`trensch2018_rigorous`,
  `trensch_rigorous_repo`, GPL-2.0). Both are reported to find the original code
  inconsistent with the paper and numerically fragile. M1 uses them as cross-checks.
- No Numba or Julia port and no official Brian2 or NEST example was found.

**Simulators and speed** (same note)

- Mature simulators cover Izhikevich neurons, STDP and delays (Brian2, GeNN, NEST
  GPU, CARLsim). None is a good fit as a dependency for the core: the report notes
  restrictions on per-synapse delays in the GPU back ends. Brian2 is a candidate
  independent cross-check.
- The nearest published speed figure is 62–72x realtime on a desktop GPU for a
  similar 1000-neuron network (`knight2021_pygenn`). No single-core figure for
  `spnet` was found, and nothing credible on Apple Silicon GPUs.

**Efficient-simulation techniques** (`notes/2026-11-24-virtual-organisms-and-simulation-techniques.md`)

- For a network this size: a fixed-step loop, a ring buffer for delays, and synapses
  in contiguous source-sorted arrays (`brette2007_review`, `pronold2022_parallel_sorting`).
- Two STDP bookkeeping options to compare in TASK-012: an incoming-synapse index
  (GeNN) or deferring the update to the next presynaptic spike (SpiNNaker,
  `knight2016_synapse_centric`).
- Procedural connectivity and exascale layouts are for 10^6 neurons and up: out of scope.

**Virtual organisms** (same note)

- **No virtual Aplysia was found**: no whole-animal simulation, no connectome, no
  whole-nervous-system cell atlas. The closest work is the Aplysia feeding
  neuromechanical models (`websterwood2020_boolean_feeding`,
  `bennington2025_feeding_model`: about 20 Boolean neurons with a body, no learning)
  and a 13-cell feeding-circuit model with reward plasticity
  (`costa2020_feeding_cpg_model`, no body).
- Projects worth imitating: the FlyWire whole-brain model for validation practice
  (a table of predictions against experiments, with limitations stated,
  `shiu2024_flywire_lif`), OpenWorm for packaging, BAAIWorm for closing the loop
  between nervous system and body.
- Open question: the neuron count of Aplysia. The figure of about 20,000 given
  earlier in this project came from memory, and the survey's 8,000–10,000 comes
  from an unopened search snippet (`katz2010_neuronbank`). Neither is sourced yet.

**Aplysia learning models** — search still running when this section was written;
M4 tasks are created from its report.
