---
name: spendly-ui-designer
description: Designs and builds modern, production-ready UI pages and components for Spendly, Ayush's personal expense tracker (Flask + Jinja + vanilla JS, github.com/Ayush-Pal-cs28/spendly). Use this skill whenever the user asks to design, create, build, redesign, restyle, or improve any Spendly page, screen, component, form, table, card, chart area, empty state, or modal, with phrases like "design the dashboard page", "create UI for add expense", "build a component for category totals", "redesign the profile page", or "make this look better". Also use it for any UI request that mentions Spendly, expenses, budgets, spending summaries or the expense tracker, even when the user does not say "design". Produces a short UI structure note plus Jinja templates, a page CSS file and icon macros that match the existing Spendly look.
---

# Spendly UI Designer

Turn a page or component request into clean, responsive, accessible UI that looks
like it was always part of Spendly. The output is a drop-in set of files for a
Flask/Jinja project, not a generic web mockup.

## Why this skill exists

Spendly has a specific look (warm paper background, forest-green accent, serif
headings) and strict project rules (no JS frameworks, no npm, `url_for()` only,
page CSS in its own file). Generic "modern SaaS" output breaks both. The job is
to add polish, hierarchy and usability **inside** that system.

## Step 0: Ground yourself in the real project

Do this before designing, quietly, without narrating it.

1. **If the repo is on disk or you have network access**, look at the live source:
   `static/css/style.css` (tokens and existing classes), `templates/base.html`,
   one or two existing templates, `AGENTS.md`, and `database/db.py` (schema).
   Clone `https://github.com/Ayush-Pal-cs28/spendly` if you can.
2. **Otherwise** read `references/design-system.md` (a snapshot) and design from it.
3. **If neither is possible and the design must match something you cannot see**
   (a page the user built that is not in the snapshot, a custom theme), ask the
   user for screenshots or the relevant CSS. Ask once, briefly, then continue
   with sensible defaults if they would rather not.

If the live CSS disagrees with the snapshot, follow the live CSS and mention the
difference in one line.

## Step 1: Understand the request

Extract:
- **What** is being designed (page or component) and its purpose.
- **Data** available. Use only real fields (`amount, category, date, description`
  on expenses; `name, email` on users). If the design wants data that does not
  exist, say so and either design around it or list it as a follow-up.
- **Constraints or references** the user gave.

Ask a clarifying question only when a wrong guess would waste the whole design
(for example, "profile page" could mean account settings or a spending summary).
Otherwise state your assumption in one line and proceed.

## Step 2: Design

Think in this order: purpose, primary action, information hierarchy, states,
responsive behaviour. Then apply the rules below.

### Look and feel
- Minimal, calm, fintech-clean. Card-based layout. Rounded corners from the
  existing radius tokens. Soft shadows (`--shadow-sm/md/lg`, see the reference).
- Reuse existing tokens and components first (buttons, inputs, cards, banners).
  Never hardcode a colour that already has a token. Never override a token.
- 8px spacing grid using the spacing scale. Clear hierarchy: one primary action
  per view, large figure for the key number, muted labels.
- Subtle colour. Use category colours for meaning, not decoration. Avoid
  gradients, heavy shadows, neon, and mixed random styles.
- Numbers: tabular figures, right-aligned in tables, currency formatted
  consistently (see the reference for the rupee convention).

### Icons
- Use Lucide icons as inline SVG through the `icon()` macro in
  `assets/_icons.html` (copy it to `templates/_icons.html`). No npm, no CDN.
- Pick icons that carry meaning (category, action, trend), not decoration. Pair
  icon-only buttons with `aria-label`.
- If you need an icon not in the macro, add its Lucide path markup to the macro
  dict and tell the user which one you added.

### States (always cover these)
Default, empty, loading or error where relevant, hover/focus, and mobile. An
empty state should say what to do next and offer the primary action.

### Usability
- Forms: visible labels, helpful placeholders, inline error text, sensible
  input types (`type="number" step="0.01"`, `type="date"`), clear primary submit.
- Destructive actions need confirmation and should not be a bare GET link.
- Keep scan paths short: the most important thing top-left or top, secondary
  details quieter.

## Step 3: Respect the project rules

These come from the repo's `AGENTS.md` and are non-negotiable unless the user
explicitly says otherwise:

- Jinja templates must `{% extends "base.html" %}` and fill `{% block content %}`.
- Every internal link and form action uses `url_for()`. Never hardcode URLs.
- Page-specific styles go in a **new** file `static/css/<page>.css`, linked from
  the page's `{% block head %}`. No inline `<style>` blocks and no inline style
  attributes except for truly dynamic values (like a bar width).
- Vanilla JS only, in `static/js/<page>.js` loaded from `{% block scripts %}`,
  and only when interaction genuinely needs it. Prefer CSS and native HTML
  (`<details>`, `<dialog>`, `:target`, form validation) first.
- No React, no jQuery, no npm packages, no new pip packages. Charts are built
  with CSS or inline SVG, not a charting library.
- **UI only.** Do not implement stub routes, DB queries, or `app.py` changes.
  When the design needs data, show the Jinja variables it expects (for example
  `expenses`, `total`, `category_totals`) in a short "Template context" list so
  the backend can supply them. Add placeholder-safe defaults in the template
  (`{{ total|default(0) }}`) so it renders before the backend exists.
- Do not edit `base.html` unless the request is explicitly about the navbar,
  footer or global layout.

## Step 4: Output format

