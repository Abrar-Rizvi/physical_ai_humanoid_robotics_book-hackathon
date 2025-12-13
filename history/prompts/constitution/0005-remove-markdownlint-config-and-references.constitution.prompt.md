---
id: 0005
title: Remove markdownlint config and references
stage: constitution
date: 2025-12-13
surface: agent
model: claude-sonnet-4-5-20250929
feature: none
branch: 006-rag-embeddings-pipeline
user: user
command: /sp.constitution
labels: ["constitution", "governance", "markdown", "linting", "workflow", "version-bump"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - .specify/memory/constitution.md (version 1.3.0 → 1.4.0)
  - .github/workflows/quality-checks.yml (removed markdownlint step)
  - .markdownlint.json (deleted)
  - robotic-book/.markdownlint.json (deleted)
tests:
  - N/A (governance/documentation changes)
---

## Prompt

User triggered `/sp.constitution` command with the following instructions:

```text
Remove markdownlint config and all related references

Tasks:
1. Permanently delete `.markdownlint.json` (or `.markdownlint.jsonc`) from repository root and any other location.
2. Update Constitution: Remove any mention of markdown linter, markdownlint, or dedicated Markdown linting tool.
   - Keep spell check if exists.
   - Retain Docusaurus compatibility requirement, but no enforced linting.
   - No new linting tools or configs.
3. Add proper Sync Impact Report (version bump to next MINOR/PATCH, list changes, templates pending if any).
4. Output full updated Constitution Markdown.

Rationale: Eliminate CI/local lint failures from AI-generated/Docusaurus content. Rely on spell check, Docusaurus build, and manual review instead.

Proceed.
```

## Response snapshot

Successfully executed constitution update to remove markdownlint configuration and enforcement:

### ✅ Files Deleted
- `.markdownlint.json` (repository root)
- `robotic-book/.markdownlint.json` (Docusaurus project)

### ✅ Constitution Updated (1.3.0 → 1.4.0)

**Version Bump**: MINOR (1.4.0) - Removed governance section which materially changes development workflow

**Changes Made**:
1. **REMOVED**: Section 4 "Markdown & Linting Style" entirely
   - Deleted MD013 line length rule reference (200 chars limit)
   - Deleted MD007 list indentation rule reference (flexible 2-4 spaces)
   - Deleted merge policy for specs/ directory
2. **RETAINED**: Docusaurus compatibility requirement (Section 6)
3. **RETAINED**: Spell check via cspell (no changes to workflow)
4. **NO NEW LINTING TOOLS**: Explicitly removed markdown linting enforcement

**Rationale**: Eliminate CI and local lint failures caused by AI-generated and Docusaurus content. Rely on cspell for spell checking, Docusaurus build validation, and manual review instead of rigid markdown linting rules that conflict with content generation workflows.

**Sync Impact Report**: Added as HTML comment at top of constitution.md documenting:
- Version change: 1.3.0 → 1.4.0
- Modified/removed sections
- Templates updated status (all verified ✅)
- Files deleted
- Version bump reasoning

### ✅ GitHub Workflow Updated

`.github/workflows/quality-checks.yml`:
- Removed `markdownlint-cli2` from npm install
- Removed "Run Markdown Linter" step entirely
- Retained "Run Spellcheck" step with cspell
- Job renamed: "Install linting and spellcheck tools" → "Install spellcheck tool"

### ✅ Template Validation

Checked all templates for markdownlint references:
- ✅ `.specify/templates/plan-template.md` - No markdownlint references found
- ✅ `.specify/templates/spec-template.md` - No markdownlint references found
- ✅ `.specify/templates/tasks-template.md` - No markdownlint references found

### 📋 Constitution Structure After Update

**Sections Renumbered** (due to Section 4 removal):
- Section 1: Purpose
- Section 2: Core Principles
- Section 3: Standards
- Section 4: Constraints (was Section 5)
- Section 5: Success Criteria (was Section 6)
- Section 6: Scope (was Section 7)
- ... (all subsequent sections renumbered)

**Key Retained Principles**:
- Docusaurus 2 Website requirement (Section 6)
- Web components MUST be mobile-friendly and dark-mode compatible (Section 3)
- Zero tolerance for layout-breaking changes (Section 3)
- Spell checking via cspell continues in CI workflow

**Removed Enforcement**:
- No markdown line length enforcement
- No markdown list indentation rules
- No markdown linting in CI pipeline
- No .markdownlint.json configuration files

## Outcome

- ✅ Impact: **Constitution amended to v1.4.0** - Removed markdown linting enforcement while retaining spell check and Docusaurus compatibility. Eliminated CI failures from AI-generated content.
- 🧪 Tests: N/A (governance/documentation changes, no code changes)
- 📁 Files: 4 files modified/deleted (.specify/memory/constitution.md updated to v1.4.0, .github/workflows/quality-checks.yml updated, 2 .markdownlint.json files deleted)
- 🔁 Next prompts: Commit changes with message: "docs: amend constitution to v1.4.0 (remove markdownlint enforcement)", validate CI workflow passes with only cspell
- 🧠 Reflection: MINOR version bump appropriate since this removes a governance section that materially changes development workflow but maintains backward compatibility. The removal of markdown linting enforcement aligns with AI-first content generation workflows while retaining quality controls via spell check and Docusaurus build validation. Sync Impact Report provides clear audit trail for the change.

## Evaluation notes (flywheel)

- Failure modes observed: None - all files updated successfully, templates validated, no markdownlint references remain
- Graders run and results (PASS/FAIL): Constitution Check PASS - all required sections present, version bumped correctly, governance section updated with new version and amendment date
- Prompt variant (if applicable): Standard /sp.constitution workflow with explicit deletion and removal instructions
- Next experiment (smallest change to try): Monitor CI workflow execution after commit to verify markdownlint step is gone and cspell continues to run successfully
