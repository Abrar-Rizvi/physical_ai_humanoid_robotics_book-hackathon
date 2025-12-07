# ADR-0006: Website Publishing Platform

- **Status:** Proposed
- **Date:** 2025-12-08
- **Feature:** 1-robotics-book-spec
- **Context:** To make the book accessible to a public audience, a reliable and easy-to-manage hosting platform is required for the static Docusaurus website. The choice of platform impacts the deployment workflow, cost, and available features.

## Decision

The project will use **GitHub Pages** as the primary platform for hosting the production website. The deployment process will be automated using GitHub Actions.

## Consequences

### Positive

- **Cost-Effective:** GitHub Pages is free for public repositories.
- **Seamless Integration:** Deployment can be seamlessly integrated into the existing GitHub repository and CI/CD workflows using GitHub Actions.
- **Simplicity:** The setup and maintenance are straightforward, requiring minimal configuration.

### Negative

- **Limited Features:** GitHub Pages is a simple static hosting service and lacks advanced features like serverless functions, advanced analytics, or per-branch preview deployments that are available on other platforms.
- **Public Only:** The free tier is limited to public repositories.

## Alternatives Considered

### Vercel / Netlify

- **Description:** Use a specialized static site hosting platform like Vercel or Netlify.
- **Reason for Rejection:** While these platforms offer more advanced features (such as instant preview deployments for pull requests), they introduce another third-party service to the workflow. For the initial release, the simplicity and direct integration of GitHub Pages are sufficient. A migration to Vercel or Netlify can be considered in the future if the project's needs evolve.

## References

- **Implementation Plan:** D:\Quarter 4\ai-book\humanoid-robotic-book\specs\1-robotics-book-spec\plan.md
- **Related ADRs:** None
