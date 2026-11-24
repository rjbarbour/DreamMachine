---
id: TASK-005
title: 'Continuous integration: lint, types, tests'
status: To Do
assignee: []
created_date: '2026-11-24T00:20:22Z'
labels:
  - infra
milestone: m-0
dependencies: []
priority: medium
ordinal: 5000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Nothing checks the branch automatically. ruff and mypy are configured in pyproject.toml but have never been run against the code.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 A GitHub Actions workflow runs ruff, mypy and pytest on every push and pull request
- [ ] #2 ruff and mypy pass on the current code or the exceptions are listed explicitly in pyproject.toml
<!-- AC:END -->
