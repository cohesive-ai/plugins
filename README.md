# Cohesive plugins

Plugins that connect AI agents to your [Cohesive](https://cohesive.ai) workspace. One source serves both Claude and ChatGPT / Codex.

| Plugin | What it does |
|---|---|
| [`cohesive`](plugins/cohesive) | Canvases, files, and automations that outlast the chat. Connects the [Cohesive MCP server](https://docs.cohesive.ai/mcp-server). |

## Install

**Claude Code**

```
/plugin marketplace add cohesive-ai/plugins
/plugin install cohesive@cohesive
```

**Codex / ChatGPT**

```
codex plugin marketplace add cohesive-ai/plugins
```

Then install `cohesive` from the plugin directory. You sign in to Cohesive the first time a tool runs; every call runs as you.

## Layout

```
.claude-plugin/marketplace.json        Claude marketplace
.agents/plugins/marketplace.json       Codex / ChatGPT marketplace
plugins/<name>/
  .claude-plugin/plugin.json           Claude manifest
  .codex-plugin/plugin.json            Codex / ChatGPT manifest
  .mcp.json                            MCP servers (shared)
  skills/<skill>/SKILL.md              Skills (shared)
```
