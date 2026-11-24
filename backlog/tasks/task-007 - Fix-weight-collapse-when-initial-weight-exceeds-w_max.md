---
id: TASK-007
title: Fix weight collapse when initial weight exceeds w_max
status: Done
assignee: []
created_date: '2026-11-24T00:20:23Z'
updated_date: '2026-11-24T00:53:46Z'
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
- [x] #1 Constructing synapses with weights outside [w_min, w_max] raises an error
- [x] #2 The example uses one consistent weight scale and its weight change is explained by STDP, not by clamping
- [x] #3 A test covers both points
<!-- AC:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
STDPSynapses raises ValueError for weights outside [w_min, w_max] or non-finite. Example uses bounds [0, 30] with weights at 15; recorded run: mean weight 15.000 to 14.807. Tests added for rejection and acceptance (commit 38fe091).
<!-- SECTION:FINAL_SUMMARY:END -->
