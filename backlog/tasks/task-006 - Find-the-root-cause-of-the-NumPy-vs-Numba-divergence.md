---
id: TASK-006
title: Find the root cause of the NumPy vs Numba divergence
status: To Do
assignee: []
created_date: '2026-11-24T00:20:22Z'
labels:
  - correctness
milestone: m-0
dependencies: []
priority: medium
type: bug
ordinal: 6000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
tests/test_neurons.py::TestNumpyNumbaEquivalence only passes because its tolerance was loosened to rtol 1e-3, atol 0.01. Suspected causes, unverified: the Numba kernel is compiled with fastmath, and it promotes dt to float64 where the NumPy path stays in float32.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 The cause is identified and written down in the task notes with evidence
- [ ] #2 The two paths agree to a tolerance justified by that cause, or one path is removed
<!-- AC:END -->
