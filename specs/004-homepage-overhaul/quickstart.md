# Quickstart Guide: Homepage Overhaul Implementation

**Feature**: Complete Homepage Overhaul with Premium Robot-Themed Visuals
**Branch**: 004-homepage-overhaul
**Date**: 2025-12-09

## Overview

This guide provides step-by-step instructions for implementing the redesigned homepage with premium robot-themed visuals. Follow these steps sequentially to ensure proper implementation.

**Estimated Time**: 4-6 hours (including image optimization and testing)

---

## Prerequisites

Before starting, ensure you have:

- [x] Node.js 20+ installed
- [x] Git repository cloned and on `004-homepage-overhaul` branch
- [x] Docusaurus development server running (`npm start` in `robotic-book/` directory)
- [x] Modern browser with DevTools (Chrome 90+, Firefox 103+, or Safari 14+)
- [x] Image optimization tool access (Squ oosh.app or equivalent)

**Verify Prerequisites**:
```bash
# Check Node version
node --version  # Should be v20.x.x or higher

# Check current branch
git branch --show-current  # Should output: 004-homepage-overhaul

# Start development server (in robotic-book/ directory)
cd robotic-book
npm start  # Opens http://localhost:3000
```

---

## Step 1: Prepare Image Assets (Est. 60-90 min)

### 1.1 Download Robot Images from Unsplash

Download the following images at the specified URLs:

**Hero Image**:
- URL: `https://images.unsplash.com/photo-1535378620166-273708d44e4c?w=1200&q=80`
- Alternative: `https://images.unsplash.com/photo-1581091226825-a6a2a5aee158?w=1200&q=80`
- Save as: `hero-robot-original.jpg`

**Feature Card Images**:
- Card 1 (Humanoid): `https://images.unsplash.com/photo-1561557944-6e7860d1a7eb?w=800&q=80` → `feature-humanoid-original.jpg`
- Card 2 (Robotic Arm): `https://images.unsplash.com/photo-1563207153-f403bf289096?w=800&q=80` → `feature-arm-original.jpg`
- Card 3 (AI Brain): `https://images.unsplash.com/photo-1677442136019-21780ecad995?w=800&q=80` → `feature-ai-brain-original.jpg`

### 1.2 Optimize Images with Squoosh

Visit https://squoosh.app and optimize each image:

**Hero Image (1200x1600px)**:
1. Upload `hero-robot-original.jpg`
2. Resize to 1200x1600px (portrait)
3. Export as **WebP**: Quality 80, target ~180KB
4. Export as **JPG**: Quality 85, target ~200KB
5. Save as `hero-robot.webp` and `hero-robot.jpg`

**Feature Card Images (800x600px each)**:
1. Upload each original feature image
2. Resize to 800x600px (landscape 4:3 ratio)
3. Export as **WebP**: Quality 75, target ~130KB
4. Export as **JPG**: Quality 85, target ~150KB
5. Save with consistent naming:
   - `feature-humanoid.webp` / `feature-humanoid.jpg`
   - `feature-arm.webp` / `feature-arm.jpg`
   - `feature-ai-brain.webp` / `feature-ai-brain.jpg`

### 1.3 Generate LQIP (Low-Quality Image Placeholders)

For each optimized image, create a tiny LQIP version:

**Using Squoosh**:
1. Resize to 20px wide (maintain aspect ratio, will be ~27px tall for hero, ~15px tall for cards)
2. Export as JPG, quality 60
3. Convert to base64 using online tool: https://www.base64-image.de/
4. Copy base64 string (starts with `data:image/jpeg;base64,`)

**LQIP Output** (save for later use in code):
- `hero-robot-lqip.txt` → Contains base64 string (~1.8KB)
- `feature-humanoid-lqip.txt` → Contains base64 string (~1.5KB)
- `feature-arm-lqip.txt` → Contains base64 string (~1.5KB)
- `feature-ai-brain-lqip.txt` → Contains base64 string (~1.5KB)

### 1.4 Move Optimized Images to Project

```bash
# From project root (humanoid-robotic-book/)
cd robotic-book/static/img

# Copy all optimized images here
# You should have:
# - hero-robot.webp, hero-robot.jpg
# - feature-humanoid.webp, feature-humanoid.jpg
# - feature-arm.webp, feature-arm.jpg
# - feature-ai-brain.webp, feature-ai-brain.jpg
```

**Verify Image Sizes**:
```bash
ls -lh *.webp *.jpg
# hero-robot.webp should be ~180KB
# Each feature-*.webp should be ~130KB
```

