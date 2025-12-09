# Research & Technical Decisions: Homepage Overhaul

**Feature**: Complete Homepage Overhaul with Premium Robot-Themed Visuals
**Branch**: 004-homepage-overhaul
**Date**: 2025-12-09

## Overview

This document resolves all technical unknowns identified in the implementation plan's Phase 0. Each research question is answered with a concrete decision, rationale, and alternatives considered.

---

## 1. LQIP (Low-Quality Image Placeholder) Implementation Strategy

### Question

How should we implement LQIP (Low-Quality Image Placeholder) technique for progressive image loading in React components without external dependencies?

### Research Findings

**LQIP Techniques Available**:

1. **Manual Base64 Generation**: Pre-generate tiny (~20x27px for hero, ~20x15px for cards) images, convert to base64, embed in component
2. **Build-Time Tool**: Use imagemin/sharp in a Node.js script to auto-generate LQIP during build
3. **Runtime Technique**: Load small thumbnail first, then swap to full image using `onLoad` event

**React Implementation Patterns**:

- **useState Hook**: Track `imageLoaded` state, conditionally apply blur filter
- **CSS Transition**: Smooth fade from LQIP to full image using `opacity` and `filter: blur()`
- **Picture Element**: Use `<picture>` with multiple sources for WebP + fallback

### Decision

**✅ Manual Base64 Generation with useState Hook**

**Implementation**:

```typescript
const [imageLoaded, setImageLoaded] = useState(false);
const lqipDataUrl = "data:image/jpeg;base64,/9j/4AAQ..."; // Tiny base64 image

<div className={styles.heroImageContainer}>
  <img
    src={lqipDataUrl}
    alt="Hero robot placeholder"
    className={styles.heroImagePlaceholder}
    style={{ filter: imageLoaded ? 'none' : 'blur(20px)' }}
  />
  <img
    src="/img/hero-robot.webp"
    alt="Futuristic humanoid robot"
    className={styles.heroImage}
    style={{ opacity: imageLoaded ? 1 : 0 }}
    onLoad={() => setImageLoaded(true)}
    loading="lazy"
  />
</div>
```

**Rationale**:

- No build-time dependencies or complex tooling required (aligns with FR-030: zero new npm packages)
- Full control over LQIP quality and file size (can hand-optimize tiny images to <2KB base64)
- Simple React pattern using standard hooks (no framework-specific magic)
- Predictable performance (no runtime image processing overhead)

**Alternatives Considered**:

- **Build-Time Tool (sharp/imagemin)**: Rejected due to added complexity and npm dependency requirement. Generates LQIPs automatically but adds build step overhead.
- **Runtime Technique (Intersection Observer)**: Rejected as over-engineered for 4 images. Better suited for image-heavy sites with dozens of lazy-loaded images.
- **CSS-only blur-up**: Rejected because CSS `background-image` doesn't support progressive loading without JavaScript state management.

**Generation Workflow**:

1. Download robot images from Unsplash at suggested URLs
2. Resize to tiny dimensions (20-30px wide) using ImageMagick or online tool (Squoosh)
3. Convert to base64 using online converter or `base64` command
4. Embed in component as string constant

**Example Base64 LQIP Size**: ~1.5-2KB per image (acceptable inline overhead)

---

## 2. WebP Fallback Implementation

### Question

How should we implement WebP images with JPG fallback for maximum browser compatibility?

### Research Findings

**Browser Support**:

- WebP support: Chrome 23+, Firefox 65+, Safari 14+, Edge 18+ (all covered by FR-019 browser requirements)
- All target browsers (Chrome 90+, Firefox 88+, Safari 14+, Edge 90+) support WebP

**Implementation Options**:

1. **`<picture>` Element**: HTML5 standard, browser automatically selects best format
2. **Dynamic `src` Switching**: JavaScript feature detection + conditional rendering
3. **WebP Only**: Skip fallback since all target browsers support WebP

### Decision

**✅ `<picture>` Element with WebP + JPG Fallback**

**Implementation**:

```typescript
<picture>
  <source srcSet="/img/hero-robot.webp" type="image/webp" />
  <source srcSet="/img/hero-robot.jpg" type="image/jpeg" />
  <img
    src="/img/hero-robot.jpg"
    alt="Futuristic humanoid robot"
    className={styles.heroImage}
    onLoad={() => setImageLoaded(true)}
    loading="lazy"
  />
</picture>
```

