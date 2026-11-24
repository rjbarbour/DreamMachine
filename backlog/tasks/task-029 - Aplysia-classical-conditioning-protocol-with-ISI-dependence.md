---
id: TASK-029
title: Aplysia classical conditioning protocol with ISI dependence
status: To Do
assignee: []
created_date: '2026-11-24T01:22:51Z'
labels: []
milestone: m-4
dependencies:
  - TASK-026
  - TASK-021
  - TASK-022
references:
  - https://pmc.ncbi.nlm.nih.gov/articles/PMC6568722/
  - https://pubmed.ncbi.nlm.nih.gov/6294833/
  - https://pubmed.ncbi.nlm.nih.gov/9334306/
  - https://pubmed.ncbi.nlm.nih.gov/12526779/
  - references/notes/2026-11-24-aplysia-withdrawal-reflex-models.md
priority: high
ordinal: 29000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Conditioning in Aplysia depends on CS-US timing: facilitation is amplified when sensory spikes precede the modulator (hawkins1983_amplification), with a postsynaptic NMDA-dependent component (murphy1997_ltp, antonov2003_neuron). The ISI curve is the main validation target and a test of the three-factor rule. Plain pair-based STDP would not produce this curve (see note).
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 An ISI sweep (CS leading US by 0.5, 1, 2, 5, 10 s; simultaneous; US leading by 0.5, 1.0, 1.5 s) is run; the model shows the largest effect at 0.5 s, a smaller one at 1.0 s and none at the others, as in hawkins1986_isi (PMC6568722, abstract text; magnitudes not read)
- [ ] #2 Unpaired and extra-US (contingency) controls give less facilitation than paired training, as in hawkins1986_isi and hawkins1983_amplification (PMID 6294833)
- [ ] #3 With the postsynaptic Hebbian term disabled, conditioning is reduced but not abolished, qualitatively matching murphy1997_ltp (PMID 9334306); the text says the comparison is qualitative
<!-- AC:END -->
