# Feature Specification: Complete Homepage Overhaul with Premium Robot-Themed Visuals

**Feature Branch**: `004-homepage-overhaul`
**Created**: 2025-12-09
**Status**: Draft
**Input**: User description: "Complete Homepage Overhaul  Hero Section + Premium Robot-Themed Features Grid (Pure Custom CSS, no Tailwind)"

## Clarifications

### Session 2025-12-09

- Q: The spec mentions lazy loading for robot images with "blur-up placeholder" (FR-024, Edge Case #2), but the specific implementation approach for blur-up placeholders isn't defined. Which approach should be used? -> A: Use low-quality image placeholder (LQIP) technique with base64-encoded tiny version that blurs into full image (industry standard)
- Q: The CTA button links to "the course introduction" (FR-006) and shows "/docs/intro", but should it have any special behavior beyond standard navigation (analytics tracking, scroll behavior, external link handling)? -> A: Standard internal navigation using Docusaurus Link component (no special tracking or behavior)
- Q: FR-019 mandates "vanilla CSS, CSS Modules, or global styles" but doesn't specify which approach. Which CSS organization method should be used? -> A: CSS Modules (*.module.css files) - scoped styles, automatic class name hashing, component-level organization
- Q: The spec mentions max-width constraints with different values: "1400-1600px" in some places and "1400px" in others. What should be the consistent max-width? -> A: 1400px max-width for both hero and features sections (consistent, optimized for readability)
- Q: User Story 4 mentions tablets (768px-1024px) where "the layout adapts with optimized column proportions or stacks". Should tablets use 2-column or stacked layout? -> A: Stack vertically on all tablets (<1024px), 2-column only on desktop (>=1024px)

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Immersive Hero Experience (Priority: P1)

When visitors land on the homepage, they immediately see a full-width, full-height hero section with a dramatic two-column layout: compelling text on the left and a stunning futuristic humanoid robot visual on the right that instantly communicates the course's cutting-edge nature.

**Why this priority**: The hero section is the first impression and primary conversion driver. A premium, professional hero immediately establishes authority and captures attention, directly impacting enrollment decisions within the critical first 3 seconds.

**Independent Test**: Can be fully tested by navigating to the homepage and verifying: (1) hero section occupies ~90vh on desktop, (2) text and robot image are displayed in 2-column layout on desktop, (3) layout stacks vertically on mobile with text above image, (4) all content is vertically and horizontally centered.

**Acceptance Scenarios**:

1. **Given** a visitor lands on the homepage on desktop (e1024px), **When** the page loads, **Then** they see a ~90vh hero with left column containing headline, subheadline, paragraph, and CTA button, and right column displaying a large robot image
2. **Given** the hero section is fully rendered, **When** the visitor reads the content, **Then** they see the H1 "Master Physical AI & Build Real Humanoid Robots", H2 about ROS 2/Gazebo/MoveIt, a 2-3 line authoritative paragraph, and a prominent "Start Learning Free �" CTA button
3. **Given** a visitor on mobile (<768px), **When** they view the homepage, **Then** the hero layout stacks vertically with text content above the robot image, maintaining readability and visual hierarchy
4. **Given** the hero is displayed in either light or dark mode, **When** the theme toggles, **Then** all text colors, backgrounds, and image overlays adapt seamlessly without layout shift

---

### User Story 2 - Premium Feature Cards Showcase (Priority: P1)

When visitors scroll below the hero, they encounter three large, visually stunning feature cards with high-resolution robot imagery that showcase the course's key value propositions through modern glassmorphism design.

**Why this priority**: Feature cards communicate the "what" and "why" of the course. Premium visuals differentiate this from generic documentation sites and signal high-quality content, directly impacting perceived value and engagement.

**Independent Test**: Can be tested by scrolling to the features section and verifying: (1) three cards display in a horizontal row on desktop, (2) each card has a unique high-resolution robot image, (3) glassmorphism effects (blur + transparency) are applied, (4) cards stack vertically on mobile.

**Acceptance Scenarios**:

1. **Given** a visitor scrolls to the features section on desktop, **When** they view the cards, **Then** they see three cards in a horizontal row with equal spacing, each displaying a unique robot theme (humanoid, robotic arm, AI brain)
2. **Given** the feature cards are rendered, **When** the visitor observes the styling, **Then** each card uses glassmorphism effects with backdrop-filter blur, semi-transparent background, subtle borders, and generous padding
3. **Given** a visitor on mobile views the features section, **When** the viewport is <768px, **Then** the three cards stack vertically with appropriate margins and full-width layout
4. **Given** a visitor hovers over a card (desktop) or taps it (mobile), **When** the interaction occurs, **Then** the card smoothly scales to 104%, displays enhanced shadow, and increases image brightness within 300ms

---

### User Story 3 - Accessible Dark Mode Experience (Priority: P2)

When users toggle between light and dark themes, both the hero and features sections adapt seamlessly with appropriate color schemes, ensuring readability and visual consistency across all theme preferences.

**Why this priority**: Dark mode is essential for modern web experiences and user preference accommodation. Given the technical audience (developers/roboticists), dark mode support is expected and directly impacts user comfort and retention.

**Independent Test**: Can be tested by toggling the Docusaurus theme switcher and verifying: (1) hero text colors adapt, (2) hero image overlay changes appropriately, (3) feature card backgrounds/borders/text adjust, (4) no layout shift occurs (CLS = 0).

**Acceptance Scenarios**:

1. **Given** the homepage is displayed in light mode, **When** the user toggles to dark mode, **Then** hero text changes to light colors, background adapts to dark tones, and image overlay adjusts for readability
2. **Given** feature cards are displayed, **When** dark mode is activated, **Then** glassmorphism backgrounds shift to dark-transparent, borders use appropriate dark-theme colors, and text remains high-contrast
3. **Given** the theme toggle occurs, **When** colors transition, **Then** the change happens smoothly without any layout shift, content jumping, or flash of unstyled content

---

### User Story 4 - Responsive Mobile-First Design (Priority: P1)

When users access the homepage on mobile devices, tablets, or smaller screens, both hero and features sections adapt flawlessly with appropriate layouts, font sizes, and spacing to ensure optimal readability and usability.

**Why this priority**: Mobile traffic represents 50-70% of web visitors. A broken mobile experience results in immediate bounce. This is equally critical as desktop visual impact for user retention and accessibility.

**Independent Test**: Can be tested by resizing browser to mobile widths (375px, 768px, 1024px) and verifying: (1) hero stacks text above image, (2) text sizes scale appropriately, (3) CTA button remains tappable (min 44px), (4) feature cards stack vertically, (5) no horizontal scrolling occurs.

**Acceptance Scenarios**:

1. **Given** a user on mobile (viewport 375px-768px), **When** they view the hero, **Then** the layout displays text content stacked above the robot image with appropriate font scaling and touch-friendly CTA button
2. **Given** a tablet user (768px-1024px), **When** they view the hero, **Then** the layout stacks vertically (same as mobile) with text content above the robot image, ensuring optimal readability and touch interaction
3. **Given** any mobile/tablet user, **When** they interact with the homepage, **Then** all touch targets meet minimum 44px size, text remains readable without zooming, and no horizontal scrolling is required

---

### Edge Cases

- **What happens when the robot image fails to load?** Display a fallback gradient background with a robot emoji (>) or SVG placeholder to maintain visual hierarchy and prevent broken layout
- **How does the system handle very slow network connections (3G)?** Lazy load the hero robot image with LQIP (low-quality image placeholder) using base64-encoded tiny version that blurs into full image; ensure text content renders immediately for instant perceived performance
- **What if the user has animations disabled (prefers-reduced-motion)?** Disable scale/transform animations on hover; retain color and shadow changes only for visual feedback
- **How does glassmorphism perform on browsers without backdrop-filter support?** Provide graceful degradation to solid semi-transparent backgrounds for older browsers (IE11, older Safari)
- **What happens on ultra-wide monitors (>2000px)?** Constrain hero and features container to a max-width of 1400px centered on the page to prevent overly stretched layouts
- **How are real robot images sourced?** Use royalty-free stock images from Unsplash/Pexels with URLs clearly commented in code for easy replacement

## Requirements *(mandatory)*

### Functional Requirements

#### Hero Section Requirements

- **FR-001**: Hero section MUST occupy approximately 90vh (90% of viewport height) on initial load
- **FR-002**: Hero MUST use a two-column layout on desktop (>=1024px): left column for text, right column for robot image
- **FR-003**: Hero MUST display heading "Master Physical AI & Build Real Humanoid Robots" as H1
- **FR-004**: Hero MUST display subheading "The most practical, hands-on course on ROS 2, Gazebo, MoveIt, LLMs and real hardware" as H2
- **FR-005**: Hero MUST include a 2-3 line paragraph with authoritative, exciting copy about the course value
- **FR-006**: Hero MUST include a prominent CTA button with text "Start Learning Free �" that links to /docs/intro using standard Docusaurus Link component navigation (no special tracking, scroll behavior, or external link handling)
- **FR-007**: Hero text content MUST be perfectly centered vertically and horizontally within the left column
- **FR-008**: Hero robot image MUST be a high-resolution futuristic humanoid robot (minimum 800px width, WebP format preferred)
- **FR-009**: Hero image MUST include a subtle gradient overlay to ensure text readability if text overlaps the image area
- **FR-010**: Hero layout MUST stack vertically on tablets and mobile (<1024px) with text content above the robot image

#### Features Section Requirements

- **FR-011**: Features section MUST display exactly three feature cards
- **FR-012**: Feature cards MUST be arranged in a single horizontal row on desktop (>=1024px viewport)
- **FR-013**: Feature cards MUST stack vertically with appropriate margins on tablets and mobile (<1024px viewport)
- **FR-014**: Each card MUST include a unique, high-resolution robot-themed image:
  - Card 1: Humanoid robot walking or posing (example: Unsplash ID or URL)
  - Card 2: Industrial robotic arm in action (example: Unsplash ID or URL)
  - Card 3: Glowing AI brain or neural network robot (example: Unsplash ID or URL)
- **FR-015**: Feature cards MUST use glassmorphism styling with backdrop-filter blur, semi-transparent background, and subtle borders
- **FR-016**: Each card MUST include a heading (32px+ font size), description text, and optional icon (react-icons or inline SVG)
- **FR-017**: Feature cards MUST implement hover effects: scale(1.04), enhanced box-shadow, and image brightness(1.1) within 300ms
- **FR-018**: Feature cards MUST use generous padding (32px+ on desktop, 24px on mobile) for breathing room

#### Styling & Theme Requirements

- **FR-019**: ALL styling MUST use CSS Modules (*.module.css files) with component-scoped styles and automatic class name hashing (NO Tailwind CSS classes, NO global CSS except for Docusaurus theme overrides if necessary)
- **FR-020**: Both hero and features MUST support light and dark modes using CSS custom properties (--ifm-* variables) or data-theme attribute
- **FR-021**: Dark mode toggle MUST NOT cause layout shift (Cumulative Layout Shift score = 0)
- **FR-022**: Hero and features sections MUST be fully responsive with primary breakpoint at 1024px (stacked layout <1024px for tablets/mobile, 2-column/horizontal layout >=1024px for desktop)
- **FR-023**: All animations MUST respect prefers-reduced-motion media query by disabling transforms

#### Performance & Accessibility Requirements

- **FR-024**: Hero robot image MUST be optimized (d200KB file size) and lazy-loaded using LQIP (low-quality image placeholder) technique with base64-encoded tiny version that blurs into full image to prevent blocking initial render
- **FR-025**: Feature card images MUST be lazy-loaded and optimized (d150KB each)
- **FR-026**: All interactive elements (CTA button, feature cards) MUST be keyboard-accessible with visible focus states
- **FR-027**: All images MUST have descriptive alt text for screen readers
- **FR-028**: Text contrast ratios MUST meet WCAG 2.1 AA standards (4.5:1 for normal text, 3:1 for large text) in both light and dark modes
- **FR-029**: CTA button MUST have minimum 44px touch target size for mobile accessibility

#### Integration & Constraints Requirements

- **FR-030**: Feature MUST NOT introduce new npm dependencies beyond optional react-icons
- **FR-031**: Redesign MUST replace existing HomepageHeader and HomepageFeatures components without breaking the overall page layout
- **FR-032**: Redesign MUST NOT interfere with existing Docusaurus navbar, footer, or Course AI Chat Widget
- **FR-033**: All image URLs MUST be clearly commented in code for easy replacement by maintainers

### Key Entities *(include if feature involves data)*

- **HeroSection**: Component representing the full-height landing section
  - Attributes: headline (H1), subheadline (H2), description paragraph, CTA button text/link, robot image URL
  - Layout properties: two-column (desktop), stacked (mobile), ~90vh height, centered content

- **FeatureCard**: Individual card entity within the features grid
  - Attributes: title (string), description (string), imageUrl (string), imageAlt (string), iconComponent (optional React element)
  - Styling properties: glassmorphism background, backdrop-filter blur, hover scale/shadow effects

- **HomepageLayout**: Overall container managing hero and features sections
  - Responsibilities: responsive breakpoints, theme integration, max-width constraints, vertical spacing

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Homepage hero section loads with all content visible within 2 seconds on 3G connection (measured via Lighthouse)
- **SC-002**: Hover animations on feature cards achieve consistent 60fps performance on modern browsers (Chrome DevTools Performance panel)
- **SC-003**: Homepage passes WCAG 2.1 AA accessibility audit with zero violations (tested with axe DevTools)
- **SC-004**: Dark mode toggle produces zero Cumulative Layout Shift (CLS score = 0) verified via Lighthouse/WebPageTest
- **SC-005**: Mobile layout (viewport 375px) displays all content without horizontal scrolling or text overflow
- **SC-006**: Lighthouse performance score remains e90 after implementation (desktop and mobile)
- **SC-007**: Hero section text achieves at least 4.5:1 contrast ratio in both light and dark modes (verified with Color Contrast Analyzer)
- **SC-008**: Feature cards receive positive feedback from at least 3 stakeholders during design review (subjective quality gate)
- **SC-009**: Time to Interactive (TTI) increases by no more than 500ms compared to current homepage
- **SC-010**: All interactive elements are fully keyboard-navigable with visible focus indicators (manual keyboard testing)

## Design Specifications

### Hero Section Design

**Desktop Layout (>=1024px)**:
- **Container**: Full viewport width, ~90vh height, max-width 1400px centered
- **Left Column (Text)**: 50% width, flexbox centered vertically and horizontally
  - H1: 56-64px font size, font-weight 800, line-height 1.2
  - H2: 24-28px font size, font-weight 600, line-height 1.4
  - Paragraph: 18-20px font size, font-weight 400, line-height 1.6, max-width 600px
  - CTA Button: 56px height, 200px min-width, 18px font size, bold, primary color background
- **Right Column (Image)**: 50% width, robot image covering full column height with object-fit: cover
- **Image Overlay**: Linear gradient overlay (from left: transparent to semi-transparent dark) for text readability

**Mobile & Tablet Layout (<1024px)**:
- **Container**: Full width, auto height (allow stacking)
- **Text Section**: 100% width, padding 40px 20px, centered text
  - H1: 36-42px font size
  - H2: 18-22px font size
  - Paragraph: 16-18px font size, max-width 100%
  - CTA Button: 48px height, full-width or centered
- **Image Section**: 100% width, 50vh height minimum, robot image with object-fit: cover

**Color Scheme**:
- **Light Mode**: Dark text (#1a1a1a) on light background (#ffffff or gradient), primary color CTA (#0066cc or brand color)
- **Dark Mode**: Light text (#f5f5f5) on dark background (#1a1a1a or gradient), adjusted CTA color for dark theme

### Features Section Design

**Card Structure**:
- **Image Placement**: Top half of card (60% height) with large robot image as background (background-size: cover)
- **Content Area**: Bottom half (40% height) with padding 32px
  - Heading: 32-36px font size, font-weight 700, margin-bottom 16px
  - Description: 16-18px font size, font-weight 400, line-height 1.6, max 2-3 lines
  - Optional Icon: 40-48px size, positioned above or beside heading

**Glassmorphism Styling**:
```css
background: rgba(255, 255, 255, 0.1); /* Light mode */
background: rgba(30, 30, 30, 0.3); /* Dark mode */
backdrop-filter: blur(10px);
border: 1px solid rgba(255, 255, 255, 0.2);
box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.1);
border-radius: 16px;
```

**Hover Effects**:
- Transform: `scale(1.04)`
- Box Shadow: `0 12px 40px 0 rgba(0, 0, 0, 0.2)`
- Image Brightness: `filter: brightness(1.1)`
- Transition: `all 300ms cubic-bezier(0.4, 0, 0.2, 1)`

**Desktop Layout (>=1024px)**:
- Three cards in a row with equal width (calc((100% - 64px) / 3))
- Gap between cards: 32px
- Container max-width: 1400px, centered
- Card min-height: 480px

**Mobile & Tablet Layout (<1024px)**:
- Cards stack vertically with 100% width
- Gap between cards: 24px
- Horizontal margins: 20px
- Card min-height: 400px

### Image Recommendations

**Hero Robot Image**:
- **Suggested URL**: `https://images.unsplash.com/photo-1535378620166-273708d44e4c?w=1200&q=80` (dramatic humanoid robot)
- **Alternative**: `https://images.unsplash.com/photo-1581091226825-a6a2a5aee158?w=1200&q=80` (futuristic robot)
- **Format**: WebP with JPG fallback
- **Dimensions**: 1200�1600px (portrait orientation for right column)
- **File Size**: d200KB after optimization
- **LQIP**: Generate 20x27px base64-encoded version for blur-up placeholder

**Feature Card Images**:
- **Card 1 (Humanoid Robot)**: `https://images.unsplash.com/photo-1561557944-6e7860d1a7eb?w=800&q=80` (walking humanoid)
- **Card 2 (Robotic Arm)**: `https://images.unsplash.com/photo-1563207153-f403bf289096?w=800&q=80` (industrial arm)
- **Card 3 (AI Brain)**: `https://images.unsplash.com/photo-1677442136019-21780ecad995?w=800&q=80` (neural network visualization)
- **Format**: WebP with JPG fallback
- **Dimensions**: 800�600px (landscape 4:3 ratio)
- **File Size**: d150KB each after optimization

### Suggested Copy

**Hero Section**:
- **H1**: "Master Physical AI & Build Real Humanoid Robots"
- **H2**: "The most practical, hands-on course on ROS 2, Gazebo, MoveIt, LLMs and real hardware"
- **Paragraph**: "Learn to design, simulate, and deploy autonomous humanoid robots from scratch. This comprehensive course combines cutting-edge AI models with industry-standard robotics frameworks, giving you the skills to build the future of physical intelligence."
- **CTA Button**: "Start Learning Free �" (links to /docs/intro)

**Feature Cards**:
- **Card 1**:
  - Title: "Industry-Standard Tools"
  - Description: "Master ROS 2, Gazebo, and MoveItthe same frameworks powering Boston Dynamics, Tesla, and leading robotics labs worldwide."
- **Card 2**:
  - Title: "Real Hardware Integration"
  - Description: "Go beyond simulation with hands-on deployment to real robots. Learn sensor fusion, motor control, and safety-critical systems."
- **Card 3**:
  - Title: "AI-Powered Intelligence"
  - Description: "Integrate LLMs, computer vision, and VLA models to create robots that perceive, reason, and act autonomously in dynamic environments."

## Technical Constraints

- **CSS-Only Styling**: No Tailwind CSS, Bootstrap, or other CSS frameworks. Use CSS Modules (*.module.css) for all component styling with scoped class names and automatic hashing
- **Browser Support**: Chrome 90+, Firefox 88+, Safari 14+, Edge 90+ (aligned with Docusaurus browserslist config)
- **Performance Budget**: No more than 500ms added to Time to Interactive (TTI) or First Contentful Paint (FCP)
- **Dependency Constraint**: Zero new npm packages except optional react-icons (already commonly used in React projects)
- **Docusaurus Integration**: Must work seamlessly with Docusaurus 3.9.2 classic theme without breaking existing components
- **No Breaking Changes**: Navbar, footer, About page, Docs section, and Course AI Chat Widget must remain fully functional

## Assumptions

1. **Image Licensing**: All suggested Unsplash URLs are royalty-free and can be used commercially with attribution per Unsplash License
2. **Font Availability**: Docusaurus default fonts (system font stack or configured fonts) are suitable; no custom font files needed
3. **Icon Library**: If icons are needed, react-icons library is acceptable as it's a common React dependency with minimal bundle impact
4. **Content Ownership**: The provided headline, subheadline, and feature card copy are approved for use; no legal/branding review required
5. **Performance Baseline**: Current homepage has a Lighthouse performance score of 80-90; target is to maintain or improve this
6. **Dark Mode Implementation**: Docusaurus theme already provides dark mode infrastructure via CSS variables and data-theme attribute
7. **Mobile Traffic**: Approximately 50-60% of visitors use mobile devices based on typical educational website analytics

## Out of Scope

- **Complete Site Redesign**: Only homepage (hero + features sections) is in scope; other pages (docs, about, blog) are unchanged
- **A/B Testing**: No analytics or experimentation framework for testing different hero copy or layouts
- **Video Integration**: No auto-playing background videos or complex media embeds (static images only)
- **Internationalization**: No i18n support for hero/feature copy (handled at Docusaurus config level if needed later)
- **CMS Integration**: Feature card content is hardcoded in component; no dynamic content loading from CMS
- **Advanced Animations**: No scroll-triggered parallax, 3D transforms, or complex animation libraries (GSAP, Framer Motion)
- **SEO Metadata**: Assumes existing Docusaurus SEO configuration (meta tags, Open Graph) handles homepage metadata

## Dependencies

### Internal Dependencies
- **Docusaurus Core**: 3.9.2 (already installed)
- **React**: 19.0.0 (already installed)
- **Docusaurus Link Component**: For CTA button navigation
- **Docusaurus Heading Component**: For semantic HTML headings
- **Existing Theme**: Docusaurus classic theme CSS variables

### External Dependencies
- **react-icons** (optional): For feature card icons if needed (~1MB total, tree-shakeable)
- **Image Assets**: Three high-resolution robot images from Unsplash (royalty-free)

### Asset Dependencies
- **Hero Robot Image**: 1200�1600px WebP, ~150-200KB
- **Feature Card Images**: 3 images at 800�600px WebP, ~100-150KB each
- **Total Asset Size**: ~600-800KB for all images (acceptable for modern web, lazy-loaded)

## Risks & Mitigations

| Risk | Probability | Impact | Mitigation |
|------|------------|--------|------------|
| Glassmorphism not supported in older Safari/Firefox | Medium | Medium | Implement feature detection (`@supports (backdrop-filter: blur())`) and fallback to solid semi-transparent backgrounds |
| Large images slow initial load on 3G/4G connections | Medium | High | Lazy load all images, use WebP format, implement LQIP (low-quality image placeholders) with base64-encoded tiny versions, and ensure text content renders immediately |
| Dark mode colors have insufficient contrast | Low | Medium | Test with Color Contrast Analyzer during implementation; use Docusaurus theme variables as base for consistency |
| Hover effects cause jank on low-end devices | Low | Low | Use CSS `will-change: transform` property, GPU-accelerated transforms, and test on throttled CPU in Chrome DevTools |
| Hero height (90vh) cuts off content on short screens (laptops with browser chrome) | Medium | Low | Use `min-height: 600px` as fallback; ensure CTA button is always visible above fold |
| Unsplash images get removed or become unavailable | Low | Medium | Download and host images locally in `static/img/` directory; comment original Unsplash URLs for attribution |

## Follow-Up Work

After this feature is complete, consider:

1. **Performance Optimization**: Implement more advanced lazy loading strategies (Intersection Observer) for below-fold content
2. **Enhanced Interactivity**: Add subtle scroll-triggered animations (fade-in, slide-up) for feature cards using lightweight libraries
3. **A/B Testing**: Integrate analytics to test different hero copy, CTA button text, or feature card layouts for conversion optimization
4. **Video Integration**: Replace static hero robot image with a subtle looping background video for added premium feel
5. **Content Personalization**: Dynamic feature card content based on user referral source or previous interactions
6. **Reusable Component Library**: Extract hero and card components into a shared library for use across other marketing pages

## References

- [Docusaurus Styling & Layout Documentation](https://docusaurus.io/docs/styling-layout)
- [CSS Glassmorphism Design Trend](https://uxdesign.cc/glassmorphism-in-user-interfaces-1f39bb1308c9)
- [Web Accessibility Guidelines (WCAG 2.1)](https://www.w3.org/WAI/WCAG21/quickref/)
- [Unsplash License Terms](https://unsplash.com/license)
- [CSS backdrop-filter Browser Support](https://caniuse.com/css-backdrop-filter)
- [Responsive Web Design Best Practices](https://web.dev/responsive-web-design-basics/)
- [Core Web Vitals Metrics](https://web.dev/vitals/)
