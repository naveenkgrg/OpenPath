# Lab 6: AI Key Concepts — Context, Skills, and Agents

**Prerequisites:** Lab 4 or Lab 5 complete — you have used an AI coding agent at least once.
**Estimated time:** 45–60 minutes
**What you will have at the end:** A working tic-tac-toe game embedded inside a profile page — built across two separate AI chat sessions using saved context — plus a reusable skill file and a practical understanding of context, skills, and agents.

---

## Overview

When you use AI tools to build software, three concepts determine whether you get consistent, high-quality output or frustrating, inconsistent results:

- **Context** — what information you give the AI
- **Skills** — reusable solutions you extract from working output
- **Agents** — AI systems that understand a goal, plan steps, and use tools

This lab is built around one concrete project: you will build a tic-tac-toe game in one AI session, save its context, then reload that context in a fresh session to extend it into a full profile page. Every concept is grounded in that real workflow.

---

## Part 1 — Understanding Context

### What is context?

Context is everything you give an AI to guide its output. It includes:

| Component | What it is | Example |
|-----------|------------|---------|
| **Goal** | What you want to build | "A tic-tac-toe game in one HTML file" |
| **Instructions** | Features and design requirements | "3×3 board, two players, highlight winning line" |
| **Constraints** | Tools, scope, limits | "Inline CSS and JS only, no external libraries" |
| **History** | Previous messages in the session | Earlier prompts and AI responses |

The more clearly you define these four components at the start, the better the AI's output will be throughout the session.

### Common context problems

As a conversation grows longer, several problems emerge:

- Important details get diluted — the AI loses track of early requirements
- The AI gives inconsistent or contradictory output across messages
- It adds features you did not ask for
- It forgets constraints you set early on
- Output quality degrades noticeably after 15–20 exchanges

These are not bugs — they are predictable consequences of how large language models handle long input. You can manage them with the patterns in this lab.

---

## Exercise 1 — Write a strong opening context

Before starting any AI-assisted build, write an opening context message. Use this structure:

```
Goal: [One sentence describing what you are building]

Features:
- [Feature 1]
- [Feature 2]
- [Feature 3]

Constraints:
- Tech stack: [list tools and frameworks]
- Scope: [what is in scope and what is explicitly out of scope]
- Output format: [e.g., "Always produce complete files, not diffs"]

Do not add features I have not asked for. Ask me before introducing new dependencies.
```

Here is the opening context you will use for this lab's main exercise:

```
Goal: Build a tic-tac-toe game in a single index.html file.

Features:
- 3x3 grid board
- Two players take turns (X and O)
- Detect and display the winner
- Highlight the winning line
- Restart button to reset the game

Constraints:
- Single file: index.html only
- Inline CSS inside a <style> block
- Inline JavaScript inside a <script> block
- No external libraries or CDN links

Output format: Always return the complete index.html file, not a diff or partial snippet.
```

Copy this — you will use it in the next step.

---

## Part 2 — The Save-and-Reload Pattern

### Why context degrades

AI sessions have no memory between chats. When you start a new chat, the AI knows nothing about previous sessions. Within a long chat, earlier messages become progressively less influential as the conversation grows. The result: the AI starts forgetting decisions, ignoring constraints, or drifting from the original design.

The fix is deliberate context management.

### The fix: context.md

Maintain a `context.md` file in your project. When a session produces good working output, capture a summary before closing the chat. When you start a new session to extend the project, reload that summary as your opening message.

---

### Worked example — Phase 1: Build the tic-tac-toe game

**Step 1 — Start a new chat with your AI tool** (Claude, Copilot, Cursor, or ChatGPT).

**Step 2 — Paste the opening context from Exercise 1** as your first message. Send it.

**Step 3 — Review the output.** The AI should return a complete `index.html` file. Open it in your browser and verify:
- The 3×3 grid renders correctly
- Players can click squares to place X and O
- The winner is detected and displayed
- The winning line is highlighted
- The restart button resets the board

If anything is broken, ask the AI to fix the specific issue. For example:
```
The winning line is not highlighted. Fix only that — do not change anything else.
```

**Step 4 — Save the working file** as `index.html` in a new folder called `lab06-tictactoe/`.

