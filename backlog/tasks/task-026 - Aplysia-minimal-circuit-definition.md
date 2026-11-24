---
id: TASK-026
title: Aplysia minimal circuit definition
status: To Do
assignee: []
created_date: '2026-11-24T01:22:32Z'
labels: []
milestone: m-4
dependencies:
  - TASK-019
  - TASK-021
references:
  - https://pmc.ncbi.nlm.nih.gov/articles/PMC6782414/
  - https://pubmed.ncbi.nlm.nih.gov/9084594/
  - https://pmc.ncbi.nlm.nih.gov/articles/PMC4448621/
  - references/notes/2026-11-24-aplysia-withdrawal-reflex-models.md
priority: high
ordinal: 26000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
M4 needs a small, sourced circuit before any protocol can be scripted. Plan section 3 principle 4 says the work is in synapses, not neuron count. Published descriptions cover LE sensory, LFS motor, L29/L30 interneurons and facilitatory input (antonov1999_monosynaptic, lieb1997_siphon_circuit, byrne2015_nonassociative); no abdominal-ganglion neuron count was found, so the circuit is a chosen subset and says so.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 A circuit file lists each cell type, count and connection with its manifest key; counts are LE about 5 and LFS 3, citing antonov1999_monosynaptic (PMC6782414 text), or the deviation is stated
- [ ] #2 With sensory input only, the LE-to-LFS monosynaptic path gives about one-third of the modelled motor drive, compared with antonov1999_monosynaptic; the result is recorded by the harness
- [ ] #3 Every omitted element (L7, L34, electrical coupling) is listed with the reason; lieb1997_siphon_circuit reports L29-L30 coupling had little effect (abstract, PMID 9084594)
<!-- AC:END -->
