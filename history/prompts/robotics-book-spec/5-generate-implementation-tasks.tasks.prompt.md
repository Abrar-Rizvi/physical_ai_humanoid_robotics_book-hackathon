---
id: 5
title: Generate implementation tasks
stage: tasks
date: 2025-12-06
surface: agent
model: claude-sonnet-4-5-20250929
feature: robotics-book-spec
branch: 1-robotics-book-spec
user: N/A
command: /sp.tasks
labels: ["tasks", "generation"]
links:
  spec: D:\Quarter 4\ai-book\humanoid-robotic-book\specs\1-robotics-book-spec\spec.md
  ticket: null
  adr: null
  pr: null
  plan: D:\Quarter 4\ai-book\humanoid-robotic-book\specs\1-robotics-book-spec\plan.md
files:
  - D:\Quarter 4\ai-book\humanoid-robotic-book\specs\1-robotics-book-spec\tasks.md
tests:

---

## Prompt

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

## Outline

1. **Setup**: Run `.specify/scripts/powershell/check-prerequisites.ps1 -Json` from repo root and parse FEATURE_DIR and AVAILABLE_DOCS list. All paths must be absolute. For single quotes in args like "I'm Groot", use escape syntax: e.g 'I'\''m Groot' (or double-quote if possible: "I'm Groot").

2. **Load design documents**: Read from FEATURE_DIR:
   - **Required**: plan.md (tech stack, libraries, structure), spec.md (user stories with priorities)
   - **Optional**: data-model.md (entities), contracts/ (API endpoints), research.md (decisions), quickstart.md (test scenarios)
   - Note: Not all projects have all documents. Generate tasks based on what's available.

3. **Execute task generation workflow**:
   - Load plan.md and extract tech stack, libraries, project structure
   - Load spec.md and extract user stories with their priorities (P1, P2, P3, etc.)
   - If data-model.md exists: Extract entities and map to user stories
   - If contracts/ exists: Map endpoints to user stories
   - If research.md exists: Extract decisions for setup tasks
   - Generate tasks organized by user story (see Task Generation Rules below)
   - Generate dependency graph showing user story completion order
   - Create parallel execution examples per user story
   - Validate task completeness (each user story has all needed tasks, independently testable)

4. **Generate tasks.md**: Use `.specify.specify/templates/tasks-template.md` as structure, fill with:
   - Correct feature name from plan.md
   - Phase 1: Setup tasks (project initialization)
   - Phase 2: Foundational tasks (blocking prerequisites for all user stories)
   - Phase 3+: One phase per user story (in priority order from spec.md)
   - Each phase includes: story goal, independent test criteria, tests (if requested), implementation tasks
   - Final Phase: Polish & cross-cutting concerns
   - All tasks must follow the strict checklist format (see Task Generation Rules below)
   - Clear file paths for each task
   - Dependencies section showing story completion order
   - Parallel execution examples per story
   - Implementation strategy section (MVP first, incremental delivery)

5. **Report**: Output path to generated tasks.md and summary:
   - Total task count
   - Task count per user story
   - Parallel opportunities identified
   - Independent test criteria for each story
   - Suggested MVP scope (typically just User Story 1)
   - Format validation: Confirm ALL tasks follow the checklist format (checkbox, ID, labels, file paths)

Context for task generation: $ARGUMENTS

The tasks.md should be immediately executable - each task must be specific enough that an LLM can complete it without additional context.

## Task Generation Rules

**CRITICAL**: Tasks MUST be organized by user story to enable independent implementation and testing.

**Tests are OPTIONAL**: Only generate test tasks if explicitly requested in the feature specification or if user requests TDD approach.

### Checklist Format (REQUIRED)

Every task MUST strictly follow this format:

```text
- [ ] [TaskID] [P?] [Story?] Description with file path
```

**Format Components**:

1. **Checkbox**: ALWAYS start with `- [ ]` (markdown checkbox)
2. **Task ID**: Sequential number (T001, T002, T003...) in execution order
3. **[P] marker**: Include ONLY if task is parallelizable (different files, no dependencies on incomplete tasks)
4. **[Story] label**: REQUIRED for user story phase tasks only
   - Format: [US1], [US2], [US3], etc. (maps to user stories from spec.md)
   - Setup phase: NO story label
   - Foundational phase: NO story label
   - User Story phases: MUST have story label
   - Polish phase: NO story label
5. **Description**: Clear action with exact file path

**Examples**:

