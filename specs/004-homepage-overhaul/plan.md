# Implementation Plan: Complete Homepage Overhaul with Premium Robot-Themed Visuals

**Branch**: `004-homepage-overhaul` | **Date**: 2025-12-09 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/004-homepage-overhaul/spec.md`

## Summary

This feature implements a complete redesign of the Docusaurus homepage with a premium, robot-themed visual identity. The redesign replaces the existing `HomepageHeader` and `HomepageFeatures` components with:

1. **Hero Section**: Full-height (~90vh) two-column layout featuring compelling course copy and a dramatic futuristic humanoid robot image, designed to capture attention and drive enrollment within 3 seconds
2. **Features Grid**: Three large glassmorphism-styled feature cards with high-resolution robot imagery showcasing ROS 2, hardware integration, and AI-powered intelligence

**Technical Approach** (from clarifications):
- **Styling**: CSS Modules (*.module.css) for component-scoped styles with automatic class name hashing
- **Image Loading**: LQIP (Low-Quality Image Placeholder) technique using base64-encoded tiny versions for progressive blur-up
- **Responsive Strategy**: Single primary breakpoint at 1024px (stacked <1024px, 2-column/horizontal >=1024px)
- **Layout Constraints**: Consistent 1400px max-width for readability on ultra-wide monitors
- **CTA Behavior**: Standard Docusaurus Link component navigation to /docs/intro

## Technical Context

**Language/Version**: TypeScript 5.6.2 (Docusaurus 3.9.2 requirement), React 19.0.0
**Primary Dependencies**:
- @docusaurus/core: 3.9.2
- @docusaurus/preset-classic: 3.9.2
- React: 19.0.0
- clsx: 2.0.0 (for conditional className composition)
- Optional: react-icons (if icons needed for feature cards)

**Storage**: N/A (static frontend component, images served from static/img/)
**Testing**: Manual browser testing (Chrome, Firefox, Safari, Edge 90+), Lighthouse performance/accessibility audits, responsive design testing at 375px, 768px, 1024px viewports
**Target Platform**: Web (Docusaurus static site), Browser support: Chrome 90+, Firefox 88+, Safari 14+, Edge 90+
**Project Type**: Docusaurus web application (single frontend project)
**Performance Goals**:
- Time to Interactive (TTI) increase ≤500ms
- Lighthouse performance score ≥90 (desktop and mobile)
- Hero section loads with all content visible within 2 seconds on 3G
- Hover animations achieve consistent 60fps

**Constraints**:
- Zero new npm dependencies (except optional react-icons)
- No Tailwind CSS or CSS frameworks
- MUST use CSS Modules (*.module.css)
- Cumulative Layout Shift (CLS) = 0 on dark mode toggle
- Image sizes: Hero ≤200KB, Feature cards ≤150KB each
- MUST NOT break existing navbar, footer, About page, Docs section, or Course AI Chat Widget

**Scale/Scope**:
- 2 components modified (HomepageHeader → Hero, HomepageFeatures → Features)
- 4 total image assets (1 hero + 3 feature cards) with LQIP placeholders
- 2 CSS Module files (hero.module.css, features.module.css)
- ~500-700 lines of TypeScript/TSX code
- ~300-400 lines of CSS

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Alignment with Constitution Principles (Section 2)

✅ **Engineering accuracy, academic clarity**: Component architecture follows React/Docusaurus best practices; responsive design based on established breakpoint standards
✅ **Verified, reproducible workflows**: All styling uses CSS Modules with deterministic class names; images sourced from verifiable Unsplash URLs
✅ **Safety-first development**: No runtime safety concerns for static frontend components; accessibility compliance with WCAG 2.1 AA
✅ **Ethical, traceable, responsible AI usage**: N/A (no AI/ML features in this component)
✅ **Alignment with official documentation**: Follows Docusaurus theming and component structure conventions

### Standards Compliance (Section 3)

✅ **Verifiable claims**: All design decisions grounded in Web Vitals metrics (CLS, TTI, FCP) and WCAG standards
✅ **Citations**: Design references Web.dev, WCAG 2.1, Docusaurus docs
✅ **Readability**: Code follows TypeScript/React conventions, comments for image URLs and LQIP logic
✅ **Diagrams and code reflect real behavior**: Component structure matches actual Docusaurus rendering flow

### Constraints Compliance (Section 4)

✅ **No length constraints**: N/A for code features
✅ **Authoritative sources**: Design patterns from Web.dev, Docusaurus official docs, WCAG
✅ **Formats**: TypeScript (.tsx), CSS Modules (.module.css), optimized images (WebP with JPG fallback)

### System Requirements (Section 7)

⚠️ **Development Environment**: Standard web development setup (Node.js 20+, modern browser)
✅ **No special hardware requirements**: Runs on any machine capable of Docusaurus development
✅ **No cloud dependencies**: Static site, no backend services

### Team Workflow Rules (Section 8)

✅ **Component structure**: Follows React functional component + CSS Modules pattern
✅ **No ROS 2/Gazebo/Unity/Isaac requirements**: This is a documentation site feature, not a robotics simulation
✅ **Testing pipeline**: Manual testing → Accessibility audit → Performance validation → Deployment

### Ethics & Safety (Section 9)

✅ **No unsafe operations**: Static frontend component with no user data collection or dangerous operations
✅ **Accessibility**: WCAG 2.1 AA compliance ensures inclusive access for all users
✅ **Performance**: LQIP technique ensures fast perceived load times, respecting users' bandwidth

### RAG Chatbot Integration (Section 14)

✅ **No conflicts**: Homepage redesign does not interfere with existing Course AI Chat Widget (FR-032)
✅ **Component isolation**: Hero and Features sections are independent of chatbot UI

### Gate Assessment

**PASS** ✅ All applicable constitution requirements met. No violations requiring justification.

**Note**: This feature is a UI/UX enhancement to the documentation site homepage and does not directly involve robotics simulation, ROS 2, or AI model integration covered in Sections 6-9 of the constitution. The constitution's web development standards (accessibility, performance, maintainability) fully apply and are satisfied.

## Project Structure

### Documentation (this feature)

```text
specs/004-homepage-overhaul/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (N/A for frontend component)
├── spec.md              # Feature specification (input)
└── checklists/          # Requirements checklist
    └── requirements.md