**Rationale**:

- **Standards-based**: HTML5 `<picture>` element is the recommended approach (no JavaScript required for format selection)
- **Automatic fallback**: Browser natively selects WebP if supported, JPG otherwise
- **Future-proof**: Easy to add AVIF or other formats later by adding `<source>` tags
- **Accessibility**: Single `<img>` tag maintains alt text and semantic HTML
- **Performance**: Browser-native selection is faster than JavaScript feature detection

**Alternatives Considered**:

- **WebP Only**: Rejected to maintain defensive coding practice, even though all target browsers support WebP. Protects against edge cases (older enterprise browsers, proxy image optimization services that strip WebP).
- **JavaScript Feature Detection**: Rejected as over-engineered. `<picture>` element handles this natively without runtime overhead.

**File Naming Convention**:

- WebP: `hero-robot.webp`, `feature-humanoid.webp`, `feature-arm.webp`, `feature-ai-brain.webp`
- JPG Fallback: Same base names with `.jpg` extension

---

## 3. CSS Modules Dark Mode Integration

### Question

How should CSS Modules access Docusaurus theme variables (--ifm-*) for light/dark mode support?

### Research Findings

**Docusaurus Theme System**:

- Docusaurus uses CSS custom properties (CSS variables) prefixed with `--ifm-*`
- Theme toggle adds `data-theme="dark"` attribute to `<html>` element
- Global theme variables defined in `src/css/custom.css`

**CSS Modules Integration Approaches**:

1. **Direct CSS Custom Properties**: Use `var(--ifm-color-primary)` in CSS Modules
2. **`data-theme` Attribute Selectors**: `[data-theme='dark'] .className { ... }`
3. **Hybrid Approach**: Use both --ifm-* variables AND data-theme selectors for override flexibility

### Decision

**✅ Hybrid Approach: CSS Custom Properties + data-theme Selectors**

**Implementation**:

```css
/* hero.module.css */
.heroContainer {
  background: var(--ifm-background-color);
  color: var(--ifm-font-color-base);
  max-width: 1400px;
}

.heroImageOverlay {
  background: linear-gradient(
    to right,
    transparent,
    rgba(0, 0, 0, 0.3)
  );
}

[data-theme='dark'] .heroImageOverlay {
  background: linear-gradient(
    to right,
    transparent,
    rgba(0, 0, 0, 0.6) /* Darker overlay for dark mode */
  );
}

.featureCard {
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
}

[data-theme='dark'] .featureCard {
  background: rgba(30, 30, 30, 0.3);
  border: 1px solid rgba(255, 255, 255, 0.1);
}
```

**Rationale**:

- **Automatic theme adaptation**: `var(--ifm-*)` variables automatically update when theme toggles
- **Granular control**: `data-theme` selectors allow component-specific dark mode adjustments (e.g., darker image overlay, adjusted glassmorphism opacity)
- **Zero layout shift**: Both approaches are CSS-only, no JavaScript recalculation, ensuring CLS = 0 (FR-021)
- **Docusaurus best practice**: Aligns with official Docusaurus theming documentation

**Alternatives Considered**:

- **CSS Custom Properties Only**: Rejected because some adjustments (glassmorphism opacity, image overlay darkness) need explicit dark mode values, not just variable swapping.
- **data-theme Selectors Only**: Rejected because it duplicates all color/spacing values instead of leveraging Docusaurus theme infrastructure.

**Theme Variables to Use**:

- `--ifm-background-color`: Container backgrounds
- `--ifm-font-color-base`: Primary text color
- `--ifm-color-primary`: CTA button background
- `--ifm-color-primary-dark`: CTA button hover state

---

## 4. Glassmorphism Browser Compatibility

### Question

How should we handle `backdrop-filter` browser compatibility and provide graceful degradation for unsupported browsers?

### Research Findings

**Browser Support for `backdrop-filter`**:

- Chrome 76+ ✅
- Firefox 103+ ✅ (enabled by default)
- Safari 9+ ✅ (with `-webkit-` prefix in older versions)
- Edge 79+ ✅

**Target Browser Compatibility** (from spec):

- Chrome 90+ ✅ Full support
- Firefox 88+ ⚠️ Partial support (needs flag in 88-102, full support in 103+)
- Safari 14+ ✅ Full support
- Edge 90+ ✅ Full support

