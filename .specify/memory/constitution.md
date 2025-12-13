<!--
SYNC IMPACT REPORT
==================
Version: 1.3.0 → 1.4.0 (MINOR)

Changes:
- REMOVED: Section 4 "Markdown & Linting Style" entirely (lines 40-44)
  - Deleted MD013 line length rule reference
  - Deleted MD007 list indentation rule reference
  - Deleted merge policy for specs/ directory
- RETAINED: Docusaurus compatibility requirement (Section 6)
- RETAINED: Spell check via cspell (no changes to cspell workflow)
- NO NEW LINTING TOOLS: Explicitly removed markdown linting enforcement

Rationale:
Eliminate CI and local lint failures caused by AI-generated and Docusaurus content.
Rely on cspell for spell checking, Docusaurus build validation, and manual review
instead of rigid markdown linting rules that conflict with content generation workflows.

Templates Updated:
- ✅ .github/workflows/quality-checks.yml - Removed markdownlint-cli2 installation and execution
- ✅ .specify/memory/constitution.md - This file (removed Section 4)
- ✅ N/A plan-template.md - No markdownlint references found
- ✅ N/A spec-template.md - No markdownlint references found
- ✅ N/A tasks-template.md - No markdownlint references found

Files Deleted:
- .markdownlint.json (repository root)
- robotic-book/.markdownlint.json

Follow-up TODOs:
- None (all changes complete)

Version Bump Reasoning:
MINOR bump (1.3.0 → 1.4.0) because this removes a governance section (Markdown & Linting Style)
which materially changes development workflow and removes enforcement constraints, but does not
break backward compatibility with existing code or content.
-->

# Constitution for Physical AI & Humanoid Robotics Book

## 1. Purpose

This Constitution defines the rules, standards, and workflows for building, simulating, and testing humanoid or proxy robots using ROS 2, Gazebo, Unity, NVIDIA Isaac, and VLA models during the Physical AI & Humanoid Robotics Hackathon. It also governs the development of the course website and integrated learning tools.

## 2. Core Principles

- Engineering accuracy, academic clarity
- Verified, reproducible robotics & AI workflows
- Safety-first development for humanoid robots
- Ethical, traceable, responsible AI usage
- Alignment with official documentation (ROS 2, Gazebo, Unity, Isaac)
- Minimal dependencies and lightweight architecture for web features
- User-centric design with mobile-first, accessible interfaces

## 3. Standards

- Claims must be verifiable via official docs or reputable research
- Citations: APA or IEEE
- At least 30% peer-reviewed sources, 0% plagiarism
- Readability: Grade 10–12 engineering level
- All diagrams and code must reflect real system behavior
- Web components MUST be mobile-friendly and dark-mode compatible
- Zero tolerance for layout-breaking changes

## 4. Constraints

- Length: 4,000–6,000 words
- Minimum 12 authoritative sources
- Formats: PDF or Markdown
- Must include:
    - Robot system architecture diagram
    - Sensor → AI → Controller → Actuator flow
    - Safety guidelines for humanoids
    - Simulation setup + validation
- Web performance: Lightweight components, no heavy libraries
- Chat widget: Maximum 20px positioning offset, click-to-open only

## 5. Success Criteria

A constitution is successful if it:

- Defines complete robot design → simulation → testing workflow
- Maps ROS 2 / Gazebo / Unity / Isaac / VLA to responsibilities
- Ensures reproducibility, safety, and ethics
- Provides clear team workflow standards
- Passes mentor technical audit
- Delivers seamless, accessible learning experience via web and chat features

## 6. Scope

Covers the entire hackathon and learning platform:

- Physical AI foundations
- ROS 2 control architecture
- Gazebo + Unity simulation
- NVIDIA Isaac perception & navigation
- VLA-based action pipelines
- Capstone: Autonomous humanoid robot
- **Docusaurus 2 Website**: Course delivery platform at https://devabdullah90.github.io/Spec-Driven-Development-Hackathon-I/docs/overview
- **Integrated Course AI Chat Widget**: Lightweight, interactive Q&A based on book content, powered by Claude via MCP

## 7. System Requirements

### Robotics Hardware & Software

- Digital Twin Workstation:
    - RTX 4070 Ti+ (ideal 3090/4090), 32–64GB RAM, Ubuntu 22.04
- Edge Kit: Jetson Orin Nano/NX
- Sensors: RealSense D435i/D455, IMU
- Robots: Unitree Go2, G1, or miniature humanoid
- Cloud: AWS g5/g6 for simulation only—not direct robot control

### Web Platform

- Node.js >= 20.0
- Docusaurus 2 (v3.9.2)
- React 19
- Modern browsers with mobile responsive design

## 8. Team Workflow Rules

### Robotics Development

- ROS 2 packages follow standard node/topic/service/action structure
- Valid URDF/SDF models; physics validated in Gazebo
- Unity for visualization; Isaac Sim for data + perception
- VLA pipeline: Whisper → LLM → ROS 2 actions
- Required pipeline:
    - Simulation → Testing → Jetson Deployment → Safety Check

