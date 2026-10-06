# HTML blocks

`canvas_node_add_block` carries the contract: position, `width`/`height`, `chromeless`, `layer`. This file is about making the result look designed rather than merely correct.

A block is one HTML document rendered in a fixed box. It cannot scroll, cannot reach the network, and is re-rendered from scratch whenever its content changes. Everything below follows from those three facts.

## Pick the size first, then design into it

The box is not negotiable at render time, so choose it before writing markup. Dimensions are multiples of 16, and no side is smaller than 128.

| Intent | Starting size |
|---|---|
| Single stat / record card | 320 × 192 |
| Rich record card (status, owner, meta) | 400 × 272 |
| KPI row (3–4 tiles) | 608 × 208 |
| Comparison table | 704 × 400 |
| Dashboard (tiles + chart) | 800 × 608 |
| Section banner | canvas-width × 128 |
| Divider / accent | 608 × 128, chromeless |

A thin divider is still possible despite the 128 minimum: make the block chromeless and draw the rule inside the box; the empty padding is invisible.

Then fill it: `body { margin: 0; overflow: hidden }`, and lay out with flex or grid at percentage or `fr` sizes rather than fixed pixel heights. Overflow is clipped, not scrolled. A block that needs scrolling is the wrong format: raise the height or cut content.

Read `layout-recipes.md` for box-filling layouts and the sizing math for KPI rows and dashboards.

## Use the token vocabulary, never raw colors

The Cohesive design tokens are injected wherever a block renders, matched to the app's theme. A block that hardcodes `#fff` or `black` is right in one theme and broken in the other. Never define the tokens yourself; use the variables.

- **Surfaces and text:** `--n-00` (page), `--n-05` (raised tile), `--n-10` (hairline border), `--n-90` (body text), `--text-muted` (secondary text). The ladder inverts between modes, so a low step against a high step is always readable.
- The steps are exactly `--n-00, --n-05, --n-10, --n-20, --n-30, --n-40, --n-50, --n-60, --n-70, --n-80, --n-90, --n-95`. `--n-02` and the like resolve to nothing.
- **Brand accents:** `--ink`, `--paper`, `--gold`, `--rust`, `--sage`, `--teal`, `--plum`, `--parchment` do not flip between modes. Use them for accents, rules and chart series; never for body text or a page background.
- **Status:** `--lc-active`, `--lc-progress`, `--lc-waiting`, `--lc-warning`, `--lc-blocked`, `--lc-done`, `--lc-neutral`.
- **Type:** `var(--font-sans)` for UI, `var(--font-serif)` for editorial text, `var(--font-mono)` for code and aligned figures.

Read `design-tokens.md` before styling anything.

## Interactivity is opt-in and ephemeral

A person can activate any block, so give one controls only when it is meant to be used (a calculator, a filterable table, tabs), and make read-only content look read-only.

There is no network, no cookies or storage, and state resets when the content or theme changes. Build things that explore what is already in the block; never anything that records input or implies persistence (polls, checklists, trackers, forms that "save"). If the state matters, keep it in a file or canvas nodes and render a display block from it.

Read `interactive-patterns.md` whenever a block has controls.

## Mark what a person should be able to edit

Text a person might reword (titles, summaries, notes, labels) goes in an element with a `data-edit-id`, so they can fix wording in place instead of asking for a regenerated block. Editable regions hold text, not controls; mark scripted elements `data-no-edit`. Use stable, meaningful ids (`title`, `summary`, `q3-note`): the id addresses the saved edit, and renaming it orphans that edit. Don't mark generated figures or anything you will overwrite on the next update.

## Changing a block that exists

Take the smallest change that does the job:

- **Content:** `file_upload` with `overwrite` to the block's file path in the canvas. Read the file first with `file_read`; the person may have edited text in place.
- **Size or position:** `canvas_node_resize` or `canvas_node_move` by node id.
- **`chromeless` or `layer`:** fixed at creation. Re-create the block with the new values, carrying over the person's in-place edits, then delete the old node.

Never re-create a block just to change its content, size, or position: that loses the person's edits.

## Before you ship a block

1. Would it overflow its box? Clipping is silent.
2. Any hardcoded color, or a neutral step not on the ladder?
3. Does anything read-only look clickable, or a control not look like one?
4. If chromeless, does it set `html, body { background: transparent }` and carry its own padding?
5. Does every piece of prose a person might reword carry a `data-edit-id`?

Starting points: `../templates/kpi-row.html` for stat and KPI blocks, `../templates/dashboard.html` for multi-panel blocks.
