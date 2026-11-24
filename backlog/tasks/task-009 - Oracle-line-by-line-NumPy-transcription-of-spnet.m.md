---
id: TASK-009
title: 'Oracle: line-by-line NumPy transcription of spnet.m'
status: To Do
assignee: []
created_date: '2026-11-24T00:20:24Z'
labels:
  - correctness
milestone: m-1
dependencies: []
references:
  - https://www.izhikevich.org/publications/spnet.m
priority: high
ordinal: 9000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
We need an implementation that is obviously correct before we write one that is fast. The oracle follows spnet.m statement by statement (1 ms step with two 0.5 ms half-steps for v, spike reset at the start of the step, per-second weight update s = clip(0.01 + s + sd, 0, 10), sd *= 0.9, STDP trace decay 0.95 per ms) and makes no attempt at speed.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Connectivity, delays and the thalamic input sequence can be supplied from outside so runs are comparable across implementations
- [ ] #2 Every deviation from spnet.m (for example the random number generator) is listed in the module docstring
<!-- AC:END -->
