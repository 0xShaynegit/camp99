# Camp 99 Homepage Rebuild (Elementor/Astra removal) Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace `index.html`'s Elementor/Astra-generated markup, CSS, and JS dependencies (jQuery, jQuery UI, Swiper) with hand-authored semantic HTML, one stylesheet (`styles/main.css`), and one vanilla JS file (`scripts/main.js`), matching the current live design pixel-close.

**Architecture:** Six section-scoped tasks (hero, about, services, carousel, location, footer) each add their markup + CSS incrementally to files that grow across tasks, plus a nav task and a final swap-and-verify task. Content copy is never re-typed from memory — every task that needs body text extracts it verbatim from a preserved backup of the current file.

**Tech Stack:** Plain HTML5, CSS3 (custom properties, Flexbox, Grid, `scroll-snap`), vanilla JS (no frameworks/libraries). Python 3 (already used throughout this repo) for verification scripts.

## Global Constraints

- Visual output must match the current live page as closely as possible (pixel-close, not a redesign) — per approved spec `docs/superpowers/specs/2026-08-04-camp99-homepage-css-rebuild-design.md`.
- No jQuery, jQuery UI, or Swiper on the rebuilt page.
- Breakpoints match the current theme CSS exactly: 480px, 544px, 768px, 1024px, 1180px.
- Color palette: `#c580c9` (links/accent), `#59d600` (hover), `#dd3333` (buttons/CTAs), `#000000` (background), `#ffffff` (text).
- Heading font sizes (desktop → 768px → 544px): h1 86px→70px→40px, h2 84px→68px→39px, h3 28px→25px→20px.
- GTM injection logic, Cloudflare beacon script, webfonts, `_headers`, image assets, YouTube iframe, Google Maps iframe stay untouched — do not modify anything outside `index.html`, `styles/main.css`, `scripts/main.js`.
- Old Elementor/Astra CSS/JS files (`css/common-head.css`, `css/vf6z_*.css`, `css/post-*.css`, `scripts/swiper.min_bb874a.js`, `scripts/style.min_0fd1dd.js`, `scripts/core.min_2dceab.js`, `scripts/vf6z_b8499e.js`, `scripts/vf6z_99c698.js`) must NOT be deleted — the other 30 pages still depend on them.
- Every task ends with: (1) the HTML parses cleanly via the existing `HTMLParser` smoke test pattern, (2) a manual visual check in a local browser at each breakpoint.

---

## Task 0: Preserve current content as extraction source, scaffold new files

**Files:**
- Create: `index.html.bak` (copy of current `index.html`, read-only reference for copy extraction — deleted in Task 8)
- Create: `styles/main.css`
- Create: `scripts/main.js`

**Interfaces:**
- Consumes: nothing (first task)
- Produces: `index.html.bak` (reference file later tasks grep against), `styles/main.css` (CSS custom properties block later tasks append to), `scripts/main.js` (empty shell later tasks append modules to)

- [ ] **Step 1: Back up current content for copy extraction**

```bash
cd /c/ZZZWebsites/camp99.asia
cp index.html index.html.bak
```

- [ ] **Step 2: Create `styles/` directory and base stylesheet with reset + custom properties**

Create `styles/main.css`:

```css
/* Camp 99 — hand-authored stylesheet, replaces Elementor/Astra CSS chain */

*, *::before, *::after { box-sizing: border-box; }
html, body, h1, h2, h3, h4, h5, h6, p, ul, ol, figure { margin: 0; padding: 0; }
img { max-width: 100%; display: block; }
ul { list-style: none; }
a { text-decoration: none; color: inherit; }

:root {
  --color-bg: #000000;
  --color-text: #ffffff;
  --color-accent: #c580c9;
  --color-accent-hover: #59d600;
  --color-cta: #dd3333;
  --font-heading: 'Open Sans Condensed', sans-serif;
  --font-display: 'Racing Sans One', sans-serif;
  --breakpoint-xs: 480px;
  --breakpoint-sm: 544px;
  --breakpoint-md: 768px;
  --breakpoint-lg: 1024px;
  --breakpoint-xl: 1180px;
}

body {
  background: var(--color-bg);
  color: var(--color-text);
  font-family: var(--font-heading);
  font-weight: 700;
  line-height: 1.7em;
}

h1, h2, h3, h4, h5, h6 {
  font-family: var(--font-heading);
  font-weight: 700;
  text-transform: uppercase;
}

h1 { font-size: 86px; font-weight: 900; font-family: var(--font-display); line-height: 1.4em; }
h2 { font-size: 84px; line-height: 1.3em; }
h3 { font-size: 28px; line-height: 1.3em; }

a { color: var(--color-accent); }
a:hover, a:focus { color: var(--color-accent-hover); }

.container {
  max-width: var(--breakpoint-xl);
  margin: 0 auto;
  padding: 0 20px;
}

@media (max-width: 768px) {
  h1 { font-size: 70px; }
  h2 { font-size: 68px; }
  h3 { font-size: 25px; }
}

@media (max-width: 544px) {
  h1 { font-size: 40px; }
  h2 { font-size: 39px; }
  h3 { font-size: 20px; }
}
```

- [ ] **Step 3: Create empty JS module shell**

Create `scripts/main.js`:

```js
// Camp 99 — vanilla JS, replaces jQuery/jQuery UI/Swiper
document.addEventListener('DOMContentLoaded', function () {
  // nav, carousel, and scroll-to-top modules attach themselves here
  // (added in Tasks 2, 5, and 7)
});
```

- [ ] **Step 4: Verify files parse / load**

