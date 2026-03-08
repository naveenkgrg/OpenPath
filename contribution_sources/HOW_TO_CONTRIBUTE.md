# How to Contribute to Open Source

This is a practical checklist for evaluating open-source projects before contributing, and for writing contributions that actually get merged.

Read this before opening your first pull request on a real project.

---

## Before you pick a project

Not every open-source project is worth contributing to right now. Ask these questions first.

### Is the project active?

- Look at the commit history. Has there been a commit in the past 6 months?
- Look at open pull requests. Are maintainers reviewing and responding?
- If the last commit was 2 years ago and PRs sit unanswered, the project may be unmaintained. Contributions there may never be reviewed.

### Does the project welcome beginners?

- Does it have a `CONTRIBUTING.md`? Read it before doing anything else.
- Are there issues labeled `good first issue` or `help wanted`?
- Is the tone in issue comments and PR reviews respectful?

### Is it a good fit for your skills?

- Look at recent issues and PRs to understand the work involved.
- If the stack or codebase is completely unfamiliar, plan time to learn before contributing — or start with documentation.

---

## Choosing an issue

- Pick an issue that is explicitly open and unassigned.
- Comment on it to say you are working on it before starting — avoids duplicated effort.
- Read the full issue thread. Sometimes the solution is discussed or the issue is no longer valid.
- For your first contribution, prefer documentation fixes, typo corrections, test additions, or small bug fixes. These are easier to scope and faster to review.

---

## Before you start coding

- Fork the repository and clone your fork.
- Set up the project locally and make sure it runs.
- Read the CONTRIBUTING.md in full — it may specify branch naming conventions, commit message format, or test requirements.
- Check if there is a related PR already open for the same issue.

---

## Writing your contribution

- Make your change on a feature branch — never on `main`.
- Keep the change focused on the issue. Avoid unrelated cleanup or refactoring in the same PR.
- Write a clear commit message that says what changed and why.
- If the project has tests, run them before opening the PR. If applicable, add a test for your change.
- If you changed something that could affect other parts of the project, note it in the PR description.

---

## Opening the pull request

Your PR description should answer:
1. **What does this change?** One or two sentences.
2. **Why?** Link to the issue it fixes (use `Closes #123` so it auto-closes).
3. **How did you test it?** Briefly describe what you verified.

Keep the title short and descriptive. Examples:
- `Fix broken link in README`
- `Add test coverage for user login function`
- `Update CONTRIBUTING.md with branch naming convention`

---

## After opening the PR

- Be patient. Maintainers of active projects are often volunteers. A week without a response is normal.
- Respond to review comments promptly and respectfully. If you disagree with feedback, explain your reasoning calmly.
- If asked to make changes, push new commits to the same branch — your PR updates automatically.
- If you do not hear back after 2-3 weeks, a polite follow-up comment is appropriate.

---

## Cross-links

- To find projects with beginner issues: `contribution_sources/OSS_BEGINNER_CONTRIBUTION_SOURCES.md`
- To understand major OSS ecosystems: `contribution_sources/OSS_PLATFORMS.md`
- To practice the full PR workflow first: `labs/first-contribution/README.md`
