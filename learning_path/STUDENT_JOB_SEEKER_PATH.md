# Student and Job Seeker Learning Path

This is a structured, phased journey for students and job seekers who want to build real open-source experience and make their GitHub profile visible to employers and communities.

The path moves from zero experience to making real contributions and starting your own project. Each phase has clear goals, concrete actions, and a checkpoint so you know when you are ready to move forward.

**OpenPath does not guarantee jobs, internships, or outcomes. This path is a guide, not a promise.**

---

## Overview

| Phase | Focus | Estimated Time |
|-------|-------|----------------|
| Phase 0 | Setup and profile | 1-2 hours |
| Phase 1 | Learn fundamentals | 2-4 weeks (self-paced) |
| Phase 2 | First contribution | 1-3 days |
| Phase 3 | Start your own project | 1 week |
| Phase 4 | Grow — internships, mentorship, community | Ongoing |

Work at your own pace. These time ranges are rough guides, not requirements.

---

## Phase 0 — Setup and Profile

**Goal:** You have a GitHub account and a basic, professional-looking profile.

### Actions

1. Create a GitHub account at https://github.com if you do not have one.
2. Fill in your profile: add a real name, a short bio, your location (optional), and a link to a portfolio or LinkedIn if you have one.
3. Set a profile photo — a clear, professional image helps.
4. Follow the **GitHub Profile Guide** to create a profile README that introduces you: see `learning_path/GITHUB_PROFILE_GUIDE.md`.
5. Complete **Lab 1 (GitHub & Git Basics)** to confirm your local setup works: see `labs/lab01-github-basics/README.md`.

### Checkpoint — you are ready for Phase 1 when:
- You have a GitHub account.
- Your profile has a name, bio, and photo.
- You have Git installed locally and can push a commit to a repository.

---

## Phase 1 — Learn Fundamentals

**Goal:** You understand Git, GitHub workflows, and at least one programming or technical area at a beginner level.

### Actions

1. Pick one or two free resources from `learning/LEARNING_RESOURCES.md` that match your background and goals.
   - For general programming: consider freeCodeCamp or OSSU Computer Science.
   - For security: consider OWASP Learning Path or TryHackMe (free tier).
   - For cloud and infrastructure: consider Kubernetes Learning Path or Linux Foundation free courses.
2. Learn Git branching and pull request workflows. GitHub Skills (linked in `learning/LEARNING_RESOURCES.md`) has short, free, interactive courses for this.
3. Read `contribution_sources/HOW_TO_CONTRIBUTE.md` to understand what good open-source contribution looks like before you start.
4. Browse `contribution_sources/OSS_PLATFORMS.md` to get a feel for the major open-source ecosystems you might eventually contribute to.

### Tips for this phase
- Do not try to learn everything. Pick one resource, go through it consistently, and ship small projects or exercises to GitHub as you go.
- Your GitHub contribution graph starts building from the moment you push commits — even from learning exercises.
- Consistent small progress (30-60 minutes a day) compounds faster than occasional long sessions.

### Checkpoint — you are ready for Phase 2 when:
- You can write a basic Git workflow from memory: clone, branch, commit, push, pull request.
- You understand what a fork is and why you would use one.
- You have at least one small project or exercise committed to a GitHub repository.

---

## Phase 2 — First Contribution

**Goal:** You have opened at least one real pull request to an open-source project that is not your own.

### Actions