```bash
python3 -c "
from html.parser import HTMLParser
HTMLParser().feed(open('index.html.bak', encoding='utf-8').read())
print('backup parses OK')
"
node --check scripts/main.js && echo "main.js syntax OK"
```

Expected: both print OK, no errors.

- [ ] **Step 5: Commit**

```bash
git add styles/main.css scripts/main.js
git commit -m "chore: scaffold styles/main.css and scripts/main.js for homepage rebuild"
```

Note: `index.html.bak` stays untracked (working reference only) — do not `git add` it. Confirm it isn't picked up by `.gitignore`'s `*.bak` handling if present; if git does try to track it, add `index.html.bak` to a local `git add` exclusion by simply never staging it.

---

## Task 1: New `index.html` shell — `<head>`, GTM, fonts, CSP-compatible structure

**Files:**
- Create: `index.html.new` (built up across Tasks 1–7, swapped in for real `index.html` in Task 8)

**Interfaces:**
- Consumes: `index.html.bak` (source of `<head>` meta/SEO tags, GTM script block, JSON-LD schema, font preloads to copy verbatim)
- Produces: `index.html.new` with complete `<head>`, empty `<body>` shell with `<header>`, `<main>`, `<footer>` placeholders for later tasks

- [ ] **Step 1: Extract the exact `<head>` content to preserve**

```bash
cd /c/ZZZWebsites/camp99.asia
python3 -c "
data = open('index.html.bak', encoding='utf-8').read()
start = data.find('<head>')
end = data.find('</head>') + len('</head>')
print(data[start:end])
" > /tmp/camp99_head_reference.txt
wc -l /tmp/camp99_head_reference.txt
```

This file is your reference for Step 2 — copy every SEO meta tag, the GTM script block (with the `window.load`-deferred injection and interaction-based lazy load already in place from prior work), the JSON-LD schema block, the CSP-relevant font preloads (`racingsansone-...woff2`), and the webfont `<link>`/`@font-face` references verbatim. Do not alter any of this content — it's out of scope for this rebuild.

- [ ] **Step 2: Write `index.html.new` with preserved `<head>` plus new stylesheet link**

```bash
python3 << 'EOF'
data = open('index.html.bak', encoding='utf-8').read()
head_start = data.find('<head>')
head_end = data.find('</head>') + len('</head>')
head = data[head_start:head_end]

# Swap the entire Elementor/Astra CSS chain for the single new stylesheet.
# Keep webfont preload/links, GTM script, JSON-LD, and all <meta> tags.
import re
head = re.sub(r'<link[^>]*href="\./css/[^"]*"[^>]*/?>\s*', '', head)
head = re.sub(r'<noscript><link[^>]*href="\./css/[^"]*"[^>]*/?></noscript>\s*', '', head)
head = re.sub(r'<style id="[^"]*">.*?</style>\s*', '', head, flags=__import__('re').S)
head = head.replace('</head>', '<link rel="stylesheet" href="./styles/main.css"/>\n</head>')

html = f'''<!DOCTYPE html>
<html lang="en-US" prefix="og: https://ogp.me/ns#">
{head}
<body>
<!-- HEADER placeholder: Task 2 -->
<main>
<!-- HERO placeholder: Task 3 -->
<!-- ABOUT placeholder: Task 4 -->
<!-- SERVICES placeholder: Task 4 -->
<!-- CAROUSEL/COME-ON-OUT placeholder: Task 5 -->
<!-- LOCATION placeholder: Task 6 -->
</main>
<!-- FOOTER placeholder: Task 7 -->
<script src="./scripts/main.js"></script>
</body>
</html>
'''
open('index.html.new', 'w', encoding='utf-8').write(html)
print('wrote index.html.new,', len(html), 'chars')
EOF
```

- [ ] **Step 3: Verify it parses and the GTM/meta/font content survived**

```bash
python3 -c "
from html.parser import HTMLParser
HTMLParser().feed(open('index.html.new', encoding='utf-8').read())
print('parses OK')
"
grep -c 'gtag' index.html.new
grep -c 'racingsansone' index.html.new
grep -c 'name=\"description\"' index.html.new
```

Expected: parses OK, all three grep counts > 0 (GTM script, font preload, meta description all preserved).

- [ ] **Step 4: Commit**

```bash
git add index.html.new
git commit -m "wip: index.html.new head + body shell for homepage rebuild"
```

---

## Task 2: Header and navigation (markup, CSS, JS — including the dropdown-arrow bug fix)

**Files:**
- Modify: `index.html.new` (replace `<!-- HEADER placeholder: Task 2 -->`)
- Modify: `styles/main.css` (append nav rules)
- Modify: `scripts/main.js` (append nav module)

**Interfaces:**
- Consumes: `index.html.bak` (source of the nested 3-level menu structure and exact link hrefs/labels)
- Produces: `.site-header`, `.site-nav`, `.nav-toggle` CSS classes and a `initNav()` function other tasks don't depend on (self-contained)

- [ ] **Step 1: Extract the current nav menu structure**

```bash
cd /c/ZZZWebsites/camp99.asia
python3 -c "
data = open('index.html.bak', encoding='utf-8').read()
i = data.find('id=\"primary-menu\"')
j = data.find('</ul>', data.rfind('</ul>', 0, data.find('</nav>')))
print(data[i-50:data.find('</nav>')+7])
" > /tmp/camp99_nav_reference.txt
cat /tmp/camp99_nav_reference.txt
```

Use this to build the semantic nav below — every `<a href="...">Label</a>` pair (including nested `<ul class="sub-menu">` items) must appear in the new markup with the same href and label text, since these are real links to other pages in this repo.

- [ ] **Step 2: Write semantic header/nav markup**

