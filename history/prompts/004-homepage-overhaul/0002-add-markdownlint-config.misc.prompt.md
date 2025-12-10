---
id: 0002
title: Add Markdownlint Config
stage: misc
date: 2025-12-10
surface: agent
model: claude-opus-4-5-20251101
feature: 004-homepage-overhaul
branch: 004-homepage-overhaul
user: Abrar-Rizvi
command: /sp.git.commit_pr
labels: ["linting", "config", "markdownlint"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - robotic-book/.markdownlint.json
tests:
  - null
---

## Prompt

anaylize my constitution and specs and do you see any rule for linter which can cause my length

(followed by: yes create it and allow so that i will not face linter issue on github)

(followed by: /sp.git.commit_pr add,commit and push to github)

## Response snapshot

Analyzed constitution and specs for linter rules. Found:
- Constitution Section 4 specifies "Length: 4,000–6,000 words" (content guideline, not linter)
- markdownlint-cli2 installed but no custom config
- Default MD013 rule (80 char line limit) likely causing issues

Created `.markdownlint.json` disabling:
- MD013 (line length)
- MD033 (inline HTML for MDX)
- MD041 (first line h1 for frontmatter)

Committed and pushed to GitHub after resolving 2 merge conflicts during rebase.

## Outcome

- ✅ Impact: Prevents GitHub linter failures for line-length violations
- 🧪 Tests: N/A (configuration file)
- 📁 Files: 1 created (robotic-book/.markdownlint.json)
- 🔁 Next prompts: Verify linter passes on next PR
- 🧠 Reflection: User had old .markdownlint.jsonc that was deleted; new .json config provides cleaner solution

## Evaluation notes (flywheel)

- Failure modes observed: Merge conflicts from diverged remote branch
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): N/A
