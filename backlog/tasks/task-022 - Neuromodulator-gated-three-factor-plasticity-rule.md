---
id: TASK-022
title: Neuromodulator-gated (three-factor) plasticity rule
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
  - https://pubmed.ncbi.nlm.nih.gov/6294833/
  - https://pmc.ncbi.nlm.nih.gov/articles/PMC6568722/
  - https://pubmed.ncbi.nlm.nih.gov/12526779/
priority: high
ordinal: 22000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Heterosynaptic facilitation depends on a third signal, a neuromodulator, in addition to pre- and postsynaptic activity. Izhikevich's large-scale model has dopamine-modulated STDP, and his 2007 paper on the distal reward problem gives a small, well-specified experiment to validate against.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 A rule with an eligibility trace gated by a modulator variable is implemented behind the rule interface
- [ ] #2 It reproduces the single-synapse reinforcement experiment of Izhikevich (2007), with the comparison recorded
<!-- AC:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
Aplysia findings (note references/notes/2026-11-24-aplysia-withdrawal-reflex-models.md): sensitization and conditioning are not pair-based STDP. Facilitation is driven by a modulator (5-HT) with no postsynaptic spike needed; Hebb's postulate alone was neither necessary nor sufficient (carew1984_hebb). Conditioning needs presynaptic spikes before the modulator, with the largest effect at a 0.5 s forward ISI and none for simultaneous or backward pairing (hawkins1986_isi). A postsynaptic NMDA-dependent Hebbian term is also required and interacts with the presynaptic one (antonov2003_neuron). The rule should take presynaptic activity, a modulator signal and an optional postsynaptic term as separate inputs.
<!-- SECTION:NOTES:END -->
