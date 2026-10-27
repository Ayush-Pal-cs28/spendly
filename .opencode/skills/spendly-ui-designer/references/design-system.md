# Spendly design system (snapshot)

Snapshot of `static/css/style.css` as of Oct 2026. **If the repo or `style.css` is
available, trust it over this file** and note any differences to the user.
If neither is available, use this file and say so in one line.

## Contents
1. Character of the design
2. Tokens that already exist
3. Tokens to add (shadows, spacing, category colours)
4. Existing components to reuse
5. Spacing and layout rules
6. Data and copy conventions
7. Responsive rules
8. Accessibility baseline

---

## 1. Character of the design

Warm, editorial, calm. Off-white "paper" background, near-black "ink", a deep
forest-green accent and a small amber secondary. Headlines use a serif
(DM Serif Display); everything else uses DM Sans. Cards are white with a hairline
border. The look is closer to a well-set financial journal than to a neon
fintech app, so avoid saturated blues/purples, gradients, glassmorphism and
heavy drop shadows.

"Modern SaaS / fintech" for Spendly means: generous whitespace, clear hierarchy,
tabular numbers, restrained colour, soft elevation.

## 2. Tokens that already exist (`:root`)

```css
--ink: #0f0f0f;          --ink-soft: #2d2d2d;
--ink-muted: #6b6b6b;    --ink-faint: #a0a0a0;
--paper: #f7f6f3;        --paper-warm: #f0ede6;   --paper-card: #ffffff;
--accent: #1a472a;       --accent-light: #e8f0eb;
--accent-2: #c17f24;     --accent-2-light: #fdf3e3;
--danger: #c0392b;       --danger-light: #fdecea;
--border: #e4e1da;       --border-soft: #eeebe4;
--font-display: 'DM Serif Display', Georgia, serif;
--font-body: 'DM Sans', system-ui, sans-serif;
--max-width: 1200px;     --auth-width: 440px;
--radius-sm: 6px;  --radius-md: 12px;  --radius-lg: 20px;
```

Never hardcode a colour that has a token. Never redefine these.

## 3. Tokens to add

The current UI is flat (borders only). Soft shadows and category colours are
new, so add them **once** in a `:root` block at the top of the page CSS file
(or, if the user agrees, to `style.css`). Do not duplicate them across files.

```css
:root {
    /* elevation: subtle, warm-tinted so it suits the paper background */
    --shadow-sm: 0 1px 2px rgba(15, 15, 15, 0.04);
    --shadow-md: 0 2px 8px rgba(15, 15, 15, 0.06), 0 1px 2px rgba(15, 15, 15, 0.04);
    --shadow-lg: 0 12px 32px rgba(15, 15, 15, 0.10);

    /* spacing scale (8px grid, 4px half-step) */
    --space-1: 0.25rem;  --space-2: 0.5rem;  --space-3: 1rem;
    --space-4: 1.5rem;   --space-5: 2rem;    --space-6: 3rem;

    /* category colours: muted, each paired with a light tint */
    --cat-food: #c17f24;           --cat-food-bg: #fdf3e3;
    --cat-transport: #2f6f8f;      --cat-transport-bg: #e6f0f5;
    --cat-bills: #6b5b95;          --cat-bills-bg: #eeeaf5;
    --cat-health: #b5483d;         --cat-health-bg: #fbece9;
    --cat-entertainment: #a8527a;  --cat-entertainment-bg: #f7e9f0;
    --cat-shopping: #1a472a;       --cat-shopping-bg: #e8f0eb;
    --cat-other: #6b6b6b;          --cat-other-bg: #efede8;
}
```

If page CSS is added, prefix the new variables' usage by class, not by
overriding existing tokens.

### Category map

| Category (exact DB string) | Icon (Lucide) | Colour token |
|---|---|---|
| Food | `utensils` | `--cat-food` |
| Transport | `car` | `--cat-transport` |
| Bills | `receipt` | `--cat-bills` |
| Health | `heart-pulse` | `--cat-health` |
| Entertainment | `clapperboard` | `--cat-entertainment` |
| Shopping | `shopping-bag` | `--cat-shopping` |
| Other | `ellipsis` | `--cat-other` |

Category strings are case-sensitive and come from the `expenses.category`
column. In Jinja, map them with a dict, not a long if/elif chain:

