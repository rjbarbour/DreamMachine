# Testing principles

These rules exist because an earlier iteration passed tests by loosening them (see `docs/plan.md`, section 1).

## Test levels

| Level | Purpose |
|-------|---------|
| Unit | One function or class in isolation. Fast, run on every change. |
| Oracle equivalence | `dreammachine.spnet.oracle` is a slow, obviously correct transcription of the reference model. The fast kernel `dreammachine.spnet.kernel` must match it exactly. |
| Property-based (hypothesis) | Structural invariants over many generated inputs, such as "no duplicate targets" and "weights stay in bounds". Example tests miss these cases. |
| Statistical validation | Firing rates, weight histogram and spectra compared with published results over several seeds. One seed proves nothing about a chaotic system. |
| Benchmarks | Recorded to a results file, never asserted in unit tests. |

## Exact and statistical comparison

The network is chaotic: a one-bit difference grows until trajectories differ. Bit-exact comparison is therefore meaningful only between implementations with identical arithmetic and operation order, such as oracle and kernel. Everything else is compared through distributions: firing rates, weight histogram, spectra.

## Tolerance policy

A tolerance may be loosened only together with a written root cause, in the test's comment and in the backlog task. A looser tolerance without a cause hides a bug. On 2026-01-31 two tests were made to pass this way (TASK-006).

## Reproducibility

- Every test involving randomness fixes its seed through `numpy.random.Generator`. A failure must be repeatable.
- The dtype is float64 unless a decision record says otherwise. Mixed precision changes results.
- Numba `fastmath` is off for anything compared exactly. It reorders operations and breaks exact equality.
- Thread count is recorded with every benchmark. Timings are meaningless without it.

## What a test may not do

- Assert performance numbers. Timings vary between machines and runs, so tests built on them are flaky.
- Depend on network access. Tests must run offline.
- Depend on files in `references/cache/` without skipping cleanly when they are absent. The cache is git-ignored, so a clean checkout does not have it.

## How to run

```bash
python -m pytest tests/ -q
```

Mark slow tests so they can be selected or skipped. Keep each test file under about 90 seconds. Longer runs belong in experiments, not in the test suite.

## Requirement traceability

Each requirement ID in `docs/spec.md` names the test or experiment that verifies it. A requirement with no named check is unverified and is reported as such. When a test is renamed or removed, update the spec in the same change.

## Reporting results

"Passes" means the suite was run and finished green. If tests were skipped, deselected or not run, say so. See `docs/policies.md`.
