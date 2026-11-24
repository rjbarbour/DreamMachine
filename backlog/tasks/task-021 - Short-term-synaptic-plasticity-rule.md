---
id: TASK-021
title: Short-term synaptic plasticity rule
status: To Do
assignee: []
created_date: '2026-11-24T00:20:30Z'
updated_date: '2026-11-24T01:22:59Z'
labels:
  - science
milestone: m-3
dependencies:
  - TASK-019
references:
  - https://pmc.ncbi.nlm.nih.gov/articles/PMC6632334/
  - https://pubmed.ncbi.nlm.nih.gov/2580065/
  - https://pubmed.ncbi.nlm.nih.gov/25031258/
  - https://modeldb.science/152200
priority: high
ordinal: 21000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Use-dependent depression and facilitation on the timescale of seconds is absent from the simulator. Izhikevich's own large-scale model includes it, and it is the class of mechanism behind synaptic depression during habituation.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 A depression/facilitation synapse model is implemented behind the rule interface
- [ ] #2 It reproduces a published paired-pulse or train response, with the source cited and the comparison recorded
<!-- AC:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
Aplysia findings (note references/notes/2026-11-24-aplysia-withdrawal-reflex-models.md): habituation is presynaptic depression with depletion of releasable pools and recovery (gingrich1985_simulation, castellucci1974_quantal). A published release model with code exists: ModelDB 152200, zhou2014_modeldb (C/C++, licence not checked), useful as a cross-check. Protocol target: 10 stimuli at 10 s ISI, habituation lasting about 1 h (antonov2010_itm); EPSP magnitudes figure-only.
<!-- SECTION:NOTES:END -->