**Fallback Strategies**:

1. **`@supports` Feature Detection**: Conditional CSS based on backdrop-filter support
2. **Solid Fallback by Default**: Always use solid background, enhance with backdrop-filter
3. **No Fallback**: Assume all target browsers support it (risky)

### Decision

**✅ `@supports` Feature Detection with Solid Semi-Transparent Fallback**

**Implementation**:

```css
/* features.module.css */
.featureCard {
  /* Fallback: solid semi-transparent background */
  background: rgba(255, 255, 255, 0.95);
  border: 1px solid rgba(255, 255, 255, 0.3);
  box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.1);
  border-radius: 16px;
  padding: 32px;
}

/* Progressive enhancement: glassmorphism for supporting browsers */
@supports (backdrop-filter: blur(10px)) {
  .featureCard {
    background: rgba(255, 255, 255, 0.1);
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255, 255, 255, 0.2);
  }
}

[data-theme='dark'] .featureCard {
  background: rgba(30, 30, 30, 0.95); /* Solid fallback */
}

@supports (backdrop-filter: blur(10px)) {
  [data-theme='dark'] .featureCard {
    background: rgba(30, 30, 30, 0.3);
    backdrop-filter: blur(10px);
  }
}
```

**Rationale**:

- **Graceful degradation**: Firefox 88-102 users (if any) get solid backgrounds instead of broken transparency
- **Progressive enhancement**: Modern browsers get premium glassmorphism effect
- **Accessibility**: Solid fallback ensures text remains readable on all browsers
- **Defensive coding**: Protects against unexpected browser edge cases or corporate proxy stripping

**Alternatives Considered**:

- **Glassmorphism Only (No Fallback)**: Rejected due to Firefox 88-102 gap. Even though this is a small subset, constitution principle "Engineering accuracy" demands robustness.
- **Solid Background Only**: Rejected because all target browsers *do* support backdrop-filter with workarounds. Missing out on premium visual effect unnecessarily.

**Testing Strategy**:

- Primary: Test in Chrome 90+, Firefox 103+, Safari 14+ (full glassmorphism)
- Edge Case: Test in Firefox 88 (if available) or use DevTools to simulate lack of backdrop-filter support

---

## 5. Performance Optimization for Large Images

### Question

How should we optimize images (hero ~200KB, feature cards ~150KB each) and implement lazy loading?

### Research Findings

**Image Optimization Tools**:

- **Squoosh.app**: Online tool, manual optimization, excellent quality/size balance
- **ImageMagick**: Command-line tool, scriptable, good quality
- **Sharp (Node.js)**: Build-time optimization, requires npm dependency
- **Online services**: TinyPNG, Compressor.io

**Lazy Loading Approaches**:

1. **Native `loading="lazy"`**: HTML attribute, browser-native, excellent support (Chrome 77+, Firefox 75+, Safari 15.4+)
2. **Intersection Observer API**: JavaScript-based, more control, requires polyfill for old browsers
3. **No lazy loading**: Load all images immediately

### Decision

**✅ Manual Optimization with Squoosh + Native `loading="lazy"`**

**Image Optimization Workflow**:

1. Download high-res images from Unsplash at suggested URLs
2. Resize using Squoosh.app:
   - Hero: 1200x1600px, WebP quality 80, target ~180KB
   - Feature cards: 800x600px, WebP quality 75, target ~130KB
3. Generate JPG fallbacks using Squoosh (JPEG quality 85)
4. Generate LQIP versions: 20px wide, base64 encode
5. Store in `static/img/` with clear naming convention

**Lazy Loading Implementation**:

```typescript
<img
  src="/img/hero-robot.webp"
  alt="Futuristic humanoid robot"
  loading="lazy"  // Native lazy loading
  className={styles.heroImage}
  onLoad={() => setImageLoaded(true)}
/>
```

**Rationale**:

- **Zero npm dependencies**: Manual optimization avoids sharp/imagemin installation (aligns with FR-030)
- **One-time setup**: Only 4 images to optimize, not hundreds. Manual workflow is acceptable.
- **Predictable quality**: Hand-tuning quality settings ensures optimal balance for each image
- **Native lazy loading**: Excellent browser support (all target browsers), zero JavaScript overhead, better performance than Intersection Observer

**Alternatives Considered**:

