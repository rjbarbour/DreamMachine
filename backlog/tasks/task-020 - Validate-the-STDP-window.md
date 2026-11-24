---
id: TASK-020
title: Validate the STDP window
status: To Do
assignee: []
created_date: '2026-11-24T00:20:29Z'
labels:
  - science
milestone: m-3
dependencies:
  - TASK-019
priority: medium
ordinal: 20000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
No test currently measures the learning window itself; the existing tests only check the sign of the change.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 An experiment sweeps the pre/post interval and compares the measured weight change with the analytic exponential window, with the result recorded
<!-- AC:END -->
