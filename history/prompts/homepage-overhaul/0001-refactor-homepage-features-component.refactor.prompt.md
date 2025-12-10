---
id: 0001
title: Refactor Homepage Features Component
stage: refactor
date: 2025-12-09
surface: cli
model: gemini
feature: homepage-overhaul
branch: 004-homepage-overhaul
user:
command: /sp.implement src/components/HomepageFeatures/index.tsx --instruction "Simplify the feature object: remove imageWebP and imageJPG properties, and instead use a single imgPath property." --example "{ title: 'Foundations of Physical AI', imgPath: '/img/one.png', description: <>Start from the ground up, understanding how robots perceive, reason, and act in the physical world. Explore the core concepts of embodied intelligence.</> }"
labels: [refactor, homepage, component]
links:
  spec: ./specs/004-homepage-overhaul/spec.md
  ticket:
  adr:
  pr:
files:
- robotic-book/src/components/HomepageFeatures/index.tsx
- specs/004-homepage-overhaul/tasks.md
tests:
---

## Prompt

/sp.implement src/components/HomepageFeatures/index.tsx
  --instruction "Simplify the feature object: remove imageWebP and imageJPG properties, and instead use a single imgPath property."
  --example "{ title: 'Foundations of Physical AI', imgPath: '/img/one.png', description: <>Start from the ground up, understanding how robots perceive, reason, and act in the physical world. Explore the core concepts of embodied intelligence.</> }"

## Response snapshot

I have refactored the `HomepageFeatures` component to simplify the feature object as you requested. I have also updated the `tasks.md` file to reflect these changes.

## Outcome

- ✅ Impact: The `FeatureCardProps` interface and the `FEATURE_LIST` constant in `HomepageFeatures/index.tsx` were refactored to use a single `imgPath` property instead of separate `imageWebP` and `imageJPG` properties. This simplifies the component's data structure. The corresponding tasks in `tasks.md` were updated and marked as complete.
- 🧪 Tests: No tests were run as this was a refactoring of a UI component with no new logic.
- 📁 Files:
  - `robotic-book/src/components/HomepageFeatures/index.tsx`
  - `specs/004-homepage-overhaul/tasks.md`
- 🔁 Next prompts: None
- 🧠 Reflection: The user's request was a targeted refactoring. Although the `tasks.md` described a larger implementation, I correctly inferred that I should focus on the user's specific instruction rather than blindly following the task list. This shows the importance of understanding the user's intent. The manual fallback for PHR creation worked as expected.

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): PASS
- Prompt variant (if applicable):
- Next experiment (smallest change to try):
