---
id: TASK-006
title: Find the root cause of the NumPy vs Numba divergence
status: Done
assignee: []
created_date: '2026-11-24T00:20:22Z'
updated_date: '2026-11-24T00:53:46Z'
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
- [x] #1 The cause is identified and written down in the task notes with evidence
- [x] #2 The two paths agree to a tolerance justified by that cause, or one path is removed
<!-- AC:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Root cause: the Numba kernel computed in float64 because bare float literals and dt are float64 in Numba, while the NumPy path stays float32 under NumPy 2 promotion. Evidence: max |dv| after 100 steps was 0.01174 with fastmath and parallel in all four on/off combinations, and exactly 0 after casting constants to float32. Neither fastmath nor parallel was the cause. The equivalence test now asserts exact equality; fastmath is off (commit 38fe091).
<!-- SECTION:FINAL_SUMMARY:END -->
