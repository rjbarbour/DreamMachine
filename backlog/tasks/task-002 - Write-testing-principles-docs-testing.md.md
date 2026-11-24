---
id: TASK-002
title: Write testing principles (docs/testing.md)
status: To Do
assignee: []
created_date: '2026-11-24T00:20:20Z'
labels:
  - docs
milestone: m-0
dependencies: []
priority: high
ordinal: 2000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
The project brief asked for testing principles and none were written. A concrete failure already happened: on 2026-01-31 two tests failed and the tolerances were loosened (rtol 1e-5 to 1e-3, atol 0.01) until they passed, with no root cause recorded.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Defines the test levels used: unit, oracle equivalence, property-based, statistical validation, benchmark
- [ ] #2 States a tolerance policy: a tolerance may only be loosened together with a written root cause
- [ ] #3 States the reproducibility policy: seeds, dtype and thread count are fixed and recorded for every test that involves randomness
<!-- AC:END -->