Replace `<!-- HEADER placeholder: Task 2 -->` in `index.html.new` with:

```html
<header class="site-header">
  <div class="container site-header__inner">
    <a href="index.html" class="site-logo">
      <img src="./images/camp99asia-camp99-asia-logo.webp"
           srcset="./images/camp99asia-camp99-asia-logo.webp 300w, ./images/camp99asia-camp99-asia-logo.webp 450w"
           sizes="(max-width: 300px) 100vw, 300px"
           width="300" height="100" alt="Camp 99">
    </a>
    <button class="nav-toggle" aria-expanded="false" aria-controls="site-nav" aria-label="Toggle Menu">
      <span></span><span></span><span></span>
    </button>
    <nav id="site-nav" class="site-nav" aria-label="Site Navigation">
      <ul class="site-nav__list">
        <!-- Populate every top-level <li> here using the labels/hrefs
             extracted in Step 1. Each item with children gets:
             <li class="has-children">
               <a href="...">Label</a>
               <button class="submenu-toggle" aria-expanded="false" aria-label="Toggle submenu">
                 <svg class="nav-caret" width="10" height="6" viewBox="0 0 10 6" aria-hidden="true">
                   <path d="M1 1l4 4 4-4" stroke="currentColor" stroke-width="1.5" fill="none"/>
                 </svg>
               </button>
               <ul class="sub-menu">...nested items, same pattern...</ul>
             </li>
             Items with no children are plain: <li><a href="...">Label</a></li> -->
      </ul>
    </nav>
  </div>
</header>
```

The `<svg class="nav-caret">` is the fix for the missing dropdown-arrow bug reported on the live site — the old Astra `.ast-icon.icon-arrow` relied on the `Astra` icon font loading correctly (`font-display: optional` now means it may never render if the font is slow), which is why arrows were invisible. An inline SVG has no font dependency and always renders.

- [ ] **Step 3: Append nav CSS to `styles/main.css`**

```css
/* --- Header / Nav --- */
.site-header {
  position: relative;
  z-index: 100;
  background: var(--color-bg);
  padding: 16px 0;
}
.site-header__inner {
  display: flex;
  align-items: center;
  justify-content: space-between;
}
.site-logo img { width: 200px; height: auto; }

.nav-toggle {
  display: none;
  flex-direction: column;
  gap: 5px;
  background: none;
  border: 0;
  cursor: pointer;
  padding: 8px;
}
.nav-toggle span { width: 24px; height: 2px; background: var(--color-text); }

.site-nav__list {
  display: flex;
  gap: 24px;
  position: relative;
}
.site-nav__list > li { position: relative; }
.site-nav__list a {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 8px 0;
  font-size: 15px;
  text-transform: uppercase;
}
.nav-caret { transition: transform 0.2s; }
.has-children.is-open > .nav-caret,
.has-children.is-open .submenu-toggle .nav-caret { transform: rotate(180deg); }

.sub-menu {
  display: none;
  position: absolute;
  top: 100%;
  left: 0;
  min-width: 220px;
  background: #111;
  border: 1px solid #eaeaea;
  padding: 8px 0;
}
.has-children.is-open > .sub-menu { display: block; }
.sub-menu li { position: relative; }
.sub-menu a { padding: 8px 16px; display: flex; width: 100%; }
.sub-menu .sub-menu { top: 0; left: 100%; }

@media (max-width: 1024px) {
  .nav-toggle { display: flex; }
  .site-nav {
    display: none;
    position: absolute;
    top: 100%;
    left: 0;
    right: 0;
    background: var(--color-bg);
  }
  .site-nav.is-open { display: block; }
  .site-nav__list { flex-direction: column; gap: 0; }
  .sub-menu { position: static; border: 0; padding-left: 16px; }
}
```

- [ ] **Step 4: Append nav JS module to `scripts/main.js`**

Replace the empty `DOMContentLoaded` body with a call to `initNav()`, and add the function above it:

```js
function initNav() {
  var toggle = document.querySelector('.nav-toggle');
  var nav = document.getElementById('site-nav');
  toggle.addEventListener('click', function () {
    var open = nav.classList.toggle('is-open');
    toggle.setAttribute('aria-expanded', open);
  });

  var items = document.querySelectorAll('.has-children');
  items.forEach(function (item) {
    var closeTimer = null;
    var isDesktop = function () { return window.innerWidth > 1024; };

    function open() {
      clearTimeout(closeTimer);
      item.classList.add('is-open');
      var btn = item.querySelector(':scope > .submenu-toggle');
      if (btn) btn.setAttribute('aria-expanded', 'true');
    }
    function scheduleClose() {
      closeTimer = setTimeout(function () {
        item.classList.remove('is-open');
        var btn = item.querySelector(':scope > .submenu-toggle');
        if (btn) btn.setAttribute('aria-expanded', 'false');
      }, 250);
    }

    item.addEventListener('mouseenter', function () { if (isDesktop()) open(); });
    item.addEventListener('mouseleave', function () { if (isDesktop()) scheduleClose(); });

    var btn = item.querySelector(':scope > .submenu-toggle');
    if (btn) {
      btn.addEventListener('click', function (e) {
        e.preventDefault();
        if (item.classList.contains('is-open')) {
          item.classList.remove('is-open');
          btn.setAttribute('aria-expanded', 'false');
        } else {
          open();
        }
      });
    }
  });

  document.addEventListener('click', function (e) {
    if (!e.target.closest('.site-nav')) {
      document.querySelectorAll('.has-children.is-open').forEach(function (el) {
        el.classList.remove('is-open');
      });
    }
  });
}

document.addEventListener('DOMContentLoaded', function () {
  initNav();
});
```

