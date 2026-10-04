---
title: "The ChatGPT Web App Controls My Mac: MCP Setup"
date: 2026-10-04
tags: ChatGPT, MCP, Model Context Protocol, ChatGPT local computer control, ChatGPT local files, ChatGPT terminal, ChatGPT MCP server, Cloudflare Tunnel, Quick Tunnel, cokacremote, AI coding
permalink: /en-chatgpt-mcp-local-development-setup/
layout: default
lang: en
alternate_lang: ko
alternate_url: /chatgpt-mcp-local-development-setup/
description: "The ChatGPT web app controls my local Mac through MCP: it can read and edit files, run terminal commands, use Git, run tests and automate the browser."
excerpt: "Not an API model or a separate CLI coding agent: the browser-based ChatGPT web app itself works on the real files, terminal and Git repositories on my Mac through MCP."
seo:
  title: "ChatGPT Web App Controls Mac Files & Terminal via MCP"
  description: "The ChatGPT web app uses MCP to read and edit local Mac files, run terminal commands, Git, tests and browser automation."
  keywords:
    - ChatGPT MCP
    - ChatGPT web app MCP
    - ChatGPT on the web MCP
    - ChatGPT MCP server
    - ChatGPT local computer
    - ChatGPT local files
    - ChatGPT terminal access
    - ChatGPT control Mac
    - ChatGPT MCP local development
    - MCP Cloudflare Tunnel
    - ChatGPT local coding agent
faq:
  - q: "Can the ChatGPT web app read and edit files directly on my local Mac?"
    a: "Yes, if you expose those capabilities through an authenticated MCP server. ChatGPT on the web does not simply connect to localhost, so the setup needs a reachable remote MCP endpoint or supported secure tunnel. In this setup, cokacremote exposes the local tools and Cloudflare Tunnel plus OAuth provides the connection."
  - q: "Can ChatGPT run terminal commands, Git and tests through MCP?"
    a: "Yes, when the MCP server exposes those tools and the connection is allowed to use them. This setup can execute shell commands, modify files, inspect Git, run builds and tests, and use browser automation on the local Mac."
  - q: "Is a Cloudflare Quick Tunnel enough to make a powerful MCP server safe?"
    a: "No. A tunnel provides connectivity, not authorization. A write-capable MCP server needs authentication and permission controls; this setup explicitly verifies that unauthenticated requests to /mcp are rejected."
image: /en-chatgpt-mcp-local-development-setup/mcp-local-development-og.png
image_width: 1200
image_height: 630
---

# The ChatGPT Web App Controls My Mac

**MCP access to local files, terminal, Git and browser automation**

<p style="background: rgba(0, 120, 212, 0.08); border-left: 4px solid #0078d4; padding: 10px 14px; margin-bottom: 22px; border-radius: 4px; font-size: 0.95rem;">
  🌐 <strong>한국어 버전:</strong> <a href="/chatgpt-mcp-local-development-setup/">웹 ChatGPT로 Mac 제어</a>
</p>

This is **not about using an OpenAI model in the abstract, nor a separate local coding agent such as Codex CLI**. The subject here is the **ChatGPT web app running in my browser**.

From a normal ChatGPT conversation, I can point at a project and use the connected MCP to read the real directory on my Mac, run terminal commands, edit files, execute tests, and inspect the Git diff.

Previously I would check `git status`, copy the relevant code into ChatGPT, paste the answer back into the repository, and then run the tests myself. A new chat also meant explaining the project state again.

Now the ChatGPT web app can work against **the current local project instead of a pasted snapshot**. This post itself was written while ChatGPT inspected and edited the local Jekyll repository through that connection.

<img src="architecture.svg" alt="Architecture connecting ChatGPT through a Cloudflare Quick Tunnel and MCP to cokacremote on a local Mac" width="1200" height="700" style="width:100%;height:auto;">

## Connecting the ChatGPT web app to my local Mac with MCP

