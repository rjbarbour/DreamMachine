---
id: TASK-011
title: Reference network builder (800 RS + 200 FS, fixed fan-out, delays)
status: Done
assignee: []
created_date: '2026-11-24T00:20:25Z'
updated_date: '2026-11-24T00:55:55Z'
labels:
  - correctness
milestone: m-1
dependencies: []
priority: high
ordinal: 11000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
The current builder makes a single all-excitatory population with random sparse connectivity and no delays. spnet has 800 regular-spiking and 200 fast-spiking neurons, exactly 100 outgoing synapses per neuron with no duplicate targets, inhibitory neurons project only to excitatory ones, excitatory delays are uniform over 1-20 ms and inhibitory delays are 1 ms, initial weights are +6 and -5.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Builder output satisfies each structural property above, checked by property-based tests
- [x] #2 Fan-out, population sizes and delay range are parameters so the same builder serves the scaling study
<!-- AC:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
dreammachine.spnet.network.build_network and make_inputs (commit 237d113). Structural properties are checked by example-based tests in tests/test_spnet_network.py; sizes are parameters. Not done as specified: the first acceptance criterion asks for property-based tests (hypothesis) and the tests are example-based, so that criterion is left unchecked.
<!-- SECTION:FINAL_SUMMARY:END -->
