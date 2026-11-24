---
id: TASK-027
title: Aplysia habituation protocol
status: To Do
assignee: []
created_date: '2026-11-24T01:22:50Z'
labels: []
milestone: m-4
dependencies:
  - TASK-026
  - TASK-021
references:
  - https://pmc.ncbi.nlm.nih.gov/articles/PMC6632334/
  - https://pmc.ncbi.nlm.nih.gov/articles/PMC434028/
  - https://pubmed.ncbi.nlm.nih.gov/2580065/
  - references/notes/2026-11-24-aplysia-withdrawal-reflex-models.md
priority: high
ordinal: 27000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Habituation is the simplest Aplysia result: homosynaptic depression at the sensory-motor synapse, presynaptic, with recovery (byrne2015_nonassociative, castellucci1974_quantal, gingrich1985_simulation). The protocol script must reproduce the stimulation schedule of a published experiment and compare the decline and recovery with it. Most magnitudes are only in figures, so extraction is part of the task.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 A scripted run of 10 sensory stimuli at 10 s ISI shows EPSP and motor output declining, compared with antonov2010_itm (PMC6632334: text says EPSP decrement approximately paralleled withdrawal; magnitude read from Fig 6B1, method recorded)
- [ ] #2 Recovery after habituation is simulated and compared with the roughly 1 h duration of behavioural habituation in antonov2010_itm; the model value and the source's are both recorded
- [ ] #3 A control with no depression term shows no decrement, and the depression is expressed only through release at the synapse, as castellucci1974_quantal (abstract, PMID 4373738) finds a presynaptic locus
<!-- AC:END -->
