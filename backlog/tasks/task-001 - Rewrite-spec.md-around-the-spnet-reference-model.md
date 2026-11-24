---
id: TASK-001
title: Rewrite spec.md around the spnet reference model
status: Done
assignee: []
created_date: '2026-11-24T00:20:20Z'
updated_date: '2026-11-24T01:07:22Z'
labels:
  - docs
milestone: m-0
dependencies: []
references:
  - https://www.izhikevich.org/publications/spnet.htm
  - docs/plan.md
priority: high
ordinal: 1000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
The original spec was written without the source material: the fetch of izhikevich.org failed on 2026-01-31 and the requirements were written from memory. It specifies a generic network and omits what defines Izhikevich's model (inhibitory population, conduction delays, the weight-derivative update). The source page and spnet.m were retrieved on 2026-11-24; parameters are summarised in docs/plan.md.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 spec.md names Izhikevich (2006) spnet as the M1 reference and lists every model parameter with its source line in spnet.m
- [x] #2 Every requirement has an ID and a named verification method (test name, validation experiment or benchmark)
- [x] #3 Requirements not yet implemented are marked as not implemented
<!-- AC:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
docs/spec.md rewritten around the spnet reference model: parameter table with spnet.m line numbers, requirement IDs each naming a test, script or validation doc, and a section listing what is not implemented. Verification names were checked against tests/ by reading; SP-PLS-02 has no direct test and says so.
<!-- SECTION:FINAL_SUMMARY:END -->
