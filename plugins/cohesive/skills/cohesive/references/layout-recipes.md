# Layout recipes for a fixed box

A block renders in exactly the width and height you asked for. There is no scrollbar and no reflow to a taller page — content that does not fit is clipped, silently. So the job is always the same: pick the box, then build a layout that *fills* it at any content length.

## The base every block starts from

```html
<style>
  html, body { height: 100%; }
  body {
    margin: 0;
    overflow: hidden;              /* clipping is the contract, make it explicit */
    font-family: var(--font-sans);
    background: var(--n-00);
    color: var(--n-90);
    display: flex;
    flex-direction: column;
    padding: 20px;
    box-sizing: border-box;
  }
</style>
```

`box-sizing: border-box` on the padded root is what keeps padding from pushing content out of the box — without it, a 600×400 block with 20px padding needs 640×440 to display.

## Fill the height with fractions, not pixels

Fixed pixel heights never add up to the box across two themes and three content lengths. Give the structural rows their natural size and let one region absorb the remainder:

```css
.header { flex: none; }            /* takes what it needs */
.body   { flex: 1; min-height: 0; } /* absorbs everything left over */
.footer { flex: none; }
```

`min-height: 0` is required on the flexible child. Without it a flex item refuses to shrink below its content size, and a long table pushes the footer out of the box instead of being clipped inside its own region.

## Grids that stay even

For a KPI row or tile grid, let the grid do the arithmetic:

```css
.grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 16px;
  flex: 1;
  min-height: 0;
}
```

`1fr` columns with a `gap` divide the remaining width correctly at any block size — which means the same markup survives a later resize through `canvas_node_resize` without you touching it.

## Sizing math

Work backwards from the content, then round each dimension up to a multiple of 16 (no side smaller than 128).

**KPI row.** Tile ≈ 175px wide reads comfortably. For _n_ tiles with 16px gaps and 20px padding: `width ≈ n×175 + (n−1)×16 + 40`. Three tiles → 597 → **608**. Four → 788 → **800**. Height 208 fits a label plus a large figure; 272 if each tile also carries a sublabel or trend.

**Table.** Header plus 20px padding takes ~90px; each row is ~36px. Ten rows → `90 + 360 = 450` → **464**. Do not plan for more than about a dozen rows in a block — past that it wants to be a document, not a canvas surface.

**Dashboard.** Give the chart region at least 250px of height or it stops being readable. A tile row plus a chart plus a footer lands naturally at **800 × 608**.

**Banner.** Height 128 (the minimum) for a title alone, 160 with a subtitle. Match the width to the span of the content it heads. For anything visually thinner than 128 — a divider, an accent rule — keep the 128-tall box but make the block chromeless and draw the thin visual inside it; the empty padding is invisible.

## Text that will not fit

Long strings are the usual cause of a clipped block. Decide per element how it degrades, rather than hoping:

```css
.truncate {                  /* one line, ellipsis */
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}
.clamp-2 {                   /* two lines, then ellipsis */
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
```

Titles and labels truncate to one line; descriptions clamp to two or three. Figures never truncate — shrink the label instead.

## Charts without a library

Blocks cannot load external scripts, so charts are hand-built. Inline SVG with a `viewBox` scales to whatever box it is given and needs no JavaScript:

```html
<svg viewBox="0 0 100 40" preserveAspectRatio="none" style="width:100%;height:100%">
  <polyline points="0,30 20,22 40,25 60,12 80,16 100,4"
            fill="none" stroke="var(--spectrum-blue)" stroke-width="2"
            vector-effect="non-scaling-stroke" />
</svg>
```

`vector-effect="non-scaling-stroke"` keeps the line an even weight after the viewBox stretches; without it a wide chart draws a visibly tapered stroke.

Bar charts are simpler as flex columns with percentage heights than as SVG. Sparklines, donuts and progress arcs are all comfortable in SVG.

## Chromeless blocks

`chromeless: true` drops the card chrome and background so the document composites directly onto the canvas — right for banners, headers, dividers and decorative art. It requires the document to say so itself:

```css
html, body { background: transparent; }
```

Without that rule the block still paints its own background and chromeless has no visible effect. Pair it with `layer: "back"` on `canvas_node_add_block` for anything meant to sit behind other nodes.

A chromeless block has no card padding — the node edge IS the document edge. Text and controls set flush against it read as clipped next to framed neighbours, so give the document its own inner padding (at least 16px on every side, 24px reads better for headings) unless the design is deliberately edge-to-edge (a backdrop, a divider rule, hero art). Never rely on the canvas to inset your content.

## Before you finish

Read the layout back at the size you actually requested, not the size you imagined. The failure to look for is a region that grows with content — a table body, a long title, a list — that has no `min-height: 0` ancestor and therefore pushes its siblings out of the box.
