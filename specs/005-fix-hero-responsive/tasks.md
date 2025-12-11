# Tasks: Fix Hero Section Responsive Image

**Input**: Design documents from `/specs/005-fix-hero-responsive/`
**Prerequisites**: plan.md (required), spec.md (required), research.md, quickstart.md

**Tests**: Manual browser testing only (no automated tests requested)

**Organization**: Tasks grouped by user story for independent implementation and testing

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Source**: `robotic-book/src/pages/`
- **CSS File**: `robotic-book/src/pages/index.module.css`
- **Component File**: `robotic-book/src/pages/index.tsx` (NO CHANGES NEEDED)

---

## Phase 1: Setup (Backup & Preparation)

**Purpose**: Create backup of existing files before making changes

- [x] T001 Create backup of CSS file: `robotic-book/src/pages/index.module.css` → `index.module.css.backup`
- [x] T002 Verify image file exists at `robotic-book/static/img/ai-robot.png`
- [ ] T003 Start local dev server with `npm run start` in `robotic-book/` directory

**Checkpoint**: Backup created, dev server running, ready for CSS changes

---

## Phase 2: Foundational (CSS Base Changes)

**Purpose**: Core CSS fixes that enable all user stories

**⚠️ CRITICAL**: These changes affect all viewports - must be done carefully

- [x] T004 Update `.heroImageContainer` mobile styles in `robotic-book/src/pages/index.module.css` (lines 89-94): Change `height: 100%` to `min-height: 300px`
- [x] T005 Update `.heroImage` mobile positioning in `robotic-book/src/pages/index.module.css` (lines 97-106): Change `position: absolute` to `position: relative`, add `height: auto`, add `min-height: 300px`, remove `top: 0` and `left: 0`
- [x] T006 Add desktop media query overrides for `.heroImageContainer` in `robotic-book/src/pages/index.module.css` (inside @media 1024px+ block): Restore `height: 100%` and `min-height: auto`
- [x] T007 Add desktop media query overrides for `.heroImage` in `robotic-book/src/pages/index.module.css` (inside @media 1024px+ block): Restore `position: absolute`, `top: 0`, `left: 0`, `height: 100%`, `min-height: auto`

**Checkpoint**: CSS changes complete - all user story testing can now begin

---

## Phase 3: User Story 1 - Mobile User Views Homepage (Priority: P1) 🎯 MVP

**Goal**: Hero image is visible and properly scaled on mobile devices (< 768px viewport)

**Independent Test**: Open homepage at 375px width and verify image is visible, fills width, no distortion

### Verification Tasks for User Story 1

- [ ] T008 [US1] Test at 320px viewport (small mobile): Verify image visible in Chrome DevTools
- [ ] T009 [US1] Test at 375px viewport (iPhone SE): Verify image visible, fills width
- [ ] T010 [US1] Test at 414px viewport (iPhone Plus): Verify image visible, no distortion
- [ ] T011 [US1] Test at 428px viewport (iPhone Pro Max): Verify image visible, aspect ratio maintained
- [ ] T012 [US1] Test mobile in dark mode: Toggle theme, verify image visible with darker overlay
- [ ] T013 [US1] Test mobile scrolling: Scroll page, verify image position stable

**Checkpoint**: User Story 1 complete - Mobile users can see the Hero image

---

## Phase 4: User Story 2 - Tablet User Views Homepage (Priority: P2)

**Goal**: Hero image is visible with proper layout on tablet devices (768px-1023px viewport)

**Independent Test**: Open homepage at 768px width and verify image is visible with balanced layout

### Verification Tasks for User Story 2

- [ ] T014 [US2] Test at 768px viewport (iPad Mini): Verify image visible, layout balanced
- [ ] T015 [US2] Test at 834px viewport (iPad): Verify image visible, no overlap with text
- [ ] T016 [US2] Test at 1023px viewport (just below breakpoint): Verify stacked layout still works
- [ ] T017 [US2] Test tablet in dark mode: Toggle theme, verify image and overlay correct
- [ ] T018 [US2] Test tablet landscape orientation: Verify no layout conflicts

**Checkpoint**: User Story 2 complete - Tablet users can see the Hero image

---

## Phase 5: User Story 3 - Desktop User Views Homepage (Priority: P3)

**Goal**: Desktop layout remains unchanged with side-by-side text and image (>= 1024px viewport)

**Independent Test**: Open homepage at 1024px+ width and verify existing side-by-side layout preserved

### Verification Tasks for User Story 3

