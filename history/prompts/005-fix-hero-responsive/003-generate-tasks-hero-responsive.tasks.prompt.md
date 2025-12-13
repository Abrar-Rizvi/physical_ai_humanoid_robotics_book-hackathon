---
id: 003
title: Generate Tasks for Hero Responsive Fix
stage: tasks
date: 2025-12-11
surface: agent
model: claude-opus-4-5-20251101
feature: 005-fix-hero-responsive
branch: 005-fix-hero-responsive
user: system
command: /sp.tasks
labels: ["tasks", "responsive", "css", "mobile", "hero-section"]
links:
  spec: specs/005-fix-hero-responsive/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/005-fix-hero-responsive/tasks.md
  - history/prompts/005-fix-hero-responsive/003-generate-tasks-hero-responsive.tasks.prompt.md
tests:
  - Manual browser testing at multiple viewports (no automated tests)
---

## Prompt

/sp.tasks

Generate implementation tasks for the Hero Section responsive image fix based on the plan.md and spec.md design documents.

## Response snapshot

Generated comprehensive tasks.md with 28 tasks organized by user story:

**Task Breakdown**:
- Phase 1 (Setup): 3 tasks - Backup, verify image, start dev server
- Phase 2 (Foundational): 4 tasks - Core CSS changes (T004-T007)
- Phase 3 (US1 Mobile): 6 tasks - Mobile viewport verification
- Phase 4 (US2 Tablet): 5 tasks - Tablet viewport verification
- Phase 5 (US3 Desktop): 5 tasks - Desktop regression testing
- Phase 6 (Polish): 5 tasks - Lighthouse, CLS, cleanup

**Key Features**:
- Tasks organized by user story for independent testing
- CSS change reference included with before/after code
- Quick implementation path (6 tasks) for fastest results
- MVP scope defined (10 tasks through US1)
- 15+ parallel opportunities within viewport tests

**Implementation Strategy**:
1. Setup → Foundational CSS → Mobile verification → Done (MVP)
2. Or continue: Tablet → Desktop → Polish (Full)

## Outcome

- ✅ Impact: Complete task list ready for /sp.implement execution
- 🧪 Tests: Manual browser testing defined (no automated tests requested)
- 📁 Files: 2 files created (tasks.md, PHR)
- 🔁 Next prompts: `/sp.implement` to execute tasks and apply CSS fix
- 🧠 Reflection: This is a minimal fix with mostly verification tasks. The actual code changes are just 4 tasks (T004-T007). Most tasks are testing/verification which ensures quality.

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): Task format validation - PASS (all tasks follow checklist format)
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Proceed to /sp.implement
