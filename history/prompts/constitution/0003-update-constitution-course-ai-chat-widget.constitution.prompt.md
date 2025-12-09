---
id: 0003
title: Update constitution for Course AI chat widget
stage: constitution
date: 2025-12-09
surface: agent
model: claude-sonnet-4-5-20250929
feature: none
branch: 1-rag-chatbot
user: Abrar Rizvi
command: /sp.constitution
labels: ["constitution", "chat-widget", "ui-ux", "claude-mcp", "docusaurus"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - .specify/memory/constitution.md
tests:
  - none
---

## Prompt

Project: Physical AI & Humanoid Robotics Course Book
Site: <https://devabdullah90.github.io/Spec-Driven-Development-Hackathon-I/docs/overview>
Stack: Docusaurus 2
Goal: Best practical humanoid robotics course on the internet

Must add: Lightweight Course AI chat widget (bottom-right, 20px, click-to-open, powered by Claude via MCP)

Rules: Mobile-friendly, dark-mode safe, no heavy libs, zero layout breaks

## Response snapshot

Updated the project constitution from version 1.1.0 to 1.2.0 with comprehensive Course AI chat widget requirements.

**Key changes:**

- Expanded Section 14 (RAG Chatbot Integration) with specific Claude via MCP integration details
- Added Section 14.5 (UI/UX Requirements) with strict design constraints:
  - Bottom-right positioning (20px offset)
  - Click-to-open only interaction
  - Mobile-friendly with touch optimization
  - Dark mode compatibility using Docusaurus CSS variables
  - Zero layout breaks with fixed positioning
  - Lazy loading for performance
- Added Section 14.6 (Integration) for seamless Docusaurus embedding
- Updated Core Principles (Section 2) to include lightweight architecture and user-centric design
- Updated Standards (Section 3) with web component requirements
- Updated Constraints (Section 4) with chat widget specifications
- Added Web Platform section to System Requirements (Section 7)
- Added Web Development workflow rules (Section 8)
- Added Data & Privacy subsection to Ethics & Safety (Section 9)
- Added Web Platform Deliverables (Section 12)
- Updated Completion Definition (Section 13) with website-specific criteria

**Version bump rationale:** MINOR version (1.1.0 → 1.2.0) because new architectural constraints and integration requirements were added without removing existing principles or making backward-incompatible changes.

## Outcome

- ✅ Impact: Constitution now governs both robotics development and web platform with strict lightweight chat widget requirements
- 🧪 Tests: Template consistency validated across plan-template.md, spec-template.md, and tasks-template.md
- 📁 Files: Updated .specify/memory/constitution.md
- 🔁 Next prompts: Implement the Course AI chat widget following the constitutional requirements
- 🧠 Reflection: Clear UI/UX constraints prevent scope creep and ensure mobile-first, accessible implementation

## Evaluation notes (flywheel)

- Failure modes observed: None - constitution update completed successfully with all placeholders resolved
- Graders run and results (PASS/FAIL): PASS - All validations passed (no unresolved placeholders, version bump justified, sync impact documented)
- Prompt variant (if applicable): Standard constitution update workflow
- Next experiment (smallest change to try): Monitor chat widget implementation for compliance with constitutional constraints