- [ ] T019 [US3] Test at 1024px viewport (breakpoint): Verify layout switches to side-by-side
- [ ] T020 [US3] Test at 1440px viewport (common desktop): Verify 50/50 layout maintained
- [ ] T021 [US3] Test at 1920px viewport (full HD): Verify layout still works at large sizes
- [ ] T022 [US3] Test desktop in dark mode: Toggle theme, verify overlay effect correct
- [ ] T023 [US3] Test responsive resize: Resize browser window across breakpoints, verify smooth transition

**Checkpoint**: User Story 3 complete - Desktop users see unchanged layout (regression protection)

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Final validation and cleanup

- [ ] T024 Run Lighthouse accessibility audit on homepage
- [ ] T025 Verify CLS (Cumulative Layout Shift) < 0.1 using Chrome DevTools Performance tab
- [ ] T026 Test with prefers-reduced-motion enabled: Verify transitions still work
- [ ] T027 Remove backup file if all tests pass: Delete `index.module.css.backup`
- [x] T028 Run `npm run build` to verify production build succeeds

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3-5)**: All depend on Foundational phase completion
  - User stories can proceed sequentially (P1 → P2 → P3) or in parallel
- **Polish (Phase 6)**: Depends on all user stories being verified

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Phase 2 - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Phase 2 - Independent of US1
- **User Story 3 (P3)**: Can start after Phase 2 - Independent of US1/US2

### Within Each Phase

- Phase 2 tasks (T004-T007) should be done sequentially to avoid CSS conflicts
- Phase 3-5 verification tasks can run in parallel (different viewport sizes)
- Phase 6 tasks should run after all verification passes

### Parallel Opportunities

Within User Story verification:
```bash
# All mobile viewport tests can run in parallel:
T008, T009, T010, T011 (different viewport sizes, same file)

# All tablet viewport tests can run in parallel:
T014, T015, T016 (different viewport sizes, same file)

# All desktop viewport tests can run in parallel:
T019, T020, T021 (different viewport sizes, same file)
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup (backup, verify, start server)
2. Complete Phase 2: CSS changes (T004-T007)
3. Complete Phase 3: Mobile verification (T008-T013)
4. **STOP and VALIDATE**: Mobile users can now see the image
5. Continue with Phase 4-6 if time permits

### Full Implementation

1. Setup → Foundational → Mobile (US1) → Tablet (US2) → Desktop (US3) → Polish
2. Each story adds confidence without breaking previous stories
3. Can stop at any checkpoint with working functionality

### Quick Implementation Path

For fastest results:
1. T001-T003 (Setup)
2. T004-T007 (CSS changes)
3. T009 (Quick mobile test at 375px)
4. T019 (Quick desktop test at 1024px)
5. Done if both pass

---

## CSS Changes Reference

**File**: `robotic-book/src/pages/index.module.css`

### T004 - heroImageContainer (lines 89-94)

```css
/* BEFORE */
.heroImageContainer {
  position: relative;
  width: 100%;
  height: 100%;
  overflow: hidden;
}

/* AFTER */
.heroImageContainer {
  position: relative;
  width: 100%;
  min-height: 300px;
  overflow: hidden;
}
```

### T005 - heroImage (lines 97-106)

```css
/* BEFORE */
.heroImagePlaceholder,
.heroImage {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: all 300ms ease;
}

/* AFTER */
.heroImagePlaceholder,
.heroImage {
  position: relative;
  width: 100%;
  height: auto;
  min-height: 300px;
  object-fit: cover;
  transition: all 300ms ease;
}
```

### T006-T007 - Desktop Override (inside @media 1024px+)

```css
@media (min-width: 1024px) {
  /* ... existing rules ... */

  /* ADD T006: */
  .heroImageContainer {
    height: 100%;
    min-height: auto;
  }

  /* ADD T007: */
  .heroImagePlaceholder,
  .heroImage {
    position: absolute;
    top: 0;
    left: 0;
    height: 100%;
    min-height: auto;
  }
}
```

---

## Notes

- All verification tasks are manual browser tests using Chrome DevTools
- No automated tests needed - this is a visual CSS fix
- [US1], [US2], [US3] labels map to user stories from spec.md
- Stop at any checkpoint to validate story independently
- CSS changes in Phase 2 are the core fix; Phases 3-5 are verification
- If any test fails, revert using backup file and debug

---

## Summary

| Metric | Value |
|--------|-------|
| Total Tasks | 28 |
| Setup Tasks | 3 |
| Foundational Tasks | 4 |
| US1 Tasks | 6 |
| US2 Tasks | 5 |
| US3 Tasks | 5 |
| Polish Tasks | 5 |
| Parallel Opportunities | 15+ (viewport tests within each story) |
| MVP Scope | Phase 1 + Phase 2 + Phase 3 (10 tasks) |
| Quick Path | 6 tasks (T001-T004, T009, T019) |
