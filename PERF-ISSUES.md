# camp99.asia PageSpeed issues

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
