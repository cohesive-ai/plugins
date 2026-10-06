# Interactive blocks

Every block is *activatable*: a user clicks into it to hand the pointer to the content, and buttons and inline scripts work until they press Esc or click away. There is no flag to set — it applies to every block, for everyone who can see the canvas, including viewers of a published canvas.

## When to set it

Set it when the block is meant to be **used**: a calculator, a filterable or sortable table, a tabbed view, a before/after slider.

Leave it off when the block is meant to be **read**. An activatable block asks the user to double-click before they can pan or drag over it, so switching it on for a static scorecard costs canvas ergonomics and buys nothing.

## What you can rely on

Inline `<script>` runs, and normal DOM APIs work. That is enough for anything self-contained.

What is **not** available, and why it shapes the design:

- **No network.** No `fetch`, no CDN scripts, no external stylesheets, no remote images. Everything ships in the document. Charts are hand-built SVG (see `layout-recipes.md`); embed images from a file record's `public_url`.
- **No persistence.** No cookies, no `localStorage`. Nothing the user does survives a reload.
- **State resets** whenever the block's content changes or the user flips the app theme.

The design consequence is the important part: interaction is for **exploring what is already in the block**, never for recording input. No polls or vote tallies, no toggle checklists, no counters or trackers, no forms that "save" — a checklist that quietly forgets its ticks is worse than no checklist. If the state matters beyond the moment, the answer is a real file record or canvas nodes, not a block.

## Patterns that work

**Filter or sort a table.** Ship the full dataset in the markup and show or hide rows. The data is already there, so filtering is instant and needs no network.

```html
<input id="q" placeholder="Filter…" />
<script>
  document.getElementById('q').addEventListener('input', function (e) {
    var q = e.target.value.toLowerCase();
    document.querySelectorAll('tbody tr').forEach(function (tr) {
      tr.style.display = tr.textContent.toLowerCase().includes(q) ? '' : 'none';
    });
  });
</script>
```

**Tabs / segmented views.** Several panels, one visible. A good way to fit three views into one box instead of asking for three blocks.

**Calculator or estimator.** Inputs plus a formula, recomputing on `input`. Give every field a sensible default so the block reads as complete before anyone touches it.

## Keeping the block usable

- **Make affordances obvious — and honest.** Buttons should look like buttons and cursors should change; a user who cannot see what is interactive will not click to find out. The canvas reads `cursor: pointer` as "this is a control" and hands such elements the pointer directly, so paint it only on things that respond to a click — never on wrappers, cards, or whole sections, which would swallow canvas gestures over them.
- **Give feedback on every action.** No network means no spinners — a click either changes something visible immediately or appears broken.
- **Size for the box.** Interactive controls add height. A block that fits while static can clip its own button row once you add one.
- **Keep controls out of editable regions.** Anything with a `data-edit-id` becomes contenteditable during an edit session; buttons inside it stop behaving like buttons. Put controls outside those elements, or mark them `data-no-edit`.
- **Links open in a new tab** and only `https:` URLs are honored. Do not build navigation that assumes the block itself can change page.
- **Guard against double-initialization.** Content updates re-run scripts, so make setup idempotent:

```html
<script>
  (function () {
    if (window.__blockInit) return;
    window.__blockInit = true;
    /* wire up listeners here */
  })();
</script>
```

## Turning interactivity on or off later

Since every block is activatable, the only decision is what the block *offers*: controls for content meant to be used, none for content meant to be read. Changing that is a content edit — `file_upload` with `overwrite` on the same path — not a presentation change.
