---
id: TASK-007
title: Fix weight collapse when initial weight exceeds w_max
status: To Do
assignee: []
created_date: '2026-11-24T00:20:23Z'
labels:
  - correctness
milestone: m-0
dependencies: []
priority: high
type: bug
ordinal: 7000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
STDPParams defaults to w_max=1.0 while examples/basic_simulation.py starts weights at 15. The first potentiation of any synapse clamps it to 1.0, so the example reports mean weight falling from 15.0 to 1.12 and this was presented as STDP working. Weight scale and bounds must be consistent with the synaptic current scale.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Constructing synapses with weights outside [w_min, w_max] raises an error
- [ ] #2 The example uses one consistent weight scale and its weight change is explained by STDP, not by clamping
- [ ] #3 A test covers both points
<!-- AC:END -->
