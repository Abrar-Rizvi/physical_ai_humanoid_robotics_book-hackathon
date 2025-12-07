# ADR-0003: Repository Structure for Docusaurus Project

- **Status:** Accepted
- **Date:** 2025-12-08
- **Feature:** 1-robotics-book-spec
- **Context:** A clear and scalable repository structure is essential for managing the Docusaurus website content alongside its extensive supporting materials, which include source code examples, simulation assets, and research notes.

## Decision

The project will adopt a **monorepo structure**. The Docusaurus project itself will be located in a dedicated `robotic-book/` subdirectory, while top-level directories for `code-examples/`, `simulations/`, and `research/` will be maintained at the repository root.

This structure provides a clean separation between the website's technical implementation and its content-related assets.

## Consequences

### Positive

- **Centralized Management:** All project assets (documentation, code, simulations) are located in a single, easy-to-navigate repository.
- **Simplified Local Development:** Developers can work on content, code, and the Docusaurus site simultaneously without managing multiple repositories.
- **Clear Separation of Concerns:** Isolating the Docusaurus application in `robotic-book/` keeps its configuration (e.g., `node_modules`, `package.json`) from cluttering the project root.

### Negative

- **Build Path Complexity:** CI/CD scripts and local commands must always specify the working directory (`./robotic-book`) for Docusaurus operations.
- **Potential for Large Repository:** The monorepo may grow large, potentially slowing down clone times, although this is not a major concern for the project's current scale.

## Alternatives Considered

### Docusaurus at Root

- **Description:** Place the Docusaurus project files directly at the repository root.
- **Reason for Rejection:** This approach was considered but ultimately rejected because the project had already been initialized with the Docusaurus site inside the `robotic-book/` directory. Migrating it to the root would be disruptive and offered little benefit over the current, cleanly separated structure.

### Separate Repositories (Polyrepo)

- **Description:** Use separate repositories for the Docusaurus site, code examples, and simulation assets.
- **Reason for Rejection:** This would introduce significant complexity in coordinating changes and managing dependencies across repositories. For a tightly integrated project like a book with code examples, a monorepo is far more efficient.

## References

- **Implementation Plan:** D:\Quarter 4\ai-book\humanoid-robotic-book\specs\1-robotics-book-spec\plan.md
- **Related ADRs:** None
