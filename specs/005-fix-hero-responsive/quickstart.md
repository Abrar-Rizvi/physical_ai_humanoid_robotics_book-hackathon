# Quickstart: Fix Hero Section Responsive Image

**Feature**: 005-fix-hero-responsive
**Estimated Effort**: ~30 minutes
**Files to Modify**: 1 (CSS only)

## Prerequisites

- Node.js >= 20.0
- Access to `robotic-book/src/pages/` directory
- Browser with DevTools for testing

## Quick Fix Summary

The Hero image disappears on mobile because `position: absolute` with `height: 100%` doesn't work when the parent only has `min-height` (not explicit `height`).

**Solution**: Use static positioning with responsive sizing on mobile viewports.

## Implementation Steps

### Step 1: Backup Current CSS (Optional)

```bash
cd robotic-book/src/pages
cp index.module.css index.module.css.backup
```

### Step 2: Update Mobile Image Styles

Open `robotic-book/src/pages/index.module.css` and modify the following sections:

**Before** (lines 97-106):
```css
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
```

**After** (mobile-first responsive):
```css
/* Mobile: Static positioning with auto height */
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

### Step 3: Add Desktop Override

Add inside the `@media (min-width: 1024px)` block:

```css
@media (min-width: 1024px) {
  /* ... existing rules ... */

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

### Step 4: Update Image Container for Mobile

**Before**:
```css
.heroImageContainer {
  position: relative;
  width: 100%;
  height: 100%;
  overflow: hidden;
}
```

**After**:
```css
.heroImageContainer {
  position: relative;
  width: 100%;
  min-height: 300px;
  overflow: hidden;
}
```

And add desktop override:
```css
@media (min-width: 1024px) {
  .heroImageContainer {
    height: 100%;
    min-height: auto;
  }
}
```

## Verification

### Local Testing

```bash
cd robotic-book
npm run start
```

Open browser DevTools and test at these widths:
- [ ] 320px (small mobile)
- [ ] 375px (iPhone SE)
- [ ] 414px (iPhone Plus)
- [ ] 768px (tablet)
- [ ] 1024px (desktop breakpoint)
- [ ] 1440px (large desktop)

### Checklist

- [ ] Image visible on all viewports
- [ ] No distortion or stretching
- [ ] Text and CTA not overlapping image
- [ ] Works in both light and dark mode
- [ ] Desktop layout unchanged

## Rollback

If issues occur:

```bash
cd robotic-book/src/pages
cp index.module.css.backup index.module.css
```

## Architecture Notes

The fix follows the mobile-first approach already established in the CSS:
1. Default styles (mobile): Static positioning, responsive height
2. Desktop override (@media 1024px+): Absolute positioning for overlay effect

This pattern ensures the image is always visible while maintaining the desktop visual design.
