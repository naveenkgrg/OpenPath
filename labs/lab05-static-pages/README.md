# Lab 05: Static and Interactive Web Demos with a Coding Agent

**Prerequisites:** Basic HTML/CSS familiarity or completion of Lab 4.
**Estimated time:** 30–45 minutes
**What you will have at the end:** A self-contained AI coding lab with three demo options: a profile page, a tic-tac-toe game, and an animated wallpaper.

---

## Overview

This lab shows how to use a coding agent to build small static web projects quickly.

You will:
- choose one of three demo options
- write a clear prompt for the agent
- generate code
- review the result
- preview the page in a browser

This is a coding agent lab: use tools like GitHub Copilot, Cursor, ChatGPT, Codex-based assistants, or Claude.

---

## Step 1 — Choose your demo option

Pick one of these projects:

1. **Profile page** — A responsive static profile card with inline CSS.
2. **Tic-tac-toe game** — A 3×3 browser game with two-player interaction.
3. **Animated wallpaper** — A full-screen animation with a centered title.

> The same lab workflow works for all three. Start with one and reuse the prompts for future practice.

---

## Step 2 — Use the best-fit prompt

Choose the prompt that matches your demo.

### Option 1 — Static profile page
`Create a responsive static profile page in index.html with inline CSS. Center a profile card with name, bio, LinkedIn, GitHub, email. Clean modern design, works on mobile.`

### Option 2 — Tic-tac-toe game
`Create a tic-tac-toe game in index.html with inline CSS and JavaScript. Use a 3x3 board, let two players click squares, show the current player, and highlight the winning line.`

### Option 3 — Animated wallpaper
`Create an animated wallpaper in index.html with inline CSS and JavaScript. Use a full-screen animated background and a centered title and subtitle on top.`

### How to use the prompt

- In VS Code with an AI extension, paste the prompt into the editor or chat window.
- In a browser chat tool, send the prompt and ask for the complete `index.html` content.
- Ask the agent to include all HTML, CSS, and JavaScript in one file if you want a single-file demo.

### Using Codex-based tools

1. Open your Codex-powered editor or OpenAI playground.
2. Paste the selected prompt and ask for a complete `index.html` file.
3. If the tool returns only code blocks, copy the full HTML output.
4. Save it as `labs/lab05-static-pages/index.html`.
5. Open the file in a browser and verify the page.

### Using Claude

1. Open Claude in your browser.
2. Paste the selected prompt into the chat.
3. Ask Claude to respond with the complete `index.html` file only.
4. Copy the generated HTML output and save it as `labs/lab05-static-pages/index.html`.
5. Preview the page in your browser and refine the prompt if needed.

---

## Step 3 — Review and refine the output

After the agent generates the page:

- Confirm the layout matches the chosen demo.
- Check for a centered card or board, depending on the option.
- Test mobile responsiveness.
- Remove any extra content you did not ask for.

Ask the agent to fix issues with a specific request, for example:

- `Center the profile card and improve spacing for mobile.`
- `Fix the tic-tac-toe JavaScript so clicking a square updates the board.`
- `Make the animated background smoother and keep the title centered.`

---

## Step 4 — Preview the page

Open `labs/lab05-static-pages/index.html` in a browser.

If the page does not display correctly:

- Check that the HTML has opening and closing tags.
- Make sure CSS is inside a `<style>` block.
- Ensure JavaScript is inside a `<script>` block if the demo uses it.
- Save and refresh the browser.

---

## Prompt examples for reuse

- Static profile page: `Create a responsive static profile page in index.html with inline CSS. Center a profile card with name, bio, LinkedIn, GitHub, email. Clean modern design, works on mobile.`
- Tic-tac-toe game: `Create a tic-tac-toe game in index.html with inline CSS and JavaScript. Use a 3x3 board, let two players click squares, show the current player, and highlight the winning line.`
- Animated wallpaper: `Create an animated wallpaper in index.html with inline CSS and JavaScript. Use a full-screen animated background and a centered title and subtitle on top.`

---

## What you learned

- How to write effective prompts for AI coding agents
- How to generate static web projects using AI
- How to review and refine generated HTML, CSS, and JavaScript
- How to preview and test browser demos locally

---

**Next step:** Lab 6 — AI Key Concepts (Context, Skills, Agents): `labs/lab06-prompt-context/README.md`
