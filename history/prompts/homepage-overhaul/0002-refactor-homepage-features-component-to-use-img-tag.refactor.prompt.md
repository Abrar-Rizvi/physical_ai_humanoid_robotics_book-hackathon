---
id: 0002
title: Refactor Homepage Features Component to Use Img Tag
stage: refactor
date: 2025-12-09
surface: cli
model: gemini
feature: homepage-overhaul
branch: 004-homepage-overhaul
user:
command: /sp.implement src/components/HomepageFeatures/index.tsx --instruction "Refactor FeatureCardProps and FEATURE_LIST to replace imageWebP/imageJPG with a single imgPath property. Update FeatureCard component to render <img src={imgPath} ... /> instead of <picture> sources." --example "{ title: 'Foundations of Physical AI', imgPath: '/img/one.png', description: <>Start from the ground up, understanding how robots perceive, reason, and act in the physical world. Explore the core concepts of embodied intelligence.</> }"
labels: [refactor, homepage, component, image]
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
  --instruction "Refactor FeatureCardProps and FEATURE_LIST to replace imageWebP/imageJPG with a single imgPath property. Update FeatureCard component to render <img src={imgPath} ... /> instead of <picture> sources."
  --example "{ title: 'Foundations of Physical AI', imgPath: '/img/one.png', description: <>Start from the ground up, understanding how robots perceive, reason, and act in the physical world. Explore the core concepts of embodied intelligence.</> }"

## Response snapshot

I have successfully refactored the `HomepageFeatures` component to directly render an `<img>` tag using the `imgPath` property, eliminating the `<picture>` element. I have also updated the `tasks.md` file to reflect this change.

## Outcome

- ✅ Impact: The `FeatureCard` component in `HomepageFeatures/index.tsx` was further refactored to directly use an `<img>` tag with the `imgPath` property, removing the `<picture>` element. This simplifies the image rendering logic. The corresponding task (T026) in `tasks.md` was updated and marked as complete.
- 🧪 Tests: No tests were run as this was a refactoring of a UI component with no new logic.
- 📁 Files:
  - `robotic-book/src/components/HomepageFeatures/index.tsx`
  - `specs/004-homepage-overhaul/tasks.md`
- 🔁 Next prompts: None
- 🧠 Reflection: I successfully recovered from an error in the previous turn where the first refactoring was not fully applied. By re-applying the first change and then the second, I was able to complete the user's request. This highlights the importance of careful `old_string` matching for the `replace` tool and verifying the file content. The manual fallback for PHR creation continues to work as expected.

## Evaluation notes (flywheel)

- Failure modes observed: `replace` tool matching error.
- Graders run and results (PASS/FAIL): PASS
- Prompt variant (if applicable):
- Next experiment (smallest change to try):
