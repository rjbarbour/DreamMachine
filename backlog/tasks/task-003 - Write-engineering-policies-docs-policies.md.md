---
id: TASK-003
title: Write engineering policies (docs/policies.md)
status: Done
assignee: []
created_date: '2026-11-24T00:20:21Z'
updated_date: '2026-11-24T00:53:45Z'
labels:
  - docs
milestone: m-0
dependencies: []
priority: medium
ordinal: 3000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
The project brief asked for policies. The README shipped a performance table that was never measured and the first commit message says about 2000x realtime where the true figure was about 2x (the example divided milliseconds by seconds). A written rule is needed so this cannot recur.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 States that any number in README, docs or commit messages must come from a recorded run and cite it
- [x] #2 Defines the definition of done for a task and how decisions are recorded (backlog decisions)
- [x] #3 Defines the branch, commit and review conventions
<!-- AC:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
docs/policies.md written (commit bf589df): measured claims, sources, work tracking and definition of done, decision records, reporting, branching, scope.
<!-- SECTION:FINAL_SUMMARY:END -->