### Web Development

- All changes MUST be tested on mobile viewports
- Dark mode compatibility is mandatory
- Component integration MUST NOT break existing layout
- Prefer CSS-only solutions over JavaScript where possible
- Progressive enhancement: core content accessible without JavaScript

## 9. Ethics & Safety

### Robotics Safety

- No unsafe or uncontrolled movements
- Mandatory Emergency Stop (E-Stop) procedure
- Cloud latency cannot influence robot safety
- All real-world tests require safe distance + logging
- AI actions must be explainable

### Data & Privacy

- User interactions with chat widget MUST be logged securely
- No collection of personally identifiable information without consent
- Transparent AI usage in learning materials

## 10. Versioning

- Semantic Versioning: MAJOR.MINOR.PATCH
- Every update must be recorded in a version history table.

## 11. Chapter Rules

Each chapter must contain:
- Title, objectives, core concepts, technical deep dive, code/pseudocode, diagrams, safety notes, assignments, references.

## 12. Deliverables

### Robotics Deliverables

- Final Constitution
- System architecture diagram
- Simulation validation report
- AI perception + planning pipeline
- Capstone humanoid functional spec

### Web Platform Deliverables

- Deployed Docusaurus website
- Functional Course AI chat widget
- Mobile-responsive design validation
- Dark mode compatibility verification

## 13. Completion Definition

Document is complete when all required sections exist, are technically accurate, include safety rules, and pass mentor audit.

The website is complete when:
- All content renders correctly on mobile and desktop
- Chat widget functions without breaking layout
- Dark mode works across all pages
- Performance metrics meet lightweight standards

## 14. Course AI Chat Widget Integration

To enhance the learning experience, a lightweight Course AI chat widget will be integrated into the Docusaurus website.

### 14.1. Purpose

The chat widget's primary purpose is to answer user questions exclusively based on the content of the book, including user-selected text snippets. This ensures responses are grounded and directly relevant to the learning material.

### 14.2. Approved Technologies

- **Claude via MCP (Model Context Protocol)**: Primary AI model for chat interactions
- **Lightweight Frontend**: No heavy libraries, minimal JavaScript footprint
- **Docusaurus Integration**: Native integration with existing React components
- **Mobile-First Design**: Responsive across all device sizes

### 14.3. Architectural Rules

- **RAG Pipeline**: The chatbot will adhere to a strict RAG pipeline:
    1. **Embeddings**: Book content will be chunked and converted into vector embeddings.
    2. **Vector Storage**: Embeddings will be stored for fast semantic search.
    3. **Retrieval**: User queries will trigger retrieval of relevant text snippets.
    4. **Claude via MCP**: The retrieved content, along with the user's query, will be fed into Claude to generate a grounded response.
- **Grounded Responses**: All chatbot responses MUST be strictly grounded in the content of the book. Claude is prohibited from generating information beyond what is present in the provided context.
- **Stateless Widget**: Each query is independent; no session persistence required unless explicitly needed.

### 14.4. Safety & Ethics

- **No Hallucination**: The chatbot MUST NOT hallucinate or generate information not explicitly found within the book's content.
- **Context Boundaries**: Claude MUST refuse to answer questions outside the book's scope with a polite redirect.
- **Privacy**: No user data collection beyond anonymous usage metrics.

### 14.5. UI/UX Requirements

The chat widget MUST adhere to the following strict design constraints:

- **Positioning**: Bottom-right corner of viewport, 20px from edges
- **Initial State**: Collapsed icon/button, non-intrusive
- **Interaction**: Click-to-open only (no auto-expansion, no hover states that expand)
- **Size**:
    - Collapsed: Small icon (max 60px × 60px)
    - Expanded: Responsive panel (max 400px width on desktop, full-width minus 20px on mobile)
- **Mobile-Friendly**:
    - Touch-optimized tap targets (min 44px)
    - Smooth animations, no janky scrolling
    - Keyboard accessibility
- **Dark Mode Safe**:
    - Colors MUST work in both light and dark themes
    - Use CSS variables from Docusaurus theme
    - No hardcoded colors
- **Zero Layout Breaks**:
    - Widget MUST use fixed positioning
    - MUST NOT affect document flow
    - MUST NOT cause page reflow or layout shift
    - MUST NOT interfere with existing navigation or footer
- **Performance**:
    - Lazy load widget code until first interaction
    - No blocking scripts on initial page load
    - Chat history limited to prevent memory issues

### 14.6. Integration

The Course AI chat widget functionality MUST be seamlessly embedded within the published book's UI on the Docusaurus website, providing an interactive question-answering experience directly within the learning environment without disrupting the core content experience.

## Governance

This constitution supersedes all other project practices. Amendments require a formal proposal, review, documentation of rationale, and approval by project mentors. Versioning follows semantic versioning rules outlined in Section 10. Compliance reviews will be conducted regularly by project mentors.

**Version**: 1.4.0 | **Ratified**: 2025-12-04 | **Last Amended**: 2025-12-13
