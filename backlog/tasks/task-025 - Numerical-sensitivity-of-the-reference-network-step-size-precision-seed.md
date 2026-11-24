---
id: TASK-025
title: Numerical sensitivity of the reference network (step size, precision, seed)
status: To Do
assignee: []
created_date: '2026-11-24T00:35:40Z'
labels:
  - science
milestone: m-1
dependencies:
  - TASK-012
references:
  - references/notes/2026-11-24-virtual-organisms-and-simulation-techniques.md
  - https://pmc.ncbi.nlm.nih.gov/articles/PMC6085985
  - https://pmc.ncbi.nlm.nih.gov/articles/PMC6275234
priority: medium
ordinal: 25000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
The reference model integrates with a 1 ms step (two 0.5 ms half-steps for v). The prior-art search reports, citing Pauli et al. 2018, that this scheme is numerically unstable and that the number of polychronous groups fell from about 4,300 to 151 when the step was reduced to 0.1 ms, which means the model's headline result depends on its numerics. Trensch et al. 2018 report membrane potentials far above the spike peak under the original scheme. We need to know which of our results survive a more accurate integration before building learning experiments on the same neuron update.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 The kernel has an original-faithful mode and a mode with configurable step and float64 arithmetic, kept as separately named models
- [ ] #2 Firing rates, rhythm and weight distribution are reported for the original scheme and for at least two smaller steps, over several seeds
- [ ] #3 A backlog decision records which integration scheme later milestones (M3, M4) use and why
<!-- AC:END -->
