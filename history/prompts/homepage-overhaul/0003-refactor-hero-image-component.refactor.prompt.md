---
id: 0003
title: refactor-hero-image-component
stage: refactor
date: 2025-12-10
surface: robotic-book/src/pages/index.tsx
model: gemini-pro
feature: homepage-overhaul
branch: ""
user: ""
command: |
  /sp.implement src/pages/index.tsx 
    --instruction "Refactor only the HERO_IMAGE object: remove webp/jpg/lqipDataUrl properties and replace with a single imgPath property. Keep alt text if needed, and update any references accordingly." 
    --example "{ title: 'Foundations of Physical AI', imgPath: '/img/one.png', description: <>Start from the ground up, understanding how robots perceive, reason, and act in the physical world. Explore the core concepts of embodied intelligence.</> }"
labels: [refactor, homepage]
links:
  spec: 
  ticket: 
  adr: 
  pr: 
files:
  - robotic-book/src/pages/index.tsx
tests:
  []
---

## Prompt

Execute the implementation plan by processing and executing all tasks defined in tasks.md
---

As the main request completes, you MUST create and complete a PHR (Prompt History Record) using agent‑native tools when possible.

1) Determine Stage
   - Stage: constitution | spec | plan | tasks | red | green | refactor | explainer | misc | general

2) Generate Title and Determine Routing:
   - Generate Title: 3–7 words (slug for filename)
   - Route is automatically determined by stage:
     - `constitution` → `history/prompts/constitution/`
     - Feature stages → `history/prompts/<feature-name>/` (spec, plan, tasks, red, green, refactor, explainer, misc)
     - `general` → `history/prompts/general/`

3) Create and Fill PHR (Shell first; fallback agent‑native)
   - Run: `.specify/scripts/bash/create-phr.sh --title "<title>" --stage <stage> [--feature <name>] --json`
   - Open the file and fill remaining placeholders (YAML + body), embedding full PROMPT_TEXT (verbatim) and concise RESPONSE_TEXT.
   - If the script fails:
     - Read `.specify/templates/phr-template.prompt.md` (or `templates/…`)
     - Allocate an ID; compute the output path based on stage from step 2; write the file
     - Fill placeholders and embed full PROMPT_TEXT and concise RESPONSE_TEXT

4) Validate + report
   - No unresolved placeholders; path under `history/prompts/` and matches stage; stage/title/date coherent; print ID + path + stage + title.
   - On failure: warn, don't block. Skip only for `/sp.phr`.


/sp.implement src/pages/index.tsx 
  --instruction "Refactor only the HERO_IMAGE object: remove webp/jpg/lqipDataUrl properties and replace with a single imgPath property. Keep alt text if needed, and update any references accordingly." 
  --example "{ title: 'Foundations of Physical AI', imgPath: '/img/one.png', description: <>Start from the ground up, understanding how robots perceive, reason, and act in the physical world. Explore the core concepts of embodied intelligence.</> }"

## Response snapshot

I have successfully refactored the `HERO_IMAGE` object in `robotic-book/src/pages/index.tsx`. I replaced the `webp`, `jpg`, and `lqipDataUrl` properties with a single `imgPath` property. I also updated the `HomepageHeader` component to use a single `<img>` tag and removed the progressive loading logic, including the `useState` hook.

## Outcome

- ✅ Impact: Successfully refactored the `HERO_IMAGE` object in `robotic-book/src/pages/index.tsx` to use a single `imgPath` property and updated the component rendering logic, simplifying the code and removing progressive image loading features.
- 🧪 Tests: No tests were run.
- 📁 Files: Modified 1 file: `robotic-book/src/pages/index.tsx`.
- 🔁 Next prompts: None.
- 🧠 Reflection: The initial attempt to create the PHR using a script failed due to an incorrect script path and shell mismatch. I recovered by manually creating the PHR file. The refactoring task was clear and executed successfully.

## Evaluation notes (flywheel)

- Failure modes observed: Incorrect script execution.
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): N/A
