---
id: TASK-030
title: 'Aplysia validation table: predictions vs published measurements'
status: To Do
assignee: []
created_date: '2026-11-24T01:22:51Z'
labels: []
milestone: m-4
dependencies:
  - TASK-027
  - TASK-028
  - TASK-029
references:
  - https://doi.org/10.1038/s41586-024-07763-9
  - references/notes/2026-11-24-aplysia-withdrawal-reflex-models.md
priority: medium
ordinal: 30000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
M4's exit criterion is a comparison with published measurements, with differences stated. The FlyWire model (shiu2024_flywire_lif) is the format to imitate: a table of predictions against experiments with limitations listed. Many Aplysia numbers are only in figures, so each row records whether the target is text or figure.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 A table has one row per protocol (habituation, sensitization, dishabituation, ISI conditioning), the model value, the published value, its source key, and 'text' or 'figure' for the target
- [ ] #2 Rows without a numeric source are labelled qualitative, and no row cites a manifest record with opened false
- [ ] #3 A limitations section lists at least what is omitted (spike broadening, kinase cascades, LTF, L7, electrical coupling) and what cannot be compared
<!-- AC:END -->