- **Build-Time Optimization (sharp)**: Rejected due to npm dependency requirement and overkill for 4 static images.
- **Intersection Observer**: Rejected as over-engineered. Native `loading="lazy"` is simpler and performs better for this use case.
- **No Lazy Loading**: Rejected because hero image is above-the-fold (okay to load immediately) but feature card images are below-the-fold and benefit from deferred loading.

**Lazy Loading Strategy**:

- **Hero Image**: Do NOT lazy load (above-the-fold, needs to render immediately)
- **Feature Card Images**: DO lazy load (below-the-fold, deferred load improves FCP and TTI)

```typescript
// Hero: No lazy loading (above fold)
<img src="/img/hero-robot.webp" alt="..." />

// Feature cards: Lazy load (below fold)
<img src="/img/feature-humanoid.webp" loading="lazy" alt="..." />
```

**Final Image Specifications**:

| Image | Dimensions | WebP Size | JPG Size | LQIP Base64 |
|-------|-----------|-----------|----------|-------------|
| hero-robot | 1200x1600px | ~180KB | ~200KB | ~1.8KB |
| feature-humanoid | 800x600px | ~130KB | ~150KB | ~1.5KB |
| feature-arm | 800x600px | ~130KB | ~150KB | ~1.5KB |
| feature-ai-brain | 800x600px | ~130KB | ~150KB | ~1.5KB |
| **Total** | - | **~570KB** | **~650KB** | **~6.3KB** |

---

## 6. Responsive Breakpoint Implementation

### Question

Should we use mobile-first (min-width) or desktop-first (max-width) media queries for the 1024px primary breakpoint?

### Research Findings

**Mobile-First Approach**:

```css
/* Base styles: mobile (<1024px) */
.heroContainer { flex-direction: column; }

/* Desktop (>=1024px) */
@media (min-width: 1024px) {
  .heroContainer { flex-direction: row; }
}
```

**Desktop-First Approach**:

```css
/* Base styles: desktop (>=1024px) */
.heroContainer { flex-direction: row; }

/* Mobile (<1024px) */
@media (max-width: 1023px) {
  .heroContainer { flex-direction: column; }
}
```

**Industry Best Practices**:

- **Mobile-first**: Recommended by Web.dev, MDN, CSS-Tricks
- Aligns with "progressive enhancement" philosophy
- Smaller base CSS (mobile styles are simpler, desktop adds complexity)
- Better performance on mobile devices (majority of traffic per spec: 50-70%)

### Decision

**✅ Mobile-First Approach with `min-width` Media Queries**

**Implementation**:

```css
/* hero.module.css */
.heroContainer {
  display: flex;
  flex-direction: column; /* Mobile: stacked */
  width: 100%;
  min-height: 100vh;
}

.heroTextSection {
  width: 100%;
  padding: 40px 20px;
}

.heroImageSection {
  width: 100%;
  min-height: 50vh;
}

/* Desktop: 2-column layout */
@media (min-width: 1024px) {
  .heroContainer {
    flex-direction: row;
    max-width: 1400px;
    margin: 0 auto;
    min-height: 90vh;
  }

  .heroTextSection {
    width: 50%;
    padding: 60px;
  }

  .heroImageSection {
    width: 50%;
    min-height: auto;
  }
}
```

**Rationale**:

- **Mobile-first best practice**: Aligns with Web.dev and Docusaurus responsive design principles
- **Performance**: Mobile devices (50-70% of traffic) load fewer CSS rules before media query evaluation
- **Simpler base styles**: Mobile layouts (stacked, 100% width) require less CSS than desktop (flexbox columns, centering)
- **Progressive enhancement**: Desktop layout is an *enhancement* of the mobile base, not a reduction

**Alternatives Considered**:

- **Desktop-First**: Rejected because mobile-first is industry standard and performs better for majority traffic (mobile/tablet).

**Breakpoint Values**:

- **Base styles**: 0px - 1023px (mobile and tablet, stacked layout)
- **`@media (min-width: 1024px)`**: Desktop (2-column hero, horizontal feature cards)
- **No intermediate breakpoint at 768px**: Simplified per clarification #5 (tablets use same stacked layout as mobile)

---

## 7. React 19.0.0 Compatibility

### Question

Are there any breaking changes or new patterns in React 19.0.0 that affect this implementation?

### Research Findings

**React 19 Major Changes**:

