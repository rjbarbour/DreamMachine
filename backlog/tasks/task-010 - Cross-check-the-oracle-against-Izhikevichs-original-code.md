---
id: TASK-010
title: Cross-check the oracle against Izhikevich's original code
status: To Do
assignee: []
created_date: '2026-11-24T00:20:24Z'
updated_date: '2026-11-24T00:24:51Z'
labels:
  - correctness
milestone: m-1
dependencies:
  - TASK-009
references:
  - https://www.izhikevich.org/publications/spnet.htm
  - references/notes/2026-11-24-spnet-replications-and-simulators.md
  - https://pmc.ncbi.nlm.nih.gov/articles/PMC6085985
  - https://github.com/INM-6/reproducing-polychronization
  - https://github.com/gtrensch/RigorousNeuralNetworkSimulations
priority: high
ordinal: 10000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
A transcription can carry a misreading. The original spnet.cpp (or spnet.m under GNU Octave) should be run with the same connectivity and input sequence as the oracle. The spnet page itself warns that the MATLAB and C versions are similar but not equivalent, and a published replication study reported pitfalls in the original code; see docs/prior-art.md.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 The original code runs in this environment with connectivity and input exported from or imported to the oracle
- [ ] #2 Spike trains are compared for at least 10 s of model time and any difference is explained
- [ ] #3 The reference implementation (spnet.m or spnet.cpp) is chosen explicitly and the choice recorded as a backlog decision, taking into account the differences reported by Pauli et al. 2018 (order of the 0.9 decay relative to the weight update; fixed versus random delay assignment)
<!-- AC:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
Prior-art search 2026-11-24: Pauli, Weidel, Kunkel and Morrison (2018, Front. Neuroinform. 12:46) report that the downloadable C++ does not match the paper and differs from the MATLAB, and that bitwise reproduction needed many fixes. Their NEST-based code (MIT) and the Trensch et al. C implementation (GPL-2.0) are candidate cross-checks. Read both papers before starting.
<!-- SECTION:NOTES:END -->
