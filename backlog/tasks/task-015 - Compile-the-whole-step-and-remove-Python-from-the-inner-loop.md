---
id: TASK-015
title: Compile the whole step and remove Python from the inner loop
status: To Do
assignee: []
created_date: '2026-11-24T00:20:27Z'
updated_date: '2026-11-24T01:07:22Z'
labels:
  - perf
milestone: m-2
dependencies:
  - TASK-012
references:
  - references/notes/2026-11-24-spnet-replications-and-simulators.md
priority: high
ordinal: 15000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Measured baseline of the current simulator on 2026-11-24: 1000 neurons and 100k synapses run at 0.23x realtime with no delays, because plasticity and spike recording are per-spike Python loops. Provisional target for the reference network: at least 20x realtime on one thread; revise it after the first profile and after reading the published figures in docs/prior-art.md.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 A profile of the M1 kernel is recorded before and after the change
- [ ] #2 The optimised kernel still matches the oracle exactly
- [ ] #3 The recorded realtime factor for the reference network meets the target in force, or the shortfall is explained
<!-- AC:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
Published comparison point (per the prior-art note): PyGeNN 2021 reports 62-72x realtime on a desktop GPU for an 800+200 Izhikevich network with dopamine-modulated STDP. No published single-core figure for spnet was found.

2026-11-24 measured (scripts/bench.py, record bench-spnet-reference-20261124T010156Z.json): reference network 10 s model time in 0.111-0.123 s over 7 repeats after warm-up, 81.5-89.9x realtime on one thread (kernel is serial), above the provisional 20x target. No before/after profile of the kernel was recorded, so criteria 1 and 3 are not checked; the kernel as written is already compiled end to end.
<!-- SECTION:NOTES:END -->
