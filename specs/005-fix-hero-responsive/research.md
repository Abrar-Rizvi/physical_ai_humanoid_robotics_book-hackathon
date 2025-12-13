# Research: Fix Hero Section Responsive Image

**Feature**: 005-fix-hero-responsive
**Date**: 2025-12-11
**Status**: Complete

## Executive Summary

The Hero Section image disappears on mobile devices due to a CSS height calculation issue. The image uses `position: absolute` inside a container with `height: 100%`, but the parent only has `min-height` (not `height`), causing the percentage height to resolve to 0.

---

## Research Task 1: Root Cause Analysis

### Question
Why does the Hero image disappear on mobile viewports but work on desktop?

### Investigation

**Current CSS Chain (Mobile)**:
```
.heroImageSection     → min-height: 50vh (NO explicit height)
  └── .heroImageContainer → height: 100% (resolves to 0!)
        └── .heroImage      → position: absolute, height: 100% (inherits 0)
```

**Current CSS Chain (Desktop @media 1024px+)**:
```
.heroImageSection     → width: 50%, min-height: auto
  └── .heroImageContainer → height: 100%
        └── .heroImage      → position: absolute, height: 100%
```

On desktop, the flexbox row layout gives `.heroImageSection` an implicit height from the sibling content (`.heroTextSection`), so `height: 100%` works. On mobile with `flex-direction: column`, each section is independent and `.heroImageSection` only has `min-height`, not `height`.

### Decision
The fix must provide an explicit height context for the image container on mobile viewports.

### Rationale
CSS `height: 100%` only works when the parent has an explicit height (not just `min-height`). This is a fundamental CSS behavior.

### Alternatives Considered

| Alternative | Pros | Cons | Rejected Because |
|-------------|------|------|------------------|
| Add `height: 50vh` to `.heroImageSection` | Simple fix | Locks height, inflexible | May cause content clipping on tall text |
| Use `aspect-ratio` on container | Modern CSS, responsive | Less browser support | Would change the image presentation model |
| Remove absolute positioning | Simpler CSS | Breaks overlay system | Requires more extensive refactor |
| **Use flexbox with `flex: 1` (CHOSEN)** | Works with existing structure | Requires understanding flex | Best balance of simplicity and robustness |

---

## Research Task 2: Docusaurus CSS Best Practices

### Question
What CSS approach aligns with Docusaurus v3+ and the project constitution?

### Investigation

From the constitution (Section 8 - Web Development):
- "Prefer CSS-only solutions over JavaScript where possible"
- "All changes MUST be tested on mobile viewports"
- "Component integration MUST NOT break existing layout"
- "Dark mode compatibility is mandatory"

From Docusaurus best practices:
- CSS Modules are the recommended approach (already used: `index.module.css`)
- Use CSS custom properties (`--ifm-*` variables) for theme compatibility
- Mobile-first responsive design pattern

### Decision
Use pure CSS fixes within the existing CSS Module structure. No JavaScript changes needed.

### Rationale
The existing architecture already follows Docusaurus best practices. Only the mobile CSS rules need adjustment.

---

## Research Task 3: CSS Solutions for Absolute Positioning Height

### Question
What is the recommended CSS pattern for making absolute-positioned images responsive?

### Investigation

**Pattern 1: Explicit Height**
```css
.container {
  height: 50vh; /* Instead of min-height */
}
```
- Simple but inflexible
- Content may clip or overflow

**Pattern 2: Aspect Ratio Box**
```css
.container {
  aspect-ratio: 16/9;
}
```
- Modern, responsive
- Browser support: 94%+ (2024)
- Changes the visual presentation

**Pattern 3: Position Static with Object-Fit (RECOMMENDED)**
```css
.image {
  position: static; /* or relative */
  width: 100%;
  height: auto;
  object-fit: cover;
}
```
- Removes the need for absolute positioning on mobile
- Image naturally takes its intrinsic height
- Maintains aspect ratio
- Simple and robust

**Pattern 4: Padding-Bottom Hack (Legacy)**
```css
.container {
  position: relative;
  padding-bottom: 56.25%; /* 16:9 ratio */
}
```
- Works everywhere but hacky
- Deprecated in favor of `aspect-ratio`

### Decision
Use **Pattern 3** for mobile: change image from `position: absolute` to `position: static` (or `relative`) with responsive sizing. Keep absolute positioning for desktop where it works correctly.

### Rationale
This is the simplest fix that:
1. Requires minimal CSS changes
2. Doesn't break the existing desktop layout
3. Follows mobile-first responsive design
4. Maintains the overlay system

---

## Research Task 4: Mobile Breakpoint Strategy

### Question
What breakpoints should be used, and should they match existing patterns?

### Investigation

Current breakpoints in the CSS:
- Mobile: `< 1024px` (default styles)
- Desktop: `>= 1024px` (media query)

Constitution requirement (Section 14.5):
- "Touch-optimized tap targets (min 44px)"
- Viewport sizes to test: 320px, 375px, 414px, 428px (mobile), 768px, 834px, 1024px (tablet)

### Decision
Maintain the existing 1024px breakpoint. Add intermediate breakpoints only if needed for the fix.

### Rationale
Consistency with existing code. The 1024px breakpoint is well-established in the codebase.

---

## Research Task 5: Testing Strategy

### Question
How should the fix be validated across devices?

### Decision
Create a testing checklist covering:
1. Chrome DevTools responsive mode at: 320px, 375px, 414px, 768px, 834px, 1024px, 1440px
2. Both light and dark themes
3. Portrait and landscape orientations
4. Accessibility audit (Lighthouse)

---

## Summary of Findings

| Topic | Decision | Confidence |
|-------|----------|------------|
| Root Cause | Missing height context for absolute positioning | High |
| Solution Approach | Remove absolute positioning on mobile | High |
| CSS Pattern | Static/relative positioning with object-fit | High |
| Breakpoint | Keep existing 1024px | High |
| Testing | Chrome DevTools + Lighthouse | High |

## Implementation Guidance

The fix requires **2-3 CSS rule changes** in `index.module.css`:

1. **Mobile image positioning**: Change from `position: absolute` to `position: relative` or `static`
2. **Mobile image sizing**: Use `width: 100%; height: auto;` instead of `height: 100%`
3. **Optionally**: Add explicit `min-height` or `aspect-ratio` to image section for consistent sizing

No changes needed to `index.tsx` - the fix is purely CSS.
