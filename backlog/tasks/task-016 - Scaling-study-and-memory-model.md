---
id: TASK-016
title: Scaling study and memory model
status: To Do
assignee: []
created_date: '2026-11-24T00:20:27Z'
labels:
  - perf
milestone: m-2
dependencies:
  - TASK-015
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
