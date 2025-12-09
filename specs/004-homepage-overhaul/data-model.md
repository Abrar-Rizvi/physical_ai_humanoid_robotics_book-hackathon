# Data Model: Homepage Overhaul Components

**Feature**: Complete Homepage Overhaul with Premium Robot-Themed Visuals
**Branch**: 004-homepage-overhaul
**Date**: 2025-12-09

## Overview

This document defines the component props interfaces, state shape, and data structures for the redesigned homepage components. Since this is a pure frontend UI feature with no backend integration or data persistence, the "data model" refers to TypeScript interfaces and React component contracts.

---

## Component Hierarchy

```
HomePage (index.tsx)
├── HeroSection
│   ├── HeroTextContent
│   │   ├── Heading (h1)
│   │   ├── Subheading (h2)
│   │   ├── Paragraph
│   │   └── CTAButton (Link)
│   └── HeroImage
│       ├── LQIP Placeholder <img>
│       └── Full Resolution <picture>
└── HomepageFeatures
    └── FeatureCard (x3)
        ├── CardImage (<picture>)
        └── CardContent
            ├── Optional Icon
            ├── Heading (h3)
            └── Description (p)
```

---

## 1. HeroSection Component

### File: `robotic-book/src/pages/index.tsx`

### Component Interface

```typescript
// No props - uses static content from spec
function HeroSection(): ReactNode {
  const [heroImageLoaded, setHeroImageLoaded] = useState<boolean>(false);

  return (
    <section className={styles.heroContainer}>
      {/* Hero content */}
    </section>
  );
}
```

### State Shape

```typescript
interface HeroImageState {
  loaded: boolean;  // Tracks when full-resolution image has loaded
}
```

### Static Content Constants

```typescript
const HERO_CONTENT = {
  headline: "Master Physical AI & Build Real Humanoid Robots",
  subheadline: "The most practical, hands-on course on ROS 2, Gazebo, MoveIt, LLMs and real hardware",
  paragraph: "Learn to design, simulate, and deploy autonomous humanoid robots from scratch. This comprehensive course combines cutting-edge AI models with industry-standard robotics frameworks, giving you the skills to build the future of physical intelligence.",
  ctaText: "Start Learning Free 🚀",
  ctaLink: "/docs/intro",
};

const HERO_IMAGE = {
  webp: "/img/hero-robot.webp",
  jpg: "/img/hero-robot.jpg",
  alt: "Futuristic humanoid robot showcasing advanced Physical AI capabilities",
  lqipDataUrl: "data:image/jpeg;base64,/9j/4AAQ...", // ~1.8KB base64 LQIP
};
```

### Entity Description

**HeroSection**: Full-height landing section designed to capture attention within 3 seconds and drive enrollment.

**Attributes**:
- `headline` (H1): Primary value proposition
- `subheadline` (H2): Technology stack and course approach
- `description` (paragraph): Detailed course benefits
- `ctaButton`: Call-to-action linking to course introduction
- `robotImage`: High-resolution humanoid robot visual

**Layout Properties**:
- Desktop (>=1024px): Two-column layout (50% text, 50% image)
- Mobile/Tablet (<1024px): Stacked layout (text above image)
- Height: ~90vh on desktop, auto on mobile
- Max-width: 1400px centered

**State Behavior**:
- Initial: LQIP visible, full image hidden (opacity: 0)
- Transition: When full image loads, LQIP blurs out, full image fades in
- Duration: ~300ms smooth transition

---

## 2. FeatureCard Component

### File: `robotic-book/src/components/HomepageFeatures/index.tsx`

### Component Interface

```typescript
interface FeatureCardProps {
  title: string;              // Card heading (h3)
  description: string;        // Card description text
  imageWebP: string;          // WebP image URL
  imageJPG: string;           // JPG fallback URL
  imageAlt: string;           // Accessibility description
  icon?: React.ComponentType<React.SVGProps<SVGSVGElement>>;  // Optional icon from react-icons
}

function FeatureCard({
  title,
  description,
  imageWebP,
  imageJPG,
  imageAlt,
  icon: Icon,
}: FeatureCardProps): ReactNode {
  return (
    <div className={styles.featureCard}>
      {/* Card content */}
    </div>
  );
}
```

### Feature List Data

