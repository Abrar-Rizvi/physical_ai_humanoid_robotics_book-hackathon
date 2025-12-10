# Tasks: Fix Hero Section Image Responsiveness

**Input**: Design documents from `/specs/003-hero-image-responsiveness/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, quickstart.md

**Organization**: Tasks are grouped into a single implementation phase as all user stories relate to the same component.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Phase 1: Setup (Shared Infrastructure)

No project setup or initialization tasks are required as this feature is an enhancement to an existing Docusaurus project.

---

## Phase 2: Foundational (Blocking Prerequisites)

No foundational or blocking prerequisites are required for this feature.

---

## Phase 3: Implementation (User Stories 1, 2, & 3)

**Goal**: Implement the responsive hero image layout as specified, ensuring it is visible and correctly positioned on desktop, tablet, and mobile devices.

**Independent Test**: The implementation can be fully verified by following the instructions in `specs/003-hero-image-responsiveness/quickstart.md`.

### Implementation Tasks

- [x] T001 [US1,US2,US3] Analyze the hero section in `robotic-book/src/pages/index.tsx` and determine if the image is implemented as a CSS `background-image` or an `<img>` tag. If it's a background image that disappears on mobile, refactor it to use a dedicated `<img>` tag to ensure it's always rendered in the DOM.
- [x] T002 [US1] In `robotic-book/src/pages/index.module.css`, review the existing CSS for the hero section. Ensure that on viewports wider than 768px, the layout correctly positions the text and the hero image side-by-side as per the current design.
- [x] T003 [US2,US3] In `robotic-book/src/pages/index.module.css`, add a CSS media query block targeting viewports `(max-width: 768px)`.
- [x] T004 [US2,US3] Inside the `(max-width: 768px)` media query, add styles to change the hero section's layout (e.g., using `flex-direction: column`) to stack the image vertically below the text content.
- [x] T005 [US2,US3] Inside the media query, target the hero image and apply styles to make it full-width (`width: 100%`), with its height adjusting automatically (`height: auto`).
- [x] T006 [US2,US3] Inside the media query, apply a `max-height` of `400px` (or `60vh`) to the image to prevent it from becoming overly tall on narrow screens. Also apply `object-fit: contain` or `object-fit: cover` to maintain its aspect ratio without distortion.
- [x] T007 [US2,US3] Inside the media query, add a `margin-top` to the image to create visual separation from the text content above it.

---

## Phase 4: Polish & Cross-Cutting Concerns

**Purpose**: Final verification and code quality improvements.

- [x] T008 [US1,US2,US3] Perform comprehensive manual testing across different browsers (Chrome, Firefox, Safari) and screen sizes as outlined in `specs/003-hero-image-responsiveness/quickstart.md` to confirm all requirements are met.
- [x] T009 [US1,US2,US3] Review and refactor the new CSS in `robotic-book/src/pages/index.module.css` to ensure it is clean, well-commented, and follows existing code style conventions.

---

## Dependencies & Execution Order

### Phase Dependencies

- **Implementation (Phase 3)**: Can start immediately.
- **Polish (Phase 4)**: Depends on the completion of all tasks in Phase 3.

### Task Dependencies

The tasks within Phase 3 are sequential and should be completed in order:
`T001 → T002 → T003 → T004 → T005 → T006 → T007`

### Parallel Opportunities

Due to the nature of this small CSS and component fix, there are no significant opportunities for parallel execution. The tasks are highly dependent and should be performed sequentially.

---

## Implementation Strategy

A single-pass implementation is recommended for this feature. All tasks should be completed in a single branch, followed by thorough testing before merging.

1.  Complete all tasks in Phase 3 (Implementation).
2.  Complete all tasks in Phase 4 (Polish).
3.  Submit the feature for review.

This approach is suitable for a small, self-contained UI fix that does not require incremental delivery.
