---
id: TASK-012
title: Simulation kernel with conduction delays and spnet STDP
status: To Do
assignee: []
created_date: '2026-11-24T00:20:25Z'
updated_date: '2026-11-24T00:35:41Z'
labels:
  - correctness
milestone: m-1
dependencies:
  - TASK-009
  - TASK-011
references:
  - references/notes/2026-11-24-spnet-replications-and-simulators.md
  - https://pmc.ncbi.nlm.nih.gov/articles/PMC6299048/
  - references/notes/2026-11-24-virtual-organisms-and-simulation-techniques.md
priority: high
ordinal: 12000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
This replaces the current simulator loop for the reference model. It must reproduce the oracle exactly; speed is addressed in M2, but the data layout (fixed fan-out arrays, delay ring buffer) should be chosen so it can be compiled and later moved to a GPU. Only excitatory synapses are plastic.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Spike trains and final weights match the oracle exactly for the same seed over at least 10 s of model time
- [ ] #2 Inhibitory weights never change and excitatory weights stay within [0, 10], checked by tests
- [ ] #3 The architecture document describes the data layout and the step order
<!-- AC:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
Layout to consider (from GeNN, Knight and Nowotny 2018, per the prior-art note): [N, fan-out] arrays for target, weight and delay with rows sorted by delay, a ring buffer of max-delay slots for delivery, and a column-major incoming index for potentiation on postsynaptic spikes.

Second layout option from the techniques survey (same date): keep synapses only in source-sorted contiguous arrays, deliver into a per-neuron ring buffer of summed input (as NEST does, per Pronold et al. 2022), and defer the potentiation update until the next presynaptic spike arrives using a short postsynaptic spike history (the SpiNNaker scheme, Knight and Furber 2016). This avoids the incoming-synapse index. Compare both options before fixing the layout; note that spnet applies potentiation at the postsynaptic spike, so a deferred scheme must be shown to give identical weights at the once-per-second update.
<!-- SECTION:NOTES:END -->