**Step 5 — Ask the AI to summarize the session** before closing it:

```
Summarize the current state of this project in bullet points for a context.md file. Include:
- What was built
- The file structure
- Key implementation decisions (layout approach, how winner detection works, color scheme)
- Any constraints that must be preserved in future changes
Keep it concise enough to paste into a new chat.
```

**Step 6 — Save the AI's summary** as `lab06-tictactoe/context.md`.

Your `context.md` should look something like this (the AI will generate the actual content):

```markdown
## Project: Tic-Tac-Toe Game

### What was built
- Single-file tic-tac-toe game in index.html
- Two-player turn-based gameplay (X and O)
- Winner detection across all 8 winning combinations
- Winning line highlighted in green
- Restart button resets the board and turn indicator

### File structure
- index.html — complete game (HTML + inline CSS + inline JS)

### Key decisions
- CSS Grid used for the 3x3 board layout
- Board state stored as a 9-element array in JavaScript
- Winner check runs after every move against 8 hardcoded winning combinations
- Color scheme: dark background (#1a1a2e), teal accent (#16213e), green win highlight (#4ecca3)

### Constraints to preserve
- Single file only — no external files or libraries
- All CSS inline in <style>, all JS inline in <script>
- Do not change the winner detection logic
```

Close the chat.

---

### Worked example — Phase 2: Extend into a profile page using saved context

Now you will open a brand new chat — zero history — and use `context.md` to extend the game into a full profile page.

**Step 1 — Start a fresh chat with your AI tool.**

**Step 2 — Open your `context.md` and paste it as the first message**, followed by the new task:

```
I am continuing a project. Here is the current context:

[paste your context.md content here]

New task: Wrap the tic-tac-toe game inside a profile page.

The profile page should:
- Have a header section with: name, one-line bio, and three icon links (GitHub, LinkedIn, Email)
- Display the tic-tac-toe game below the header under a section titled "Mini Game"
- Use the same color scheme already established in the game
- Keep everything in one index.html file
- Do not change the game logic — only add the profile wrapper around it

Return the complete updated index.html.
```

**Step 3 — Review the output.** Open the updated `index.html` in your browser and verify:
- The profile header renders above the game
- The name, bio, and icon links appear correctly
- The game still works exactly as before
- The color scheme is consistent between the profile section and the game

**Step 4 — Notice what the context.md enabled.** Without it, you would have needed to re-explain the game's color scheme, file structure, and constraints from scratch. With it, the AI picked up exactly where the previous session left off — preserving decisions that were already made.

---

## Part 3 — AI Skills

### What is a skill?

A skill is a reusable prompt you extract from a working session. Instead of writing a prompt from scratch next time you need something similar, you save what worked so you can reuse or adapt it.

Skills follow this lifecycle:

```
Build once → Extract the prompt → Save it → Reuse anywhere
```

### Skill types

| Skill type | Example from this lab |
|------------|----------------------|
| **Logic skill** | The tic-tac-toe game prompt |
| **UI skill** | The profile page wrapper prompt |
| **Composition skill** | Reload context → extend existing project |

---

### Exercise 2 — Extract two skills from this lab

Create a folder called `lab06-tictactoe/skills/`. Save two files:

**`skills/tictactoe-game-skill.md`:**

```markdown
# Skill: Tic-Tac-Toe Game

## What it does
Generates a complete, working single-file tic-tac-toe game with winner detection and restart.

## Prompt
Goal: Build a tic-tac-toe game in a single index.html file.

Features:
- 3x3 grid board
- Two players take turns (X and O)
- Detect and display the winner
- Highlight the winning line
- Restart button to reset the game

Constraints:
- Single file: index.html only
- Inline CSS inside a <style> block
- Inline JavaScript inside a <script> block
- No external libraries or CDN links

Output format: Always return the complete index.html file, not a diff or partial snippet.

## What to customize
- Color scheme (background, accent, win highlight colors)
- Board size (change from 3x3 to 4x4 by adjusting the grid and win conditions)
- Player labels (X/O can be changed to any symbols or names)

## Expected output
A single index.html file with a playable two-player tic-tac-toe game that runs in any browser.
```

**`skills/profile-wrapper-skill.md`:**

