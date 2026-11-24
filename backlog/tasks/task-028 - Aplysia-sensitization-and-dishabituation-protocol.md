---
id: TASK-028
title: Aplysia sensitization and dishabituation protocol
status: To Do
assignee: []
created_date: '2026-11-24T01:22:50Z'
labels: []
milestone: m-4
dependencies:
  - TASK-026
  - TASK-021
  - TASK-022
references:
  - https://pmc.ncbi.nlm.nih.gov/articles/PMC6632334/
  - https://pubmed.ncbi.nlm.nih.gov/25031258/
  - https://pmc.ncbi.nlm.nih.gov/articles/PMC4448621/
  - references/notes/2026-11-24-aplysia-withdrawal-reflex-models.md
priority: high
ordinal: 28000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Tail shock drives facilitatory interneurons that release serotonin; the effect on the sensory-motor synapse does not need postsynaptic firing and differs after habituation (byrne2015_nonassociative, antonov2010_itm, zhou2014_pkc). It is the first test of the neuromodulator-gated rule. Pair-based STDP does not represent it; see the note.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 One tail-shock-like modulator event raises the EPSP and lasts minutes; four events (2 s apart) give a longer effect. Compared with antonov2010_itm (PMC6632334): one shock behaviour significant at 2.5 and 17.5 min, about 30 min; four shocks EPSP facilitation significant 2.5-62.5 min. Percent magnitudes are figure-only and extraction is recorded
- [ ] #2 After the habituation protocol, a modulator event restores the response (dishabituation), and facilitation of a depressed synapse is reproduced through a mobilisation route, as in zhou2014_pkc (abstract, PMID 25031258)
- [ ] #3 Facilitation occurs with the postsynaptic cell silenced, and the run is stated to be qualitative for anything beyond the stated time windows
<!-- AC:END -->
