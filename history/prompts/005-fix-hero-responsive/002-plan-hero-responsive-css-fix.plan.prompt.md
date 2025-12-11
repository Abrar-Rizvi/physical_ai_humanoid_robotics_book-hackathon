---
id: 002
title: Plan Hero Responsive CSS Fix
stage: plan
date: 2025-12-11
surface: agent
model: claude-opus-4-5-20251101
feature: 005-fix-hero-responsive
branch: 005-fix-hero-responsive
user: system
command: /sp.plan
labels: ["responsive", "css", "planning", "mobile", "docusaurus", "hero-section"]
links:
  spec: specs/005-fix-hero-responsive/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/005-fix-hero-responsive/plan.md
  - specs/005-fix-hero-responsive/research.md
  - specs/005-fix-hero-responsive/quickstart.md
  - history/prompts/005-fix-hero-responsive/002-plan-hero-responsive-css-fix.plan.prompt.md
tests:
  - N/A - planning phase, manual testing checklist defined
---

## Prompt

Responsive Fix Plan for Docusaurus Hero Image

Objective:
Make the Hero Section image fully visible and responsive on desktop, tablet, and mobile.

Phases:

1. Diagnose
   - Check HeroSection (index.tsx + index.module.css).
   - Look for fixed width/height or hidden classes on small screens.
   - Inspect if Docusaurus theme styles override visibility.

2. Responsive Strategy
   - Use CSS Modules.
   - Apply: max-width: 100%, height: auto, object-fit as needed.
   - Ensure container uses a mobile-friendly layout.

3. Apply Fix
   - Remove fixed pixel sizes.
   - Add responsive breakpoints.
   - Use flex/grid so the image stays visible on all screens.

4. Testing
   - Test on 375px (mobile) + 768px (tablet).
   - Ensure no clipping, distortion, or disappearance.

5. Docusaurus Optimization
   - Verify CSS module scoping.
   - Check Tailwind responsiveness (if used).
   - Confirm no theme conflict.

6. Final Output
   - Provide updated React component + CSS.
   - Briefly explain root cause.
   - Ensure code is maintainable.

## Response snapshot

Created comprehensive implementation plan for the Hero Section responsive image fix:

**Root Cause Identified**:
The image uses `position: absolute` with `height: 100%`, but the parent container (`.heroImageSection`) only has `min-height: 50vh`, not explicit `height`. CSS percentage heights require an explicit parent height, so the image height resolves to 0 and becomes invisible on mobile.

**Solution Designed**:
Mobile-first CSS approach:
1. Change image from `position: absolute` to `position: relative` on mobile
2. Use `height: auto` with `min-height: 300px` for consistent visibility
3. Add desktop media query override to restore absolute positioning for desktop layout

**Artifacts Created**:
- `plan.md` - Full implementation plan with CSS changes, testing matrix, risk assessment
- `research.md` - Root cause analysis, CSS pattern evaluation, decision rationale
- `quickstart.md` - Step-by-step implementation guide

**Constitution Check**: PASSED all gates (mobile-first, CSS-only, dark mode compatible, no layout breaks)

## Outcome

- ✅ Impact: Complete implementation plan ready for task generation
- 🧪 Tests: Manual testing matrix defined for 8 viewport/theme combinations
- 📁 Files: 4 files created (plan.md, research.md, quickstart.md, PHR)
- 🔁 Next prompts: `/sp.tasks` to generate task list, then implementation
- 🧠 Reflection: This is a minimal CSS fix - no JavaScript changes needed. The root cause was a common CSS gotcha with percentage heights and absolute positioning.

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): Constitution Check - PASS (all 6 gates)
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Proceed to /sp.tasks for task breakdown
