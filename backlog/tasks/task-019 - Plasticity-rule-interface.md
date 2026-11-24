---
id: TASK-019
title: Plasticity rule interface
status: To Do
assignee: []
created_date: '2026-11-24T00:20:29Z'
labels:
  - science
milestone: m-3
dependencies:
  - TASK-012
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
