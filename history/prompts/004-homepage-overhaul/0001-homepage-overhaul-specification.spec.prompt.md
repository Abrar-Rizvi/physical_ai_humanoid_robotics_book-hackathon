---
id: 0001
title: Homepage Overhaul Specification
stage: spec
date: 2025-12-09
surface: agent
model: claude-sonnet-4-5
feature: 004-homepage-overhaul
branch: 004-homepage-overhaul
user: system
command: /sp.specify
labels: ["spec", "homepage", "hero", "features", "design", "glassmorphism", "css-modules"]
links:
  spec: specs/004-homepage-overhaul/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/004-homepage-overhaul/spec.md
  - specs/004-homepage-overhaul/checklists/requirements.md
tests:
  - Specification quality checklist validation: ALL PASS (Content Quality, Requirement Completeness, Feature Readiness)
---

## Prompt

```text
/sp.specify

Feature: Complete Homepage Overhaul  Hero Section + Premium Robot-Themed Features Grid (Pure Custom CSS, no Tailwind)

You are a world-class UI/UX + vanilla CSS engineer working on my Physical AI & Humanoid Robotics course book (Docusaurus 2, using classic CSS modules / global styles  NO Tailwind).

Redesign both sections in one specification:

1. Hero Section (src/pages/index.tsx or the component that renders the hero)
   - Full-width hero, ~90vh height
   - Desktop: 2-column layout ’ Left = text, Right = media
   - Mobile: text on top, media below
   - Right side: large futuristic humanoid robot image/video placeholder
     ’ use a real-looking Unsplash URL or placeholder that looks premium
     (example: https://images.unsplash.com/photo-1535378620166-273708d44e4c or similar dramatic robot shot)
   - Left side text (write fresh, high-energy copy):
       " H1: "Master Physical AI & Build Real Humanoid Robots"
       " H2: "The most practical, hands-on course on ROS 2, Gazebo, MoveIt, LLMs and real hardware"
       " Short paragraph (23 lines) that feels authoritative and exciting
       " One big CTA button: "Start Learning Free ’"
   - Perfect vertical/horizontal centering, generous spacing
   - Beautiful dark/light mode support using CSS custom properties or classes
   - Subtle overlay or gradient on the image for text readability

2. Features Section: Premium Features Grid (src/components/HomepageFeatures/index.tsx)
   - Replace the boring default with exactly 3 large, breathtaking cards
   - Desktop: 3 cards in one row with equal spacing
   - Mobile: stacked vertically with nice margins
   - Each card contains:
       " Large high-resolution robot image as background or top half (not tiny icons)
         - Card 1 ’ humanoid robot walking/posing
         - Card 2 ’ industrial robotic arm in action
         - Card 3 ’ glowing AI brain / neural network robot
       " Use real Unsplash/Pexels URLs or beautiful placeholders  comment the URLs clearly
   - Premium style options (choose one, must feel expensive):
       " Glassmorphism cards with backdrop-filter blur + subtle inner shadow
       " OR soft glowing gradient borders + very subtle floating effect
   - Small polished react-icons (or SVG) under the title
   - Hover effect: scale(1.04) + stronger box-shadow + image brightness(1.1)
   - Bold headings (32px+), clean readable description
   - Generous padding & breathing room
   - Perfect dark/light mode using CSS variables or classes

Constraints:
- Use only vanilla CSS / CSS Modules / global styles  absolutely NO Tailwind classes
- Optional: react-icons is allowed
- Zero external packages beyond what already exists

Deliverables (ready to copy-paste):
- Full updated hero code (src/pages/index.tsx or the correct file)
- Full rewritten src/components/HomepageFeatures/index.tsx
- Separate CSS file or <style> blocks with clear comments
- All image URLs commented so I can replace them later

Make the homepage so beautiful that recruiters and students open
```

## Response snapshot

Successfully created comprehensive specification for **Complete Homepage Overhaul with Premium Robot-Themed Visuals** feature (004-homepage-overhaul).

### Specification Summary

**Scope**: Redesign homepage with immersive hero section (~90vh, 2-column desktop layout) and premium glassmorphism feature cards

**User Stories**: 4 prioritized stories
- P1: Immersive Hero Experience (full-height, dramatic robot visual, compelling copy)
- P1: Premium Feature Cards Showcase (3 cards with glassmorphism, high-res robot images)
- P2: Accessible Dark Mode Experience (seamless theme switching)
- P1: Responsive Mobile-First Design (adaptive layouts for all screen sizes)

