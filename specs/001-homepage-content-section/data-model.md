# Data Model: Homepage Content Section

## Component Structure

### ContentSectionComponent
- **Purpose**: Main component that renders the two-column content section
- **Props**:
  - `className?: string` - Additional CSS classes for customization
  - `heading?: string` - Optional custom heading (defaults to "A New Chapter in Robotics: Beyond Automation")
- **Children**: None required - content is built into the component

### ContentCard Component
- **Purpose**: Sub-component representing each of the two content blocks
- **Props**:
  - `title: string` - Title for the card
  - `content: string[]` - Array of content paragraphs
  - `iconType?: 'check' | 'nike'` - Type of icon to use for bullet points
  - `className?: string` - Additional CSS classes for customization

## Content Structure

### Heading Section
- **text**: "A New Chapter in Robotics: Beyond Automation"
- **alignment**: Centered
- **styling**: Professional typography with appropriate sizing for hierarchy

### Left Card Content
- **title**: To be determined based on content strategy
- **content**: Array of strings containing paragraphs with bullet points
- **iconType**: 'check' for Nike-style bullet points

### Right Card Content
- **title**: To be determined based on content strategy
- **content**: Array of strings containing paragraphs with bullet points
- **iconType**: 'check' for Nike-style bullet points

## Styling Properties

### Responsive Layout
- **desktop**: Two columns side-by-side using CSS Grid
- **mobile**: Stacked vertically using CSS Grid
- **breakpoint**: 1024px (consistent with existing site)

### Card Styling
- **border**: Thin border (1px)
- **borderRadius**: Subtle rounded corners
- **padding**: Comfortable spacing (consistent with existing cards)
- **margin**: Appropriate spacing between cards
- **hoverEffects**: Subtle transformations for interactivity

### Typography
- **fontFamily**: Consistent with Docusaurus theme
- **fontSize**: Appropriate hierarchy for content
- **lineHeight**: Optimized for readability
- **color**: Using CSS variables for theme compatibility