The core is a [Model Context Protocol (MCP)](https://modelcontextprotocol.io/) server. Mine is based on [cokacremote](https://github.com/kstost/cokacremote), running locally on my Mac.

At a high level:

```text
ChatGPT
   ↓  MCP over HTTPS + OAuth
Cloudflare Quick Tunnel
   ↓
cokacremote (localhost)
   ↓
my Mac
 ├─ filesystem
 ├─ shell
 ├─ Git
 ├─ builds and tests
 ├─ browser automation
 └─ project context
```

OpenAI's current developer documentation supports connecting an HTTPS `/mcp` endpoint from ChatGPT developer mode. For development, Cloudflare Quick Tunnels can give a local HTTP service a temporary public `trycloudflare.com` URL without first setting up a permanent domain.

One point matters more than the convenience: **the tunnel is not the security boundary.** My MCP server can execute commands and modify or delete files with the permissions of the local process. I therefore run it behind OAuth and make the setup script explicitly verify that an unauthenticated `/mcp` request gets `401`.

## What changes when the ChatGPT web app can use local files and the terminal

My original goal was basically "remote shell access from ChatGPT." In practice, the useful part isn't the shell by itself.

I can start a conversation with something like:

> This directory is the project. Inspect the current state before changing anything.

From there, the conversation can drive the full loop.

<img src="project-workflow.svg" alt="Workflow where ChatGPT bootstraps project context, checks Git and code, edits, verifies, and checkpoints the result" width="1200" height="690" style="width:100%;height:auto;">

Instead of me manually doing `git status → find docs → inspect code → edit → test → review diff`, ChatGPT can perform those steps against the repository that actually exists on disk.

That distinction matters. The model is no longer reasoning only from a pasted snapshot. If another session changed the code, or I edited something manually, the next session can re-read the current Git and filesystem state before making decisions.

## I automated the Quick Tunnel setup too

Initially I started the MCP server, launched `cloudflared`, copied the newly generated URL, adjusted OAuth-related settings, and reconnected ChatGPT by hand.

That got old quickly.

I now use a `setup-oauth-quicktunnel.sh` script that handles most of the boring parts.

The current version roughly does this:

1. Locate and validate the real cokacremote checkout
2. Inspect the currently running local service
3. Build it if required
4. Start a Quick Tunnel pointing at `127.0.0.1:3000`
5. Extract the generated public URL
6. Prepare OAuth state and key material
7. Start the MCP server with the public URL
8. Verify local `/health`
9. Verify public `/health`
10. Verify OAuth discovery metadata
11. **Verify that unauthenticated `/mcp` returns `401`**
12. Print the MCP URL to enter in ChatGPT
13. Clean up only the processes the script itself owns when it exits

I don't want a real tunnel hostname or approval key in a public screenshot, so the following image is a **redacted reconstruction of the verified output flow**, not a screenshot containing my live credentials.

<img src="setup-terminal-redacted.svg" alt="Sanitized terminal output for the Cloudflare Quick Tunnel and OAuth MCP setup script" width="1200" height="720" style="width:100%;height:auto;">

A Quick Tunnel hostname is temporary and can change when the process restarts. That's fine for how I currently use this on my own development machine. If I needed a stable long-lived endpoint, I would use a named Cloudflare Tunnel or another permanent HTTPS deployment instead.

## The next problem: new chats still forget project history

Giving ChatGPT filesystem access solves only part of the problem.

It can see the current code, but it does not automatically know **why a decision was made, which approach was rejected, what a previous session finished, or which constraints are still active**.

So I added a lightweight project-context layer.

The authority order I use is roughly:

```text
current executable code / Git state
        ↓
current-state docs / checkpoint
        ↓
accepted architecture and decisions
        ↓
older project memory
        ↓
old conversation memory
```

The key rule is that old memory never gets to override the repository.

At a project or session boundary I run a fast bootstrap that reads the current Git state and the small amount of current project context needed to resume work. Meaningful decisions and material changes are checkpointed back into the repository. Deeper historical recall is optional instead of being loaded on every prompt.

I'm still testing this part. **A feature working is not the same thing as proving that it reduces total token or time cost**, so I'm deliberately not claiming that the context layer is already an optimal solution.

## What changed in day-to-day use

Before:

```text
Here is the file...
Here is the error...
Another model changed this...
Don't touch these parts...
This is what I tried...
```

Now:

```text
Inspect this project and verify its current state first.
```

That doesn't make the model infallible. In fact, because the model has real host access, I need stricter operating rules than I did when it was only returning code snippets.

The rules that matter most in my setup are:

- inspect current Git and code before making changes;
- current executable state outranks old memory;
- reuse existing implementations instead of creating duplicate helpers;
- run the real build/tests after changes;
- checkpoint meaningful implementation or architecture decisions;
- never expose write-capable MCP tools anonymously on a public endpoint.

With those rules in place, ChatGPT feels less like a code-generation window and more like a **control surface for the development environment that already exists on my machine**.

## Why I am not publishing every line of the setup here

I intentionally left out some details.

The full `setup-oauth-quicktunnel.sh`, the complete OAuth approval configuration, the tunnel URL retry logic, and the exact project-checkpoint format would make this post much longer. More importantly, this MCP server has powerful host permissions. I don't want a partial copy-paste recipe to encourage someone to expose an unrestricted local command server carelessly.

The architecture and security boundary are not hidden, though.

If you're building something similar, leave a comment with the specific part you want to see. Useful topics would be:

- the ChatGPT MCP registration flow;
- OAuth 2.1 / DCR configuration;
- extracting and retrying Quick Tunnel URLs;
- process ownership and cleanup in the setup shell script;
- restoring project context across new chats;
- combining Git, tests and browser automation in one workflow;
- keeping a local MCP service running on macOS.

If I can share the relevant part safely, I'll post the actual configuration or a reduced code sample in the comments. If the same question keeps coming up, I'll move it into this article or make it a follow-up post.

## FAQ

### Can the ChatGPT web app read and edit files directly on my local Mac?

Yes, if those capabilities are exposed through an authenticated MCP server. ChatGPT on the web does not simply connect to your machine's localhost; the setup needs a reachable remote MCP endpoint or a supported secure tunnel. In my setup, **cokacremote exposes the local tools and Cloudflare Tunnel plus OAuth provides the connection**.

### Can ChatGPT run terminal commands, Git and tests through MCP?

Yes. In this setup, file operations, shell execution, Git inspection, builds, tests and browser automation are exposed as MCP tools. ChatGPT is not merely suggesting a terminal command: **it can invoke the tool on the local Mac and read the result back into the conversation**.

### Is a Cloudflare Quick Tunnel enough to secure this?

No. A tunnel provides connectivity, not authorization. A write-capable MCP server needs authentication and careful permission handling. My setup therefore checks the public health and OAuth metadata and also verifies that an unauthenticated request to /mcp is rejected with 401.

## References

- [OpenAI Plugins Quickstart — connect an MCP server](https://developers.openai.com/plugins/quickstart)
- [OpenAI — MCP server authentication](https://developers.openai.com/plugins/build/auth)
- [Cloudflare Docs — Quick Tunnels](https://developers.cloudflare.com/tunnel/get-started/quick-tunnels/)
- [Model Context Protocol](https://modelcontextprotocol.io/)

My current takeaway is simple: **for serious development work, giving ChatGPT a properly authenticated MCP interface to the real environment feels much more natural than continuously copying snapshots of that environment into the chat.** Once you do that, though, permissions and state verification become first-class engineering problems.
