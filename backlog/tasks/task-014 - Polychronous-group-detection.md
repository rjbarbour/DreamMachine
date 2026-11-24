---
id: TASK-014
title: Polychronous group detection
status: To Do
assignee: []
created_date: '2026-11-24T00:20:26Z'
updated_date: '2026-11-24T00:24:51Z'
labels:
  - science
milestone: m-1
dependencies:
  - TASK-013
references:
  - references/notes/2026-11-24-spnet-replications-and-simulators.md
priority: low
ordinal: 14000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
The headline result of the 2006 paper is the number of polychronous groups (1973 found after 18000 s, 211 with shuffled synapses, per the spnet page). Reproducing it is the strongest replication claim but is not needed for later milestones.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Group search ported from polygroup.m / polychron.m and run on a trained network and on its shuffled control
- [ ] #2 Group counts are reported next to the published ones
<!-- AC:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
Pauli et al. 2018 report that group counts depend strongly on the analysis threshold (as summarised in the prior-art note), so the threshold must be stated with any count.
<!-- SECTION:NOTES:END -->
