# GitHub Profile Guide

Your GitHub profile is your public open-source portfolio. For students and job seekers, it is often the first thing a hiring manager, mentor, or collaborator will look at. This guide covers how to make it clear, professional, and job-ready.

This guide does not require paid tools or accounts. Everything described here is free.

---

## Profile Basics

These are the fields GitHub shows on your profile page. Fill them all in.

### Name
Use your real name or a consistent professional name. This is what appears on your contributions and pull requests.

### Bio
Write one or two sentences that describe who you are and what you are working on or interested in. Keep it honest and specific.

Examples:
- "Computer science student interested in cloud-native infrastructure and open source."
- "Self-taught developer learning Python and contributing to open-source projects."
- "Backend engineer exploring distributed systems and CNCF projects."

Avoid vague phrases like "passionate developer" or "coding enthusiast." Be specific.

### Location
Optional, but including a city or region makes you more discoverable and signals you are a real person.

### Website or link
If you have a portfolio site, LinkedIn, or personal blog, add it here. If not, leave it blank — do not add a placeholder.

### Profile photo
Use a clear, professional photo where your face is visible. Avatars or illustrations are fine if they are consistent with a professional image.

---

## Profile README

A profile README is a special file that appears at the top of your GitHub profile page. It is created by making a repository with the same name as your GitHub username and adding a `README.md` to it.

**How to create it:**
1. Create a new repository named exactly your GitHub username (for example, if your username is `janesmith`, create a repo called `janesmith`).
2. Make it public.
3. Initialize it with a README.
4. Edit the README — it will automatically appear on your profile page.

### What to include in your profile README

Keep it short and readable. A profile README that is too long will not be read.

**Recommended sections:**
- A one or two sentence introduction (who you are, what you are focused on).
- What you are currently learning or working on.
- A brief list of your skills or technologies you use (be honest — only list things you can actually use).
- Links: personal site, LinkedIn, or email if you want to be contacted.
- Optional: a sentence about your open-source interests or goals.

**What to avoid:**
- Auto-generated stats badges that are just there for decoration.
- Long lists of technologies you have only touched briefly.
- Copying someone else's README structure without adapting it to your actual situation.

### Minimal profile README template

```markdown
# Hi, I am [Your Name]

[One sentence about your background and focus area.]

Currently working on: [project or learning goal].

Skills I use: [language 1], [language 2], [tool 1].

Open to: [contributions, collaboration, mentorship — whatever applies].

[Optional: link to portfolio or contact]
```

Adapt this to your situation. Authenticity matters more than completeness.

---

## Pinned Repositories

You can pin up to six repositories on your profile. These are the first thing visitors see after your bio.

### What to pin

- Projects you built yourself — even small ones with good documentation.
- Repositories where you made notable contributions (forks count if they show your work).
- A curated list or resource you maintain.
- Learning projects that show progression, if they have clear READMEs.

### What not to pin

- Empty repositories or repositories with only a default README.
- Tutorial follow-alongs with no changes or additions of your own.
- Repositories you created just to pin something — it shows.

### How to pin

Go to your GitHub profile, click "Customize your pins," and select from your repositories or repositories you have starred or contributed to.

---

## Contribution Graph

The green contribution graph on your profile shows commits, pull requests, issues, and code reviews over the past year. Recruiters and collaborators do look at this.

### Building a consistent graph

- Commit regularly, even in small amounts. One commit per day or a few per week is better than one large burst per month.
- Learning exercises pushed to GitHub count — do not leave them only on your local machine.
- PRs and issues on other projects count too, not only your own repositories.
- Keep your email consistent — contributions only count if the email in your Git config matches your GitHub account email.

### Setting your Git email

```bash
git config --global user.email "your-github-email@example.com"
```

Use the same email you registered with on GitHub. If you use GitHub's privacy email, use that.

---

## Repository Topics and Discoverability

When you create or maintain a repository, add **topics** (tags) to it. Topics make your project findable when people search GitHub.

**How to add topics:**
1. Go to your repository.
2. Click the gear icon next to "About" on the right side.
3. Add relevant topics (for example: `python`, `beginner-friendly`, `open-source`, `cli-tool`).

Use topics that accurately describe what the project does and what technologies it uses. Use common tags that people actually search for.

---

## For Students — Portfolio-Specific Tips

If you are applying for internships or entry-level roles, your GitHub profile is often reviewed before or during the hiring process. Here is what helps:

- **A few good projects beat many empty ones.** Three repositories with solid READMEs, clear purpose, and real code are better than ten placeholder repos.
- **Document your work.** A project without a README is invisible. Write one even for small projects.
- **Show process, not just results.** Commit history, issues, and a CONTRIBUTING.md signal that you know collaborative workflows.
- **Link to your GitHub in your resume.** Make sure the profile is up to date before you do.
- **Remove or archive things you are not proud of.** You can archive old repositories so they do not appear by default but are still accessible.

---

## Cross-Links

- To set up your profile from scratch and make your first commit: `labs/github-basics/README.md`
- To create a project worth pinning: `labs/start-your-project/README.md`
- To see examples of contributor profiles and journeys: `success_stories/SUCCESS_STORIES.md`
- To follow a full learning path from setup to internship: `learning_path/STUDENT_JOB_SEEKER_PATH.md`

---

*OpenPath does not guarantee any employment outcomes. These are practical recommendations based on common practices in the open-source and tech hiring community.*
