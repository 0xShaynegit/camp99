# camp99.asia PageSpeed issues

## Round 6 — 2026-08-04 2:04 PM report was stale (PSI cache, not Cloudflare) — real gap fixed anyway
The 2:04 PM report still showed h5/h6 headings and the WP Statistics tracker — both were already fixed
and confirmed live via direct curl with a cache-busting query string. This is PageSpeed Insights' own
server-side report cache, not Cloudflare's edge cache; Cloudflare purges can't touch it. To get a
genuinely fresh read, add a throwaway query string when testing (`https://camp99.asia/?t=1`) or use
Lighthouse directly instead of the PSI web UI.

While verifying, found one real leftover: `facility-230.webp` still had the fake duplicate-file
`srcset` pattern from round 3 (only recompressed, never given real 300w/768w variants). Also swept the
rest of the page for the same pattern and found four more: `gallery-223`, `facility-228`,
`facility-206`, `facility-232` — all had `srcset` entries pointing at the same file for every width.
Generated real variants and fixed all five. Left `camp99asia-camp99-asia-logo.webp`'s duplicate srcset
alone — it's a 5KB file, not worth a variant.

## Round 5 — 2026-08-04 1:31 PM report (CLS regressed to 0.066) — FIXED (commit pending)
Self-inflicted regression from round 2's render-blocking-CSS fix: `post-249_b187d0.css` contains
`.elementor-element-ef67603 img{width:70%}`, the rule that sizes the facility-212 hero image. Making
that stylesheet load via preload+swap meant the image now painted at full width first, then snapped
to 70% once the CSS applied — a 0.054 layout shift (the bulk of the 0.066 total). Reverted just this
one stylesheet back to a normal blocking `<link>` — it's only 4.5KB and page-specific, so the
render-blocking cost is negligible next to the CLS it was causing. Left the other 4 shared stylesheets
on preload+swap since none of them size above-the-fold elements the same way.

