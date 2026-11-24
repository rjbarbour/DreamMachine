---
id: TASK-004
title: Benchmark and experiment recording harness
status: Done
assignee: []
created_date: '2026-11-24T00:20:21Z'
updated_date: '2026-11-24T01:07:21Z'
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
- [x] #1 One command runs a named benchmark with repeats and writes a JSON record with git SHA, machine, CPU model, thread count, package versions, parameters and timings
- [ ] #2 Records are committed under a tracked directory and README numbers are generated from them
- [x] #3 The current simulator baseline (1000 neurons, 100k synapses: 0.23x realtime on 2026-11-24) is re-recorded through the harness
<!-- AC:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
scripts/bench.py provides spnet-reference, prototype-baseline and spnet-scaling; each writes one JSON record (git SHA, UTC time, CPU model, core count, Numba threads, versions, parameters, repeats, every wall time, min/median) to benchmarks/records/. Records bench-spnet-reference-20261124T010156Z.json, bench-prototype-baseline-20261124T010209Z.json, bench-spnet-scaling-20261124T010600Z.json; summary in docs/validation/benchmarks.md. Not met: criterion 2 in part. Records are tracked, but the README figure was copied by hand, not generated. Criterion 3 re-recorded the legacy simulator: 4.7-4.9x realtime with 12.0 drive to 20 neurons after JIT warm-up, which differs from the earlier unrecorded 0.23x; the cause of the difference was not investigated. Only the cloud container was measured.
<!-- SECTION:FINAL_SUMMARY:END -->
