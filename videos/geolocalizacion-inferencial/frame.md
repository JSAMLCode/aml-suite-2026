---
version: alpha
name: Deep Navy Consulting Cinematic — Frame (video / frame layer)
description: >
  Cinematic consulting-briefing look. Deep navy canvas (#051C2C) with a soft radial vignette, white
  action-title headlines (full-sentence claims), electric cyan-blue (#2FB8FF) as the data accent and
  #2251FF as the fill color for exhibits. Space Grotesk (titles, numerals, chrome) + Inter (body).
  Thin hairline rules, glass cards, grid and dot-matrix textures, slow camera pushes and parallax.
  Every content frame carries a source footnote. Motion is part of the system.
unit: the frame — 1920×1080 primary; 9:16 and 1:1 documented
principle: atoms are sacred · composition is free · numbers come from the script

colors:
  bg: "#051C2C"
  surface: "#0B2A44"
  primary: "#2FB8FF"
  secondary: "#2251FF"
  text: "#FFFFFF"
  text-muted: "#A9BCCC"
  text-light: "#6F8799"
  accent-light: "rgba(47,184,255,0.10)"
  accent-medium: "rgba(47,184,255,0.18)"
  border: "rgba(169,188,204,0.22)"
  card-bg: "rgba(255,255,255,0.04)"
  positive: "#2ED8A3"
  negative: "#FF5C6C"

radii:
  pill: "100px"
  card-lg: "14px"
  card-md: "12px"
  card-sm: "10px"
  bar: "6px"
  circle: "50%"

typography:
  # — reading ramp (Inter body + Space Grotesk chrome) —
  body:    { fontFamily: "Inter", cqw: 0.85, weight: 400, lineHeight: 1.6, color: "text-muted" }
  h4-eyebrow:{ fontFamily: "Space Grotesk", cqw: 0.8, weight: 600, tracking: "0.08em", upper: true, color: "primary" }
  tag:     { fontFamily: "Space Grotesk", px: 12, weight: 500, color: "primary" }
  counter: { fontFamily: "Space Grotesk", px: 13, weight: 500, tracking: "0.05em", color: "text-muted" }
  # — display / numerical ramp (Space Grotesk, near-black headings / cobalt numerals) —
  h3:      { fontFamily: "Space Grotesk", cqw: 1.25, weight: 500, lineHeight: 1.3, tracking: "-0.02em", color: "text" }
  stat-num:{ fontFamily: "Space Grotesk", cqw: 1.9, weight: 700, lineHeight: 1.0, color: "primary" }
  blockquote:{ fontFamily: "Space Grotesk", cqw: 2.4, weight: 500, lineHeight: 1.35, color: "text" }
  h2:      { fontFamily: "Space Grotesk", cqw: 2.6, weight: 600, lineHeight: 1.1, tracking: "-0.02em", color: "text" }
  metric-value:{ fontFamily: "Space Grotesk", cqw: 3.0, weight: 700, lineHeight: 1.0, color: "primary" }
  h1:      { fontFamily: "Space Grotesk", cqw: 4.2, weight: 700, lineHeight: 1.08, tracking: "-0.02em", color: "text" }
  quote-mark:{ fontFamily: "Space Grotesk", cqw: 8.0, weight: 700, lineHeight: 0.5, color: "primary", opacity: 0.15 }

spacing:
  pad-x: "5cqw"
  pad-y-top: "5cqw"
  gap-cards: "1.4cqw"
  accent-line: "60px × 4px"

components:
  card-tinted:
    backgroundColor: "{colors.card-bg}"
    border: "1.5px solid {colors.border}"
    rounded: "{radii.card-lg}"
    shadow: "none"
    description: "Universal content card. Never solid-colored, never opaque-bordered, NO shadow."
  metric-card:
    backgroundColor: "{colors.card-bg}"
    border: "1.5px solid {colors.border}"
    rounded: "{radii.card-lg}"
    typography: "{typography.metric-value} ({colors.primary}) + {typography.metric-label} + {typography.metric-desc}"
    description: "+ optional inline ↑/↓ change chip ({colors.positive}/{colors.negative} text, no fill)."
  tag-pill:
    backgroundColor: "{colors.accent-light}"
    textColor: "{colors.primary}"
    rounded: "{radii.pill}"
    typography: "{typography.tag}"
    description: "Top-right of the slide-header."
  cta-button:
    backgroundColor: "{colors.primary}"
    textColor: "{colors.bg}"
    rounded: "{radii.pill}"
    typography: "Space Grotesk 600"
    shadow: "soft cobalt on hover only — the system's only shadow"
    description: "The one solid element."
  accent-line:
    backgroundColor: "{colors.primary}"
    size: "60×4, 2px radius"
    description: "Above cover titles / eyebrow separators."
  bar-track:
    backgroundColor: "{colors.accent-light}"
    fill: "{colors.primary} (display:block so width resolves)"
    rounded: "{radii.bar}"
    description: "28px track; fill carries the value."
  step-circle:
    backgroundColor: "{colors.primary}"
    textColor: "{colors.bg}"
    rounded: "50%"
    size: "56px"
    description: "Sequential steps fade opacity 1.0→0.85→0.7→0.55."
  split-highlight:
    backgroundColor: "{colors.accent-light}"
    borderLeft: "4px solid {colors.primary}"
    rounded: "{radii.card-md}"
    description: "Inline pull-quote callout."
  slide-header:
    typography: "{typography.h4-eyebrow} (cobalt) left, tag-pill right; {typography.h2} below"
    description: "Top band of every content frame."
  atmosphere:
    elements: "clipped diagonal cobalt-tint panel, 3×3 cobalt dot grid, concentric closing rings"
    description: "Cover/closing only. Never on content frames."
  progress-bar:
    backgroundColor: "{colors.primary}"
    size: "3px tall, bottom edge, width grows with index"
    description: "Persistent progress strip."
---

# Deep Navy Consulting Cinematic — Frame

## Overview

A **boardroom-briefing look with a film-grade finish**. The ground is deep navy with a soft radial
vignette and a faint grid / dot-matrix texture, so every frame has depth before anything appears.
Headlines are **action titles** — a complete sentence that states the conclusion, not a topic label —
set in white Space Grotesk. Data is the hero: large cyan numerals, thin-line exhibits, hairline rules,
glass cards. The one gesture that makes it cinematic is **camera behavior**: slow pushes, parallax
layers, light sweeps and focus pulls rather than slide-to-slide cuts.

## The Frame

- **Format:** 1080×1080 (1:1) for this project; authored in `cqw` against a `container-type: size` ground.
- **Safe area:** `pad-x` 6cqw; top band reserved for eyebrow + tag; bottom 9cqw reserved for the source footnote + progress hairline; captions (when on) sit in the lower band above the footnote.
- **Container law:** every frame ground sets `container-type: size`; all frame-relative units are `cqw`/`cqh`.

## Colors

`bg` navy is the universal ground, lifted by a radial gradient (`#0B2A44` → `#051C2C` → `#030F18` at the corners) — the vignette. `primary` cyan (#2FB8FF) is the **data/accent** color: numerals, eyebrows, active nodes, highlights. `secondary` electric blue (#2251FF) is the **fill** color for bars, areas and glow behind primary elements. Text is white; muted `#A9BCCC`; tertiary `#6F8799`. Cards are glass: 4% white fill, 1px hairline border at 22% muted. `positive`/`negative` appear only as semantic state (match / stop), never as decoration.

## Typography

- **Space Grotesk** — action titles (white, 600, −0.02em, line 1.12), numerals (cyan, 700), eyebrows (cyan, uppercase, 0.08em, 600), chrome.
- **Inter** — body, labels, footnotes (muted, 400, line 1.55).
- Action title ≤ 3 lines, ≤ 84cqw measure, 6–8cqw. Hero numerals up to 28cqw. Any load-bearing line ≥ 3.2cqw on the 1:1 canvas (≈ 1.4cqw at 16:9 scale).

## Depth & Surface

- **Vignette + grid:** a 4cqw hairline grid at 4% white, masked to fade toward the edges.
- **Glass cards:** 4% white fill, 1px hairline border, 2cqw radius, `backdrop-filter` is not allowed (render-unsafe) — fake with a gradient fill.
- **Glow:** a blurred `secondary` radial behind the focal element (opacity ≤ 0.45). One glow per frame.
- **Light sweep:** a diagonal 8% white gradient band that crosses a card or title once.
- No hard drop shadows.

## Components

- **action-title:** white Space Grotesk claim sentence, one cyan keyword allowed.
- **eyebrow + tag:** cyan uppercase eyebrow (left), hairline-outlined pill tag (right).
- **exhibit-label:** small caps "EXHIBIT N" style label above a chart/diagram with a thin cyan rule.
- **source-footnote:** bottom-left, Inter 3cqw muted: "Fuente: …"; every content frame has one.
- **so-what callout:** glass card with a 0.6cqw cyan left rule and one conclusion sentence.
- **progress hairline:** 0.4cqw cyan line at the bottom edge, width grows with frame index.
- **node / link:** circle (cyan fill when active, hairline when idle) joined by 1px lines that draw on.

## Frame Treatments

1. **Cinematic cover** — giant numerals on the vignette, slow push-in, radar rings.
2. **Toggle / state flip** — a switch or label changes state; before → after.
3. **Map exhibit** — dot-matrix map or abstract plane, probability halos, no precise pins.
4. **Hub-and-spoke exhibit** — a core node with grouped satellite nodes that link in.
5. **Decision-flow exhibit** — boxes and diamonds connected by drawn lines, with pass/stop outcomes.
6. **Gantt / timeline exhibit** — workstream bars against a deadline line.
7. **Spotlight question** — two options, one beam of light, large question title.
8. **Source card** — footnote-style closing with firm signature.

## Composition Rules

### Do
- Lead every content frame with an action title; support it with one exhibit.
- Use cyan only for what matters most on the frame; blue glow behind it.
- Keep generous negative space; one dominant focal at 3–6× its neighbors.
- Animate with camera logic: push-in, parallax, drawn lines, count-ups, sweeps.

### Don't
- No stock imagery, no 3D gradients blobs, no emoji, no clip-art icons.
- No invented figures: numerals come from the script (30·06·2027, 9 months, 8 signals, 14, 53, 4 tasks).
- No drop shadows; no `backdrop-filter`; no second accent beyond cyan + electric blue.
- No more than one glow and one light sweep per frame.

## Numerals & Claims (hard rule)

Every figure on screen traces to the script. Illustrative schematics (e.g. the workplan bars) carry the label "Esquema ilustrativo". Do not show percentages, dates or counts that the narration does not state.

## Pre-Render Self-Audit

- Squint: one white action title or one cyan numeral dominates.
- Exhibit: one clear diagram per content frame; no decoration without meaning.
- Source: footnote present on frames 2–7.
- Depth: vignette + grid visible; one glow; no shadows.
- Type: Space Grotesk titles, Inter body; floors respected.