1. Complete **Lab 3 (Your First Open-Source Contribution)**: see `labs/lab03-first-contribution/README.md`. This walks you through contributing to a practice repository designed for beginners.
2. After completing the lab, find a real beginner-friendly issue using the sources in `contribution_sources/OSS_BEGINNER_CONTRIBUTION_SOURCES.md`. Good starting points:
   - Good First Issue (https://goodfirstissue.dev)
   - Up For Grabs (https://up-for-grabs.net)
   - CodeTriage (https://www.codetriage.com)
3. Before opening your PR, re-read `contribution_sources/HOW_TO_CONTRIBUTE.md` — especially the due diligence checklist.
4. After your PR is merged, note it somewhere. This is your first proof of open-source contribution.

### Tips for this phase
- Start with documentation fixes, typos, or test additions — they are legitimate contributions and easier to get merged for first-timers.
- Read the project's CONTRIBUTING.md before opening any PR.
- Be patient. Reviews can take days or weeks on active projects.

### Checkpoint — you are ready for Phase 3 when:
- You have opened at least one PR to a real open-source project (not just the practice repo).
- You understand the fork-and-PR workflow end to end.

---

## Phase 3 — Start Your Own Project

**Goal:** You have a public GitHub repository that demonstrates your interests, skills, or ideas — pinned on your profile.

### Actions

1. Complete **Lab 2 (Start Your Own Open-Source Project)**: see `labs/lab02-start-your-project/README.md`. This walks you through creating a well-structured public repository.
2. Choose a project topic that reflects genuine interest. Ideas:
   - A tool or script you actually use.
   - A curated list (like OpenPath itself) on a topic you know well.
   - A beginner tutorial or walkthrough on something you just learned.
   - A small data set or collection with clear documentation.
3. Write a clear README, add a LICENSE, and add a CONTRIBUTING.md — the lab covers all of these.
4. Create at least one Issue on your own repo labeled `good first issue` — this signals the project is open to contributions and helps with discoverability.
5. Pin the repository on your GitHub profile.

### Tips for this phase
- The project does not need to be large or impressive. A well-documented, clearly scoped small project is better than an ambitious, abandoned one.
- Commit regularly. A project with 20 commits over a month shows sustained effort.
- Add GitHub topics/tags to the repository so others can find it.

### Checkpoint — you are ready for Phase 4 when:
- You have a public repository with a README, LICENSE, and at least a few commits.
- The repository is pinned on your GitHub profile.
- You could explain the project's purpose in two sentences.

---

## Phase 4 — Grow

**Goal:** You are building reputation, connections, and opportunities through sustained open-source participation.

### Actions

1. Apply for structured programs. See `contribution_sources/INTERNSHIPS_AND_MENTORSHIP.md` for:
   - **GSoC (Google Summer of Code)** — paid, summer program, very competitive.
   - **LFX Mentorship** — Linux Foundation program, stipended, multiple cohorts per year.
   - **Outreachy** — paid internship for underrepresented groups in tech.
   - **CNCF Mentored Projects** — cloud-native focused, multiple tracks.
2. Engage with communities around projects you contribute to. Join their Slack, Discord, or mailing list. Introduce yourself.
3. Continue making contributions — even one PR per month to an existing project builds a visible track record over time.
4. Read success stories in `success_stories/SUCCESS_STORIES.md` to see how others navigated similar paths.
5. If you have a story to share, submit it via pull request using the template in `success_stories/SUCCESS_STORIES.md`.

### Tips for this phase
- Application deadlines for GSoC, Outreachy, and LFX shift each year. Check `contribution_sources/INTERNSHIPS_AND_MENTORSHIP.md` regularly for updated dates.
- Most structured programs prefer applicants who have already made at least one contribution to the relevant project — start early.
- Your GitHub profile, contribution history, and your own project are your portfolio. Keep them current.

---

## Quick Reference — Files in This Repository

| What you need | Where to find it |
|---------------|-----------------|
| Beginner issue finders | `contribution_sources/OSS_BEGINNER_CONTRIBUTION_SOURCES.md` |
| How to write a good PR | `contribution_sources/HOW_TO_CONTRIBUTE.md` |
| OSS ecosystems overview | `contribution_sources/OSS_PLATFORMS.md` |
| Internships and mentorship programs | `contribution_sources/INTERNSHIPS_AND_MENTORSHIP.md` |
| Free learning resources | `learning/LEARNING_RESOURCES.md` |
| GitHub profile tips | `learning_path/GITHUB_PROFILE_GUIDE.md` |
| Lab 1: Git basics | `labs/lab01-github-basics/README.md` |
| Lab 2: Start your project | `labs/lab02-start-your-project/README.md` |
| Lab 3: First contribution | `labs/lab03-first-contribution/README.md` |
| Lab 4: AI coding agents | `labs/lab04-ai-coding-agent/README.md` |
| Lab 5: Static web demos | `labs/lab05-static-pages/README.md` |
| Lab 6: Context, skills, agents | `labs/lab06-prompt-context/README.md` |
| Lab 7: MCP integration | `labs/lab07-mcp-integration/README.md` |
| Lab 8: MVP delivery | `labs/lab08-mvp-delivery/README.md` |
| Contributor success stories | `success_stories/SUCCESS_STORIES.md` |

---

*This path was designed to be followed sequentially, but you can skip phases you have already completed. If you are stuck, the labs and linked resources are the fastest way to unblock yourself.*