Also present in this report but not touched: two long main-thread tasks from GTM (upstream, already
deferred to `window.load`, can't reduce further) and ~0.008+0.004 CLS from three web fonts swapping
in (Open Sans Condensed, Font Awesome, RacingSansOne) — small enough to leave alone given the
functional cost of `font-display:optional` (icons/headline font may not render at all on slow
connections).

## Round 4 — 2026-08-04, Best Practices 96 — FIXED (commit pending)
- Console error: `wp-json/wp-statistics/v2/hit` 403 — dead WP Statistics tracker calling a REST endpoint that doesn't exist on this static export. Removed the tracker script and its config block entirely; GA/GTM already cover real analytics.
- Console error: `/cdn-cgi/rum` 404 — Cloudflare's own auto-injected RUM beacon, not present in this repo's HTML. Out of our control; a Cloudflare zone-level setting, not app code.
- Trust and Safety (unscored, but addressed): added `Content-Security-Policy`, `Cross-Origin-Opener-Policy: same-origin`, and `Strict-Transport-Security ... preload` to `_headers`. CSP still uses `'unsafe-inline'` for script-src/style-src because this exported page has dozens of inline `<script>`/`<style>` blocks with no nonce infrastructure — tightening further would need refactoring every inline block, out of scope here. This also means the "Trusted Types" finding stays open: `require-trusted-types-for 'script'` needs every DOM-sink write (innerHTML, etc.) audited across third-party libs (jQuery UI, Swiper) first, or it will silently break them.

## Round 1 — 2026-08-04 11:16 AM report (mobile score 64) — FIXED (commit bc7c653)
- Render-blocking CSS (common-head.css, vf6z_1b1df8.css, post-249_b187d0.css, vf6z_066dfd.css, fonts.css) — converted to preload+swap.
- Oversized/uncompressed hero images (facility-212, facility-250, hero-lakeside-view) — recompressed, added responsive srcset for facility-212.
- 4 icon images missing width/height — added.

## Round 2 — 2026-08-04 1:10 PM report (mobile score 65 → this round's fixes got it to 85) — FIXED (commit 1a1efe1)
- Render-blocking jQuery + flexibility polyfill (300ms) — deferred both, wrapped their jQuery-dependent inline scripts in `DOMContentLoaded` so execution order stays safe.
- GTM (162KB, long main-thread tasks, forced reflow) — delayed injection until `window.load`.
- Font-display fallback on Astra icon font — switched to `optional`.
- Swiper slide images with empty `src` and no reserved space (CLS risk) — added `aspect-ratio` to `.swiper-slide-image`.
- Further recompression of facility-250 / hero-lakeside-view / facility-212 variants.
- Cache lifetimes on Cloudflare beacon.min.js / email-decode.min.js — confirmed out of our control (Cloudflare-managed, not files in this repo).

## Round 3 — 2026-08-04 1:20 PM report (mobile score 85) — IN PROGRESS

### Image delivery — 500KB savings (the big one this round)
Four below-the-fold "large" images were shipping their full WordPress "large" size instead of what's actually displayed, and all had fake `srcset` entries that pointed at the same file for every width (no real size variants existed):
- `facility-210.webp` — delivered 1440×810 for a 651×366 display box (198KB waste) + needed more compression (59.6KB).
- `facility-202.webp` — delivered 1104×1280 for a 651×755 display box (173KB waste) + compression (35.8KB). Its `srcset` also referenced a dead file (`Camp-99-asia-camp99asia-202-259x300_a085e7.jpg`, never existed on disk).
- `facility-225.webp` — delivered 960×631 for a 651×428 display box (28.2KB waste).
- `facility-212-1024w.webp` (from round 1's srcset) — still 15.8KB of compression headroom.
- `facility-230.webp` — 4.6KB of compression headroom (low priority).
- `facility-250.webp` (background overlay) — still 43.6KB of compression headroom on top of round 2's pass.
- `hero-lakeside-view.webp` (background) — still 11.4KB of compression headroom.

**Fix applied**: resized each base file down to its actual "large" WordPress size (1024w/883w/960w), generated real 300w/768w variants (not duplicate references), fixed the `srcset` attributes to point at the real files, dropped the dead jpg reference, and recompressed. `facility-250` and `hero-lakeside-view` were pushed to more aggressive compression again — they're both near the floor of what WebP lossy encoding can squeeze at this resolution without visible banding, so further gains there are marginal.

### Reduce unused CSS — 62KB (not attempted, documented in round 2, still open)
`vf6z_066dfd.css` (32.1KB) and `common-head.css` (30KB) are shared theme CSS loaded site-wide. Purging requires auditing every page that shares them — flagged for a dedicated pass, not attempted per-page.

### Reduce unused JS — 129KB (not attempted, documented in round 2, still open)
GTM (68.4KB) is third-party and can't be trimmed. `swiper.min.js` (38.4KB) and jQuery (22.5KB) are full third-party libraries; trimming needs a real build/tree-shake step, out of scope for a manual pass.

### Minify CSS — 2KB (skipped)
Negligible savings on a 278KB hand-shared stylesheet; not worth the corruption risk of manual minification.

### Trust and Safety (from round 1's report, not reprinted in rounds 2/3 but still applies — Cloudflare edge, not app code)
- No CSP header (High severity)
- No HSTS `preload` directive (Medium)
- No COOP header (High)
- No CSP Trusted Types directive (High)
These are Cloudflare Pages response-header level, not something this repo's HTML/CSS controls directly — would need a `_headers` file entry or a Cloudflare Transform Rule. Flagged as an open item, not yet actioned.

### Forced reflow / long main-thread tasks from GTM
Still shows up (159ms + 92ms tasks) even after the `window.load` defer, since GTM's own script does synchronous DOM reads on init. This is upstream in Google's script, not something we can patch from our side beyond further delaying load (already delayed to `window.load`, further delay would visibly lag analytics).

### Non-composited animations (96 elements, informational)
Report lists `border-*-width`, `margin-*`, `padding-*`, `color`, `outline-width` etc. as "Unsupported CSS Property" against nearly every Elementor widget wrapper. This is Elementor's transition/hover CSS applying non-GPU-accelerated properties broadly (borders, margins, colors) — a site-wide Elementor theme behavior, not a one-off bug. Fixing means rewriting Elementor's generated hover/transition CSS to isolate composited-only properties (transform/opacity), which risks breaking hover effects across the whole site. Flagged, not attempted this round — needs a dedicated animation-audit pass, see `animation-decision-framework` skill if picked up later.
