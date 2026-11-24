# Engineering policies

These policies respond to the audit in `docs/plan.md`, section 1.

## Claims must be measured

Any number in the README, docs, commit messages or summaries comes from a recorded run and says where the record is. An unrecorded number cannot be checked. Two precedents: an unmeasured performance table in the README, and a realtime factor overstated 1000x by a unit error ("2080x" was 2.08x).

## Sources

- Nothing is cited unless it is in `references/manifest.jsonl`. This keeps every claim traceable.
- Records with `opened: false` are leads. They may not support a requirement, a parameter value or a validation target, because nobody has read the source.
- Copyrighted material stays in the git-ignored `references/cache/`. The repository is public.

## Work tracking

Tasks live in `backlog/` and are changed only through the `backlog` CLI. Direct edits break metadata and history.

A task is done when:

- its acceptance criteria are met and checked;
- tests pass;
- docs that the change makes untrue are updated.

## Decisions

Choices that constrain later work are recorded with `backlog decision create`, including the alternatives rejected. Examples: reference implementation, numeric precision, integration scheme, GPU backend. A later reader needs the reason and the options that were not taken.

## Correct before fast

An optimisation is accepted only if the oracle equivalence tests still pass. Speed that changes results is a bug.

## Reporting

State failures, skipped steps and unverified items plainly in summaries. "Passes" means it was run. A summary that hides a gap sends the next person to the wrong place.

## Branching and commits

- Work on the designated feature branch.
- No force-push and no history rewriting. The first commit message repeats a wrong figure and cannot be fixed this way; correct it in a later commit and in the docs instead.
- Commit messages describe what changed and why.

## Scope

This project implements what its milestones need. It does not grow into a general-purpose simulator, because mature simulators already exist for that. Work outside the milestones needs a backlog task and a stated reason. Prefer reusing existing tools and cross-checking against them (see `references/notes/`) over rebuilding them.
