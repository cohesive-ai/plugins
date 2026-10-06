# Design tokens for canvas blocks

The Cohesive tokens are baked into every block at create time, carrying both light and dark values; the correct set is selected automatically from the app's theme. You never write a dark-mode variant, never need a media query, and never write the token definitions yourself.

The single rule that prevents most visual bugs: **style with tokens, not literal colors.** A hardcoded `#fff` or `black` is correct in exactly one theme.

## The neutral ladder

`--n-00 --n-05 --n-10 --n-20 --n-30 --n-40 --n-50 --n-60 --n-70 --n-80 --n-90 --n-95`

Those are the only steps. `--n-02`, `--n-15` and similar do not exist; a `var()` on them resolves to nothing and the property is simply dropped.

The ladder is **relative, not absolute** — it inverts between modes. `--n-00` is the page surface in both themes (near-white in light, near-black in dark), and `--n-90`/`--n-95` are the strongest text in both. So a low step against a high step is readable either way, and you can reason purely in terms of distance:

| Role | Token |
|---|---|
| Page / block background | `--n-00` |
| Raised tile, table header, well | `--n-05` |
| Hairline border, divider | `--n-10` |
| Heavier border, disabled text | `--n-20` – `--n-30` |
| Secondary text | `--text-muted` |
| Body text | `--n-90` |
| Headline / maximum contrast | `--n-95` |

`--text-muted` already resolves to the right mid-step per mode; prefer it over picking `--n-50` yourself.

## Brand accents — fixed, do not flip

`--ink --paper --gold --rust --sage --teal --plum --parchment`

These are fixed brand colors with the same value in both themes. They are accents: rules, keylines, chart series, a tinted panel, an emphasized figure.

Using them as body text or a page background is the most common way to ship a block that looks fine while you build it and is unreadable for anyone on the other theme — `--ink` is near-black in *both* modes, so `--ink` on a dark background disappears. Reach for the neutral ladder for anything text-on-surface.

## Status colors

`--lc-progress` (blue) `--lc-active` (green) `--lc-waiting` (amber) `--lc-warning` (orange) `--lc-blocked` (red) `--lc-done` (purple) `--lc-neutral`

Use these for state — pipeline stages, health, pass/fail, ticket status — rather than arbitrary greens and reds, so status reads consistently across every block on the canvas.

Pair with a shape or label as well as color: a red dot alone is invisible to a colorblind reader.

## Categorical colors for charts

Each spectrum hue exists in three weights: `--spectrum-{hue}`, `--spectrum-{hue}-light`, `--spectrum-{hue}-dark`.

Hues: `blue indigo violet mulberry red orange yellow olive green brown`

For a categorical series, walk hues rather than weights — adjacent weights of one hue are hard to tell apart at small sizes. A dependable order that stays distinguishable:

```
--spectrum-blue, --spectrum-orange, --spectrum-green, --spectrum-mulberry,
--spectrum-yellow, --spectrum-indigo, --spectrum-brown, --spectrum-red
```

Beyond about eight categories, stop coloring and group the tail into "Other" — more hues stop being distinguishable, especially at chart scale.

## Sticky-note palette

`--sticky-apricot --sticky-butter --sticky-clay --sticky-meadow --sticky-mist --sticky-oat --sticky-orchid --sticky-rose --sticky-sea`, with `--sticky-foreground` for text on any of them.

These are the canvas's own note colors. Use them when a block should feel like part of the canvas furniture — callouts, pinned annotations, legend swatches that match nearby notes. Always put `--sticky-foreground` on top of them; the neutral ladder is not tuned for these backgrounds.

## Typography

`var(--font-sans)` — UI, labels, most body text.
`var(--font-serif)` — editorial passages, pull quotes, anything that should read as written rather than displayed.
`var(--font-mono)` — code, IDs, and figures in a column you want optically aligned.

Set a family explicitly on `body`; do not assume an inherited default.

## Elevation and rules

`--elev-0` … `--elev-5` are ready-made shadow values, and `--hairline` is the standard 1px rule color.

Blocks sit on a canvas that already has depth, so stay low: `--elev-1` for a raised tile, `--elev-2` for something genuinely floating. Heavy shadows read as clutter next to real canvas cards.

## Quick self-check

- Any literal hex, `white`, `black`, or `rgb()` in the document? Replace it.
- Any neutral step that is not on the ladder above?
- Is a brand accent doing the job of text-on-surface?
- Does every status color also carry a label or shape?
