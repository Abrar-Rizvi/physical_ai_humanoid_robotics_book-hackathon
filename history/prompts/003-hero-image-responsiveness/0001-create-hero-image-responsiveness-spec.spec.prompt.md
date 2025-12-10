---
id: 0001
title: create-hero-image-responsiveness-spec
stage: spec
date: 2025-12-10
surface: cli
model: gemini
feature: 003-hero-image-responsiveness
branch: 003-hero-image-responsiveness
user:
command: /sp.specify
labels: []
links:
  spec: specs/003-hero-image-responsiveness/spec.md
  ticket:
  adr:
  pr:
files:
  - specs/003-hero-image-responsiveness/spec.md
  - specs/003-hero-image-responsiveness/checklists/requirements.md
tests:
---

## Prompt

Feature: Fix Hero Section Image Responsiveness (Only Image Adjustment – No Theme/Color Change)Current issue:- On large screens: Robot image appears on the right side → perfect- On small screens (mobile/tablet): Image completely disappears + hero looks emptyTask (only touch the hero image part):1. Make the hero image visible on ALL screen sizes (including mobile)2. Desktop (> 768px): Image stays on the right side, same size/position as now3. Tablet & Mobile (≤ 768px): - Image moves below the text (stack vertically) - Image becomes full-width (100%) but height auto (so it doesn't get too tall) - Add max-height: 400px (or 60vh) so it doesn't dominate the screen - Keep aspect ratio (object-fit: contain or cover with proper cropping) - Add subtle top margin so text and image don't stick together4. Keep existing background color, text, button, everything exactly the same5. Use only existing CSS classes or minimal custom CSS – no Tailwind if not already used6. If using <img> tag → make it responsive with max-width: 100%, height: auto7. If background-image → switch to <img> tag or use background-size: contain + proper media queriesDeliverables:- Only the updated hero section code (src/pages/index.tsx or wherever it lives)- Minimal CSS changes clearly commented- Image must be visible and beautiful on mobile, tablet, and desktopDo NOT change colors, fonts, button style, or layout direction – only fix image visibility and sizing.

## Response snapshot

Successfully created the feature specification after bypassing a failing script by performing the steps manually.

- Created branch `003-hero-image-responsiveness`
- Created spec file `specs/003-hero-image-responsiveness/spec.md`
- Created checklist `specs/003-hero-image-responsiveness/checklists/requirements.md`

The specification is ready for the next phase.

## Outcome

- ✅ Impact: The feature specification was successfully created, enabling the project to move to the planning phase.
- 🧪 Tests: No tests were run.
- 📁 Files: 2 files were created.
- 🔁 Next prompts: /sp.plan
- 🧠 Reflection: The `create-new-feature.ps1` script is unreliable and should be investigated. Manually performing the steps was a successful workaround.

## Evaluation notes (flywheel)

- Failure modes observed: The `create-new-feature.ps1` script repeatedly failed with a `ParameterBindingException`.
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Investigate the PowerShell script execution environment.
