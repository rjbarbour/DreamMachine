---
id: TASK-016
title: Scaling study and memory model
status: To Do
assignee: []
created_date: '2026-11-24T00:20:27Z'
updated_date: '2026-11-24T01:07:22Z'
labels:
  - perf
milestone: m-2
dependencies:
  - TASK-015
references:
  - references/notes/2026-11-24-virtual-organisms-and-simulation-techniques.md
priority: medium
ordinal: 16000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Scalable has to be shown, not asserted. The earlier README claimed linear scaling without a measurement.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Recorded runs at 1k, 10k and 100k neurons with fixed fan-out report wall time, realtime factor and peak memory
- [ ] #2 Bytes per synapse and per neuron are stated and agree with measured memory
- [ ] #3 The network size at which the kernel drops below realtime is reported for each machine tested
<!-- AC:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
Out of scope per the techniques survey: procedural connectivity (Knight and Nowotny 2021) and the NEST exascale layouts target 10^6 neurons and above.

2026-11-24 measured (record bench-spnet-scaling-20261124T010600Z.json, one run per size, 20 s model time): 1k 127x realtime, 177 MB peak RSS; 10k 17.4x, 328 MB, 344 bytes/synapse; 100k 1.46x, 1416 MB, 148 bytes/synapse. No size fell below realtime, so the crossover is not yet found. Caveat: input is one pulse per ms to a random neuron, so mean rates were 3.3, 0.099 and 0.010 Hz; larger networks were nearly silent and the figures flatter them. build_network at 100k took 101 s. Only the cloud container was measured. Bytes per neuron not stated separately; criteria not checked.
<!-- SECTION:NOTES:END -->