```jinja
{% set cat_icons = {'Food': 'utensils', 'Transport': 'car', 'Bills': 'receipt',
   'Health': 'heart-pulse', 'Entertainment': 'clapperboard',
   'Shopping': 'shopping-bag', 'Other': 'ellipsis'} %}
{{ icon(cat_icons.get(expense.category, 'ellipsis')) }}
```

For the CSS class use `cat-{{ expense.category|lower }}`.

## 4. Existing components to reuse (do not re-invent)

| Need | Reuse | Notes |
|---|---|---|
| Primary button | `.btn-primary` | ink background, green on hover |
| Secondary button | `.btn-ghost` | bordered, transparent |
| Full-width form submit | `.btn-submit` | |
| Text input | `.form-input` inside `.form-group` | label above, 0.85rem |
| Card | `.auth-card` pattern: white, 1px `--border`, `--radius-md`, 2rem padding | For new cards, create a `.card` class with the same recipe plus `--shadow-sm` |
| Error / success banner | `.auth-error` / `.auth-success` | flashed messages already use them in `base.html` |
| Page container | `max-width: var(--max-width); margin: 0 auto; padding: 0 2rem;` | |
| Section heading | `font-family: var(--font-display)` | |

The navbar, footer and flash handling live in `base.html`. Do not rebuild them
inside a page template.

## 5. Spacing and layout rules

- 8px grid: use multiples of `0.5rem` (half-steps of `0.25rem` allowed for tight icon gaps).
- Card padding `1.5rem` (compact) or `2rem` (default). Gap between cards `1rem` to `1.5rem`.
- Page top padding about `2rem` to `3rem`; section gap `2rem` to `3rem`.
- Radius: `--radius-sm` for inputs/buttons/badges, `--radius-md` for cards, `--radius-lg` for large panels and modals.
- Hairline borders (`1px solid var(--border)`) stay on cards even when a shadow is added.
- Page titles: `--font-display`, about `2rem`. Card titles: `--font-body` 600, about `1rem`. Labels: `0.75rem` to `0.85rem`, `--ink-muted`, optionally uppercase with `letter-spacing: 0.04em`.

## 6. Data and copy conventions

- **Currency:** the product voice is rupee-based ("Track every rupee"). Format money as `₹1,234.50` and wrap amounts in an element with `font-variant-numeric: tabular-nums`. Do not hardcode a symbol in many places; use a Jinja filter or macro (e.g. `{{ amount|inr }}`) and tell the user if the filter does not exist yet. Seed data currently has plain decimals, so flag the currency question once if it matters to the design.
- **Dates:** stored as ISO `YYYY-MM-DD` text. Display as `12 Oct 2026` (or `12 Oct` inside the current year).
- **Expense fields:** `id, user_id, amount (REAL), category, date, description (nullable), created_at`. Never invent columns. If a design needs data that does not exist (tags, payment method, notes, budgets), say so and design with what exists, or list the missing field as a follow-up.
- **Empty descriptions:** show a muted fallback (the category name), not a blank.
- **Tone:** plain, friendly, short. Empty states say what to do next ("No expenses yet. Add your first one.").
- **Negative vs positive:** spending is the default, so do not paint every amount red. Use colour only for meaning (over budget, error, delta direction).

## 7. Responsive rules

The existing breakpoints are `900px` (collapse grids to one column) and `600px`
(hide secondary nav links, reduce padding). Reuse them. Design mobile-first
inside each component:

- Card grids: `repeat(auto-fit, minmax(240px, 1fr))` or an explicit 3 → 2 → 1 collapse.
- Tables become stacked card rows under `600px`; never allow horizontal page scroll.
- Tap targets at least `44px` tall on touch layouts.

## 8. Accessibility baseline

- Text contrast at least 4.5:1. `--ink-faint` (#a0a0a0) fails on white, so use it only for placeholders and decorative text, never for meaningful content.
- Icon-only buttons need `aria-label` (and `title` if useful). Decorative icons are already `aria-hidden` through the icon macro.
- Visible `:focus-visible` outline using `--accent`; do not remove outlines.
- Real elements: `<button>` for actions, `<a>` for navigation, `<label for>` for inputs, `<table>` with `<th scope>` for tabular data.
- Destructive actions (delete) need a confirmation step. The delete route is currently a GET stub, so recommend a POST form plus a confirm dialog when you design it.
- Respect `prefers-reduced-motion` for any animation.
