---
name: cohesive
description: Work in a person's Cohesive workspace through the Cohesive MCP tools — build and edit canvases, show a canvas in the conversation, save and read files, and set up automations that run on a schedule. Use when a request names a Cohesive canvas, board, workspace, Library file, or automation, or asks for work to be saved somewhere it outlasts the chat.
---

# Working in Cohesive

Cohesive is where work outlives the chat: a canvas, a file, or an automation stays in the person's workspace after the conversation ends. Every tool call runs as the signed-in person and sees only what they can.

The tool descriptions are the reference for each tool's properties. This skill covers what no single description can: which tools to combine, in what order, and the judgment calls between them. For a tool's full help, call `tool_help` with its name; a family name like `canvas_node_*` lists the tools under it.

## The shape of the platform

An organization holds workspaces. A workspace holds canvases (boards of nodes joined by edges), chats, and a file Library. Every file is a file record parented to exactly one of a workspace, a canvas, or a chat.

Start from what exists. `search` finds anything by name across workspaces, canvases, chats, and files; `workspace_list` and `canvas_list` enumerate. When a request names a workspace or canvas, find its id this way rather than guessing, and when two match, ask which one.

## Show a canvas, or look at it

Two tools render a canvas, for two different readers:

- **`canvas_view` shows it to the person.** Hosts that support apps draw an interactive board in the conversation. Use it whenever the person asks to see, open, or show a canvas, and after building one.
- **`canvas_capture` shows it to you.** It returns an image of the canvas as drawn, so you can check layout, overlaps, and how an edit came out. It takes tens of seconds; use it to verify work, not to present it.

Call `canvas_view` directly, never from inside a code or script tool: a host only draws the board for a direct call.

## Building a canvas

1. **Create or find it.** `canvas_create` makes an empty canvas in a workspace. Use the id it returns for every call that follows.
2. **Pick the right node for each piece of content:**

   | Content | Tool |
   |---|---|
   | A short idea, a list, a takeaway | `canvas_node_add_note` (a titled sticky) |
   | A heading or caption | `canvas_node_add_label` |
   | A long document a person opens and reads | `canvas_node_add_document` (a page card) |
   | A live HTML component drawn in a fixed box | `canvas_node_add_block` (read `references/html-blocks.md` first) |
   | An existing file or a record from another service | `canvas_node_add_entity` |
   | Structure: groups, flow, emphasis | `canvas_node_add_shape`, `canvas_edge_add` |

3. **Lay it out on the 16px lattice.** Keep 16–32px between related nodes and 64px or more between groups, and never overlap. Lay groups out left to right or top to bottom, the order a person reads them.
4. **Check it.** `canvas_capture` the result and fix overlaps or cramped spacing before calling it done.
5. **Show it.** `canvas_view`, so the person sees what was built.

Two rules prevent most bad edits:

- **A node id is the only id that addresses a node**, for updates, moves, deletes, and edge endpoints. For a file the canvas placed, the node id is not the file id. Read node ids from `canvas_view`.
- **Read before you write.** `canvas_view` truncates long text; read a node in full with `canvas_node_get` before editing it.

## Files

`file_upload` takes exactly one source:

- **`content`** for text you wrote: markdown, HTML, CSV, code.
- **`from_url`** for bytes that already live at a public URL, including another service's signed download link. The server fetches and stores them, so they never pass through the conversation.

Never encode file bytes as base64 into a call; there is no property that takes them.

Read inline only what you need to see. `file_read` returns text and small images. For anything larger, binary, or headed somewhere other than your own context, `file_get` returns `download_url`, a signed link to hand to whatever needs the bytes.

## Which URL to give a person

Every canvas and file comes back with URLs the platform built. Use them as returned; never construct or edit one.

- **`dashboard_url`** opens it in the Cohesive app for someone signed in. The link for anything unpublished.
- **`view_url`** is the public page of a published canvas or file. `canvas_publish` or `file_publish` creates it; publish only when the person asks to share publicly.
- **`raw_url`** serves a published file's bytes for fetching or embedding. Never give it to a person: it opens as a bare asset, not a page.

## Automations

An automation is instructions an agent runs later, on a canvas or a workspace. Pick the schedule from what the person said:

- "every Monday at 9", "daily": a recurring `cron`, with the person's time zone in `tz`.
- "tomorrow at 3pm", "on the 1st": a one-off `run_at`.
- "when I ask": neither; it runs only through `automation_run`.

Write the instructions so they stand alone: the agent that runs them later has none of this conversation.

## When a call fails

- **Not found** usually means the id is outside what the person can see. Check the workspace or organization (`server_info` shows which one this connection acts as), not the spelling.
- **Payment required** means the organization's plan does not cover the action. Tell the person; do not retry.
- **Usage** means a property was wrong. Read the tool's full help with `tool_help` and correct the call.