```markdown
# Skill: Profile Page Wrapper

## What it does
Wraps an existing HTML project inside a profile page with header, bio, and icon links —
using the project's existing color scheme and preserving all existing functionality.

## Prompt
[Paste your context.md here first, then add:]

New task: Wrap the existing project inside a profile page.

The profile page should:
- Have a header section with: name, one-line bio, and three icon links (GitHub, LinkedIn, Email)
- Display the existing project below the header under a section titled "[Section Title]"
- Use the same color scheme already established in the project
- Keep everything in one index.html file
- Do not change any existing logic — only add the profile wrapper around it

Return the complete updated index.html.

## What to customize
- Name, bio text, and icon link URLs
- Section title ("Mini Game", "Live Demo", "Project Preview", etc.)
- Which project is being wrapped (update the context.md accordingly)

## Expected output
A single index.html file with a profile header above the existing project,
using a consistent color scheme throughout.
```

These two files are now reusable assets. The next time you want to build a game or wrap any project in a profile page, start from the skill instead of from scratch.

---

## Part 4 — AI Agents

### What is an agent?

An AI agent is a system that:
1. Understands a goal
2. Plans the steps to achieve it
3. Uses tools to complete each step
4. Reports back or continues autonomously

The agent loop looks like this:

```
Goal → Plan → Use tool → Check result → Next step → ... → Done
```

### The four components of an agent

| Component | What it does |
|-----------|-------------|
| **Context** | What the agent knows: input, constraints, current state |
| **Skills** | Reusable capabilities it can call on |
| **Tools** | External actions it can take: write files, call APIs, run commands |
| **Agent logic** | Decides which skill or tool to use next and in what order |

### Agents you have already used

Every time you used Claude Code or Cursor's composer mode and it planned the file structure, created multiple files in sequence, or fixed errors automatically — that was agent behavior. You set the goal; the AI acted as the agent.

### The difference between a chatbot and an agent

| Chatbot | Agent |
|---------|-------|
| Responds to one prompt at a time | Chains multiple steps toward a goal |
| Does not use tools | Can write files, call APIs, run commands |
| Forgets state between prompts | Maintains state across a plan |
| You decide what to do next | Agent decides what to do next |

---

### Exercise 3 — Describe the agent version of this lab

Write out what an agent would have done to complete both phases of this lab automatically — as if you were designing the agent:

```
Goal: Build a tic-tac-toe game, then extend it into a profile page.

Step 1: Generate the game
  Skill: tictactoe-game-skill
  Tool: write file → index.html
  Output: working single-file game

Step 2: Summarize and save context
  Tool: write file → context.md
  Output: reloadable project snapshot

Step 3: Extend into profile page
  Skill: profile-wrapper-skill (using context.md as input)
  Tool: write file → index.html (overwrite)
  Output: profile page wrapping the game

Step 4: Verify
  Tool: open index.html in browser
  Output: confirm game works and profile renders correctly
```

This is not code — it is a plan. Writing it out trains you to think in agent terms: what does the agent need to know, what can it reuse, and what does it produce at each step.

---

## Lab Complete

You have:
- Built a tic-tac-toe game using a structured opening context prompt
- Saved the session state as `context.md` and reloaded it in a fresh chat
- Extended the game into a profile page using only the saved context — no re-explanation needed
- Extracted two reusable skills from the work
- Described the equivalent agent workflow

---

## Your project folder should look like this

```
lab06-tictactoe/
├── index.html          ← profile page with tic-tac-toe game embedded
├── context.md          ← saved session state
└── skills/
    ├── tictactoe-game-skill.md
    └── profile-wrapper-skill.md
```

---

## Key takeaways

- **Context is the most important input you give an AI.** A clear opening context with goal, features, and constraints produces dramatically better output than a vague prompt.
- **Context degrades in long sessions.** Save `context.md` at the end of every productive session — reload it when you continue.
- **Skills save time.** A prompt that worked once will work again. Capture it.
- **Agents are context + skills + tools + logic.** Every tool you use — Claude Code, Cursor, Copilot — is some version of this pattern.

---

## Next step

Lab 7 — MCP Integration: Connect Claude Desktop to GitHub and your filesystem.
→ `labs/lab07-mcp-integration/README.md`
