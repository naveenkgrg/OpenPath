# Lab 7: MCP Integration — Connect Claude Desktop to GitHub and Your Filesystem

**Prerequisites:** Lab 6 complete. Claude Desktop installed. Docker Desktop installed and running.
**Estimated time:** 45–60 minutes
**What you will have at the end:** Claude Desktop connected to your local filesystem and GitHub via MCP, with Claude able to list repos, read files, and interact with your machine directly.

---

## Overview

MCP (Model Context Protocol) is an open standard created by Anthropic. It connects AI models to external tools, APIs, and data sources in a structured, predictable way.

Without MCP, Claude works only inside the chat window — it can generate text and code but cannot read your files, interact with your GitHub account, or call live APIs.

With MCP, Claude can:
- Read and write files on your local machine
- List, search, and interact with your GitHub repositories
- Query live data from any connected source
- Take actions across tools using one consistent protocol

This lab sets up two MCP servers using Docker: **GitHub** (access to your repos) and **Filesystem** (access to your local files).

---

## Background: How MCP Works

MCP uses a client-server architecture:

```
Claude Desktop (client)
        ↓
MCP Server — runs as a Docker container
        ↓
External tool (GitHub API, local filesystem, etc.)
```

Each MCP server is a Docker container that exposes a set of tools Claude can call. Claude Desktop reads a config file (`claude_desktop_config.json`) on startup and launches each configured container.

The key constraint: **Claude Desktop must be fully quit and relaunched** for any config change to take effect.

---

## Step 1 — Verify Prerequisites

**Docker Desktop:**

```bash
docker --version
docker ps
```

Both should succeed with no errors. If Docker is not installed, download it from https://www.docker.com/products/docker-desktop, install it, and start the app before continuing.

**Claude Desktop:**

Download and install from https://claude.ai/download if you have not already.

**GitHub Personal Access Token (PAT):**

You need a GitHub token so the MCP server can authenticate with GitHub on your behalf.

1. Go to https://github.com/settings/tokens
2. Click **Generate new token → Generate new token (classic)**
3. Name it `mcp-claude-desktop`
4. Set expiration to 90 days
5. Under **Scopes**, check **repo** (full repository access)
6. Click **Generate token**
7. Copy the token immediately — GitHub will not show it again

---

## Step 2 — Pull the MCP Docker Images

Pull both images before configuring Claude Desktop. This avoids connection timeouts on the first launch.

```bash
docker pull ghcr.io/github/github-mcp-server
docker pull mcp/filesystem
```

Verify both downloaded successfully:

```bash
docker images | grep -E "github-mcp-server|filesystem"
```

You should see both images listed with a recent timestamp.

---

## Step 3 — Test the GitHub MCP Container Manually

Before touching Claude's config, confirm the container runs correctly in your terminal:

```bash
docker run -i --rm \
  -e GITHUB_PERSONAL_ACCESS_TOKEN=your_token_here \
  ghcr.io/github/github-mcp-server
```

Replace `your_token_here` with your actual token.

Expected output (the process starts and waits):

```
GitHub MCP Server running on stdio
```

Press `Ctrl+C` to stop it. If you see this output, the container is working correctly.

---

## Step 4 — Edit the Claude Desktop Config File

The config file location depends on your operating system:

