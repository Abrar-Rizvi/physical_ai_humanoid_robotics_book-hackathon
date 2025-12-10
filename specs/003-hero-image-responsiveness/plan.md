# Implementation Plan: Fix Hero Section Image Responsiveness

**Branch**: `003-hero-image-responsiveness` | **Date**: 2025-12-10 | **Spec**: [specs/003-hero-image-responsiveness/spec.md](specs/003-hero-image-responsiveness/spec.md)
**Input**: Feature specification from `specs/003-hero-image-responsiveness/spec.md`

## Summary

This plan outlines the implementation of responsive adjustments to the hero section image on the homepage. The goal is to ensure the image remains visible and correctly positioned across all device sizes (desktop, tablet, mobile) by modifying the existing Docusaurus React component and its associated styling. No other design elements (colors, fonts, buttons) will be altered.

## Technical Context

**Language/Version**: JavaScript/TypeScript (React), CSS (handled by Docusaurus).
**Primary Dependencies**: React, Docusaurus framework.
**Storage**: N/A
**Testing**: Manual visual inspection across various browser sizes and device emulators. Potential for automated visual regression testing if a framework is introduced.
**Target Platform**: Web browsers (desktop, tablet, mobile).
**Project Type**: Web application (Docusaurus frontend).
**Performance Goals**: The changes to image loading and layout rendering must not negatively impact page load times or overall user experience. The Load Contentful Paint (LCP) score should not degrade by more than 5%.
**Constraints**:
- No modifications to the hero section's background color, text content, typography, or button styling.
- Implementation should primarily utilize existing CSS classes or introduce minimal custom CSS to achieve the responsive behavior. No new CSS frameworks (e.g., Tailwind CSS) should be introduced if not already in use.
- The breakpoint for switching between desktop and mobile/tablet layouts is strictly set at 768px.
- On smaller screens (<= 768px), the image's height must be capped at 400px or 60% of the viewport height to prevent it from dominating the screen.
- The image's aspect ratio must be preserved across all screen sizes.
**Scale/Scope**: The implementation is limited solely to the homepage hero section.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

The proposed changes are fully compliant with the project's Constitution. They adhere to core principles of engineering accuracy and reproducible workflows, and do not introduce any violations regarding scope, ethics, safety, or system requirements. The frontend UI focus of this task ensures no conflict with rules pertaining to ROS 2, VLA pipelines, or other backend systems.

## Project Structure

### Documentation (this feature)

```text
specs/003-hero-image-responsiveness/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (N/A for this feature)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (N/A for this feature)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
robotic-book/
├── src/
│   ├── components/ # Potentially custom components for the hero image if extracted
│   ├── css/
│   │   └── custom.css # General Docusaurus styles, may contain global overrides
│   ├── pages/
│   │   └── index.tsx # The main homepage component where the Hero section resides
│   │   └── index.module.css # Module-specific styles for the homepage, likely including hero styles
│   └── theme/
└── package.json # To run Docusaurus commands (start, build)
```

**Structure Decision**: The existing Docusaurus project structure will be utilized. Modifications will primarily target `robotic-book/src/pages/index.tsx` for component logic and structure, and `robotic-book/src/pages/index.module.css` for styling adjustments specific to the hero section. `robotic-book/src/css/custom.css` may be updated for global styles if necessary, but preference is given to module-specific CSS.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

N/A - No Constitution Check violations.