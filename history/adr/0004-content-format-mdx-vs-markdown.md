# ADR-0004: Content Format: MDX over Markdown

- **Status:** Accepted
- **Date:** 2025-12-08
- **Feature:** 1-robotics-book-spec
- **Context:** The book's educational goals require a rich content experience that goes beyond static text and images. To effectively demonstrate complex topics, the ability to embed interactive diagrams, formatted code examples, and consistent, styled citations is necessary.

## Decision

The project will use **MDX (`.mdx`)** as the primary format for all documentation pages instead of plain Markdown (`.md`). This enables the use of custom React components directly within the content.

## Consequences

### Positive

- **Rich Interactivity:** Allows for the creation and embedding of custom React components, such as `<Diagram>`, `<CodeExample>`, and `<Citation>`, leading to a more engaging and effective learning experience.
- **Enhanced Content Quality:** Ensures a consistent and high-quality presentation for complex elements that are difficult to manage with plain Markdown.
- **Future-Proofing:** Provides the flexibility to add more sophisticated interactive components in the future without changing the content format.

### Negative

- **Slightly Increased Complexity:** Authors must be familiar with basic JSX syntax to use the custom components, which introduces a slightly higher learning curve than plain Markdown.
- **Tighter Coupling to React:** The content is more tightly coupled to the Docusaurus/React frontend.

## Alternatives Considered

### Plain Markdown (`.md`)

- **Description:** Use only standard Markdown for all content.
- **Reason for Rejection:** While simpler, plain Markdown cannot support the custom, interactive components that are critical for meeting the book's quality standards for usability and educational value. The benefits of using MDX to create a richer user experience far outweigh the minor increase in complexity.

## References

- **Implementation Plan:** D:\Quarter 4\ai-book\humanoid-robotic-book\specs\1-robotics-book-spec\plan.md
- **Related ADRs:** None
