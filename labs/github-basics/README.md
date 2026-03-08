# Lab 1: GitHub and Git Basics

**Prerequisites:** None — this is the starting point.
**Estimated time:** 30 minutes
**What you will have at the end:** A GitHub account, Git installed locally, and a repository with your first commit pushed to GitHub.

---

## Overview

This lab walks you through setting up Git and GitHub from scratch. Every step is a real command you will run on your machine. Expected output is shown so you know what to look for.

If a command produces output that looks different, do not skip it — read the error and troubleshoot before continuing.

---

## Step 1 — Create a GitHub Account

Go to https://github.com and click **Sign up**. Choose a username you are comfortable putting on a resume — this will be visible on all your contributions.

After creating your account:
- Fill in your name, bio, and a profile photo (see `learning_path/GITHUB_PROFILE_GUIDE.md` for guidance).
- Verify your email address — GitHub requires this before you can push code.

---

## Step 2 — Install Git

**Check if Git is already installed:**

```bash
git --version
```

Expected output (version may differ):

```
git version 2.43.0
```

If you see a version number, Git is already installed. Skip to Step 3.

**If Git is not installed:**

- **macOS:** Run `xcode-select --install` in your terminal, or install via Homebrew: `brew install git`
- **Windows:** Download from https://git-scm.com/download/win and run the installer.
- **Linux (Debian/Ubuntu):** `sudo apt-get install git`
- **Linux (Fedora/RHEL):** `sudo dnf install git`

After installing, run `git --version` again to confirm it worked.

---

## Step 3 — Configure Git

Tell Git your name and email. These appear on every commit you make.

```bash
git config --global user.name "Your Name"
git config --global user.email "your-email@example.com"
```

Use the same email address you used to sign up for GitHub. If you prefer to keep your email private, GitHub provides a no-reply email address you can use — find it at https://github.com/settings/emails under "Keep my email addresses private."

Verify your configuration:

```bash
git config --global --list
```

Expected output:

```
user.name=Your Name
user.email=your-email@example.com
```

---

## Step 4 — Authenticate with GitHub

GitHub removed password authentication in 2021. You need to set up one of two methods before you can clone private repos or push anything.

**Choose one: HTTPS with a Personal Access Token (simpler) or SSH keys (recommended for daily use).**

---

### Option A — Personal Access Token (HTTPS)

A Personal Access Token (PAT) is a password replacement you generate on GitHub and paste when Git asks for credentials.

**Create the token:**

1. Go to https://github.com/settings/tokens
2. Click **Generate new token → Generate new token (classic)**
3. Give it a name (e.g., `my-laptop`)
4. Set an expiration (90 days is a safe default)
5. Under **Scopes**, check **repo**
6. Click **Generate token**
7. Copy the token immediately — GitHub will not show it again

**Cache the token so you are not prompted every time:**

macOS:
```bash
git config --global credential.helper osxkeychain
```

Windows:
```bash
git config --global credential.helper manager
```

Linux:
```bash
git config --global credential.helper store
```

The first time you `clone` or `push`, Git will prompt for your GitHub username and password. Enter your GitHub username, and paste the token as the password. It will be saved and reused automatically after that.

---

### Option B — SSH Keys (recommended)

SSH keys let you authenticate without ever entering a password or token. Once set up, they work silently on every push and clone.

**Step 1 — Generate an SSH key pair:**

```bash
ssh-keygen -t rsa -b 4096 -C "your-email@example.com"
```

When prompted:
- Press **Enter** to accept the default file location (`~/.ssh/id_rsa`)
- Enter a passphrase (optional but recommended) or press **Enter** to skip

**Step 2 — Add the key to the SSH agent:**

macOS / Linux:
```bash
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_rsa
```

Windows (Git Bash):
```bash
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_rsa
```

**Step 3 — Copy your public key:**

macOS:
```bash
pbcopy < ~/.ssh/id_rsa.pub
```

Linux:
```bash
cat ~/.ssh/id_rsa.pub
# Copy the output manually
```

Windows (Git Bash):
```bash
clip < ~/.ssh/id_rsa.pub
```

