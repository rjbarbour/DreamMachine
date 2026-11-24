---
id: TASK-013
title: Statistical validation against the 2006 paper
status: To Do
assignee: []
created_date: '2026-11-24T00:20:26Z'
updated_date: '2026-11-24T00:24:51Z'
labels:
  - science
milestone: m-1
dependencies:
  - TASK-012
references:
  - references/notes/2026-11-24-spnet-replications-and-simulators.md
  - https://pmc.ncbi.nlm.nih.gov/articles/PMC6085985
  - https://pmc.ncbi.nlm.nih.gov/articles/PMC6275234
priority: medium
ordinal: 13000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Matching the oracle shows we implemented spnet.m; matching the paper shows the network behaves as published. The paper reports slow oscillations early in the run, gamma-range rhythms after the weights reorganise, and a characteristic weight distribution.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 A recorded run of at least one hour of model time reports firing rates per population, the power spectrum of population activity over time and the weight histogram
- [ ] #2 Each quantity is compared with the corresponding figure or statement in the paper, and differences are stated
- [ ] #3 Results are also compared with the replication study of Pauli et al. 2018 (firing rates, bimodal weights, gamma peak near 60 Hz or 40 Hz depending on seed) over multiple seeds, using distribution comparisons in the manner of Trensch et al. 2018
<!-- AC:END -->
