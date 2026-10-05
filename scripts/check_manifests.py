#!/usr/bin/env python3
"""Fail when the Claude and Codex manifests for a plugin disagree.

Each plugin ships two manifests (.claude-plugin/ and .codex-plugin/) and is
listed in two marketplaces; nothing else keeps them in step.
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SHARED_FIELDS = ("name", "version", "description", "license")

errors = []


def load(path):
    try:
        return json.loads(path.read_text())
    except FileNotFoundError:
        errors.append(f"{path.relative_to(ROOT)}: missing")
    except json.JSONDecodeError as e:
        errors.append(f"{path.relative_to(ROOT)}: invalid JSON: {e}")
    return None


def entries(marketplace, path_of):
    if marketplace is None:
        return {}
    return {p["name"]: (ROOT / path_of(p)).resolve() for p in marketplace.get("plugins", [])}


claude_market = entries(load(ROOT / ".claude-plugin/marketplace.json"), lambda p: p["source"])
codex_market = entries(load(ROOT / ".agents/plugins/marketplace.json"), lambda p: p["source"]["path"])
on_disk = {d.name: d.resolve() for d in sorted((ROOT / "plugins").iterdir()) if d.is_dir()}

for label, market in (("Claude", claude_market), ("Codex", codex_market)):
    if market.keys() != on_disk.keys():
        errors.append(f"{label} marketplace lists {sorted(market)}, plugins/ has {sorted(on_disk)}")
    for name, path in market.items():
        if on_disk.get(name) not in (None, path):
            errors.append(f"{label} marketplace: {name} points at {path}, not plugins/{name}")

for name, plugin_dir in on_disk.items():
    claude = load(plugin_dir / ".claude-plugin/plugin.json")
    codex = load(plugin_dir / ".codex-plugin/plugin.json")
    if claude is None or codex is None:
        continue
    if claude.get("name") != name:
        errors.append(f"plugins/{name}: manifest name is {claude.get('name')!r}")
    for field in SHARED_FIELDS:
        if claude.get(field) != codex.get(field):
            errors.append(f"plugins/{name}: {field} differs between .claude-plugin and .codex-plugin")

    mcp_path = plugin_dir / ".mcp.json"
    if mcp_path.exists():
        mcp = load(mcp_path)
        for server, cfg in (mcp or {}).get("mcpServers", {}).items():
            if cfg.get("type") != "http" or not cfg.get("url"):
                errors.append(f"plugins/{name}/.mcp.json: {server} needs type http and a url")

for e in errors:
    print(f"error: {e}")
sys.exit(1 if errors else 0)
