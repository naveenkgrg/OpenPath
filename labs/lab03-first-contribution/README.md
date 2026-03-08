# Lab 2: Your First Open-Source Contribution

**Prerequisites:** Lab 1 complete — you have Git installed, a GitHub account, and can push commits.
**Estimated time:** 30 minutes
**What you will have at the end:** A merged pull request on a real open-source practice repository.

---

## Overview

This lab walks you through the full fork-and-pull-request workflow — the standard way open-source contributions work. You will fork a practice repository, make a change, and open a pull request.

The practice repository used in this lab (`first-contributions`) was created specifically for beginners. It is safe to experiment with and is maintained by the community.

---

## Background: Why Fork?

When you contribute to a project you do not own, you cannot push directly to it. Instead:
1. You **fork** the repository — creating your own copy of it on GitHub.
2. You **clone your fork** to your machine and make changes there.
3. You push the changes to your fork.
4. You open a **pull request** — a request for the original project to include your changes.

This workflow keeps the original project safe while allowing anyone to propose improvements.

---

## Step 1 — Fork the Practice Repository

Go to https://github.com/firstcontributions/first-contributions in your browser.

Click the **Fork** button in the top-right corner of the page. GitHub will create a copy of this repository under your account.

After forking, you will be at `https://github.com/YOUR-USERNAME/first-contributions`.

---

## Step 2 — Clone Your Fork

Copy the HTTPS URL from the green **Code** button on your fork's page. It will look like:

```
https://github.com/YOUR-USERNAME/first-contributions.git
```

Clone it:

```bash
git clone https://github.com/YOUR-USERNAME/first-contributions.git
```

Expected output:

```
Cloning into 'first-contributions'...
remote: Enumerating objects: ...
Receiving objects: 100% ...
done.
```

Move into the directory:

```bash
cd first-contributions
```

---

## Step 3 — Create a Branch

Never make changes directly on the `main` branch. Create a new branch for your contribution.

```bash
git checkout -b add-YOUR-NAME
```

Replace `YOUR-NAME` with your actual name (no spaces — use hyphens). For example: `add-jane-smith`.

Expected output:

```
Switched to a new branch 'add-jane-smith'
```

---

## Step 4 — Make Your Change

Open the file `Contributors.md` in a text editor. Add your name to the list following the existing format.

For example, if the file contains lines like:

```
- Jane Smith
- Alex Johnson
```

Add your name in the same format:

```
- Your Name
```

Save the file.

---

## Step 5 — Commit Your Change

Check what changed:

```bash
git status
```

Expected output:

```
On branch add-your-name
Changes not staged for commit:
  (use "git add <file>..." to update what will be committed)
        modified:   Contributors.md
```

Stage the change:

```bash
git add Contributors.md
```

Commit it:

```bash
git commit -m "Add YOUR-NAME to Contributors list"
```

Expected output:

```
[add-your-name abc1234] Add YOUR-NAME to Contributors list
 1 file changed, 1 insertion(+)
```

---

## Step 6 — Push to Your Fork

```bash
git push origin add-YOUR-NAME
```

Replace `add-YOUR-NAME` with the branch name you created in Step 3.

Expected output:

```
Enumerating objects: 5, done.
...
To https://github.com/YOUR-USERNAME/first-contributions.git
 * [new branch]      add-your-name -> add-your-name
```

---

## Step 7 — Open a Pull Request

Go to your fork on GitHub at `https://github.com/YOUR-USERNAME/first-contributions`.

You should see a yellow banner saying **"Your recently pushed branches"** with a **"Compare & pull request"** button. Click it.

If you do not see the banner:
1. Click the **Pull requests** tab.
2. Click **New pull request**.
3. Set **base repository** to `firstcontributions/first-contributions` and **base** to `main`.
4. Set **head repository** to your fork and **compare** to your branch.

On the pull request form:
- The title should be filled in automatically. It should describe your change: "Add [Your Name] to Contributors list."
- Add a short description if the title is not self-explanatory.

Click **Create pull request**.

---

## Step 8 — What Happens Next

The `first-contributions` maintainers review and merge incoming PRs regularly. Your PR will be merged, usually within a few hours or days.

You will receive a GitHub notification when it is merged. After it is merged, your name will appear in the Contributors list on the original repository.

This is your first open-source contribution.

---

## Lab Complete

You have:
- Forked a repository.
- Cloned your fork.
- Created a branch.
- Made a change, committed it, and pushed it to your fork.
- Opened a pull request to the original project.

**Next step:** Lab 3 — Start Your Own Open-Source Project: `labs/lab02-start-your-project/README.md`

---

## Going Further

Now that you know the fork-and-PR workflow, you can apply it to real open-source projects.

Good places to find your next contribution:
- `contribution_sources/OSS_BEGINNER_CONTRIBUTION_SOURCES.md` — curated list of beginner issue finders.
- Good First Issue: https://goodfirstissue.dev
- Up For Grabs: https://up-for-grabs.net

Before opening a PR on a real project, read `contribution_sources/HOW_TO_CONTRIBUTE.md` for a checklist on evaluating projects and writing quality contributions.

---

## Common Issues

**"You are not allowed to push code to this repository" or "Permission denied":**
Make sure you cloned your fork (`YOUR-USERNAME/first-contributions`), not the original (`firstcontributions/first-contributions`). Check the remote URL with `git remote -v`.

**GitHub shows "This branch has no changes" when creating the PR:**
Your push may not have gone through, or you may be comparing the wrong branches. Check that the "compare" branch is your feature branch, not `main`.

**You cannot find Contributors.md:**
Run `ls` in the cloned directory to see the files. The file may be named differently. Read the repository's own README for instructions specific to that repo.
