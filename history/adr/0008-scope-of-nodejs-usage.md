# ADR-0008: Scope of Node.js Usage

- **Status:** Accepted
- **Date:** 2025-12-08
- **Feature:** 1-robotics-book-spec
- **Context:** Node.js is a necessary dependency for running the Docusaurus build system. A clear boundary must be defined to prevent "technology bleed," where it might be used for other tasks like backend demos or scripting, thereby increasing the project's complexity.

## Decision

The use of **Node.js and the associated npm ecosystem will be strictly limited to powering the Docusaurus website** within the `robotic-book/` directory.

All robotics-related logic, including code examples, simulation scripts, and API demos, will be implemented in **Python**.

## Consequences

### Positive

- **Clear Separation of Concerns:** Establishes a clean architectural boundary between the "frontend/documentation" stack (JavaScript/Node.js) and the "backend/robotics" stack (Python).
- **Reduced Cognitive Load:** Readers can focus on a single, consistent language (Python) for all core robotics and AI concepts.
- **Simplified Toolchain:** Avoids the need for a separate JavaScript/Node.js environment and dependency management system for the robotics code.

### Negative

- **Rigidity:** Prevents the use of JavaScript/TypeScript for robotics-related scripting, even in scenarios where it might be a viable or interesting alternative (e.g., using a Node.js-based robotics library). This is an acceptable trade-off for the sake of consistency.

## Alternatives Considered

### Use Node.js for Backend/Scripting

- **Description:** Allow the use of Node.js (with frameworks like Express or libraries like `johnny-five`) for backend demos and hardware scripting.
- **Reason for Rejection:** This was rejected to maintain a strong focus on the Python-centric ecosystem that dominates the target fields (ROS 2, computer vision, AI/ML). Introducing a second language for core logic would unnecessarily complicate the learning path.

## References

- **Implementation Plan:** D:\Quarter 4\ai-book\humanoid-robotic-book\specs\1-robotics-book-spec\plan.md
- **Related ADRs:**
  - `ADR-0007: Backend Technology for API Demos`