---

## Step 2: Update Hero Section (Est. 90 min)

### 2.1 Backup Current Homepage

```bash
cd robotic-book/src/pages
cp index.tsx index.tsx.backup
cp index.module.css index.module.css.backup
```

### 2.2 Replace index.tsx with New Hero Section

Open `robotic-book/src/pages/index.tsx` and replace `HomepageHeader` function with:

```typescript
import {useState} from 'react';
import type {ReactNode} from 'react';
import clsx from 'clsx';
import Link from '@docusaurus/Link';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import Layout from '@theme/Layout';
import HomepageFeatures from '@site/src/components/HomepageFeatures';
import Heading from '@theme/Heading';

import styles from './index.module.css';

function HomepageHeader() {
  const [heroImageLoaded, setHeroImageLoaded] = useState(false);

  // LQIP base64 data (replace with your actual base64 string from hero-robot-lqip.txt)
  const heroLQIP = "data:image/jpeg;base64,/9j/4AAQ..."; // Paste your LQIP here

  return (
    <header className={styles.heroContainer}>
      <div className={styles.heroTextSection}>
        <Heading as="h1" className={styles.heroHeadline}>
          Master Physical AI & Build Real Humanoid Robots
        </Heading>
        <Heading as="h2" className={styles.heroSubheadline}>
          The most practical, hands-on course on ROS 2, Gazebo, MoveIt, LLMs and real hardware
        </Heading>
        <p className={styles.heroParagraph}>
          Learn to design, simulate, and deploy autonomous humanoid robots from scratch.
          This comprehensive course combines cutting-edge AI models with industry-standard
          robotics frameworks, giving you the skills to build the future of physical intelligence.
        </p>
        <Link className={styles.heroCTA} to="/docs/intro">
          Start Learning Free 🚀
        </Link>
      </div>

      <div className={styles.heroImageSection}>
        <div className={styles.heroImageContainer}>
          {/* LQIP placeholder */}
          <img
            src={heroLQIP}
            alt="Hero robot placeholder"
            className={styles.heroImagePlaceholder}
            style={{
              filter: heroImageLoaded ? 'blur(0px)' : 'blur(20px)',
              opacity: heroImageLoaded ? 0 : 1,
            }}
          />

          {/* Full-resolution image with WebP fallback */}
          <picture>
            <source srcSet="/img/hero-robot.webp" type="image/webp" />
            <source srcSet="/img/hero-robot.jpg" type="image/jpeg" />
            <img
              src="/img/hero-robot.jpg"
              alt="Futuristic humanoid robot showcasing advanced Physical AI capabilities"
              className={styles.heroImage}
              style={{ opacity: heroImageLoaded ? 1 : 0 }}
              onLoad={() => setHeroImageLoaded(true)}
            />
          </picture>

          {/* Gradient overlay for text readability */}
          <div className={styles.heroImageOverlay} />
        </div>
      </div>
    </header>
  );
}

export default function Home(): ReactNode {
  const {siteConfig} = useDocusaurusContext();
  return (
    <Layout
      title={`Learn Physical AI & Humanoid Robotics`}
      description="Master ROS 2, Gazebo, MoveIt, LLMs and real robot hardware with hands-on projects">
      <HomepageHeader />
      <main>
        <HomepageFeatures />
      </main>
    </Layout>
  );
}
```

### 2.3 Replace index.module.css with Hero Styling

Open `robotic-book/src/pages/index.module.css` and replace entire content with:

