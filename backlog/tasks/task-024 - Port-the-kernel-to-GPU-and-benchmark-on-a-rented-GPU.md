---
id: TASK-024
title: Port the kernel to GPU and benchmark on a rented GPU
status: To Do
assignee: []
created_date: '2026-11-24T00:20:31Z'
labels:
  - perf
milestone: m-5
dependencies:
  - TASK-023
priority: low
ordinal: 24000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Only to be started when the gate in the milestone description is met.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 The GPU kernel matches the oracle within the tolerance set by the precision decision
- [ ] #2 Harness records compare CPU and GPU across network sizes, including the size below which the CPU is faster
<!-- AC:END -->
