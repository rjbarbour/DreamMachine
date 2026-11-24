---
id: TASK-021
title: Short-term synaptic plasticity rule
status: To Do
assignee: []
created_date: '2026-11-24T00:20:30Z'
labels:
  - science
milestone: m-3
dependencies:
  - TASK-019
priority: high
ordinal: 21000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Use-dependent depression and facilitation on the timescale of seconds is absent from the simulator. Izhikevich's own large-scale model includes it, and it is the class of mechanism behind synaptic depression during habituation.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 A depression/facilitation synapse model is implemented behind the rule interface
- [ ] #2 It reproduces a published paired-pulse or train response, with the source cited and the comparison recorded
<!-- AC:END -->