```typescript
const FEATURE_LIST: FeatureCardProps[] = [
  {
    title: "Industry-Standard Tools",
    description: "Master ROS 2, Gazebo, and MoveIt—the same frameworks powering Boston Dynamics, Tesla, and leading robotics labs worldwide.",
    imageWebP: "/img/feature-humanoid.webp",
    imageJPG: "/img/feature-humanoid.jpg",
    imageAlt: "Humanoid robot demonstrating bipedal locomotion and balance",
    // icon: Optional - can add from react-icons if needed
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
```

### Entity Description

**FeatureCard**: Individual card showcasing a key course value proposition through premium robot imagery and glassmorphism styling.

**Attributes**:
- `title` (string): Card heading (e.g., "Industry-Standard Tools")
- `description` (string): 2-3 sentence value proposition
- `imageUrl` (string): Robot-themed background image (WebP primary, JPG fallback)
- `imageAlt` (string): Descriptive alt text for accessibility
- `iconComponent` (optional React element): Icon from react-icons library

**Styling Properties**:
- **Glassmorphism**:
  - Background: `rgba(255, 255, 255, 0.1)` (light), `rgba(30, 30, 30, 0.3)` (dark)
  - Backdrop filter: `blur(10px)`
  - Border: `1px solid rgba(255, 255, 255, 0.2)`
- **Hover Effects**:
  - Transform: `scale(1.04)`
  - Box shadow: Enhanced depth
  - Image brightness: `brightness(1.1)`
  - Transition: `300ms cubic-bezier(0.4, 0, 0.2, 1)`

**Layout Properties**:
- Desktop (>=1024px): Horizontal row, 3 cards, `calc((100% - 64px) / 3)` width each
- Mobile/Tablet (<1024px): Vertical stack, 100% width, 24px gap
- Min-height: 480px (desktop), 400px (mobile)

---

## 3. Image Asset Specifications

### Hero Robot Image

```typescript
interface HeroImageAsset {
  webp: string;           // "/img/hero-robot.webp"
  jpg: string;            // "/img/hero-robot.jpg"
  alt: string;            // Descriptive alt text
  lqipDataUrl: string;    // Base64-encoded LQIP (~1.8KB)
  dimensions: {
    width: number;        // 1200px
    height: number;       // 1600px (portrait orientation)
  };
  fileSize: {
    webp: number;         // ~180KB
    jpg: number;          // ~200KB
  };
}

const HERO_IMAGE_ASSET: HeroImageAsset = {
  webp: "/img/hero-robot.webp",
  jpg: "/img/hero-robot.jpg",
  alt: "Futuristic humanoid robot showcasing advanced Physical AI capabilities",
  lqipDataUrl: "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD...", // Placeholder
  dimensions: { width: 1200, height: 1600 },
  fileSize: { webp: 180000, jpg: 200000 },
};
```

### Feature Card Image Assets

```typescript
interface FeatureImageAsset {
  webp: string;
  jpg: string;
  alt: string;
  dimensions: {
    width: number;        // 800px
    height: number;       // 600px (landscape 4:3)
  };
  fileSize: {
    webp: number;         // ~130KB
    jpg: number;          // ~150KB
  };
}

const FEATURE_IMAGE_ASSETS: FeatureImageAsset[] = [
  {
    webp: "/img/feature-humanoid.webp",
    jpg: "/img/feature-humanoid.jpg",
    alt: "Humanoid robot demonstrating bipedal locomotion and balance",
    dimensions: { width: 800, height: 600 },
    fileSize: { webp: 130000, jpg: 150000 },
  },
  {
    webp: "/img/feature-arm.webp",
    jpg: "/img/feature-arm.jpg",
    alt: "Industrial robotic arm performing precision manipulation tasks",
    dimensions: { width: 800, height: 600 },
    fileSize: { webp: 130000, jpg: 150000 },
  },
  {
    webp: "/img/feature-ai-brain.webp",
    jpg: "/img/feature-ai-brain.jpg",
    alt: "Neural network visualization representing AI-driven robot cognition",
    dimensions: { width: 800, height: 600 },
    fileSize: { webp: 130000, jpg: 150000 },
  },
];
```

---

## 4. CSS Module Class Names

### Hero Section Classes (index.module.css)

```typescript
interface HeroStyles {
  heroContainer: string;          // Main section container
  heroTextSection: string;        // Left column (desktop)
  heroImageSection: string;       // Right column (desktop)
  heroHeadline: string;           // H1 styling
  heroSubheadline: string;        // H2 styling
  heroParagraph: string;          // Description text
  heroCTA: string;                // CTA button
  heroImageContainer: string;     // Image wrapper (for LQIP overlay)
  heroImagePlaceholder: string;   // LQIP img element
  heroImage: string;              // Full-resolution img
  heroImageOverlay: string;       // Gradient overlay for text readability
}
```

