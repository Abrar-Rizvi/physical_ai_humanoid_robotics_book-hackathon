# Implementation Plan: Fix Hero Section Responsive Image

**Branch**: `005-fix-hero-responsive` | **Date**: 2025-12-11 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `specs/005-fix-hero-responsive/spec.md`

## Summary

Fix the Hero Section image visibility issue on mobile viewports by changing the CSS positioning strategy. The image currently uses `position: absolute` with `height: 100%`, but the parent container only has `min-height` (not explicit `height`), causing the percentage height to resolve to 0 on mobile. The solution uses static positioning with responsive sizing for mobile viewports while preserving the existing desktop layout.

## Technical Context

**Language/Version**: CSS3, TypeScript/React (no TS changes needed)
**Primary Dependencies**: Docusaurus v3+, CSS Modules
**Storage**: N/A
**Testing**: Manual browser testing with Chrome DevTools responsive mode
**Target Platform**: Web (modern browsers - Chrome, Firefox, Safari, Edge)
**Project Type**: Web application (Docusaurus static site)
**Performance Goals**: CLS < 0.1, image visible within 3s on 3G
**Constraints**: Must work in light/dark mode, must not break desktop layout
**Scale/Scope**: Single page fix (homepage only), 1 CSS file modification

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Status | Evidence |
|-----------|--------|----------|
| Mobile-first design (Section 8) | PASS | Fix uses mobile-first CSS pattern |
| CSS-only solution preferred (Section 8) | PASS | No JavaScript changes required |
| Dark mode compatibility (Section 8) | PASS | Uses existing CSS variables |
| No layout-breaking changes (Section 3) | PASS | Desktop layout preserved |
| Mobile viewport testing (Section 8) | PLANNED | Testing checklist included |
| Zero tolerance for layout breaks (Section 3) | PASS | Regression protection via desktop override |

**Gate Result**: PASS - All constitution requirements satisfied.

## Project Structure

### Documentation (this feature)

```text
specs/005-fix-hero-responsive/
├── spec.md              # Feature requirements
├── plan.md              # This file
├── research.md          # Root cause analysis and CSS patterns
├── quickstart.md        # Implementation guide
├── checklists/
│   └── requirements.md  # Specification quality checklist
└── tasks.md             # (Created by /sp.tasks - NOT this command)
```

### Source Code (repository root)

```text
robotic-book/
└── src/
    └── pages/
        ├── index.tsx           # Hero Section component (NO CHANGES NEEDED)
        └── index.module.css    # Hero Section styles (FIX APPLIED HERE)
```

**Structure Decision**: This is a CSS-only fix within the existing Docusaurus project structure. No new files needed.

## Root Cause Analysis

### The Problem

```
Mobile CSS Chain:
.heroImageSection     → min-height: 50vh (NO explicit height)
  └── .heroImageContainer → height: 100% (resolves to 0!)
        └── .heroImage      → position: absolute, height: 100% (0px height)
```

CSS `height: 100%` requires the parent to have an explicit `height` value. With only `min-height`, the percentage resolves to 0, making the absolutely positioned image invisible.

### The Solution

Change from absolute to static/relative positioning on mobile, allowing the image to use its intrinsic dimensions:

```
Mobile CSS Chain (FIXED):
.heroImageSection     → min-height: 50vh
  └── .heroImageContainer → min-height: 300px
        └── .heroImage      → position: relative, height: auto
```

## Design Decisions

### Decision 1: Positioning Strategy

**Choice**: Static/relative positioning for mobile, absolute for desktop

**Rationale**:
- Simplest fix with minimal changes
- Preserves existing desktop overlay effect
- No JavaScript needed
- Mobile-first approach matches existing pattern

**Alternatives Rejected**:
- Adding explicit `height` to parent: Inflexible, may clip content
- Using `aspect-ratio`: Would change visual presentation
- Full refactor to remove absolute positioning: Unnecessary scope creep

### Decision 2: Minimum Height Value

**Choice**: `min-height: 300px` for image container on mobile

**Rationale**:
- Ensures image is always visible even on small viewports
- 300px provides good visual impact without dominating the viewport
- Works across 320px-1023px viewport range

### Decision 3: Breakpoint

**Choice**: Keep existing 1024px breakpoint

**Rationale**:
- Consistency with current CSS structure
- Well-tested boundary between mobile and desktop experiences

## CSS Changes Summary

### File: `robotic-book/src/pages/index.module.css`

| Line Range | Change Type | Description |
|------------|-------------|-------------|
| 89-94 | MODIFY | Update `.heroImageContainer` for mobile |
| 97-106 | MODIFY | Update `.heroImage` positioning for mobile |
| 137-177 | ADD | Desktop overrides for absolute positioning |

### Detailed Changes

**1. Mobile Image Container**
```css
/* BEFORE */
.heroImageContainer {
  position: relative;
  width: 100%;
  height: 100%;  /* Problem: Parent has no explicit height */
  overflow: hidden;
}

/* AFTER */
.heroImageContainer {
  position: relative;
  width: 100%;
  min-height: 300px;  /* Ensures visibility */
  overflow: hidden;
}
```

**2. Mobile Image Styles**
```css
/* BEFORE */
.heroImagePlaceholder,
.heroImage {
  position: absolute;  /* Problem: No height context */
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
  position: relative;  /* FIX: Normal document flow */
  width: 100%;
  height: auto;        /* FIX: Intrinsic height */
  min-height: 300px;   /* FIX: Minimum visibility */
  object-fit: cover;
  transition: all 300ms ease;
}
```

**3. Desktop Override (inside @media 1024px+)**
```css
@media (min-width: 1024px) {
  /* ... existing rules ... */

  .heroImageContainer {
    height: 100%;
    min-height: auto;
  }

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

## Testing Plan

### Manual Testing Matrix

| Viewport | Theme | Expected Result |
|----------|-------|-----------------|
| 320px | Light | Image visible, fills width |
| 320px | Dark | Image visible, overlay darker |
| 375px | Light | Image visible, fills width |
| 414px | Light | Image visible, fills width |
| 768px | Light | Image visible, tablet layout |
| 834px | Dark | Image visible, tablet layout |
| 1024px | Light | Desktop layout, side-by-side |
| 1440px | Dark | Desktop layout maintained |

### Accessibility Testing

- [ ] Run Lighthouse accessibility audit
- [ ] Verify alt text is present and descriptive
- [ ] Check color contrast with overlay
- [ ] Test with reduced motion preference

### Performance Testing

- [ ] Verify CLS < 0.1 on page load
- [ ] Check image loads within 3s on throttled 3G

## Risk Assessment

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Desktop layout regression | Low | High | Desktop overrides preserve existing styles |
| Overlay not visible on mobile | Low | Medium | Overlay uses relative positioning |
| Image distortion | Low | Medium | `object-fit: cover` maintains aspect ratio |
| Browser compatibility | Very Low | Low | Uses standard CSS, no vendor prefixes needed |

## Complexity Tracking

No constitution violations requiring justification. This is a minimal CSS fix.

## Dependencies

**Upstream**: None
**Downstream**: None
**External**: None

## Next Steps

1. Run `/sp.tasks` to generate implementation task list
2. Implement CSS changes
3. Test across all viewport sizes
4. Verify dark mode compatibility
5. Run Lighthouse audit
6. Create PR for review

---

**Plan Status**: Ready for `/sp.tasks`
**Estimated Implementation**: 1 task (CSS modification + testing)