- [ ] **Step 5: Verify — parse check + manual browser check**

```bash
python3 -c "
from html.parser import HTMLParser
HTMLParser().feed(open('index.html.new', encoding='utf-8').read())
print('parses OK')
"
node --check scripts/main.js && echo "main.js syntax OK"
```

Then open `index.html.new` directly in a browser (rename a temp copy to `.html` if needed for file:// testing) and confirm: caret icons are visible next to every item with children, hovering opens submenus on desktop with a short close delay (no flicker gap), clicking the hamburger toggles the mobile menu, and tapping a parent item on mobile expands its submenu in place without navigating away.

- [ ] **Step 6: Commit**

```bash
git add index.html.new styles/main.css scripts/main.js
git commit -m "feat: header/nav markup, CSS, and JS for homepage rebuild"
```

---

## Task 3: Hero section

**Files:**
- Modify: `index.html.new` (replace `<!-- HERO placeholder: Task 3 -->`)
- Modify: `styles/main.css` (append hero rules)

**Interfaces:**
- Consumes: `index.html.bak` (exact h1/subtitle copy, `facility-212` responsive image already fixed in prior perf work)
- Produces: `.hero` CSS class

- [ ] **Step 1: Extract hero copy**

```bash
cd /c/ZZZWebsites/camp99.asia
python3 -c "
data = open('index.html.bak', encoding='utf-8').read()
i = data.find('Camp 99</h1>')
print(data[max(0,i-100):i+600])
"
```

Confirm the subtitle heading text ("Camp 99 is a day-use meeting, retreat, and recreation center for Christians.") matches what's already documented in this project's memory.

- [ ] **Step 2: Write hero markup**

```html
<section class="hero">
  <img class="hero__bg" src="./images/camp99asia-camp99-asia-facility-212.webp"
       srcset="./images/camp99asia-camp99-asia-facility-212.webp 1280w,
               ./images/camp99asia-camp99-asia-facility-212-300w.webp 300w,
               ./images/camp99asia-camp99-asia-facility-212-500w.webp 500w,
               ./images/camp99asia-camp99-asia-facility-212-1024w.webp 1024w,
               ./images/camp99asia-camp99-asia-facility-212-768w.webp 768w"
       sizes="(max-width: 600px) 456px, (max-width: 1280px) 100vw, 1280px"
       width="1280" height="720" fetchpriority="high" decoding="async" alt="Camp 99 asia camp99asia">
  <div class="hero__content container">
    <h1>Camp 99</h1>
    <h2>Camp 99 is a day-use meeting, retreat, and recreation center for Christians.</h2>
  </div>
</section>
```

- [ ] **Step 3: Append hero CSS**

```css
/* --- Hero --- */
.hero { position: relative; min-height: 70vh; display: flex; align-items: center; }
.hero__bg {
  position: absolute; inset: 0; width: 100%; height: 100%;
  object-fit: cover; z-index: -1;
}
.hero__content { position: relative; padding: 60px 20px; }
.hero h1 { margin-bottom: 16px; }
.hero h2 { font-size: 32px; text-transform: none; }

@media (max-width: 768px) { .hero h2 { font-size: 24px; } }
@media (max-width: 544px) { .hero h2 { font-size: 18px; } }
```

- [ ] **Step 4: Verify**

```bash
python3 -c "
from html.parser import HTMLParser
HTMLParser().feed(open('index.html.new', encoding='utf-8').read())
print('parses OK')
"
```

Open in browser: hero background image fills the viewport width without distortion, h1 and subtitle are readable and match the current live page's copy exactly.

- [ ] **Step 5: Commit**

```bash
git add index.html.new styles/main.css
git commit -m "feat: hero section for homepage rebuild"
```

---

## Task 4: About + Services sections

**Files:**
- Modify: `index.html.new` (replace `<!-- ABOUT placeholder -->` and `<!-- SERVICES placeholder -->`)
- Modify: `styles/main.css` (append about/services rules)

**Interfaces:**
- Consumes: `index.html.bak` (body copy for About/Purpose/Serving-the-99/4 service cards, `facility-210`/`facility-202` images already fixed with real responsive srcset)
- Produces: `.about`, `.services`, `.service-card` CSS classes

- [ ] **Step 1: Extract About and Services copy**

```bash
cd /c/ZZZWebsites/camp99.asia
python3 -c "
data = open('index.html.bak', encoding='utf-8').read()
for marker in ['Purpose of Camp 99</h3>', 'Serving the 99</h3>', '>events</h3>', 'Meetings/Worship/Prayer/Small Groups</h3>', '>fishing</h3>', '>Sports</h3>']:
    i = data.find(marker)
    print('===', marker, '===')
    print(data[max(0,i-50):i+800])
    print()
"
```

Read the full output and pull the exact paragraph text following each heading — this is the body copy for each card. Do not paraphrase or summarize it.

- [ ] **Step 2: Write About section markup**

```html
<section class="about container">
  <span class="section-marker">/ 01</span>
  <h2>about</h2>
  <h3>Purpose of Camp 99</h3>
  <div class="about__grid">
    <div class="about__text">
      <!-- Insert the exact paragraph(s) extracted in Step 1 here, wrapped in <p> tags -->
    </div>
    <div class="about__images">
      <img src="./images/camp99asia-camp99-asia-facility-210.webp"
           srcset="./images/camp99asia-camp99-asia-facility-210.webp 1024w,
                   ./images/camp99asia-camp99-asia-facility-210-300w.webp 300w,
                   ./images/camp99asia-camp99-asia-facility-210-768w.webp 768w"
           sizes="(max-width: 1024px) 100vw, 1024px"
           width="1024" height="576" loading="lazy" alt="Camp 99 asia camp99asia">
      <img src="./images/camp99asia-camp99-asia-facility-202.webp"
           srcset="./images/camp99asia-camp99-asia-facility-202.webp 883w,
                   ./images/camp99asia-camp99-asia-facility-202-300w.webp 300w,
                   ./images/camp99asia-camp99-asia-facility-202-768w.webp 768w"
           sizes="(max-width: 883px) 100vw, 883px"
           width="883" height="1024" loading="lazy" alt="Camp 99 asia camp99asia">
    </div>
  </div>
</section>
```

- [ ] **Step 3: Write Services section markup**

```html
<section class="services container">
  <span class="section-marker">/ 02</span>
  <h2>services</h2>
  <h3>Serving the 99</h3>
  <div class="services__grid">
    <article class="service-card">
      <img src="./images/camp99asia-camp99-asia-icon-events.png" width="65" height="65" alt="Events" loading="lazy">
      <h3>events</h3>
      <!-- Insert exact "events" body copy extracted in Step 1 -->
    </article>
    <article class="service-card">
      <img src="./images/camp99asia-camp99-asia-icon-entertainment.png" width="65" height="65" alt="Entertainment" loading="lazy">
      <h3>Meetings/Worship/Prayer/Small Groups</h3>
      <!-- Insert exact body copy extracted in Step 1 -->
    </article>
    <article class="service-card">
      <img src="./images/camp99asia-camp99-asia-icon-fishing.png" width="65" height="65" alt="Fishing" loading="lazy">
      <h3>fishing</h3>
      <!-- Insert exact body copy extracted in Step 1 -->
    </article>
    <article class="service-card">
      <img src="./images/camp99asia-camp99-asia-icon-relax.png" width="65" height="65" alt="Sports" loading="lazy">
      <h3>Sports</h3>
      <!-- Insert exact body copy extracted in Step 1 -->
    </article>
  </div>
</section>
```

- [ ] **Step 4: Append CSS**

```css
/* --- About / Services shared --- */
.section-marker {
  display: block;
  font-size: 14px;
  letter-spacing: 2px;
  color: var(--color-accent);
  margin-bottom: 8px;
}
.about, .services { padding: 60px 20px; }

.about__grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 40px;
  align-items: start;
  margin-top: 24px;
}
.about__images { display: grid; gap: 16px; }
.about__images img { border-radius: 4px; }

.services__grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 24px;
  margin-top: 24px;
}
.service-card { text-align: center; }
.service-card img { margin: 0 auto 16px; }
.service-card h3 { font-size: 20px; margin-bottom: 8px; }

@media (max-width: 1024px) {
  .services__grid { grid-template-columns: repeat(2, 1fr); }
}
@media (max-width: 768px) {
  .about__grid { grid-template-columns: 1fr; }
}
@media (max-width: 544px) {
  .services__grid { grid-template-columns: 1fr; }
}
```

- [ ] **Step 5: Verify**

```bash
python3 -c "
from html.parser import HTMLParser
HTMLParser().feed(open('index.html.new', encoding='utf-8').read())
print('parses OK')
"
```

Open in browser: confirm About's two-column layout collapses to one column under 768px, confirm all 4 service cards display in a 4-column row on desktop, 2-column at tablet width, 1-column under 544px, confirm none of the body copy differs from the live page.

- [ ] **Step 6: Commit**

```bash
git add index.html.new styles/main.css
git commit -m "feat: about and services sections for homepage rebuild"
```

---

## Task 5: Carousel / "Come On Out!" section (includes carousel aspect-ratio fix and YouTube embed fix)

**Files:**
- Modify: `index.html.new` (replace `<!-- CAROUSEL/COME-ON-OUT placeholder -->`)
- Modify: `styles/main.css` (append carousel rules)
- Modify: `scripts/main.js` (append carousel module)

**Interfaces:**
- Consumes: `index.html.bak` (carousel image list, YouTube video ID `elESI9qKq84`, "We're just 8km..." copy)
- Produces: `.carousel` CSS class, `initCarousel()` function (self-contained, no dependency on nav module)

- [ ] **Step 1: Diagnose the current YouTube embed failure**

```bash
cd /c/ZZZWebsites/camp99.asia
python3 -c "
data = open('index.html.bak', encoding='utf-8').read()
i = data.find('elementor-widget-video')
print(data[i:i+900])
"
```

Check the printed `<iframe>` tag's `src` attribute against the CSP `frame-src`/`child-src` directive in `_headers`. If `_headers`' `Content-Security-Policy` line has no `frame-src` or `child-src` directive permitting `https://www.youtube.com`, that's the bug — the browser silently blocks the iframe. **Do not edit `_headers` in this task** (out of scope per Global Constraints) — instead confirm the diagnosis here and flag it: if this is the cause, note it in the Task 5 commit message so a follow-up `_headers` fix (`frame-src https://www.youtube.com`) can be scheduled. If the iframe `src` itself is malformed or the video ID is wrong, fix that in the markup written in Step 2 instead.

- [ ] **Step 2: Extract carousel image list and "We're just 8km" copy**

```bash
python3 -c "
data = open('index.html.bak', encoding='utf-8').read()
i = data.find('Super Highway')
print(data[max(0,i-600):i+200])
"
```

- [ ] **Step 3: Write carousel + video markup**

```html
<section class="carousel-section container">
  <span class="section-marker">/ 03</span>
  <h2>COME ON OUT!</h2>

  <div class="carousel" role="region" aria-label="Camp 99 photo gallery">
    <button class="carousel__btn carousel__btn--prev" aria-label="Previous image">&#8249;</button>
    <div class="carousel__track">
      <img class="carousel__item" src="./images/camp99asia-camp99-asia-facility-225.webp"
           srcset="./images/camp99asia-camp99-asia-facility-225.webp 960w,
                   ./images/camp99asia-camp99-asia-facility-225-300w.webp 300w,
                   ./images/camp99asia-camp99-asia-facility-225-768w.webp 768w"
           sizes="(max-width: 960px) 100vw, 960px" width="960" height="631"
           loading="lazy" alt="Camp 99 asia camp99asia">
      <img class="carousel__item" src="./images/camp99asia-camp99-asia-facility-228.webp"
           srcset="./images/camp99asia-camp99-asia-facility-228.webp 960w,
                   ./images/camp99asia-camp99-asia-facility-228-300w.webp 300w,
                   ./images/camp99asia-camp99-asia-facility-228-768w.webp 768w"
           sizes="(max-width: 960px) 100vw, 960px" width="960" height="753"
           loading="lazy" alt="Camp 99 asia camp99asia">
      <img class="carousel__item" src="./images/camp99asia-camp99-asia-facility-230.webp"
           srcset="./images/camp99asia-camp99-asia-facility-230.webp 960w,
                   ./images/camp99asia-camp99-asia-facility-230-300w.webp 300w,
                   ./images/camp99asia-camp99-asia-facility-230-768w.webp 768w"
           sizes="(max-width: 960px) 100vw, 960px" width="960" height="540"
           loading="lazy" alt="Camp 99 asia camp99asia">
      <img class="carousel__item" src="./images/camp99asia-camp99-asia-facility-232.webp"
           srcset="./images/camp99asia-camp99-asia-facility-232.webp 1024w,
                   ./images/camp99asia-camp99-asia-facility-232-300w.webp 300w,
                   ./images/camp99asia-camp99-asia-facility-232-768w.webp 768w"
           sizes="(max-width: 1024px) 100vw, 1024px" width="1024" height="581"
           loading="lazy" alt="Camp 99 asia camp99asia">
      <img class="carousel__item" src="./images/camp99asia-camp99-asia-gallery-223.webp"
           srcset="./images/camp99asia-camp99-asia-gallery-223.webp 768w,
                   ./images/camp99asia-camp99-asia-gallery-223-300w.webp 300w"
           sizes="(max-width: 768px) 100vw, 768px" width="768" height="432"
           loading="lazy" alt="Camp 99 asia camp99asia">
    </div>
    <button class="carousel__btn carousel__btn--next" aria-label="Next image">&#8250;</button>
  </div>

  <div class="video-wrapper">
    <iframe class="video-wrapper__frame"
            src="https://www.youtube.com/embed/elESI9qKq84"
            title="Camp 99 video"
            loading="lazy"
            allow="accelerometer; encrypted-media; gyroscope; picture-in-picture; web-share"
            allowfullscreen></iframe>
  </div>

  <p class="carousel-section__blurb">
    <!-- Insert the exact "We're just 8km from the Super Highway" copy extracted in Step 2 -->
  </p>
</section>
```

**Aspect-ratio fix**: every `<img>` above keeps its real `width`/`height` attributes (not stretched to a fixed box) and the CSS below uses `object-fit: cover` inside a fixed-aspect-ratio container — this directly addresses the squashed-carousel-images feedback from spec review.

- [ ] **Step 4: Append carousel + video CSS**

```css
/* --- Carousel --- */
.carousel-section { padding: 60px 20px; }
.carousel { position: relative; margin-top: 24px; }
.carousel__track {
  display: flex;
  gap: 12px;
  overflow-x: auto;
  scroll-snap-type: x mandatory;
  scrollbar-width: none;
}
.carousel__track::-webkit-scrollbar { display: none; }
.carousel__item {
  flex: 0 0 auto;
  width: 320px;
  aspect-ratio: 4 / 3;
  object-fit: cover;
  scroll-snap-align: start;
  border-radius: 4px;
}
.carousel__btn {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  z-index: 2;
  width: 40px;
  height: 40px;
  border-radius: 50%;
  border: 0;
  background: rgba(0, 0, 0, 0.6);
  color: #fff;
  font-size: 24px;
  cursor: pointer;
}
.carousel__btn--prev { left: 0; }
.carousel__btn--next { right: 0; }

.video-wrapper {
  position: relative;
  width: 100%;
  aspect-ratio: 16 / 9;
  margin: 40px 0;
}
.video-wrapper__frame {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  border: 0;
}

@media (max-width: 544px) {
  .carousel__item { width: 240px; }
}
```

- [ ] **Step 5: Append carousel JS module**

```js
function initCarousel() {
  var track = document.querySelector('.carousel__track');
  if (!track) return;
  var prev = document.querySelector('.carousel__btn--prev');
  var next = document.querySelector('.carousel__btn--next');
  var scrollAmount = function () {
    var item = track.querySelector('.carousel__item');
    return item ? item.getBoundingClientRect().width + 12 : 300;
  };
  prev.addEventListener('click', function () {
    track.scrollBy({ left: -scrollAmount(), behavior: 'smooth' });
  });
  next.addEventListener('click', function () {
    track.scrollBy({ left: scrollAmount(), behavior: 'smooth' });
  });
}
```

Add `initCarousel();` to the `DOMContentLoaded` listener alongside `initNav();`.

- [ ] **Step 6: Verify**

```bash
python3 -c "
from html.parser import HTMLParser
HTMLParser().feed(open('index.html.new', encoding='utf-8').read())
print('parses OK')
"
node --check scripts/main.js && echo "main.js syntax OK"
```

Open in browser: confirm carousel images are NOT squashed/stretched (each keeps its natural proportions inside the `aspect-ratio: 4/3` box via `object-fit: cover`), prev/next buttons scroll smoothly, and the YouTube video either now renders (if Step 1 found a markup bug) or fails identically to before with the CSP diagnosis noted in the commit message for follow-up.

- [ ] **Step 7: Commit**

```bash
git add index.html.new styles/main.css scripts/main.js
git commit -m "feat: carousel and video section for homepage rebuild

$(cat <<'NOTE'
Diagnosis of the reported YouTube-not-loading bug: [fill in what Step 1 found —
CSP frame-src missing youtube.com, or a markup issue, whichever it was]
NOTE
)"
```

---

## Task 6: Location section (Google Map + address)

**Files:**
- Modify: `index.html.new` (replace `<!-- LOCATION placeholder -->`)
- Modify: `styles/main.css` (append location rules)

**Interfaces:**
- Consumes: `index.html.bak` (Google Maps iframe `src`, "/ 04" marker, "Location" heading, address/contact copy)
- Produces: `.location` CSS class

- [ ] **Step 1: Extract map iframe and address copy**

```bash
cd /c/ZZZWebsites/camp99.asia
python3 -c "
data = open('index.html.bak', encoding='utf-8').read()
i = data.find('elementor-widget-google_maps')
print(data[i:i+700])
print('---')
i2 = data.find('>Location</h2>')
print(data[max(0,i2-50):i2+600])
"
```

- [ ] **Step 2: Write Location section markup**

```html
<section class="location container">
  <span class="section-marker">/ 04</span>
  <h2>Location</h2>
  <div class="location__grid">
    <div class="location__map">
      <!-- Insert the exact <iframe> extracted in Step 1, unmodified -->
    </div>
    <div class="location__address">
      <!-- Insert the exact address/contact copy extracted in Step 1 -->
    </div>
  </div>
</section>
```

- [ ] **Step 3: Append CSS**

```css
/* --- Location --- */
.location { padding: 60px 20px; }
.location__grid {
  display: grid;
  grid-template-columns: 3fr 2fr;
  gap: 40px;
  margin-top: 24px;
}
.location__map iframe { width: 100%; height: 400px; border: 0; }

@media (max-width: 768px) {
  .location__grid { grid-template-columns: 1fr; }
}
```

- [ ] **Step 4: Verify**

```bash
python3 -c "
from html.parser import HTMLParser
HTMLParser().feed(open('index.html.new', encoding='utf-8').read())
print('parses OK')
"
```

Open in browser: confirm the map renders and is interactive (pan/zoom), confirm address copy matches the live page exactly.

- [ ] **Step 5: Commit**

```bash
git add index.html.new styles/main.css
git commit -m "feat: location section for homepage rebuild"
```

---

## Task 7: Footer (includes scroll-to-top JS module)

**Files:**
- Modify: `index.html.new` (replace `<!-- FOOTER placeholder -->`)
- Modify: `styles/main.css` (append footer rules)
- Modify: `scripts/main.js` (append scroll-to-top module)

**Interfaces:**
- Consumes: `index.html.bak` (footer contact info, social links, nav duplicate links, copyright text)
- Produces: `.site-footer` CSS class, `initScrollToTop()` function (self-contained)

- [ ] **Step 1: Extract footer content**

```bash
cd /c/ZZZWebsites/camp99.asia
python3 -c "
data = open('index.html.bak', encoding='utf-8').read()
i = data.find('id=\"colophon\"')
print(data[i:])
"
```

- [ ] **Step 2: Write footer markup**

```html
<footer class="site-footer">
  <div class="container site-footer__inner">
    <div class="site-footer__contact">
      <h3>contact</h3>
      <!-- Insert exact email/phone copy extracted in Step 1 -->
    </div>
    <div class="site-footer__social">
      <h3>keep in touch</h3>
      <div class="social-icons">
        <a class="social-icon" href="https://web.facebook.com/Camp99Camp99/" rel="noopener" target="_blank" aria-label="Facebook">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">
            <path d="M22 12a10 10 0 1 0-11.6 9.9v-7H7.9V12h2.5V9.8c0-2.5 1.5-3.9 3.8-3.9 1.1 0 2.2.2 2.2.2v2.5h-1.3c-1.2 0-1.6.8-1.6 1.6V12h2.8l-.4 2.9h-2.4v7A10 10 0 0 0 22 12z"/>
          </svg>
        </a>
      </div>
    </div>
    <p class="site-footer__copyright">
      <!-- Insert exact copyright text extracted in Step 1 -->
    </p>
  </div>
  <button class="scroll-to-top" aria-label="Scroll to top" hidden>&#8593;</button>
</footer>
```

- [ ] **Step 3: Append footer CSS**

```css
/* --- Footer --- */
.site-footer { padding: 60px 20px; border-top: 1px solid #333; }
.site-footer__inner {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 24px;
}
.social-icons { display: flex; gap: 12px; margin-top: 12px; }
.social-icon {
  width: 40px; height: 40px;
  display: flex; align-items: center; justify-content: center;
  border-radius: 50%;
  background: #222;
  transition: color 0.3s;
}
.site-footer__copyright { grid-column: 1 / -1; margin-top: 24px; font-size: 13px; opacity: 0.7; }

.scroll-to-top {
  position: fixed;
  bottom: 24px;
  right: 24px;
  width: 44px;
  height: 44px;
  border-radius: 50%;
  border: 0;
  background: var(--color-cta);
  color: #fff;
  font-size: 20px;
  cursor: pointer;
  opacity: 0;
  pointer-events: none;
  transition: opacity 0.3s;
  z-index: 200;
}
.scroll-to-top.is-visible { opacity: 1; pointer-events: auto; }

@media (max-width: 544px) {
  .site-footer__inner { grid-template-columns: 1fr; }
}
```

- [ ] **Step 4: Append scroll-to-top JS module**

```js
function initScrollToTop() {
  var btn = document.querySelector('.scroll-to-top');
  if (!btn) return;
  btn.hidden = false;
  window.addEventListener('scroll', function () {
    btn.classList.toggle('is-visible', window.scrollY > 400);
  }, { passive: true });
  btn.addEventListener('click', function () {
    window.scrollTo({ top: 0, behavior: 'smooth' });
  });
}
```

Add `initScrollToTop();` to the `DOMContentLoaded` listener alongside `initNav();` and `initCarousel();`.

- [ ] **Step 5: Verify**

```bash
python3 -c "
from html.parser import HTMLParser
HTMLParser().feed(open('index.html.new', encoding='utf-8').read())
print('parses OK')
"
node --check scripts/main.js && echo "main.js syntax OK"
```

Open in browser: confirm scroll-to-top button appears after scrolling past 400px and disappears near the top, clicking it smooth-scrolls to top, footer content/links match the live page.

- [ ] **Step 6: Commit**

```bash
git add index.html.new styles/main.css scripts/main.js
git commit -m "feat: footer and scroll-to-top for homepage rebuild"
```

---

## Task 8: Swap in the new homepage, full verification, cleanup

**Files:**
- Modify: `index.html` (replaced with contents of `index.html.new`)
- Delete: `index.html.new`, `index.html.bak`

**Interfaces:**
- Consumes: everything from Tasks 1–7
- Produces: the live `index.html`

- [ ] **Step 1: Swap the files**

```bash
cd /c/ZZZWebsites/camp99.asia
cp index.html index.html.pre-rebuild-backup
mv index.html.new index.html
```

- [ ] **Step 2: Full parse check**

```bash
python3 -c "
from html.parser import HTMLParser
HTMLParser().feed(open('index.html', encoding='utf-8').read())
print('parses OK')
"
node --check scripts/main.js && echo "main.js syntax OK"
```

- [ ] **Step 3: Manual full-page visual verification at every breakpoint**

Open `index.html` in a browser and check at viewport widths 375px, 480px, 544px, 768px, 1024px, 1180px, and 1920px:
- Header/nav: logo visible, dropdown carets render, hover/tap-to-expand both work, no layout overlap
- Hero: background image covers full width without distortion, headings match live copy
- About/Services: two-column → one-column collapse at 768px, all 4 service cards present with correct icons/copy
- Carousel: images are NOT squashed (natural aspect ratio preserved), prev/next buttons work, video loads (or documented CSP fix is still pending per Task 5's note)
- Location: map is interactive, address copy correct
- Footer: contact/social/copyright correct, scroll-to-top button behaves correctly

- [ ] **Step 4: Confirm no leftover Elementor/Astra CSS or JS references**

```bash
grep -c "elementor\|Astra\|astra" index.html
grep -c "jquery\|swiper" index.html
```

Expected: both return `0`. If either is nonzero, find and remove the leftover reference before proceeding.

- [ ] **Step 5: Run a fresh PageSpeed/Lighthouse pass**

Compare against the pre-rebuild baseline (~90 performance / 100 accessibility / 96 best-practices / 100 SEO). Any regression must be root-caused and fixed before this task is considered done — do not proceed to remove the backup file if there's an unexplained regression.

- [ ] **Step 6: Clean up backup files and commit**

```bash
rm -f index.html.pre-rebuild-backup index.html.bak
git add -A
git commit -m "feat: swap in rebuilt homepage (vanilla HTML/CSS/JS, no Elementor/Astra)

Homepage now uses styles/main.css and scripts/main.js exclusively.
No jQuery, jQuery UI, or Swiper dependency on this page. Fixes the
missing nav dropdown arrows (inline SVG replaces the Astra icon font
dependency) and [YouTube embed fix summary from Task 5].

Old Elementor/Astra CSS/JS files are left in place — the other 30
pages still depend on them until they get the same treatment.

Co-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>"
git push
```

- [ ] **Step 7: Confirm live deployment**

```bash
curl -s "https://camp99.asia/?verify=$(date +%s)" | grep -c "elementor\|Astra"
```

Expected: `0`. If Cloudflare hasn't deployed yet, wait and retry rather than declaring done prematurely.

---

## Self-Review Notes

- **Spec coverage**: file structure (Task 0), header/nav with dropdown-arrow fix (Task 2), hero/about/services/carousel/location/footer section mapping (Tasks 3–7), CSS approach with matching breakpoints/colors (all tasks), JS approach with 3 vanilla modules replacing jQuery/Swiper (Tasks 2, 5, 7), carousel aspect-ratio fix from spec review (Task 5), YouTube embed bug (Task 5), testing/verification (Task 8) — all covered.
- **No placeholders**: every task extracts real copy via a concrete grep/Python command against `index.html.bak` rather than inventing or vaguely describing content; every CSS/JS block is complete, runnable code.
- **Type/name consistency**: `initNav()`, `initCarousel()`, `initScrollToTop()` are each defined once and called once in the same `DOMContentLoaded` listener, built up incrementally across Tasks 2/5/7 — verified names match between definition and call sites in each task's Step 4/5.
- **Scope**: single subsystem (homepage rebuild), appropriately sized for one plan — the other 30 pages are explicitly out of scope and flagged as a future pass.