### Feature Cards Classes (styles.module.css)

```typescript
interface FeatureStyles {
  featuresContainer: string;      // Main section wrapper
  featuresGrid: string;           // Flexbox/grid container
  featureCard: string;            // Individual card
  featureCardImage: string;       // Card background image area
  featureCardContent: string;     // Card text content area
  featureIcon: string;            // Optional icon (if used)
  featureHeading: string;         // Card h3
  featureDescription: string;     // Card description text
}
```

---

## 5. Responsive Breakpoint Behavior

### Breakpoint Configuration

```typescript
const BREAKPOINTS = {
  mobile: '0px - 1023px',       // Stacked layout for hero and features
  desktop: '1024px+',           // 2-column hero, horizontal feature cards
  maxWidth: '1400px',           // Content max-width for ultra-wide monitors
};
```

### Layout Transformations by Breakpoint

#### Hero Section

| Breakpoint | Layout | Text Section | Image Section |
|------------|--------|--------------|---------------|
| Mobile (<1024px) | Stacked (column) | 100% width, text-align center | 100% width, min-height 50vh |
| Desktop (>=1024px) | Two-column (row) | 50% width, left-aligned | 50% width, full column height |

#### Feature Cards

| Breakpoint | Layout | Card Width | Card Spacing |
|------------|--------|------------|--------------|
| Mobile (<1024px) | Stacked (column) | 100% | 24px vertical gap |
| Desktop (>=1024px) | Horizontal (row) | calc((100% - 64px) / 3) | 32px horizontal gap |

---

## 6. Validation Rules

### Required Fields

**HeroSection**:
- ✅ headline: Non-empty string
- ✅ subheadline: Non-empty string
- ✅ paragraph: Non-empty string
- ✅ ctaText: Non-empty string
- ✅ ctaLink: Valid Docusaurus route (starts with `/`)
- ✅ image URLs: Valid paths to static/img/ assets

**FeatureCard**:
- ✅ title: Non-empty string, max 50 characters (for card layout)
- ✅ description: Non-empty string, max 200 characters (2-3 lines max)
- ✅ imageWebP: Valid path to WebP asset
- ✅ imageJPG: Valid path to JPG asset
- ✅ imageAlt: Non-empty string for accessibility

### Image Constraints

- **File Size**: Hero ≤200KB (WebP), Feature cards ≤150KB each (WebP)
- **Dimensions**: Hero 1200x1600px, Feature cards 800x600px
- **Format**: WebP primary with JPG fallback
- **LQIP**: Base64-encoded, ≤2KB per image

### Accessibility Requirements

- All images MUST have descriptive `alt` text
- CTA button MUST have minimum 44px touch target (mobile)
- Text contrast MUST meet WCAG 2.1 AA (4.5:1 normal, 3:1 large)
- Keyboard navigation MUST work (Tab, Enter)

---

## 7. State Transitions

### Hero Image Loading State Machine

```
Initial State: LQIP Visible
│
├─> [Full image starts loading]
│   └─> State: loading=false, LQIP blurred (20px), full image hidden (opacity: 0)
│
├─> [Full image onLoad event fires]
│   └─> State: loading=true, LQIP fades out, full image fades in (opacity: 1)
│
└─> Final State: Full Image Visible
    └─> State: loading=true, LQIP removed from visual flow, full image fully visible
```

### Dark Mode Transition

```
Light Mode (data-theme="light")
│
├─> [User clicks theme toggle]
│   └─> Docusaurus adds data-theme="dark" to <html>
│
├─> [CSS variables update instantly]
│   ├─> --ifm-background-color changes
│   ├─> --ifm-font-color-base changes
│   └─> [data-theme='dark'] selectors activate
│
└─> Dark Mode Active (data-theme="dark")
    └─> Layout MUST NOT shift (CLS = 0)
```

---

## Summary

This data model defines all component interfaces, state shapes, and data structures required for the homepage overhaul implementation. All entities are pure frontend constructs with no backend persistence or API integration.

**Key Entities**:
1. **HeroSection**: Full-height hero with 2-column layout (desktop) or stacked (mobile)
2. **FeatureCard**: Glassmorphism-styled cards with robot imagery (3 instances)
3. **Image Assets**: 4 optimized images with WebP + JPG fallback + LQIP

**Next Steps**: Generate `quickstart.md` for developer implementation guide.
