---
description: "Task list for Complete Homepage Overhaul with Premium Robot-Themed Visuals"
---

# Tasks: Complete Homepage Overhaul with Premium Robot-Themed Visuals

**Input**: Design documents from `/specs/004-homepage-overhaul/`
**Prerequisites**: plan.md ✅, spec.md ✅, research.md ✅, data-model.md ✅, quickstart.md ✅

**Tests**: NOT requested in feature specification - no test tasks included

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3, US4)
- Include exact file paths in descriptions

## Path Conventions

- **Docusaurus project**: `robotic-book/` at repository root
- **Components**: `robotic-book/src/components/`
- **Pages**: `robotic-book/src/pages/`
- **Static assets**: `robotic-book/static/img/`

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Image asset preparation and project initialization

- [ ] T001 Download hero robot image from Unsplash (https://images.unsplash.com/photo-1535378620166-273708d44e4c?w=1200&q=80) as hero-robot-original.jpg
- [ ] T002 [P] Download feature card 1 image from Unsplash (https://images.unsplash.com/photo-1561557944-6e7860d1a7eb?w=800&q=80) as feature-humanoid-original.jpg
- [ ] T003 [P] Download feature card 2 image from Unsplash (https://images.unsplash.com/photo-1563207153-f403bf289096?w=800&q=80) as feature-arm-original.jpg
- [ ] T004 [P] Download feature card 3 image from Unsplash (https://images.unsplash.com/photo-1677442136019-21780ecad995?w=800&q=80) as feature-ai-brain-original.jpg
- [ ] T005 Optimize hero-robot-original.jpg to 1200x1600px WebP (~180KB) and JPG (~200KB) using Squoosh, save as robotic-book/static/img/hero-robot.webp and hero-robot.jpg
- [ ] T006 [P] Optimize feature-humanoid-original.jpg to 800x600px WebP (~130KB) and JPG (~150KB), save as robotic-book/static/img/feature-humanoid.webp and feature-humanoid.jpg
- [ ] T007 [P] Optimize feature-arm-original.jpg to 800x600px WebP (~130KB) and JPG (~150KB), save as robotic-book/static/img/feature-arm.webp and feature-arm.jpg
- [ ] T008 [P] Optimize feature-ai-brain-original.jpg to 800x600px WebP (~130KB) and JPG (~150KB), save as robotic-book/static/img/feature-ai-brain.webp and feature-ai-brain.jpg
- [ ] T009 Generate LQIP for hero-robot (20x27px, base64-encoded, ~1.8KB) and save base64 string to hero-robot-lqip.txt
- [ ] T010 [P] Generate LQIP for feature-humanoid (20x15px, base64-encoded, ~1.5KB) - optional for future use
- [ ] T011 [P] Generate LQIP for feature-arm (20x15px, base64-encoded, ~1.5KB) - optional for future use
- [ ] T012 [P] Generate LQIP for feature-ai-brain (20x15px, base64-encoded, ~1.5KB) - optional for future use
- [ ] T013 Backup current homepage: cp robotic-book/src/pages/index.tsx to index.tsx.backup and index.module.css to index.module.css.backup
- [ ] T014 Backup current features: cp robotic-book/src/components/HomepageFeatures/index.tsx to index.tsx.backup and styles.module.css to styles.module.css.backup

**Checkpoint**: All images optimized and backup files created

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: No foundational blocking tasks for this UI-only feature

**⚠️ NOTE**: This is a pure frontend feature with no shared infrastructure requirements. User stories can proceed immediately after Setup.

**Checkpoint**: Setup complete - user story implementation can now begin

---

## Phase 3: User Story 1 - Immersive Hero Experience (Priority: P1) 🎯 MVP

**Goal**: When visitors land on the homepage, they immediately see a full-width, full-height hero section with a dramatic two-column layout: compelling text on the left and a stunning futuristic humanoid robot visual on the right that instantly communicates the course's cutting-edge nature.

**Independent Test**: Navigate to homepage and verify: (1) hero section occupies ~90vh on desktop, (2) text and robot image are displayed in 2-column layout on desktop, (3) layout stacks vertically on mobile with text above image, (4) all content is vertically and horizontally centered.

**Why this priority**: The hero section is the first impression and primary conversion driver. A premium, professional hero immediately establishes authority and captures attention, directly impacting enrollment decisions within the critical first 3 seconds.

### Implementation for User Story 1

- [ ] T015 [US1] Replace HomepageHeader function in robotic-book/src/pages/index.tsx with new HeroSection component (useState hook for imageLoaded state, LQIP placeholder, full-resolution picture element with WebP/JPG sources)
- [ ] T016 [US1] Add hero content constants to robotic-book/src/pages/index.tsx (HERO_CONTENT with headline/subheadline/paragraph/CTA, HERO_IMAGE with WebP/JPG/alt/lqipDataUrl from hero-robot-lqip.txt)
- [ ] T017 [US1] Implement hero JSX structure in robotic-book/src/pages/index.tsx (heroContainer with heroTextSection for left column and heroImageSection for right column, LQIP img + picture element + gradient overlay)
- [ ] T018 [US1] Replace index.module.css with mobile-first hero styling in robotic-book/src/pages/index.module.css (heroContainer flexbox column, heroTextSection/heroImageSection 100% width, mobile font sizes: H1 36-42px, H2 18-22px, paragraph 16-18px)
- [ ] T019 [US1] Add desktop media query styles to robotic-book/src/pages/index.module.css (@media min-width 1024px: flex-direction row, 50% width columns, max-width 1400px, H1 56-64px, H2 24-28px, paragraph 18-20px)
- [ ] T020 [US1] Implement LQIP progressive loading styles in robotic-book/src/pages/index.module.css (heroImagePlaceholder and heroImage with position absolute, transition all 300ms ease, blur filter on placeholder)
- [ ] T021 [US1] Add CTA button styling to robotic-book/src/pages/index.module.css (heroCTA with primary color background, 48px min-height mobile / 56px desktop, hover effects with translateY and box-shadow)
- [ ] T022 [US1] Implement gradient overlay styles in robotic-book/src/pages/index.module.css (heroImageOverlay with linear-gradient transparent to rgba(0,0,0,0.3), dark mode adjustment to rgba(0,0,0,0.6))
- [ ] T023 [US1] Add prefers-reduced-motion accessibility support to robotic-book/src/pages/index.module.css (disable transform animations, keep opacity transitions only)

**Checkpoint**: Hero section fully functional and testable independently (desktop 2-column, mobile stacked, LQIP blur-up, responsive, dark mode, accessible)

---

## Phase 4: User Story 2 - Premium Feature Cards Showcase (Priority: P1)

**Goal**: When visitors scroll below the hero, they encounter three large, visually stunning feature cards with high-resolution robot imagery that showcase the course's key value propositions through modern glassmorphism design.

**Independent Test**: Scroll to features section and verify: (1) three cards display in a horizontal row on desktop, (2) each card has a unique high-resolution robot image, (3) glassmorphism effects (blur + transparency) are applied, (4) cards stack vertically on mobile.

**Why this priority**: Feature cards communicate the "what" and "why" of the course. Premium visuals differentiate this from generic documentation sites and signal high-quality content, directly impacting perceived value and engagement.

### Implementation for User Story 2

- [x] T024 [US2] Define FeatureCardProps interface in robotic-book/src/components/HomepageFeatures/index.tsx (title, description, imgPath, imageAlt, optional icon from react-icons)
- [x] T025 [US2] Create FEATURE_LIST constant in robotic-book/src/components/HomepageFeatures/index.tsx with 3 cards using the new imgPath property.
- [x] T026 [US2] Implement FeatureCard component in robotic-book/src/components/HomepageFeatures/index.tsx (featureCard div with featureCardImage section containing an img element using imgPath, and loading="lazy", featureCardContent with h3 and description)
- [ ] T027 [US2] Update HomepageFeatures export function in robotic-book/src/components/HomepageFeatures/index.tsx (featuresContainer section with featuresGrid, map over FEATURE_LIST to render 3 FeatureCard instances)
- [ ] T028 [US2] Replace styles.module.css with mobile-first feature card styling in robotic-book/src/components/HomepageFeatures/styles.module.css (featuresContainer padding 60px/20px, featuresGrid flex column gap 24px, featureCard min-height 400px border-radius 16px)
- [ ] T029 [US2] Implement glassmorphism styling with fallback in robotic-book/src/components/HomepageFeatures/styles.module.css (base solid background rgba(255,255,255,0.95), @supports backdrop-filter with rgba(255,255,255,0.1) and blur(10px), border 1px solid rgba(255,255,255,0.2))
- [ ] T030 [US2] Add dark mode glassmorphism styles to robotic-book/src/components/HomepageFeatures/styles.module.css ([data-theme='dark'] featureCard with rgba(30,30,30,0.3) inside @supports block, solid fallback rgba(30,30,30,0.95) outside)
- [ ] T031 [US2] Implement hover effects in robotic-book/src/components/HomepageFeatures/styles.module.css (featureCard:hover with scale(1.04), box-shadow 0 12px 40px, cardImage brightness(1.1), transition 300ms cubic-bezier)
- [ ] T032 [US2] Add card layout styles to robotic-book/src/components/HomepageFeatures/styles.module.css (featureCardImage 60% height with background cover, featureCardContent 40% height with padding 24px mobile / 32px desktop)
- [ ] T033 [US2] Add desktop media query to robotic-book/src/components/HomepageFeatures/styles.module.css (@media min-width 1024px: featuresGrid flex-direction row gap 32px max-width 1400px, featureCard flex:1 min-height 480px)
- [ ] T034 [US2] Add prefers-reduced-motion support to robotic-book/src/components/HomepageFeatures/styles.module.css (disable scale transform on hover, keep box-shadow transition, disable cardImage transitions)

**Checkpoint**: Feature cards fully functional (3 cards, glassmorphism, hover effects, responsive, dark mode, accessible)

---

## Phase 5: User Story 3 - Accessible Dark Mode Experience (Priority: P2)

**Goal**: When users toggle between light and dark themes, both the hero and features sections adapt seamlessly with appropriate color schemes, ensuring readability and visual consistency across all theme preferences.

**Independent Test**: Toggle Docusaurus theme switcher and verify: (1) hero text colors adapt, (2) hero image overlay changes appropriately, (3) feature card backgrounds/borders/text adjust, (4) no layout shift occurs (CLS = 0).

**Why this priority**: Dark mode is essential for modern web experiences and user preference accommodation. Given the technical audience (developers/roboticists), dark mode support is expected and directly impacts user comfort and retention.

### Implementation for User Story 3

- [ ] T035 [US3] Add CSS custom properties integration to robotic-book/src/pages/index.module.css (heroTextSection background var(--ifm-background-color), color var(--ifm-font-color-base), heroCTA background var(--ifm-color-primary), hover var(--ifm-color-primary-dark))
- [ ] T036 [US3] Verify heroImageOverlay dark mode gradient already implemented in robotic-book/src/pages/index.module.css ([data-theme='dark'] selector with darker overlay rgba(0,0,0,0.6) - should exist from T022)
- [ ] T037 [US3] Add CSS custom properties to feature card text in robotic-book/src/components/HomepageFeatures/styles.module.css (featureHeading and featureDescription color var(--ifm-font-color-base), featuresContainer background var(--ifm-background-color))
- [ ] T038 [US3] Verify glassmorphism dark mode styles already implemented in robotic-book/src/components/HomepageFeatures/styles.module.css ([data-theme='dark'] selectors with darker backgrounds - should exist from T030)
- [ ] T039 [US3] Test dark mode toggle with Lighthouse CLS measurement (open DevTools Performance panel, record theme toggle, verify CLS = 0 in Experience section)
- [ ] T040 [US3] Verify no layout shift occurs by visual inspection (toggle dark mode multiple times, watch for content jumping or height changes)

**Checkpoint**: Dark mode fully functional with zero layout shift (hero adapts, features adapt, CLS = 0)

---

## Phase 6: User Story 4 - Responsive Mobile-First Design (Priority: P1)

**Goal**: When users access the homepage on mobile devices, tablets, or smaller screens, both hero and features sections adapt flawlessly with appropriate layouts, font sizes, and spacing to ensure optimal readability and usability.

**Independent Test**: Resize browser to mobile widths (375px, 768px, 1024px) and verify: (1) hero stacks text above image, (2) text sizes scale appropriately, (3) CTA button remains tappable (min 44px), (4) feature cards stack vertically, (5) no horizontal scrolling occurs.

**Why this priority**: Mobile traffic represents 50-70% of web visitors. A broken mobile experience results in immediate bounce. This is equally critical as desktop visual impact for user retention and accessibility.

### Implementation for User Story 4

- [ ] T041 [US4] Verify mobile-first hero layout already implemented in robotic-book/src/pages/index.module.css (base styles with flex-direction column, 100% width, mobile font sizes - should exist from T018)
- [ ] T042 [US4] Verify desktop breakpoint already implemented in robotic-book/src/pages/index.module.css (@media min-width 1024px with flex-direction row - should exist from T019)
- [ ] T043 [US4] Test hero at 375px viewport (DevTools Responsive mode, verify text stacks above image, H1 readable, CTA button min 48px height)
- [ ] T044 [US4] Test hero at 768px viewport (verify stacked layout same as 375px per clarification, text remains readable, no horizontal scroll)
- [ ] T045 [US4] Test hero at 1024px viewport (verify 2-column layout activates, 50% width columns, max-width 1400px centered)
- [ ] T046 [US4] Verify mobile-first feature cards already implemented in robotic-book/src/components/HomepageFeatures/styles.module.css (base styles flex column, 100% width, gap 24px - should exist from T028)
- [ ] T047 [US4] Verify desktop feature card breakpoint already implemented in robotic-book/src/components/HomepageFeatures/styles.module.css (@media min-width 1024px with flex-direction row - should exist from T033)
- [ ] T048 [US4] Test feature cards at 375px viewport (verify vertical stack, 100% width, no horizontal scroll, cards readable)
- [ ] T049 [US4] Test feature cards at 768px viewport (verify vertical stack same as 375px, appropriate spacing)
- [ ] T050 [US4] Test feature cards at 1024px viewport (verify horizontal row with 3 equal-width cards, gap 32px)
- [ ] T051 [US4] Test ultra-wide at 2000px viewport (verify max-width 1400px constraint prevents overstretching, content centered)
- [ ] T052 [US4] Verify all touch targets meet 44px minimum (CTA button 48px mobile / 56px desktop - should exist from T021)

**Checkpoint**: Responsive design fully functional (375px mobile, 768px tablet, 1024px desktop, 2000px ultra-wide, no horizontal scroll, touch-friendly)

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Validation, accessibility, and performance verification

- [ ] T053 [P] Run Lighthouse performance audit on desktop (open DevTools Lighthouse tab, select Desktop + Performance, verify score ≥90, TTI ≤3s, CLS = 0)
- [ ] T054 [P] Run Lighthouse performance audit on mobile (select Mobile preset, verify score ≥90, check mobile-specific metrics)
- [ ] T055 [P] Test 3G loading performance (DevTools Network tab, set throttling to Slow 3G, hard reload, verify hero text renders within 2 seconds, LQIP shows before full image)
- [ ] T056 [P] Run Lighthouse accessibility audit (Lighthouse → Accessibility category, verify WCAG 2.1 AA compliance with 0 critical violations)
- [ ] T057 [P] Install and run axe DevTools extension (install from Chrome Web Store or Firefox Add-ons, click "Scan ALL of my page", verify 0 violations)
- [ ] T058 [P] Verify all images have descriptive alt text (inspect hero-robot alt, feature-humanoid alt, feature-arm alt, feature-ai-brain alt in DOM)
- [ ] T059 [P] Test keyboard navigation (Tab through CTA button, verify visible focus outline, press Enter to activate link, verify Docusaurus Link navigation works)
- [ ] T060 [P] Verify color contrast ratios (use Color Contrast Analyzer or DevTools, check hero text ≥4.5:1, feature card text ≥4.5:1, CTA button text ≥4.5:1 in both light and dark modes)
- [ ] T061 [P] Test hover animations at 60fps (DevTools Performance panel, record hover over feature card, check FPS graph stays at 60fps, verify no jank)
- [ ] T062 [P] Cross-browser testing in Firefox 103+ (open homepage in Firefox, verify glassmorphism renders, WebP images load, responsive breakpoints work)
- [ ] T063 [P] Cross-browser testing in Safari 14+ (open homepage in Safari, verify WebP images with JPG fallback, webkit prefixes work if needed, layout correct)
- [ ] T064 [P] Cross-browser testing in Edge 90+ (open homepage in Edge, verify all features match Chrome behavior)
- [ ] T065 Verify existing components not broken (manually test navbar links, footer links, About page, Docs section, Course AI Chat Widget remains functional)
- [ ] T066 Compare performance vs original homepage (run Lighthouse before and after, verify TTI increase ≤500ms, no performance regression)
- [ ] T067 [P] Verify image file sizes meet constraints (check hero-robot.webp ≤200KB, feature-humanoid.webp ≤150KB, feature-arm.webp ≤150KB, feature-ai-brain.webp ≤150KB)
- [ ] T068 Run quickstart.md validation (follow quickstart.md steps 4.1-4.5 to verify all acceptance criteria pass)

**Checkpoint**: All validations pass, performance ≥90, accessibility WCAG 2.1 AA, cross-browser compatible, existing components unaffected

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: N/A (no foundational phase for this UI feature)
- **User Stories (Phase 3-6)**: All depend on Setup completion
  - User Story 1 (Hero): Depends on Setup (images ready)
  - User Story 2 (Features): Depends on Setup (images ready), independent of User Story 1
  - User Story 3 (Dark Mode): Depends on User Story 1 and 2 (adds dark mode to existing components)
  - User Story 4 (Responsive): Verification phase, depends on User Story 1 and 2 (tests existing responsive implementations)
- **Polish (Phase 7)**: Depends on all user stories (1-4) being complete

### User Story Dependencies

- **User Story 1 (P1 - Hero)**: Can start after Setup - No dependencies on other stories
- **User Story 2 (P1 - Features)**: Can start after Setup - Independent of User Story 1 (different files)
- **User Story 3 (P2 - Dark Mode)**: Depends on User Story 1 AND 2 (enhances both components with dark mode)
- **User Story 4 (P1 - Responsive)**: Depends on User Story 1 AND 2 (verifies responsive behavior already implemented)

### Within Each User Story

**User Story 1 (Hero)**:
- T015-T017: Component structure (sequential - modify same file)
- T018-T020: Mobile styling (sequential - modify same CSS file)
- T021-T023: Enhancements (sequential - modify same CSS file)

**User Story 2 (Features)**:
- T024-T027: Component structure (sequential - modify same file)
- T028-T034: Styling (sequential - modify same CSS file)

**User Story 3 (Dark Mode)**:
- T035-T040: All sequential (verify and enhance existing implementations)

**User Story 4 (Responsive)**:
- T041-T052: All verification tasks, can run in parallel with manual testing

**Phase 7 (Polish)**:
- T053-T068: All marked [P] can run in parallel (independent checks)

### Parallel Opportunities

- **Setup Phase**: T002-T004 (image downloads), T006-T008 (image optimizations), T010-T012 (LQIP generation) can all run in parallel
- **User Story 1 vs User Story 2**: Entire User Story 2 (T024-T034) can run in parallel with User Story 1 (T015-T023) since they modify different files (index.tsx vs HomepageFeatures/index.tsx)
- **Polish Phase**: Most validation tasks (T053-T064, T067) can run in parallel

---

## Parallel Example: Setup Phase

```bash
# Launch image downloads in parallel:
Task: "Download feature card 1 image from Unsplash as feature-humanoid-original.jpg"
Task: "Download feature card 2 image from Unsplash as feature-arm-original.jpg"
Task: "Download feature card 3 image from Unsplash as feature-ai-brain-original.jpg"

# Launch image optimizations in parallel (after downloads complete):
Task: "Optimize feature-humanoid-original.jpg to 800x600px WebP and JPG"
Task: "Optimize feature-arm-original.jpg to 800x600px WebP and JPG"
Task: "Optimize feature-ai-brain-original.jpg to 800x600px WebP and JPG"

# Launch LQIP generation in parallel (after optimizations complete):
Task: "Generate LQIP for feature-humanoid (20x15px, base64-encoded)"
Task: "Generate LQIP for feature-arm (20x15px, base64-encoded)"
Task: "Generate LQIP for feature-ai-brain (20x15px, base64-encoded)"
```

---

## Parallel Example: User Story 1 AND User Story 2 Together

```bash
# Developer A works on User Story 1 (Hero):
Task: "Replace HomepageHeader function in robotic-book/src/pages/index.tsx"
Task: "Replace index.module.css with mobile-first hero styling"
...

# Developer B works on User Story 2 (Features) IN PARALLEL:
Task: "Define FeatureCardProps interface in robotic-book/src/components/HomepageFeatures/index.tsx"
Task: "Replace styles.module.css with mobile-first feature card styling"
...

# These can run simultaneously because they modify different files
```

---

## Implementation Strategy

### MVP First (User Stories 1 + 2 Only)

Since both User Story 1 (Hero) and User Story 2 (Features) are P1 priority and critical for first impressions:

1. Complete Phase 1: Setup (images ready)
2. Complete User Story 1 (Hero) AND User Story 2 (Features) in parallel
3. **STOP and VALIDATE**: Test both independently
4. Complete User Story 3 (Dark Mode) - adds theme support to both
5. Complete User Story 4 (Responsive) - validates responsive behavior
6. Complete Phase 7: Polish - comprehensive validation
7. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup → Images ready
2. Add User Story 1 (Hero) → Test independently → Partial homepage ready
3. Add User Story 2 (Features) → Test independently → Full homepage visual redesign complete (MVP!)
4. Add User Story 3 (Dark Mode) → Test dark theme toggle → Enhanced UX
5. Add User Story 4 (Responsive) → Test all breakpoints → Mobile-ready
6. Add Phase 7 (Polish) → Comprehensive validation → Production-ready

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup together (T001-T014)
2. Once Setup is done:
   - Developer A: User Story 1 (Hero) T015-T023
   - Developer B: User Story 2 (Features) T024-T034 (IN PARALLEL with A)
3. Once User Stories 1 & 2 complete:
   - Developer A: User Story 3 (Dark Mode) T035-T040
   - Developer B: User Story 4 (Responsive) T041-T052 (IN PARALLEL with A)
4. Both developers: Phase 7 (Polish) T053-T068 in parallel

---

## Notes

- [P] tasks = different files or independent checks, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- User Story 1 and 2 can run in parallel (different files)
- User Story 3 enhances User Story 1 and 2 with dark mode
- User Story 4 validates responsive implementations from User Story 1 and 2
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Total tasks: 68 (14 setup + 9 US1 + 11 US2 + 6 US3 + 12 US4 + 16 polish)
- Estimated time: 4-6 hours per quickstart.md (1h setup + 1.5h US1 + 1.5h US2 + 0.5h US3 + 0.5h US4 + 1h polish)
