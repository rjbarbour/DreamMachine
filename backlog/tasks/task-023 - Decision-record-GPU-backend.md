---
id: TASK-023
title: 'Decision record: GPU backend'
status: To Do
assignee: []
created_date: '2026-11-24T00:20:31Z'
updated_date: '2026-11-24T00:24:52Z'
labels:
  - perf
milestone: m-5
dependencies:
  - TASK-016
references:
  - references/notes/2026-11-24-spnet-replications-and-simulators.md
priority: low
ordinal: 23000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Options discussed with the owner on 2026-11-24: MLX on the Mac, PyTorch (MPS locally, CUDA on rented GPUs) and purpose-built CUDA simulators such as GeNN or CARLsim. The view at that time was to skip MLX and not start GPU work until a measured need exists.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 A backlog decision states the chosen backend, the benchmark that triggered the work and the alternatives rejected
<!-- AC:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
Prior-art search 2026-11-24 found no credible work running this kind of network (delays plus STDP) on Apple Silicon GPUs, and no simulator listing a Metal or MPS backend. Brian2CUDA handles heterogeneous delays but reports them as slow in combination with STDP; Brian2GeNN does not support them.
<!-- SECTION:NOTES:END -->