- ✅ CORRECT: `- [ ] T001 Create project structure per implementation plan`
- ✅ CORRECT: `- [ ] T005 [P] Implement authentication middleware in src/middleware/auth.py`
- ✅ CORRECT: `- [ ] T012 [P] [US1] Create User model in src/models/user.py`
- ✅ CORRECT: `- [ ] T014 [US1] Implement UserService in src/services/user_service.py`
- ❌ WRONG: `- [ ] Create User model` (missing ID and Story label)
- ❌ WRONG: `T001 [US1] Create model` (missing checkbox)
- ❌ WRONG: `- [ ] [US1] Create User model` (missing Task ID)
- ❌ WRONG: `- [ ] T001 [US1] Create model` (missing file path)

### Task Organization

1. **From User Stories (spec.md)** - PRIMARY ORGANIZATION:
   - Each user story (P1, P2, P3...) gets its own phase
   - Map all related components to their story:
     - Models needed for that story
     - Services needed for that story
     - Endpoints/UI needed for that story
     - If tests requested: Tests specific to that story
   - Mark story dependencies (most stories should be independent)

2. **From Contracts**:
   - Map each contract/endpoint → to the user story it serves
   - If tests requested: Each contract → contract test task [P] before implementation in that story's phase

3. **From Data Model**:
   - Map each entity to the user story(ies) that need it
   - If entity serves multiple stories: Put in earliest story or Setup phase
   - Relationships → service layer tasks in appropriate story phase

4. **From Setup/Infrastructure**:
   - Shared infrastructure → Setup phase (Phase 1)
   - Foundational/blocking tasks → Foundational phase (Phase 2)
   - Story-specific setup → within that story's phase

### Phase Structure

- **Phase 1**: Setup (project initialization)
- **Phase 2**: Foundational (blocking prerequisites - MUST complete before user stories)
- **Phase 3+**: User Stories in priority order (P1, P2, P3...)
  - Within each story: Tests (if requested) → Models → Services → Endpoints → Integration
  - Each phase should be a complete, independently testable increment
- **Final Phase**: Polish & Cross-Cutting Concerns

## Response snapshot

The tasks for the "Physical AI & Humanoid Robotics Book" project have been successfully generated and saved to `specs/1-robotics-book-spec/tasks.md`.

**Path to Tasks File**: `D:\Quarter 4\ai-book\humanoid-robotic-book\specs\1-robotics-book-spec\tasks.md`

**Summary of Tasks**:
*   **Total Tasks**: 59
*   **Tasks by Phase**:
    *   Phase 1 (Setup): 10 tasks
    *   Phase 2 (Foundational Tasks): 4 tasks
    *   Phase 3 (User Story 1 - Learning Physical AI Fundamentals): 6 tasks
    *   Phase 4 (User Story 2 - Simulating Robotics with ROS 2 and Gazebo/Unity): 10 tasks
    *   Phase 5 (User Story 3 - Exploring NVIDIA Isaac Ecosystem): 5 tasks
    *   Phase 6 (User Story 4 - Building Vision-Language-Action Pipelines): 6 tasks
    *   Phase 7 (Polish & Cross-Cutting Concerns): 18 tasks

**Parallel Opportunities**: Many tasks are marked with `[P]`, indicating opportunities for parallel execution, particularly within content creation, asset development, and quality assurance phases.

**Independent Test Criteria per User Story**:
*   **US1**: Student can explain embodied intelligence and its relevance; can visualize complex concepts like control loops from diagrams.
*   **US2**: Student can create a simple robot model (URDF snippet) and launch it in Gazebo/Unity; simulated robot responds to ROS 2 commands.
*   **US3**: Student can describe how Isaac Sim and Isaac ROS enable advanced simulations and real-world deployment; understands VSLAM and Nav2 for autonomous navigation.
*   **US4**: Student can outline steps from spoken command to robot execution; identifies LLM's role in interpreting commands and generating ROS 2 actions.

**Suggested MVP Scope**: Complete Phase 1 (Setup), Phase 2 (Foundational Tasks), and Phase 3 (User Story 1 - Learning Physical AI Fundamentals) to establish a functional Docusaurus site with core content.

All tasks adhere to the specified checklist format: `- [ ] [TaskID] [P?] [Story?] Description with file path`.

## Outcome

- ✅ Impact: Implementation tasks generated and saved to `tasks.md`.
- 🧪 Tests: N/A
- 📁 Files: `D:\Quarter 4\ai-book\humanoid-robotic-book\specs\1-robotics-book-spec\tasks.md` created.
- 🔁 Next prompts: User to review tasks and initiate implementation.
- 🧠 Reflection: The `/sp.tasks` command successfully generated a detailed, actionable task list based on the implementation plan and feature specification.

## Evaluation notes (flywheel)

- Failure modes observed: Script for PHR creation not found.
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Continue investigating and fixing the `create-phr.sh` script issue for automated PHR generation.