- **macOS:** `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows:** `%APPDATA%\Claude\claude_desktop_config.json`
- **Linux:** `~/.config/Claude/claude_desktop_config.json`

Open the file in any text editor. If it does not exist, create it.

Replace the contents with the following — substituting the two values marked with `<angle brackets>`:

```json
{
  "mcpServers": {
    "github": {
      "command": "docker",
      "args": [
        "run",
        "-i",
        "--rm",
        "-e",
        "GITHUB_PERSONAL_ACCESS_TOKEN",
        "ghcr.io/github/github-mcp-server"
      ],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "<YOUR-GITHUB-TOKEN>"
      }
    },
    "filesystem": {
      "command": "docker",
      "args": [
        "run",
        "-i",
        "--rm",
        "--mount",
        "type=bind,src=<ABSOLUTE-PATH-TO-YOUR-DIRECTORY>,dst=/projects",
        "mcp/filesystem",
        "/projects"
      ]
    }
  }
}
```

**Substitution guide:**

| Placeholder | Replace with |
|-------------|-------------|
| `<YOUR-GITHUB-TOKEN>` | The token you created in Step 1, e.g. `ghp_xxxxxxxxxxxxxxxxxxxx` |
| `<ABSOLUTE-PATH-TO-YOUR-DIRECTORY>` | The full path to a directory on your machine you want Claude to access, e.g. `/Users/yourname/Projects` |

**Example completed config (macOS):**

```json
{
  "mcpServers": {
    "github": {
      "command": "docker",
      "args": [
        "run",
        "-i",
        "--rm",
        "-e",
        "GITHUB_PERSONAL_ACCESS_TOKEN",
        "ghcr.io/github/github-mcp-server"
      ],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "ghp_xxxxxxxxxxxxxxxxxxxx"
      }
    },
    "filesystem": {
      "command": "docker",
      "args": [
        "run",
        "-i",
        "--rm",
        "--mount",
        "type=bind,src=/Users/yourname/Projects,dst=/projects",
        "mcp/filesystem",
        "/projects"
      ]
    }
  }
}
```

Save the file.

---

## Step 5 — Fully Quit and Relaunch Claude Desktop

Claude loads the MCP config only on startup. Closing the window is not enough — you must fully quit the app.

- **macOS:** Press `Cmd+Q`, or right-click the Claude icon in the Dock → **Quit**
- **Windows:** Right-click the Claude icon in the system tray → **Quit**
- **Linux:** Use the application menu to quit, or kill the process

Then reopen Claude Desktop.

---

## Step 6 — Verify the MCP Connections

After Claude Desktop reopens:

1. Click the **Settings** icon (gear icon, top right)
2. Go to **Developer → MCP Servers**
3. You should see `github` and `filesystem` listed
4. Each should show a **green** status indicator — this means the container started and connected successfully

If a server shows red or an error, check the **Logs** section next to it. Common causes:

| Problem | Likely cause |
|---------|-------------|
| `docker: command not found` | Docker Desktop is not running — start it and relaunch Claude |
| `unauthorized` or `bad credentials` | GitHub token is wrong, expired, or missing the `repo` scope |
| `bind mount failed` | The filesystem path in your config does not exist — create it or correct the path |
| Config change not reflected | You did not fully quit Claude Desktop — `Cmd+Q` and relaunch |

---

## Step 7 — Run the Hands-On Exercises

With both servers connected, try these prompts in Claude Desktop:

**GitHub exercises:**

```
List all my GitHub repositories.
```

```
What are the most recently updated repositories in my GitHub account?
```

```
Search my GitHub repositories for anything related to Python.
```

**Filesystem exercises:**

```
List the files in my projects directory.
```

```
Read the README.md in my OpenPath project.
```

**Combined exercise:**

```
Look at the files in my local OpenPath directory, then tell me 
which labs exist and what each one covers based on the README files.
```

---

## Step 8 — Understand What Just Happened

When Claude responds to those prompts using real data, it is not guessing — it is calling tools through MCP:

1. You type a prompt in Claude Desktop
2. Claude identifies it needs a tool (e.g. `list_repos` from the GitHub server)
3. Claude sends a structured request to the running Docker container
4. The container calls the real GitHub API with your token
5. The response comes back to Claude as structured JSON
6. Claude uses that data to formulate its answer

This is the same architecture used in production AI applications. Understanding it gives you a foundation for building your own MCP-connected tools.

---

## Going Further — Add More MCP Servers

Any MCP server published as a Docker image can be added to your config using the same `docker run` pattern. Some useful ones:

| Server | Image | What it does |
|--------|-------|-------------|
| PostgreSQL | `mcp/postgres` | Query a Postgres database |
| Brave Search | `mcp/brave-search` | Web search from Claude |
| Slack | Available via third-party | Read and send Slack messages |

Full list of official MCP servers: https://github.com/modelcontextprotocol/servers

---

## Lab Complete

You have:
- Understood the MCP client-server architecture
- Set up the GitHub and Filesystem MCP servers using Docker
- Verified live connections to both servers
- Run real queries against your GitHub account and local files through Claude

---

## Next step

Lab 8 — End-to-End MVP Delivery: from idea to deployed app.
→ `labs/lab08-mvp-delivery/README.md`