```

### Source Code (repository root)

```text
robotic-book/  # Docusaurus project root
├── src/
│   ├── components/
│   │   ├── HomepageFeatures/
│   │   │   ├── index.tsx               # [MODIFIED] New premium feature cards
│   │   │   └── styles.module.css       # [MODIFIED] Glassmorphism styling
│   │   ├── CourseChatWidget/           # [UNCHANGED] Existing chatbot
│   │   │   ├── index.tsx
│   │   │   ├── styles.module.css
│   │   │   └── types.ts
│   │   └── [other components]          # [UNCHANGED]
│   ├── pages/
│   │   ├── index.tsx                   # [MODIFIED] New hero section
│   │   ├── index.module.css            # [MODIFIED] Hero styling
│   │   ├── about.mdx                   # [UNCHANGED]
│   │   └── markdown-page.md            # [UNCHANGED]
│   ├── css/
│   │   └── custom.css                  # [UNCHANGED] Global Docusaurus theme
│   └── theme/
│       └── Root.js                     # [UNCHANGED]
├── static/
│   └── img/
│       ├── hero-robot.webp             # [NEW] Hero robot image (1200x1600px, ~180KB)
│       ├── hero-robot.jpg              # [NEW] Fallback JPG
│       ├── hero-robot-lqip.txt         # [NEW] Base64 LQIP data
│       ├── feature-humanoid.webp       # [NEW] Card 1 (800x600px, ~130KB)
│       ├── feature-humanoid.jpg        # [NEW] Fallback JPG
│       ├── feature-arm.webp            # [NEW] Card 2 (800x600px, ~130KB)
│       ├── feature-arm.jpg             # [NEW] Fallback JPG
│       ├── feature-ai-brain.webp       # [NEW] Card 3 (800x600px, ~130KB)
│       └── feature-ai-brain.jpg        # [NEW] Fallback JPG
├── docs/                               # [UNCHANGED] Documentation markdown
├── blog/                               # [UNCHANGED]
├── docusaurus.config.ts                # [UNCHANGED]
├── package.json                        # [UNCHANGED] No new dependencies
└── tsconfig.json                       # [UNCHANGED]
```

**Structure Decision**: This is a Docusaurus web application following the standard Docusaurus classic theme structure. All components live in `robotic-book/src/components/` and `robotic-book/src/pages/`, with styling via CSS Modules co-located with components. Images are stored in `static/img/` for static asset serving. No backend or API layer is required.

## Complexity Tracking

> **Not Applicable**: No Constitution violations detected. This section would only be filled if constitutional gates failed.

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|--------------------------------------|
| N/A | N/A | N/A |

---

## Phase 0: Research & Technical Decisions

**Status**: Ready to generate research.md

### Research Questions to Resolve

1. **LQIP Implementation Strategy**
   - Research: How to generate and embed base64 LQIP placeholders in React components
   - Research: Best practices for progressive image loading without external libraries
   - Decision needed: Manual base64 generation vs. build-time tool vs. runtime technique

2. **WebP Fallback Implementation**
   - Research: How to implement WebP with JPG fallback in React/Docusaurus
   - Research: Browser support detection for WebP (or rely on `<picture>` element)
   - Decision needed: `<picture>` element vs. dynamic `src` switching

3. **CSS Modules Dark Mode Integration**
   - Research: How to access Docusaurus theme variables (--ifm-*) from CSS Modules
   - Research: Best practices for theme-aware styling in Docusaurus 3.9.2
   - Decision needed: CSS custom properties vs. data-theme attribute selectors

4. **Glassmorphism Browser Compatibility**
   - Research: `backdrop-filter` support in Safari 14+, Firefox 88+
   - Research: Graceful degradation strategy for unsupported browsers
   - Decision needed: Feature detection with `@supports` vs. solid fallback by default

5. **Performance Optimization for Large Images**
   - Research: Image optimization tools (sharp, imagemin, squoosh)
   - Research: Lazy loading implementation with native `loading="lazy"` vs. Intersection Observer
   - Decision needed: Build-time optimization vs. manual optimization workflow

6. **Responsive Breakpoint Implementation**
   - Research: CSS media query best practices for 1024px primary breakpoint
   - Research: Mobile-first vs. desktop-first approach in CSS Modules
   - Decision needed: Mobile-first (min-width) vs. desktop-first (max-width) media queries

### Technologies Requiring Best Practices Review

- **React 19.0.0**: Review breaking changes and new patterns (if any)
- **TypeScript 5.6.2**: Ensure type safety for image imports and CSS Module imports
- **Docusaurus 3.9.2**: Review component override patterns and theme customization
- **CSS Modules**: Best practices for scoped styling with theme integration

---

## Phase 1: Design & Contracts

**Prerequisites**: research.md complete (all NEEDS CLARIFICATION resolved)

### Data Model

**Note**: This is a pure frontend UI component with no data storage or backend integration. The "data model" here refers to component props interfaces and state shape.

#### HeroSection Component Props

```typescript
interface HeroSectionProps {
  // No props needed - uses static content from spec
}