Respond in this order. Keep prose tight.

### 1. UI structure (brief)
- **Layout:** one or two lines on the page skeleton (for example "page header,
  4 stat cards, two-column: recent expenses table + category breakdown").
- **Key sections:** a short list of the main blocks and what each shows.
- **UX decisions:** 3 to 5 bullets on choices that matter and why (hierarchy,
  empty state, mobile behaviour, destructive-action handling).
- **Template context:** the variables the template expects.

### 2. Code
Provide files, each with its path as a heading, in this order:
1. `templates/<page>.html` (extends base, uses macros)
2. `templates/_components.html` or partials, only if there are reusable pieces
   (Jinja `{% macro %}`s such as `stat_card`, `expense_row`, `category_badge`)
3. `static/css/<page>.css` (organised with the same banner-comment style as
   `style.css`; tokens first, then components, then responsive)
4. `static/js/<page>.js` only if needed
5. A note when `templates/_icons.html` must be added or extended

Rules for the code:
- Modular and minimal: no dead CSS, no boilerplate repetition, small macros over
  copy-paste.
- Semantic HTML, BEM-lite class names prefixed by the page or component
  (`.exp-table`, `.stat-card`) so styles do not leak across pages.
- Sample data: when the backend is not ready, include a clearly marked
  `{# sample data #}` block at the top of the template that can be deleted, so
  the user can preview the page. Never leave fake data mixed into the markup.
- When delivering as files (more than about 20 lines of code), create actual
  files and present them. Short snippets can stay inline.

### 3. Close
End with one or two lines: how to wire it up (the route should
`render_template("<page>.html", ...)`), and any follow-ups (missing data,
missing route, currency filter). Do not restate the design.

## Redesign / improve requests

When asked to redesign or improve an existing page, read the current template
and CSS first. Keep the content and behaviour, change structure, hierarchy,
spacing, and polish. Briefly list what changed and why (3 to 6 bullets), then
give the full replacement files. Do **not** introduce a new palette, font or
visual direction unless the user explicitly asks for a visual refresh. If they
do, confirm the direction in one line, then change tokens in one place.

## Verify before replying (when you have a shell)

If you can run code, render the template before handing it over; it catches
most bugs. Copy the repo (or the files into a scratch copy), import `app` and
call `render_template(...)` inside `app.test_request_context()` with realistic
context **and** with empty context. If a headless browser is available
(Playwright Chromium), screenshot at 1280px and 390px and check that there is
no horizontal scroll and nothing breaks. Fix what you see, then reply. Never
claim you tested something you did not. If no shell is available, say the
design is untested.

## Known pitfalls (learned from real test runs)

- **Never put `display: flex` or `grid` on a `<td>` or `<tr>` in the base
  (desktop) rules.** It breaks row borders and column alignment. Put the
  flex container in a `<div>` inside the cell. The only exception is the
  stacked mobile layout under 600px, where cells intentionally become blocks.
- **Specificity in responsive overrides.** A rule like `.exp-table td {...}`
  beats `.exp-actions-cell {...}`. Write overrides as `.exp-table td.exp-actions-cell`
  or restructure so the override is not needed.
- **Mobile stat cards:** four full-width cards make a long scroll. Use a 2x2
  grid with tighter padding under 600px and hide decorative icon tiles.
- **Table to card on mobile:** hide `<thead>`, make rows blocks, and give each
  `<td>` a `data-label` that shows via `::before`. Icon-only action cells need
  44px targets and right alignment.
- **Dynamic widths** (progress bars) are the one place an inline `style` is
  acceptable; everything else lives in the CSS file.

## Quality checklist (run silently before replying)

- Matches existing tokens, radii and fonts; no stray hex colours except the
  documented category and shadow additions.
- Spacing follows the 8px scale; one clear primary action per view.
- Works at 1200px, 900px and 600px; no horizontal page scroll; touch targets
  at least 44px on mobile.
- Contrast at least 4.5:1 for meaningful text; icon-only buttons labelled;
  visible focus states; semantic elements.
- Every state covered (empty, error, hover, focus, mobile).
- Extends `base.html`, uses `url_for()`, no inline `<style>`, no frameworks,
  no backend changes.
- Jinja renders without error with the documented context (and with empty data).

## Avoid

- Generic or dated UI: default-Bootstrap look, heavy gradients, drop-shadow
  stacks, emoji as icons, mixed icon styles.
- Unstructured code dumps: one giant file, repeated markup instead of macros,
  CSS without sections.
- Inventing data fields, routes or libraries the project does not have.
- Long design essays. The structure note should be scannable in seconds.

## Bundled resources

- `references/design-system.md`: token snapshot, category colour/icon map,
  component inventory, spacing, data and copy conventions, responsive and
  accessibility rules. Read it in Step 0 when the live repo is unavailable, and
  whenever you need a convention (currency, dates, categories).
- `assets/example-profile/`: a finished, tested Profile page (template,
  `_components.html` macros, CSS, JS) rendered against the real Spendly
  `base.html`. Treat it as the quality and style bar: read it before building
  a data-heavy page (dashboard, expense list, summary) and reuse its macros
  (`money`, `short_date`, `category_badge`, `stat_card`, `empty_state`) instead
  of rewriting them. It is an example of structure and polish, not a template
  to copy blindly.
- `assets/_icons.html`: Jinja `icon()` macro with 41 Lucide icons (navigation,
  actions, trends, the seven expense categories). Copy into `templates/`.