**Step 4 — Add the key to GitHub:**

1. Go to https://github.com/settings/keys
2. Click **New SSH key**
3. Give it a title (e.g., `My Laptop`)
4. Paste the key into the **Key** field
5. Click **Add SSH key**

**Step 5 — Test the connection:**

```bash
ssh -T git@github.com
```

Expected output:
```
Hi YOUR-USERNAME! You've successfully authenticated, but GitHub does not provide shell access.
```

If you use SSH, use the SSH clone URL (`git@github.com:USERNAME/repo.git`) instead of the HTTPS URL when cloning.

---

## Step 5 — Create Your First Repository on GitHub

1. Go to https://github.com and click the **+** icon in the top-right corner, then click **New repository**.
2. Name the repository `my-first-repo` (or anything you like).
3. Set it to **Public**.
4. Check **Add a README file**.
5. Click **Create repository**.

You should now see your new repository at `https://github.com/YOUR-USERNAME/my-first-repo`.

---

## Step 6 — Clone the Repository Locally

Cloning downloads the repository to your machine so you can work on it.

Go to your repository page on GitHub and click the green **Code** button. Copy the HTTPS URL — it looks like:

```
https://github.com/YOUR-USERNAME/my-first-repo.git
```

Then run:

```bash
git clone https://github.com/YOUR-USERNAME/my-first-repo.git
```

Expected output:

```
Cloning into 'my-first-repo'...
remote: Enumerating objects: 3, done.
remote: Counting objects: 100% (3/3), done.
remote: Compressing objects: 100% (2/2), done.
Receiving objects: 100% (3/3), done.
```

Now move into the cloned directory:

```bash
cd my-first-repo
```

---

## Step 7 — Create a File, Commit, and Push

**Create a new file:**

```bash
echo "# My Notes" > notes.md
```

**Check the status of your repository:**

```bash
git status
```

Expected output:

```
On branch main
Untracked files:
  (use "git add <file>..." to include in what will be committed)
        notes.md

nothing added to commit but untracked files present (use "git add" to track)
```

**Stage the file:**

```bash
git add notes.md
```

**Commit the change:**

```bash
git commit -m "Add notes file"
```

Expected output:

```
[main abc1234] Add notes file
 1 file changed, 1 insertion(+)
 create mode 100644 notes.md
```

The commit hash (`abc1234`) will be different on your machine — that is normal.

**Push to GitHub:**

```bash
git push origin main
```

Expected output:

```
Enumerating objects: 4, done.
Counting objects: 100% (4/4), done.
Compressing objects: 100% (2/2), done.
Writing objects: 100% (3/3), 299 bytes | 299.00 KiB/s, done.
Total 3 (delta 0), reused 0 (delta 0), pack-reused 0
To https://github.com/YOUR-USERNAME/my-first-repo.git
   abc1234..def5678  main -> main
```

If Git prompts for credentials on push, refer back to Step 4 for HTTPS token setup or switch to the SSH remote URL.

---

## Step 8 — Verify on GitHub

Go to `https://github.com/YOUR-USERNAME/my-first-repo` in your browser. You should see the `notes.md` file listed in the repository, along with your commit message "Add notes file."

Click on the commit message or the clock icon to see your full commit history.

---

## Lab Complete

You have:
- Created a GitHub account.
- Installed and configured Git.
- Created a repository on GitHub.
- Cloned it locally.
- Made a file, committed it, and pushed it to GitHub.

**Next step:** Lab 2 — Your First Open-Source Contribution: `labs/first-contribution/README.md`

---

## Common Issues

**"Permission denied" when pushing:**
GitHub no longer accepts password authentication for Git. Use a Personal Access Token or set up SSH keys. See https://docs.github.com/en/authentication.

**"src refspec main does not match any" when pushing:**
Your default branch may be called `master` instead of `main`. Try `git push origin master` or check with `git branch`.

**"fatal: not a git repository" error:**
You are not inside the cloned directory. Run `cd my-first-repo` (or whatever you named it) before running Git commands.
