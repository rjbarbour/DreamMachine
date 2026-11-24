---
id: TASK-009
title: 'Oracle: line-by-line NumPy transcription of spnet.m'
status: Done
assignee: []
created_date: '2026-11-24T00:20:24Z'
updated_date: '2026-11-24T00:55:55Z'
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
- [x] #1 Connectivity, delays and the thalamic input sequence can be supplied from outside so runs are comparable across implementations
- [x] #2 Every deviation from spnet.m (for example the random number generator) is listed in the module docstring
<!-- AC:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
dreammachine.spnet.oracle.run_oracle transcribes the spnet.m loop (commit 237d113). Connectivity, delays and the input sequence are supplied by the caller. Deviations are listed in the module docstring. Reviewed line by line against spnet.m by the main session; not yet compared with a run of the original (TASK-010).
<!-- SECTION:FINAL_SUMMARY:END -->
