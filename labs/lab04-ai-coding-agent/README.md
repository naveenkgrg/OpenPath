# Lab 4: AI Coding Agents and Build with AI

**Prerequisites:** Basic GitHub and VS Code familiarity. Lab 1 is helpful but not required.
**Estimated time:** 45–60 minutes
**What you will have at the end:** A working simple project created with AI help, a prompt workflow, and a better understanding of how to use coding agents safely.

---

## Overview

This lab shows you how to use AI coding agents to build a small web project.

You will:
- install or access an AI tool
- choose a simple project idea
- write a clear prompt
- generate code
- test and refine the result

AI is a helper, not a replacement. Your job is to guide it, verify the output, and make the final project your own.

---

## What is a Coding Agent?

A coding agent is an AI-powered assistant that helps write, debug, and improve code.
It turns your natural language prompt into working code and acts like a pair programmer.

Common examples:
- GitHub Copilot inside VS Code
- Cursor IDE
- ChatGPT in the browser
- Claude in the browser

---

## Step 1 — Install or access your AI tool

Choose one tool and make sure it is ready.

### GitHub Copilot (recommended for VS Code)
1. Install [VS Code](https://code.visualstudio.com/).
2. Open Extensions and search for `GitHub Copilot`.
3. Install the extension.
4. Sign in with GitHub and enable Copilot.

### Cursor IDE
1. Go to https://cursor.sh.
2. Download the app.
3. Install and sign in.

### ChatGPT / Claude
- Open the service in your browser.
- Send your prompt in the chat.
- Copy the generated code into your editor.

> If you do not have paid access, use the free tier and keep prompts smaller.

---

## Step 2 — Choose a simple project idea

Pick one of these starter projects:
- Static HTML page — profile, about page, or landing page
- Simple game — tic-tac-toe, number guess, or memory game
- Live wallpaper — animated background with CSS motion
- Calendar page — month grid with a highlighted day

Choose the easiest idea you can finish in one session.

---

## Step 3 — Write a clear prompt

A good prompt is specific and describes what you want.

### Example prompts
- `Create a simple HTML page with a profile card, responsive layout, and a blue gradient background.`
- `Create a basic tic-tac-toe game using HTML, CSS, and JavaScript that works in the browser.`
- `Create an animated background wallpaper using CSS and JavaScript with circles moving across the page.`

### Static app sample prompt
Use this prompt to build a simple demo page:

`Create a static HTML/CSS landing page with a modern profile section, a hero header, a responsive card layout, a placeholder profile image, name, short bio, three social link buttons, and a footer.`

### Wallpaper demo prompt
Try this for a simple animation page:

`Create a static HTML page with a full-screen animated background using CSS. Add a centered title and subtitle on top of the moving gradient background.`

### Prompt best practices
- Start simple.
- Describe exactly what you want.
- Name the files you expect: `index.html`, `styles.css`, `script.js`.
- Ask for a complete example.

---

## Step 4 — Generate the code

Use your AI tool to create the project.

- In VS Code with Copilot, type a prompt comment such as:

```html
<!-- Create a simple HTML project with a responsive profile card and styled buttons -->
```

- In ChatGPT or Claude, paste your prompt and ask for the complete code.

Create or update these files:
- `index.html`
- `styles.css`
- `script.js`

Copy the code into your editor and save each file.

---

## Step 5 — Test locally

Open `index.html` in your browser.

If something does not work:
- Check the browser console for errors.
- Ask the AI to fix the exact error message.
- Change one thing at a time.

Example refinements:
- `The page is not centered. Please update the CSS to center the profile card.`
- `The tic-tac-toe game does not register clicks. Fix the JavaScript so clicks update the board.`

---

## Step 6 — Practice project options

Choose one option and use the prompt below.

### Option 1 — Static profile page
`Create a simple HTML page with a profile card. Use CSS for a responsive layout, a profile image placeholder, name, bio, and social links.`

### Option 2 — Tic-tac-toe game
`Create a basic tic-tac-toe game using HTML, CSS, and JavaScript. The game should let two players click squares, show the current player, and highlight the winner.`

### Option 3 — Animated wallpaper
`Create an animated wallpaper using HTML, CSS, and JavaScript. Use moving shapes or gradients that change over time.`

### Option 4 — Calendar page
`Create a basic calendar page using HTML and CSS. Show a month grid and highlight the current day.`

---

## Step 7 — Review the generated code

AI can help write code, but you must understand it.
- Read the HTML, CSS, and JavaScript.
- Confirm the page matches your idea.
- Remove any extra code or features you did not ask for.
- Simplify the result where possible.

---

## Step 8 — Commit your work

If you do not have a repository yet, create one on GitHub first (see Lab 2), clone it locally, then run the commands below inside that repo's directory.

Create a branch, stage your files, and push:

```bash
git checkout -b ai-agent-lab
git add index.html styles.css script.js
git commit -m "Add AI-generated web project"
git push origin ai-agent-lab
```

Then open a pull request on GitHub to merge `ai-agent-lab` into `main`.

---

## Key takeaways
- AI coding agents can speed up code creation.
- Clear prompts and frequent testing are the most important skills.
- Always read and verify generated code.
- Use AI as a helper, not a replacement for your understanding.

---

## Resources
- [GitHub Copilot](https://github.com/features/copilot)
- [Cursor](https://cursor.sh)
- [ChatGPT](https://chat.openai.com)
- [Claude](https://www.anthropic.com)

---

**Next step:** Lab 5 — Static and Interactive Web Demos: `labs/lab05-static-pages/README.md`

