---
id: TASK-019
title: Plasticity rule interface
status: To Do
assignee: []
created_date: '2026-11-24T00:20:29Z'
updated_date: '2026-11-24T01:22:59Z'
labels:
  - science
milestone: m-3
dependencies:
  - TASK-012
references:
  - references/notes/2026-11-24-aplysia-withdrawal-reflex-models.md
priority: high
ordinal: 19000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Pair STDP is hard-wired into the synapse class. The learning experiments planned for Aplysia rely on rule classes other than pair STDP (see docs/prior-art.md), so rules must be swappable without rewriting the kernel.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 A rule declares its per-synapse and per-neuron state and its update functions, and the compiled kernel runs any rule that follows the interface
- [ ] #2 The spnet STDP rule is re-expressed through the interface with unchanged results
<!-- AC:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
Aplysia findings: M4 needs short-term depression, modulator-gated facilitation and a three-factor conditioning rule, not only pair STDP. The interface should let a rule read a per-synapse state (release resources) and a modulator input, besides pre/post spike traces.
<!-- SECTION:NOTES:END -->
