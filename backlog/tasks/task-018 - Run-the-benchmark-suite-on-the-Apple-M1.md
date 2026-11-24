---
id: TASK-018
title: Run the benchmark suite on the Apple M1
status: To Do
assignee: []
created_date: '2026-11-24T00:20:28Z'
labels:
  - perf
milestone: m-2
dependencies:
  - TASK-004
  - TASK-015
priority: medium
ordinal: 18000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
The cloud container is a 4-vCPU x86 virtual machine with AVX-512 on shared hardware; the owner's development machine is an Apple M1 (ARM). Timings do not transfer between them. This needs a local session or a Remote Control connection to the Mac.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Harness records from the M1 are committed alongside the cloud records
<!-- AC:END -->