interface HeroImageState {
  loaded: boolean;          // Track when full-res image loads
  lqipDataUrl: string;     // Base64 LQIP placeholder
  fullImageUrl: string;    // Full-resolution WebP/JPG URL
}
```

#### FeatureCard Component Props

```typescript
interface FeatureCardProps {
  title: string;                      // Card heading
  description: string;                // Card description text
  imageUrl: string;                   // WebP image URL
  imageFallback: string;              // JPG fallback URL
  imageAlt: string;                   // Accessibility description
  icon?: React.ComponentType;         // Optional react-icons component
}

const FeatureList: FeatureCardProps[] = [
  // 3 cards with robot-themed content
];
```

### API Contracts

**N/A**: No backend API, GraphQL, or REST endpoints required. This is a static frontend component.

### Component Contracts (React Props)

See Data Model section above for TypeScript interfaces.

---

## Phase 2: Task Decomposition

**Status**: Will be generated by `/sp.tasks` command (NOT by this `/sp.plan` command)

Task generation is deferred to the `/sp.tasks` command, which will create `tasks.md` with:
- Granular implementation tasks
- Test scenarios for each requirement
- Acceptance criteria per task
- Dependency ordering

---

## Implementation Notes

### Critical Path Items

1. **Image Preparation** (blocking): Download and optimize 4 robot images from Unsplash, generate LQIP placeholders
2. **CSS Modules Setup**: Ensure CSS Modules are properly configured in Docusaurus (already should be by default)
3. **Theme Integration**: Test dark mode behavior early to ensure --ifm-* variables work correctly
4. **Breakpoint Testing**: Validate responsive behavior at 375px, 768px, 1024px, 1400px+

### Risk Mitigation Strategies

1. **Glassmorphism fallback**: Implement `@supports (backdrop-filter: blur())` detection early
2. **Image loading performance**: Test LQIP technique on 3G throttling in Chrome DevTools before full implementation
3. **Dark mode CLS**: Measure CLS during theme toggle in development, adjust if >0
4. **Existing component preservation**: Create backup of current index.tsx and HomepageFeatures before modification

### Performance Validation Checklist

- [ ] Lighthouse performance score ≥90 (desktop)
- [ ] Lighthouse performance score ≥90 (mobile)
- [ ] TTI increase ≤500ms vs. current homepage
- [ ] CLS = 0 during dark mode toggle
- [ ] Hero visible within 2s on 3G (Chrome DevTools throttling)
- [ ] 60fps hover animations (Chrome DevTools Performance panel)

### Accessibility Validation Checklist

- [ ] WCAG 2.1 AA compliance (axe DevTools)
- [ ] All images have descriptive alt text
- [ ] CTA button has 44px touch target (mobile)
- [ ] Keyboard navigation works (Tab, Enter)
- [ ] Focus indicators visible
- [ ] Color contrast ≥4.5:1 (normal text), ≥3:1 (large text)

---

## Appendix: Design Decisions Log

### Decision 1: CSS Modules over Global CSS
- **Rationale**: Scoped styling prevents conflicts with existing Docusaurus components and Course AI Chat Widget
- **Alternative Rejected**: Global CSS (risk of style conflicts and specificity wars)

### Decision 2: Single 1024px Breakpoint
- **Rationale**: Simplifies responsive logic, aligns with mobile-first principles, reduces edge cases
- **Alternative Rejected**: Multiple breakpoints at 768px and 1024px (added complexity for minimal UX benefit)

### Decision 3: LQIP over Solid Color Placeholder
- **Rationale**: Industry standard progressive loading, provides superior perceived performance
- **Alternative Rejected**: Solid color or gradient placeholder (less engaging, no shape preview)

### Decision 4: Standard Docusaurus Link for CTA
- **Rationale**: Keeps implementation simple, analytics can be added site-wide via Docusaurus config
- **Alternative Rejected**: Custom analytics onClick handler (premature optimization, scope creep)

### Decision 5: 1400px Max-Width
- **Rationale**: Optimizes readability on ultra-wide monitors, aligns with modern design standards
- **Alternative Rejected**: 1600px (too wide for comfortable reading), no max-width (poor UX on 2000px+ displays)

---

**Plan Status**: ✅ Complete
**Next Command**: Generate research.md via Phase 0 workflow
