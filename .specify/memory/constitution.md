<!--
Sync Impact Report:
Version change: 1.0.0 → 1.1.0
Modified principles:
- Section 6 (Scope) updated to include RAG Chatbot.
Added sections:
- Section 14 (RAG Chatbot Integration) and its subsections.
Removed sections: None
Templates requiring updates:
- .specify/templates/plan-template.md ⚠ pending (check for RAG chatbot specific rules in "Approved Technologies")
- .specify/templates/spec-template.md ⚠ pending (check for RAG chatbot specific requirements)
- .specify/templates/tasks-template.md ⚠ pending (check for RAG chatbot specific task types)
- .specify/templates/commands/*.md ⚠ pending (check for outdated references)
Follow-up TODOs: None
-->
# Constitution for Physical AI & Humanoid Robotics Book

## 1. Purpose

This Constitution defines the rules, standards, and workflows for building, simulating, and testing humanoid or proxy robots using ROS 2, Gazebo, Unity, NVIDIA Isaac, and VLA models during the Physical AI & Humanoid Robotics Hackathon.

## 2. Core Principles

- Engineering accuracy, academic clarity
- Verified, reproducible robotics & AI workflows
- Safety-first development for humanoid robots
- Ethical, traceable, responsible AI usage
- Alignment with official documentation (ROS 2, Gazebo, Unity, Isaac)

## 3. Standards

- Claims must be verifiable via official docs or reputable research
- Citations: APA or IEEE
- At least 30% peer-reviewed sources, 0% plagiarism
- Readability: Grade 10–12 engineering level
- All diagrams and code must reflect real system behavior

## 4. Constraints

- Length: 4,000–6,000 words
- Minimum 12 authoritative sources
- Formats: PDF or Markdown
- Must include:
    - Robot system architecture diagram
    - Sensor → AI → Controller → Actuator flow
    - Safety guidelines for humanoids
    - Simulation setup + validation

## 5. Success Criteria

A constitution is successful if it:

- Defines complete robot design → simulation → testing workflow
- Maps ROS 2 / Gazebo / Unity / Isaac / VLA to responsibilities
- Ensures reproducibility, safety, and ethics
- Provides clear team workflow standards
- Passes mentor technical audit

## 6. Scope

Covers the entire hackathon:

- Physical AI foundations
- ROS 2 control architecture
- Gazebo + Unity simulation
- NVIDIA Isaac perception & navigation
- VLA-based action pipelines
- Capstone: Autonomous humanoid robot
- **Integrated RAG Chatbot:** Interactive Q&A based on book content.

## 7. System Requirements

- Digital Twin Workstation:
    - RTX 4070 Ti+ (ideal 3090/4090), 32–64GB RAM, Ubuntu 22.04
- Edge Kit: Jetson Orin Nano/NX
- Sensors: RealSense D435i/D455, IMU
- Robots: Unitree Go2, G1, or miniature humanoid
- Cloud: AWS g5/g6 for simulation only—not direct robot control

## 8. Team Workflow Rules

- ROS 2 packages follow standard node/topic/service/action structure
- Valid URDF/SDF models; physics validated in Gazebo
- Unity for visualization; Isaac Sim for data + perception
- VLA pipeline: Whisper → LLM → ROS 2 actions
- Required pipeline:
    - Simulation → Testing → Jetson Deployment → Safety Check

## 9. Ethics & Safety

- No unsafe or uncontrolled movements
- Mandatory Emergency Stop (E-Stop) procedure
- Cloud latency cannot influence robot safety
- All real-world tests require safe distance + logging
- AI actions must be explainable

## 10. Versioning

- Semantic Versioning: MAJOR.MINOR.PATCH
- Every update must be recorded in a version history table.

## 11. Chapter Rules

Each chapter must contain:
- Title, objectives, core concepts, technical deep dive, code/pseudocode, diagrams, safety notes, assignments, references.

## 12. Deliverables

- Final Constitution
- System architecture diagram
- Simulation validation report
- AI perception + planning pipeline
- Capstone humanoid functional spec

## 13. Completion Definition

Document is complete when all required sections exist, are technically accurate, include safety rules, and pass mentor audit.

## 14. RAG Chatbot Integration

To enhance the learning experience, an integrated Retrieval-Augmented Generation (RAG) chatbot will be developed.

### 14.1. Purpose

The chatbot's primary purpose is to answer user questions exclusively based on the content of the book, including user-selected text snippets. This ensures responses are grounded and directly relevant to the learning material.

### 14.2. Approved Technologies

-   **OpenAI Agents/ChatKit SDKs:** For chatbot development and interaction logic.
-   **FastAPI:** To serve as the backend API for the chatbot.
-   **Neon Serverless Postgres:** For data storage, particularly for logging and metadata.
-   **Qdrant Cloud Free Tier:** For vector database storage of book embeddings, enabling efficient retrieval.

### 14.3. Architectural Rules

-   **RAG Pipeline:** The chatbot will adhere to a strict RAG pipeline:
    1.  **Embeddings:** Book content will be chunked and converted into vector embeddings.
    2.  **Qdrant:** Embeddings will be stored and indexed in Qdrant for fast semantic search.
    3.  **Retrieval:** User queries will trigger retrieval of relevant text snippets from Qdrant.
    4.  **LLM:** The retrieved content, along with the user's query, will be fed into a Large Language Model (LLM) to generate a grounded response.
-   **Grounded Responses:** All chatbot responses MUST be strictly grounded in the content of the book. The LLM is prohibited from generating information beyond what is present in the provided context.

### 14.4. Safety & Ethics

-   **No Hallucination:** The chatbot MUST NOT hallucinate or generate information not explicitly found within the book's content.
-   **Safe Logging:** All chatbot interactions and system logs MUST be stored securely in Neon Serverless Postgres, adhering to privacy and data retention policies.

### 14.5. Integration

The RAG chatbot functionality MUST be seamlessly embedded within the published book's UI, providing an interactive question-answering experience directly within the learning environment.

## Governance

This constitution supersedes all other project practices. Amendments require a formal proposal, review, documentation of rationale, and approval by project mentors. Versioning follows semantic versioning rules outlined in Section 10. Compliance reviews will be conducted regularly by project mentors.

**Version**: 1.1.0 | **Ratified**: 2025-12-04 | **Last Amended**: 2025-12-08