```css
/* Hero Container - Mobile First */
.heroContainer {
  display: flex;
  flex-direction: column;
  width: 100%;
  min-height: 100vh;
  position: relative;
  overflow: hidden;
}

/* Hero Text Section - Mobile */
.heroTextSection {
  width: 100%;
  padding: 40px 20px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  text-align: center;
  background: var(--ifm-background-color);
  color: var(--ifm-font-color-base);
  z-index: 2;
}

.heroHeadline {
  font-size: 36px;
  font-weight: 800;
  line-height: 1.2;
  margin-bottom: 16px;
  max-width: 100%;
}

.heroSubheadline {
  font-size: 18px;
  font-weight: 600;
  line-height: 1.4;
  margin-bottom: 20px;
  max-width: 100%;
  opacity: 0.9;
}

.heroParagraph {
  font-size: 16px;
  font-weight: 400;
  line-height: 1.6;
  margin-bottom: 32px;
  max-width: 100%;
  opacity: 0.85;
}

.heroCTA {
  display: inline-block;
  padding: 14px 32px;
  font-size: 18px;
  font-weight: 700;
  background: var(--ifm-color-primary);
  color: white;
  border-radius: 8px;
  text-decoration: none;
  transition: all 200ms ease;
  min-height: 48px;
  line-height: 1.2;
}

.heroCTA:hover {
  background: var(--ifm-color-primary-dark);
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  text-decoration: none;
  color: white;
}

/* Hero Image Section - Mobile */
.heroImageSection {
  width: 100%;
  min-height: 50vh;
  position: relative;
}

.heroImageContainer {
  position: relative;
  width: 100%;
  height: 100%;
  overflow: hidden;
}

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

.heroImagePlaceholder {
  z-index: 1;
}

.heroImage {
  z-index: 2;
}

.heroImageOverlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: linear-gradient(to right, transparent 0%, rgba(0, 0, 0, 0.3) 100%);
  z-index: 3;
  pointer-events: none;
}

[data-theme='dark'] .heroImageOverlay {
  background: linear-gradient(to right, transparent 0%, rgba(0, 0, 0, 0.6) 100%);
}

/* Desktop Layout (>=1024px) */
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
    align-items: flex-start;
    text-align: left;
  }

  .heroHeadline {
    font-size: 56px;
    max-width: 600px;
  }

  .heroSubheadline {
    font-size: 24px;
    max-width: 600px;
  }

  .heroParagraph {
    font-size: 18px;
    max-width: 600px;
  }

  .heroCTA {
    min-height: 56px;
    min-width: 200px;
    padding: 18px 40px;
  }

  .heroImageSection {
    width: 50%;
    min-height: auto;
  }
}

/* Accessibility: Reduced Motion */
@media (prefers-reduced-motion: reduce) {
  .heroCTA:hover {
    transform: none;
  }

  .heroImagePlaceholder,
  .heroImage {
    transition: opacity 300ms ease; /* Keep fade, remove blur transform */
  }
}
```

### 2.4 Test Hero Section

