# ADR-0001: ROS 2 Version Selection

- **Status:** Accepted
- **Date:** 2025-12-08
- **Feature:** 1-robotics-book-spec
- **Context:** The project requires a specific version of ROS 2 for all examples and simulations to ensure consistency and reproducibility. The choice of version impacts stability, feature availability, and community support.

## Decision

The project will standardize on **ROS 2 Humble Hawksbill (LTS)** for all development, documentation, and simulation examples.

## Consequences

### Positive

- **Long-Term Support (LTS):** As an LTS release, Humble is supported until May 2027, ensuring stability, security updates, and a reliable foundation for the project's lifespan.
- **Wide Compatibility:** Most ROS 2 packages and tools are compatible with Humble, reducing integration friction.
- **Community & Documentation:** Benefits from extensive documentation, tutorials, and a large user community, which is ideal for the book's target audience.

### Negative

- **Not Cutting-Edge:** Does not include the newest features available in the latest rolling or non-LTS releases (like ROS 2 Iron). This is a minor drawback as stability is prioritized over new features for this project.

## Alternatives Considered

### ROS 2 Iron Irwini (or latest non-LTS)

- **Description:** Use the latest available ROS 2 release to leverage the most modern features.
- **Reason for Rejection:** Non-LTS releases have a shorter support lifespan and may exhibit less stability. For an educational project focused on reproducibility, the stability and guaranteed support of an LTS release are more valuable than access to the newest, potentially less-tested, features.

## References

- **Implementation Plan:** D:\Quarter 4\ai-book\humanoid-robotic-book\specs\1-robotics-book-spec\plan.md
- **Related ADRs:** None