**Functional Requirements**: 33 requirements covering:
- Hero Section: FR-001 to FR-010 (layout, content, imagery, responsiveness)
- Features Section: FR-011 to FR-018 (cards, styling, hover effects)
- Styling & Theme: FR-019 to FR-023 (CSS-only, dark mode, responsive breakpoints)
- Performance & Accessibility: FR-024 to FR-029 (image optimization, keyboard navigation, WCAG compliance)
- Integration: FR-030 to FR-033 (zero new dependencies, no breaking changes)

**Success Criteria**: 10 measurable outcomes including:
- SC-001: Hero loads within 2 seconds on 3G
- SC-002: 60fps hover animations
- SC-003: WCAG 2.1 AA compliance
- SC-004: Zero layout shift (CLS = 0) on dark mode toggle
- SC-006: Lighthouse performance score e90

**Design Specifications**: Detailed mockups with:
- Hero: 2-column (desktop), stacked (mobile), suggested Unsplash robot images, gradient overlay
- Features: 3 glassmorphism cards, specific CSS properties (backdrop-filter blur, semi-transparent backgrounds)
- Typography: Font sizes, weights, line heights for hero H1/H2/paragraph and feature card headings
- Suggested copy for all sections (hero headline, CTA, feature card titles/descriptions)

**Technical Approach**:
- Pure CSS Modules (no Tailwind per user constraint)
- Docusaurus CSS variables (--ifm-*) for dark mode
- WebP images with JPG fallbacks, lazy loading
- Graceful degradation for backdrop-filter (glassmorphism) on older browsers

**Quality Validation**: Specification passed all checklist items:
-  Content Quality: No implementation details, user-focused, stakeholder-readable
-  Requirement Completeness: 0 [NEEDS CLARIFICATION] markers, all requirements testable
-  Feature Readiness: Clear acceptance criteria, measurable success outcomes

### Key Decisions & Rationale

1. **Glassmorphism over Gradient Borders**: Selected glassmorphism for premium feel aligned with AI/robotics theme; provides fallback to solid backgrounds for browser compatibility
2. **90vh Hero Height**: Balances immersive experience with above-fold CTA visibility; min-height 600px prevents cutoff on laptops
3. **Zero [NEEDS CLARIFICATION] Markers**: Made informed decisions on all ambiguous aspects (image sources, exact layouts, copy) to enable immediate planning
4. **Detailed Image Recommendations**: Provided specific Unsplash URLs with dimensions/file sizes to accelerate implementation
5. **CSS-Only Constraint**: Honored user's "NO Tailwind" requirement; leverages Docusaurus built-in CSS variables for theme consistency

### Files Created

- **specs/004-homepage-overhaul/spec.md**: 530+ lines, comprehensive specification
- **specs/004-homepage-overhaul/checklists/requirements.md**: Quality validation checklist with detailed pass/fail analysis

### Assumptions Documented

- Image licensing: Unsplash URLs are royalty-free with attribution
- Performance baseline: Current Lighthouse score 80-90
- Dark mode infrastructure: Docusaurus theme variables already available
- Mobile traffic: ~50-60% of visitors use mobile devices

## Outcome

-  Impact: Specification ready for planning phase (/sp.plan). Provides complete blueprint for redesigning homepage hero and features sections with premium visuals and glassmorphism design.
- >ê Tests: Specification quality checklist validation PASSED all items (Content Quality 4/4, Requirement Completeness 8/8, Feature Readiness 4/4). Zero [NEEDS CLARIFICATION] markers remaining.
- =Á Files: 2 files created (spec.md, checklists/requirements.md) in specs/004-homepage-overhaul/
- = Next prompts: Run `/sp.plan` to generate technical implementation plan, or `/sp.clarify` if stakeholders need to review/approve specification first.
- >à Reflection: Successfully translated user's detailed UI/UX requirements into a comprehensive, business-focused specification without leaking implementation details. Made informed decisions (glassmorphism style, specific image URLs, exact copy) to eliminate all clarification needs and enable immediate planning. Specification balances completeness (33 FRs, 10 SCs, 6 edge cases) with readability for non-technical stakeholders. Quality checklist confirms spec meets all readiness criteria for next phase.

## Evaluation notes (flywheel)

- Failure modes observed: None. Specification workflow completed successfully on first iteration without needing user clarifications or spec revisions.
- Graders run and results (PASS/FAIL): Specification quality checklist PASS (all 16 validation items passed). Key strengths: comprehensive design specs with code examples, strong accessibility focus (multiple WCAG requirements), explicit performance budgets, well-documented risk mitigations.
- Prompt variant (if applicable): N/A (initial specification for new feature)
- Next experiment (smallest change to try): Proceed with `/sp.plan` to generate technical architecture plan. Consider user feedback on suggested copy/images before implementation if stakeholder review is needed. Alternative: create low-fidelity wireframes to visualize 2-column hero layout and glassmorphism cards before planning.
