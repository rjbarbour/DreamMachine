---
id: TASK-022
title: Neuromodulator-gated (three-factor) plasticity rule
status: To Do
assignee: []
created_date: '2026-11-24T00:20:30Z'
labels:
  - science
milestone: m-3
dependencies:
  - TASK-019
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
