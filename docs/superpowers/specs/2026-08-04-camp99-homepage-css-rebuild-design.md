# Camp 99 Homepage Rebuild: Vanilla HTML/CSS/JS (Elementor/Astra removal)

## Purpose

Replace the Elementor/Astra-generated markup, CSS, and JS dependencies on the homepage
(`index.html`) with hand-authored semantic HTML, a single custom stylesheet, and a small
vanilla JS file. Visual output should match the current live page as closely as possible
(pixel-close, not a redesign). This is the pilot page; once approved and verified, the same
approach rolls out to the other 30 pages.

## Scope

**In scope**: `index.html` markup, a new `styles/main.css`, a new `scripts/main.js`.

**Out of scope / unchanged**: GTM injection logic, Cloudflare beacon, webfonts (Racing Sans
One, Open Sans Condensed, Montserrat, Font Awesome, Astra icon font), all image assets,
`_headers`, YouTube video iframe embed, Google Maps iframe embed, the CSP/COOP/HSTS headers.
The old Elementor/Astra CSS/JS files (`common-head.css`, `vf6z_*.css`, `post-*.css`,
`swiper.min.js`, `style.min.js`, `core.min.js`, etc.) stay on disk untouched — the other 30
pages still depend on them until they get the same treatment in a future pass.

## Known bugs to fix as part of this rebuild

- Nav dropdown arrows are not visibly rendering on the current live site.
- The YouTube video embed is not displaying/loading on the current live site — root cause
  to be diagnosed during implementation (dead iframe src, blocked by CSP, or a layout issue
  hiding it).

## File structure

```
index.html          (rewritten)
styles/main.css      (new)
scripts/main.js       (new)
```

## Header & navigation

Semantic `<header>` containing the logo and a `<nav>`. The current menu has three levels of
nesting (e.g. "DigitalMission Media" → "Still Photography" → "Media Training Sessions").

- **Desktop**: JS-driven `mouseenter`/`mouseleave` with a short close-delay (not pure CSS
  `:hover`) — matches the pattern already proven to avoid the dropdown hover-gap bug
  documented elsewhere in this workspace. Each item with children shows a visible
  down-arrow/caret indicator.
- **Mobile**: hamburger toggle reveals the menu; tapping an item with children expands its
  submenu in place (replaces the current `tns-mobile-dropdown-tap` inline script).

## Homepage sections

Mapped from the current page, top to bottom. Each becomes a plain semantic block with its
own descriptive CSS class name (no `elementor-element-<hash>` naming anywhere).

1. **Hero** — `<h1>CAMP 99</h1>` + subtitle heading + background image
   (`camp99asia-camp99-asia-facility-212*.webp`, existing responsive srcset).
2. **About** ("/ 01") — heading + "Purpose of Camp 99" + body copy + facility-210/202 images.
3. **Services** ("/ 02") — "Serving the 99" intro + 4 cards (Events / Meetings / Fishing /
   Sports), each with icon + heading + body text.
4. **Come On Out!** ("/ 03") — image carousel (facility-225/228/230/232, gallery-223, etc.)
   + "We're just 8km..." blurb. Includes fixing the YouTube embed (see bugs above).
5. **Location** ("/ 04") — Google Map iframe + address/contact block.
6. **Footer** — contact info, social icons (with the `transition:color` fix already applied
   upstream in the shared CSS — not relevant to this rebuild since footer gets its own CSS),
   nav links, copyright.

## CSS approach

Single file, mobile-first. Breakpoints match what's already established in the current
theme CSS: 480px / 544px / 768px / 1024px / 1180px, so responsive behavior doesn't shift.
CSS custom properties for the existing color palette (`#c580c9` accent, `#59d600` hover,
`#dd3333` buttons, black background) and spacing scale already in use on the live page.
Flexbox for the nav and card rows; CSS Grid for the services/carousel sections.

## JS approach

Three small, independent modules in `scripts/main.js`:

1. **Nav** — dropdown hover/close-delay (desktop) + tap-to-expand (mobile).
2. **Carousel** — CSS `scroll-snap` strip with two button handlers (prev/next); no Swiper
   dependency needed for a simple image strip.
3. **Scroll-to-top** — shows/hides a button based on scroll position, animates scroll on
   click. Replaces the current jQuery-based `hfe-scroll-to-top` behavior.

No jQuery, no jQuery UI, no Swiper on this page after the rebuild.

## Testing / verification

- Serve locally and visually compare against the current live homepage at each breakpoint
  (480/544/768/1024/1180/desktop-wide).
- Confirm nav dropdowns work (hover + click-outside-to-close on desktop, tap-to-expand on
  mobile) and arrows render.
- Confirm carousel scrolls/advances correctly on both mouse and touch.
- Confirm YouTube video and Google Map both render and are interactive.
- Confirm scroll-to-top button appears/disappears and scrolls smoothly.
- Re-run a Lighthouse/PageSpeed pass to confirm no regression versus the current ~90
  performance / 100 accessibility / 96 best-practices / 100 SEO baseline.
- Validate HTML parses cleanly (existing `HTMLParser` smoke test used throughout this
  project's other fixes).
