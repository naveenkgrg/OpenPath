# Lab 3: Start Your Own Open-Source Project

**Prerequisites:** Lab 1 and Lab 2 complete — you can push commits and open pull requests.
**Estimated time:** 45 minutes
**What you will have at the end:** A public GitHub repository with a README, a LICENSE, a CONTRIBUTING.md, GitHub topics, and an open issue — pinned on your profile.

---

## Overview

Starting your own project demonstrates initiative, ownership, and real-world workflow skills. Even a small, well-documented project is valuable in a portfolio. This lab walks through every step of setting one up correctly from the start.

Choose a project topic before you begin. See the tips below if you are unsure what to make.

---

## Choosing a Project Topic

The project does not need to be complex or original. Pick something you genuinely care about or find useful. Good options for beginners:

- A script or tool you already use informally (automate something in your workflow).
- A curated list of resources on a topic you know well (similar to OpenPath itself).
- A beginner tutorial or walkthrough on something you recently learned.
- A collection of practice exercises, notes, or examples from your learning.

Avoid picking something too ambitious. A small, finished, documented project is better than a large, unfinished one.

---

## Step 1 — Create a New Public Repository

Go to https://github.com and click the **+** icon, then **New repository**.

Fill in the form:
- **Repository name:** Choose a short, descriptive, lowercase name with hyphens (not underscores). For example: `python-snippets`, `devops-notes`, `beginner-ml-resources`.
- **Description:** Write one sentence about what the project is.
- **Visibility:** Set to **Public**.
- **Initialize this repository with:** Check **Add a README file**.
- **License:** Select a license now (see Step 3 for guidance).

Click **Create repository**.

---

## Step 2 — Write a Good README

The README is the most important file in your repository. It is the first thing anyone sees.

Clone your repository:

```bash
git clone https://github.com/YOUR-USERNAME/YOUR-REPO-NAME.git
cd YOUR-REPO-NAME
```

Open `README.md` in your editor. Replace the default content with a README that answers these questions:

1. What is this project?
2. Who is it for?
3. How do you use it (or get started)?
4. How can someone contribute?

**Minimal README template:**

```markdown
# Project Name

One sentence describing what this is and who it is for.

## What is included

- Item or feature 1
- Item or feature 2
- Item or feature 3

## How to use

[Step 1]
[Step 2]
[Step 3]

## Contributing

Contributions are welcome. Please read [CONTRIBUTING.md](CONTRIBUTING.md) before opening a pull request.

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.
```

Adapt this to your project. Remove sections that do not apply. Add sections that do.

Save the file.

---

## Step 3 — Add a LICENSE

A repository without a LICENSE is not legally open source — others cannot use or contribute to it safely. Always add a license.

If you initialized the repository with a license on GitHub (Step 1), the `LICENSE` file is already there. If not:

1. Go to your repository on GitHub.
2. Click **Add file** > **Create new file**.
3. Name it `LICENSE`.
4. Click **Choose a license template** on the right side.
5. Select **MIT License** (most permissive, most common for open-source projects).
6. Fill in the year and your name.
7. Click **Review and submit**.

**Which license to choose:**
- **MIT** — permissive, easy, good for most projects. Anyone can use, copy, and modify your code with attribution.
- **Apache 2.0** — similar to MIT but includes explicit patent protection.
- **GPL v3** — requires derivative works to also be open source.

For most beginner projects, MIT is the right choice.

---

## Step 4 — Add a CONTRIBUTING.md

A `CONTRIBUTING.md` file tells others how to contribute to your project. It signals professionalism and makes collaboration easier.

Create the file:

```bash
touch CONTRIBUTING.md
```

Open it and add content like the following template:

```markdown
# Contributing to [Project Name]

Thank you for your interest in contributing.

## How to contribute

1. Fork this repository.
2. Create a branch: `git checkout -b your-feature-name`.
3. Make your changes and commit them: `git commit -m "Describe your change"`.
4. Push to your fork: `git push origin your-feature-name`.
5. Open a pull request against the `main` branch of this repository.

## Guidelines

- Keep pull requests focused on a single change.
- Write clear commit messages.
- If your change is significant, open an issue first to discuss it.

## Questions

Open an issue if you have questions or ideas.
```

Adapt this to your project. Save the file.

---

## Step 5 — Commit and Push Your Changes

Stage, commit, and push everything:

```bash
git add README.md CONTRIBUTING.md
git commit -m "Add README and CONTRIBUTING guide"
git push origin main
```

Expected output:

```
Enumerating objects: 5, done.
...
To https://github.com/YOUR-USERNAME/YOUR-REPO-NAME.git
   abc1234..def5678  main -> main
```

---

## Step 6 — Add GitHub Topics for Discoverability

Topics are tags that make your repository findable when people search GitHub.

1. Go to your repository on GitHub.
2. Click the gear icon next to **About** on the right side.
3. In the **Topics** field, add relevant tags. Examples:
   - `python`, `beginner`, `open-source`, `learning`, `cli`, `tutorial`, `resources`
4. Click **Save changes**.

Add 3-5 topics that accurately describe your project. Use terms people actually search for.

---

## Step 7 — Create Your First Issue

Creating an issue on your own repo — labeled `good first issue` — signals that the project is open to contributions. It also helps with discoverability on sites like Good First Issue.

1. Go to your repository on GitHub.
2. Click the **Issues** tab.
3. Click **New issue**.
4. Write a title and description for something you want to add or improve. Example:
   - Title: "Add examples section to README"
   - Description: "The README would benefit from concrete examples showing how to use the project. This is a good starting task for a first-time contributor."
5. On the right side, click **Labels** and add `good first issue` and `enhancement`.
6. Click **Submit new issue**.

---

## Step 8 — Pin the Repository on Your Profile

1. Go to your GitHub profile at `https://github.com/YOUR-USERNAME`.
2. Click **Customize your pins**.
3. Find your new repository in the list and check it.
4. Click **Save pins**.

Your repository now appears on your profile page, visible to anyone who visits.

---

## Lab Complete

You have:
- Created a public repository with a clear name and description.
- Written a useful README.
- Added a LICENSE.
- Added a CONTRIBUTING.md.
- Added topics for discoverability.
- Created your first issue.
- Pinned the repository on your profile.

This repository is now part of your open-source portfolio.

---

## What to Do Next

- **Keep committing.** A project with activity over time is more convincing than one with a single large initial commit. Even small improvements — fixing a typo, adding an example, improving documentation — keep the contribution graph active.
- **Share it.** Post the link in communities related to the project's topic. Ask for feedback.
- **Respond to issues and PRs.** If someone opens an issue or a pull request, respond in a timely and respectful way — even if the answer is "not planned."

For the bigger picture of where this fits in your journey: `learning_path/STUDENT_JOB_SEEKER_PATH.md`

For guidance on making your GitHub profile strong around this project: `learning_path/GITHUB_PROFILE_GUIDE.md`

---

## Common Issues

**"I do not know what to build":**
Start with a curated list. Pick a topic you know something about (a programming language, a game, a hobby, a city, a tool) and write a list of useful resources for beginners in that area. It is a legitimate project, easy to maintain, and demonstrates writing and curation skills.

**The repository feels too small or simple:**
Small and well-documented is genuinely better than large and messy. Do not inflate the project — build it up incrementally with real additions over time.

**Nobody is contributing:**
This is normal for new projects. Focus on making the project genuinely useful or interesting first. Share it in relevant communities — forums, Discord servers, Reddit threads related to the topic.
