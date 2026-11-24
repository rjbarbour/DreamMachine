---
id: TASK-017
title: 'Decision record: numeric precision, fastmath and threading'
status: To Do
assignee: []
created_date: '2026-11-24T00:20:28Z'
updated_date: '2026-11-24T00:35:41Z'
labels:
  - perf
milestone: m-2
dependencies: []
references:
  - references/notes/2026-11-24-virtual-organisms-and-simulation-techniques.md
priority: medium
ordinal: 17000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
The prototype uses float32, fastmath and a parallel loop over neurons without a stated reason. These choices trade reproducibility against speed and affect whether results can be compared across x86, ARM and GPU.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 A backlog decision records the choice for each of the three, with a measurement supporting it
<!-- AC:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
Relevant sources from the techniques survey: Hopkins and Furber 2015 and Hopkins et al. 2020 on fixed-point and reduced-precision Izhikevich solvers (abstracts only were read); Pauli et al. 2018 on divergence caused by operation order alone.
<!-- SECTION:NOTES:END -->
