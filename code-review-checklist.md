
# Code Review Checklist

## PR: #[PR_NUMBER]
## Branch: [BRANCH_NAME]

### 1. Understanding the Goal
- [ ] What is the purpose of this PR?
- [ ] What issue does it fix? #[ISSUE_NUMBER]

### 2. Mergeability
- [ ] **Conflicts**: Does this branch have merge conflicts with `main`?
  - If yes, run the following commands:
    ```bash
    git checkout main
    git pull origin main
    git checkout [BRANCH_NAME]
    git merge main
    # Resolve conflicts in your editor
    git add .
    git commit -m "Merge main"
    git push
    ```
- [ ] **Failing Checks**: Are there any failing status checks?
  - If yes, what are they?
    - [ ] Linting errors?
    - [ ] Test failures?
    - [ ] Build failures?
  - How to fix:
    - *[Provide specific instructions based on the failure]*

### 3. Code Quality
- [ ] **Clarity**: Is the code easy to understand?
- [ ] **Convention**: Does it follow the project's coding conventions?
- [ ] **Simplicity**: Is there a simpler way to achieve the same result?
- [ ] **Testing**: Are there new tests for new features? Do existing tests pass?

### 4. Final Steps
- [ ] All conversations on the PR have been resolved.
- [ ] The PR has been approved by at least one other developer.