1. Save files and check browser (http://localhost:3000)
2. Verify mobile layout (DevTools → Responsive mode → 375px width)
3. Verify desktop layout (Resize to 1400px+ width)
4. Test dark mode toggle (click sun/moon icon in navbar)
5. Verify CLS = 0 during theme toggle (Performance panel → Experience → Cumulative Layout Shift)

---

## Step 3: Update Feature Cards (Est. 90 min)

### 3.1 Backup Current Features Component

```bash
cd robotic-book/src/components/HomepageFeatures
cp index.tsx index.tsx.backup
cp styles.module.css styles.module.css.backup
```

### 3.2 Replace HomepageFeatures/index.tsx

Open `robotic-book/src/components/HomepageFeatures/index.tsx` and replace entire content with:

```typescript
import type {ReactNode} from 'react';
import clsx from 'clsx';
import Heading from '@theme/Heading';
import styles from './styles.module.css';

interface FeatureCardProps {
  title: string;
  description: string;
  imageWebP: string;
  imageJPG: string;
  imageAlt: string;
}

const FEATURE_LIST: FeatureCardProps[] = [
  {
    title: "Industry-Standard Tools",
    description: "Master ROS 2, Gazebo, and MoveIt—the same frameworks powering Boston Dynamics, Tesla, and leading robotics labs worldwide.",
    imageWebP: "/img/feature-humanoid.webp",
    imageJPG: "/img/feature-humanoid.jpg",
    imageAlt: "Humanoid robot demonstrating bipedal locomotion and balance",
  },
  {
    title: "Real Hardware Integration",
    description: "Go beyond simulation with hands-on deployment to real robots. Learn sensor fusion, motor control, and safety-critical systems.",
    imageWebP: "/img/feature-arm.webp",
    imageJPG: "/img/feature-arm.jpg",
    imageAlt: "Industrial robotic arm performing precision manipulation tasks",
  },
  {
    title: "AI-Powered Intelligence",
    description: "Integrate LLMs, computer vision, and VLA models to create robots that perceive, reason, and act autonomously in dynamic environments.",
    imageWebP: "/img/feature-ai-brain.webp",
    imageJPG: "/img/feature-ai-brain.jpg",
    imageAlt: "Neural network visualization representing AI-driven robot cognition",
  },
];

function FeatureCard({title, description, imageWebP, imageJPG, imageAlt}: FeatureCardProps) {
  return (
    <div className={styles.featureCard}>
      <div className={styles.featureCardImage}>
        <picture>
          <source srcSet={imageWebP} type="image/webp" />
          <source srcSet={imageJPG} type="image/jpeg" />
          <img
            src={imageJPG}
            alt={imageAlt}
            className={styles.cardImage}
            loading="lazy"
          />
        </picture>
      </div>
      <div className={styles.featureCardContent}>
        <Heading as="h3" className={styles.featureHeading}>
          {title}
        </Heading>
        <p className={styles.featureDescription}>{description}</p>
      </div>
    </div>
  );
}

export default function HomepageFeatures(): ReactNode {
  return (
    <section className={styles.featuresContainer}>
      <div className={styles.featuresGrid}>
        {FEATURE_LIST.map((props, idx) => (
          <FeatureCard key={idx} {...props} />
        ))}
      </div>
    </section>
  );
}
```

### 3.3 Replace HomepageFeatures/styles.module.css

Open `robotic-book/src/components/HomepageFeatures/styles.module.css` and replace entire content with:

```css
/* Features Container */
.featuresContainer {
  padding: 60px 20px;
  background: var(--ifm-background-color);
}

/* Features Grid - Mobile First */
.featuresGrid {
  display: flex;
  flex-direction: column;
  gap: 24px;
  max-width: 100%;
  margin: 0 auto;
}

/* Feature Card - Mobile */
.featureCard {
  display: flex;
  flex-direction: column;
  min-height: 400px;
  border-radius: 16px;
  overflow: hidden;
  position: relative;

  /* Fallback for browsers without backdrop-filter support */
  background: rgba(255, 255, 255, 0.95);
  border: 1px solid rgba(255, 255, 255, 0.3);
  box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.1);

  transition: all 300ms cubic-bezier(0.4, 0, 0.2, 1);
}

/* Glassmorphism effect for supporting browsers */
@supports (backdrop-filter: blur(10px)) {
  .featureCard {
    background: rgba(255, 255, 255, 0.1);
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255, 255, 255, 0.2);
  }

  [data-theme='dark'] .featureCard {
    background: rgba(30, 30, 30, 0.3);
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255, 255, 255, 0.1);
  }
}

[data-theme='dark'] .featureCard {
  background: rgba(30, 30, 30, 0.95); /* Solid fallback for dark mode */
  border: 1px solid rgba(255, 255, 255, 0.15);
}

.featureCard:hover {
  transform: scale(1.04);
  box-shadow: 0 12px 40px 0 rgba(0, 0, 0, 0.2);
}

/* Feature Card Image (Top Half) */
.featureCardImage {
  position: relative;
  width: 100%;
  height: 60%;
  overflow: hidden;
}

.cardImage {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: filter 300ms ease;
}

.featureCard:hover .cardImage {
  filter: brightness(1.1);
}

/* Feature Card Content (Bottom Half) */
.featureCardContent {
  padding: 24px;
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  height: 40%;
}

.featureHeading {
  font-size: 28px;
  font-weight: 700;
  margin-bottom: 12px;
  color: var(--ifm-font-color-base);
}

.featureDescription {
  font-size: 16px;
  line-height: 1.6;
  color: var(--ifm-font-color-base);
  opacity: 0.85;
  margin: 0;
}

/* Desktop Layout (>=1024px) */
@media (min-width: 1024px) {
  .featuresContainer {
    padding: 80px 40px;
  }

  .featuresGrid {
    flex-direction: row;
    gap: 32px;
    max-width: 1400px;
  }

  .featureCard {
    flex: 1;
    min-height: 480px;
  }

  .featureCardContent {
    padding: 32px;
  }

  .featureHeading {
    font-size: 32px;
    margin-bottom: 16px;
  }

  .featureDescription {
    font-size: 18px;
  }
}

/* Accessibility: Reduced Motion */
@media (prefers-reduced-motion: reduce) {
  .featureCard {
    transition: box-shadow 300ms ease; /* Keep shadow, remove scale */
  }

  .featureCard:hover {
    transform: none;
  }

  .cardImage {
    transition: none;
  }
}
```

### 3.4 Test Feature Cards

1. Save files and reload browser
2. Verify mobile layout (single column stack)
3. Verify desktop layout (3-card horizontal row)
4. Test hover effects (scale, shadow, image brightness)
5. Test glassmorphism (check backdrop blur renders correctly)
6. Test dark mode (glassmorphism adapts to dark background)

---

## Step 4: Validation & Testing (Est. 60 min)

### 4.1 Performance Validation

**Run Lighthouse Audit**:
1. Open DevTools → Lighthouse tab
2. Select "Desktop" and "Performance + Accessibility"
3. Click "Analyze page load"
4. Verify:
   - Performance score ≥90
   - TTI (Time to Interactive) ≤3s
   - CLS (Cumulative Layout Shift) = 0

**Repeat for Mobile**:
1. Switch to "Mobile" preset
2. Run Lighthouse audit
3. Verify performance score ≥90

**Test 3G Loading**:
1. Open DevTools → Network tab
2. Set throttling to "Slow 3G"
3. Hard reload (Ctrl+Shift+R)
4. Verify hero text renders within 2 seconds
5. Verify LQIP shows before full image loads

### 4.2 Accessibility Validation

**Install axe DevTools Extension**:
- Chrome: https://chrome.google.com/webstore → Search "axe DevTools"
- Firefox: https://addons.mozilla.org → Search "axe DevTools"

**Run Accessibility Audit**:
1. Open axe DevTools panel
2. Click "Scan ALL of my page"
3. Verify 0 violations for WCAG 2.1 AA
4. Check specific items:
   - All images have `alt` text
   - CTA button has sufficient color contrast
   - Keyboard navigation works (Tab through all interactive elements)

**Test Keyboard Navigation**:
1. Click in browser address bar
2. Press Tab repeatedly
3. Verify:
   - CTA button receives focus with visible outline
   - Feature cards (if clickable) receive focus
   - Enter key activates CTA button

### 4.3 Responsive Design Testing

Test at these breakpoints:

| Viewport | Expected Behavior |
|----------|------------------|
| 375px (Mobile) | Hero stacked, features stacked vertically |
| 768px (Tablet Portrait) | Hero stacked, features stacked vertically |
| 1024px (Tablet Landscape) | Hero 2-column, features horizontal row |
| 1400px (Desktop) | Full layout, max-width container |
| 2000px (Ultra-wide) | Max-width 1400px, centered |

**Chrome DevTools Responsive Mode**:
1. Open DevTools → Toggle device toolbar (Ctrl+Shift+M)
2. Test each breakpoint above
3. Verify no horizontal scrolling at any width
4. Verify text remains readable without zooming

### 4.4 Dark Mode Testing

1. Toggle dark mode (navbar icon)
2. Verify hero section colors adapt
3. Verify feature card glassmorphism adapts (darker background)
4. Verify image overlay darkens appropriately
5. Measure CLS during toggle (should be 0)

**CLS Measurement**:
1. Open DevTools → Performance panel
2. Start recording
3. Toggle dark mode
4. Stop recording
5. Check "Experience" section → Cumulative Layout Shift → Should show 0

### 4.5 Cross-Browser Testing

Test in all supported browsers:

- ✅ Chrome 90+ (primary development browser)
- ✅ Firefox 103+ (test glassmorphism)
- ✅ Safari 14+ (test WebP fallback, -webkit- prefixes)
- ✅ Edge 90+ (test compatibility)

---

## Step 5: Git Commit & Documentation (Est. 30 min)

### 5.1 Review Changes

```bash
# From project root
git status

# Review modified files
git diff robotic-book/src/pages/index.tsx
git diff robotic-book/src/components/HomepageFeatures/index.tsx
```

### 5.2 Commit Changes

```bash
# Stage all homepage changes
git add robotic-book/src/pages/index.tsx
git add robotic-book/src/pages/index.module.css
git add robotic-book/src/components/HomepageFeatures/index.tsx
git add robotic-book/src/components/HomepageFeatures/styles.module.css
git add robotic-book/static/img/hero-robot.*
git add robotic-book/static/img/feature-*.*

# Commit with descriptive message
git commit -m "feat(homepage): Implement premium robot-themed hero and features

- Replace hero section with full-height 2-column layout (desktop) / stacked (mobile)
- Add LQIP progressive image loading for hero robot image
- Implement glassmorphism feature cards with robot imagery
- Add WebP images with JPG fallback for all assets
- Ensure WCAG 2.1 AA compliance and CLS = 0 dark mode toggle
- Optimize images: Hero ~180KB WebP, features ~130KB WebP each
- Responsive breakpoint at 1024px (mobile-first approach)
- Use CSS Modules for all styling (no Tailwind)

Closes #004-homepage-overhaul
"
```

---

## Troubleshooting

### Issue: LQIP Doesn't Blur Correctly

**Symptom**: Tiny placeholder image visible without blur effect

**Solution**:
1. Verify inline style applies `filter: blur(20px)`
2. Check that LQIP and full image have `position: absolute` in same container
3. Ensure `transition: all 300ms ease` is set for smooth effect

### Issue: Glassmorphism Not Showing

**Symptom**: Feature cards have solid backgrounds instead of frosted glass effect

**Solution**:
1. Check browser support: Firefox <103 doesn't support `backdrop-filter` by default
2. Verify `@supports (backdrop-filter: blur(10px))` block exists
3. Test in Chrome/Safari which have full support
4. Check DevTools → Computed Styles → verify `backdrop-filter` property exists

### Issue: Dark Mode CLS > 0

**Symptom**: Layout shifts when toggling dark mode

**Solution**:
1. Ensure all sizing uses CSS custom properties, not hard-coded values
2. Verify no `height: auto` switching between themes
3. Check that images have explicit dimensions or `object-fit: cover`
4. Measure specific shift using DevTools Performance panel

### Issue: Images Not Loading

**Symptom**: Broken image icons instead of robot images

**Solution**:
1. Verify images are in `robotic-book/static/img/` directory
2. Check file names match exactly (case-sensitive)
3. Ensure Docusaurus dev server is running
4. Clear browser cache (Ctrl+Shift+R)
5. Check browser console for 404 errors

### Issue: Hero Text Overlaps Image on Tablet

**Symptom**: Text and image overlap at 768-1023px breakpoint

**Solution**:
1. Verify media query is `@media (min-width: 1024px)` not `max-width`
2. Check that base styles (mobile) use `flex-direction: column`
3. Ensure tablet viewports (<1024px) use stacked layout
4. Test at exact 1024px breakpoint to confirm transition

---

## Success Checklist

Before marking this feature complete, verify all items:

### Functionality
- [ ] Hero section displays on homepage
- [ ] Hero layout is 2-column on desktop (>=1024px)
- [ ] Hero layout stacks vertically on mobile/tablet (<1024px)
- [ ] CTA button links to /docs/intro
- [ ] LQIP loads first, then blurs into full image
- [ ] WebP images load with JPG fallback
- [ ] 3 feature cards display in horizontal row (desktop)
- [ ] Feature cards stack vertically (mobile/tablet)
- [ ] Glassmorphism effect renders correctly
- [ ] Hover effects work (scale, shadow, brightness)

### Performance
- [ ] Lighthouse performance score ≥90 (desktop)
- [ ] Lighthouse performance score ≥90 (mobile)
- [ ] Hero visible within 2s on 3G connection
- [ ] TTI increase ≤500ms vs. original homepage
- [ ] All images optimized (hero ≤200KB, cards ≤150KB)

### Accessibility
- [ ] WCAG 2.1 AA compliance (axe DevTools: 0 violations)
- [ ] All images have descriptive alt text
- [ ] CTA button has 44px+ touch target (mobile)
- [ ] Keyboard navigation works (Tab, Enter)
- [ ] Focus indicators visible
- [ ] Color contrast ≥4.5:1 (normal), ≥3:1 (large)

### Responsive Design
- [ ] Mobile (375px): Stacked layout, no horizontal scroll
- [ ] Tablet (768px): Stacked layout, readable text
- [ ] Desktop (1024px+): 2-column hero, horizontal features
- [ ] Ultra-wide (1400px+): Max-width container, centered

### Dark Mode
- [ ] Hero adapts to dark theme
- [ ] Feature cards adapt to dark theme (darker glassmorphism)
- [ ] Image overlay darkens in dark mode
- [ ] CLS = 0 during theme toggle
- [ ] Text contrast maintained in both themes

### Code Quality
- [ ] CSS Modules used for all styling
- [ ] No Tailwind CSS classes
- [ ] TypeScript types correct (no errors)
- [ ] No console errors or warnings
- [ ] Existing components not broken (navbar, footer, chatbot)

---

## Next Steps

After completing this implementation:

1. **Run `/sp.tasks`** command to generate task decomposition in `tasks.md`
2. **Manual Testing**: Test on real mobile device (iOS/Android)
3. **Stakeholder Review**: Get feedback on visual design from 3+ reviewers
4. **Performance Monitoring**: Set up tracking for Core Web Vitals
5. **Documentation**: Update project README with screenshots

**Estimated Total Time**: 4-6 hours (1h images + 1.5h hero + 1.5h features + 1h testing + 0.5h commit)

**Status**: ✅ Quickstart guide complete