- **Actions**: New form actions and `useActionState` hook (not relevant for this feature)
- **Server Components**: RSC support (not applicable to Docusaurus client-side rendering)
- **Ref Handling**: Improved ref forwarding (not used in this feature)
- **Hooks**: No breaking changes to `useState`, `useEffect`

**Docusaurus 3.9.2 + React 19 Compatibility**:

- Docusaurus 3.9.2 officially supports React 19.0.0 (confirmed in package.json)
- No known compatibility issues with functional components + hooks

### Decision

**✅ Use Standard React Hooks (useState) - No Changes Required**

**Implementation**:

```typescript
import {useState} from 'react';

function HeroSection() {
  const [imageLoaded, setImageLoaded] = useState(false);

  // Standard React patterns work as expected
}
```

**Rationale**:

- React 19 is backward-compatible for functional components and hooks
- No new patterns required for this static UI component
- Existing Docusaurus + React best practices apply

**No Action Required**: Proceed with standard React functional components and hooks.

---

## 8. TypeScript 5.6.2 Type Safety

### Question

How should we handle TypeScript types for image imports and CSS Module imports?

### Research Findings

**Docusaurus TypeScript Configuration**:

- Docusaurus 3.9.2 includes @docusaurus/module-type-aliases for built-in type definitions
- CSS Modules automatically typed via `*.module.css` pattern
- Image imports require manual type declaration or `require()` syntax

**Type Declaration Approaches**:

1. **Module declaration**: Create `global.d.ts` with image types
2. **`require()` syntax**: Bypass TypeScript strict checking
3. **ES import with assertion**: Use `import img from './img.webp'` (requires type declaration)

### Decision

**✅ Use Direct String Paths for Images (No Import Required)**

**Implementation**:

```typescript
// ✅ Recommended: Direct string paths (images in static/img/)
<img src="/img/hero-robot.webp" alt="..." />

// CSS Modules: Automatically typed
import styles from './hero.module.css';
<div className={styles.heroContainer}>
```

**Rationale**:

- **Simpler**: No TypeScript configuration required, no type declarations
- **Static assets**: Images in `static/img/` are served as-is by Docusaurus, not bundled
- **No build-time processing**: Direct paths bypass webpack/module bundling complexity
- **Type safety**: CSS Modules automatically get type definitions from `*.module.css` pattern

**Alternatives Considered**:

- **Image Imports with require()**: Rejected because images are static assets, not bundled modules.
- **Custom Type Declarations**: Rejected as unnecessary overhead for static image paths.

**CSS Module Typing**:

```typescript
// Automatic type inference from styles.module.css
import styles from './hero.module.css';

// TypeScript knows these class names exist:
className={styles.heroContainer}  // ✅ Type-safe
className={styles.typoError}      // ❌ TypeScript error
```

---

## Summary of Decisions

| Research Question | Decision | Key Rationale |
|-------------------|----------|---------------|
| **1. LQIP Implementation** | Manual base64 generation + useState | Zero dependencies, full control, simple React pattern |
| **2. WebP Fallback** | `<picture>` element with WebP + JPG | Standards-based, automatic browser selection, future-proof |
| **3. Dark Mode Integration** | CSS custom properties + data-theme selectors | Automatic theme adaptation + granular control |
| **4. Glassmorphism Fallback** | `@supports` with solid fallback | Graceful degradation, Firefox 88-102 compatibility |
| **5. Image Optimization** | Manual Squoosh + native `loading="lazy"` | Zero dependencies, hand-tuned quality, excellent browser support |
| **6. Responsive Breakpoints** | Mobile-first with `min-width: 1024px` | Industry best practice, performance for mobile majority |
| **7. React 19 Compatibility** | Standard hooks (no changes needed) | Backward-compatible, Docusaurus 3.9.2 support |
| **8. TypeScript Typing** | Direct string paths for images | Simpler, static assets, auto-typed CSS Modules |

---

## Next Steps

All technical unknowns resolved. Ready for **Phase 1: Design & Contracts**.

Phase 1 will produce:

1. **data-model.md**: Component props interfaces and state shape (completed in this document, see Section 1)
2. **quickstart.md**: Developer guide for implementing the redesigned components
3. **contracts/**: N/A (no API contracts for frontend component)

**Status**: ✅ Research Complete
**Phase 0 Output**: This file (research.md)
**Next Command**: Continue to Phase 1 to generate data-model.md and quickstart.md
