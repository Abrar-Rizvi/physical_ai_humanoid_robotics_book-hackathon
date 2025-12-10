# Research Findings: Fix Hero Section Image Responsiveness

**Date**: 2025-12-10
**Feature**: `003-hero-image-responsiveness`

## 1. Identification of Hero Section Components

### Decision:
The hero section component is primarily located in `robotic-book/src/pages/index.tsx`. The specific styling for the hero banner, including the image, is managed within `robotic-book/src/pages/index.module.css`.

### Rationale:
A search for the term "hero" within the `robotic-book/src` directory revealed direct matches in these two files:
- `robotic-book/src/pages/index.tsx`: Contains the React component structure for the homepage, including `<header className={clsx('hero hero--primary', styles.heroBanner)}>`, `hero__title`, and `hero__subtitle`. This strongly indicates it's the primary component for the hero section.
- `robotic-book/src/pages/index.module.css`: Contains CSS rules specifically targeting `.heroBanner` and related classes, confirming it as the style source for the hero section.

### Alternatives Considered:
- Global `custom.css`: While `robotic-book/src/css/custom.css` exists for general Docusaurus styles, `index.module.css` is module-specific and directly linked to `index.tsx`, making it the more precise location for component-level styling adjustments.

## 2. Technology Stack Best Practices for Responsiveness

### Decision:
Utilize CSS Media Queries for breakpoint-based layout adjustments and flexible box (Flexbox) or grid layout for element positioning. For image responsiveness, ensure the `<img>` tag is used with `max-width: 100%` and `height: auto`, and potentially `object-fit` for aspect ratio control.

### Rationale:
- **CSS Media Queries**: The most standard and effective approach for applying different styles based on screen width, directly aligning with the requirement for `Desktop (> 768px)` and `Tablet & Mobile (≤ 768px)` specific layouts.
- **Flexbox/Grid**: Provides robust and maintainable ways to arrange content, easily allowing elements to switch from horizontal alignment (desktop) to vertical stacking (mobile) at specified breakpoints.
- **`<img>` tag with `max-width: 100%, height: auto`**: Standard practice for responsive images, ensuring they scale within their container without overflowing while maintaining their aspect ratio. `object-fit` can further refine how the image fits its container.

### Alternatives Considered:
- JavaScript-based responsiveness: Rejected as the requirements can be met purely with CSS, adhering to the constraint of minimal custom CSS and avoiding new JS-based layout libraries.
- CSS Frameworks (e.g., Tailwind CSS): Rejected as the prompt explicitly states "no Tailwind if not already used" and encourages using existing CSS classes or minimal custom CSS. The goal is to fix a specific issue with minimal external dependency changes.

## 3. Assumptions Validation

All assumptions outlined in the specification (single breakpoint at 768px, existing image suitability, CSS-only solution) are validated and supported by the research findings.
