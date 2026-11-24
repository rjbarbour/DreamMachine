---
id: TASK-004
title: Benchmark and experiment recording harness
status: To Do
assignee: []
created_date: '2026-11-24T00:20:21Z'
labels:
  - infra
milestone: m-0
dependencies: []
priority: high
ordinal: 4000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
The brief asked for recorded and analysed execution. Today timings are printed by an example script and copied by hand. Note that .gitignore currently ignores results/ and *.npz, which would hide recorded results.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 One command runs a named benchmark with repeats and writes a JSON record with git SHA, machine, CPU model, thread count, package versions, parameters and timings
- [ ] #2 Records are committed under a tracked directory and README numbers are generated from them
- [ ] #3 The current simulator baseline (1000 neurons, 100k synapses: 0.23x realtime on 2026-11-24) is re-recorded through the harness
<!-- AC:END -->
