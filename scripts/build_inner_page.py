import html

HEAD_TEMPLATE = '''<!DOCTYPE html>
<html lang="en-US" prefix="og: https://ogp.me/ns#">
<head>
  <!-- Google tag (gtag.js) -->
  <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){{dataLayer.push(arguments);}}
    gtag('js', new Date());
    gtag('config', 'G-VZ7EQZDMK6');
    function loadGtagScript(){{
      if (window.__gtagScriptLoaded) return;
      window.__gtagScriptLoaded = true;
      var s = document.createElement('script');
      s.async = true;
      s.src = 'https://www.googletagmanager.com/gtag/js?id=G-VZ7EQZDMK6';
      document.head.appendChild(s);
      ['scroll','mousemove','touchstart','keydown','click'].forEach(function(evt){{
        window.removeEventListener(evt, loadGtagScript, {{passive:true}});
      }});
    }}
    ['scroll','mousemove','touchstart','keydown','click'].forEach(function(evt){{
      window.addEventListener(evt, loadGtagScript, {{passive:true}});
    }});
    window.addEventListener('load', function(){{
      setTimeout(loadGtagScript, 5000);
    }});
  </script>

<meta charset="utf-8"/>
<meta content="width=device-width, initial-scale=1" name="viewport"/>
<link href="https://gmpg.org/xfn/11" rel="profile"/>
<title>{title}</title>
<meta content="{description}" name="description"/>
<meta content="follow, index, max-snippet:-1, max-video-preview:-1, max-image-preview:large" name="robots"/>
<link href="https://camp99.asia/pages/{slug}.html" rel="canonical"/>
<meta content="en_US" property="og:locale"/>
<meta content="website" property="og:type"/>
<meta content="{title}" property="og:title"/>
<meta content="{description}" property="og:description"/>
<meta content="https://camp99.asia/pages/{slug}.html" property="og:url"/>
<meta content="Camp 99" property="og:site_name"/>
<meta property="og:image" content="https://camp99.asia/images/camp99asia-camp99-asia-logo.webp">
<meta content="summary_large_image" name="twitter:card"/>
<meta content="{title}" name="twitter:title"/>
<meta content="{description}" name="twitter:description"/>
<link rel="preload" href="../fonts/racingsansone-sykr-yrtm7evtrxnxkv5jfkkydcakhdn_0d14ba.woff2" as="font" type="font/woff2" crossorigin/>
<link rel="preload" href="../fonts/fonts.css" as="style">
<link rel="stylesheet" href="../fonts/fonts.css" media="print" onload="this.media='all'">
<noscript><link rel="stylesheet" href="../fonts/fonts.css"></noscript>
<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "LocalBusiness",
  "name": "Camp 99",
  "url": "https://camp99.asia",
  "logo": "https://camp99.asia/images/camp99asia-camp99-asia-logo.webp",
  "description": "Camp 99 is a day-use meeting, retreat, and recreation center in Chiang Mai for Christian groups, sports events, and community gatherings.",
  "contactPoint": {{
    "@type": "ContactPoint",
    "contactType": "Customer Service",
    "email": "info@camp99.asia"
  }},
  "address": {{
    "@type": "PostalAddress",
    "streetAddress": "Chiang Mai",
    "addressCountry": "TH"
  }},
  "geo": {{
    "@type": "GeoCoordinates",
    "latitude": "18.783900600000003",
    "longitude": "99.0730178935791"
  }}
}}
</script>
<link rel="stylesheet" href="../styles/main.css"/>
</head>
'''

NAV_ITEMS = [
    ('friends-of-camp-99', 'Friends of Camp 99', None),
    ('digitalmission-media', 'DigitalMission Media', [
        ('ministry-photos', 'Still Photography', [
            ('media-training-sessions', 'Media Training Sessions'),
            ('prayer-card-portraits', 'Prayer Card Portraits'),
            ('faces-of-thailand', 'Faces of Thailand'),
            ('drone-images', 'Drone Images'),
            ('bob-on-the-go', 'Bob on the go'),
        ]),
        ('sample-video-projects', 'Sample Video Projects', None),
        ('a-journey-to-remember', 'A Journey to Remember', None),
        ('end-of-the-spear', 'End of the Spear', None),
    ]),
    ('visit-bob', 'Visit Thailand', [
        ('chiang-mai-ambassador', 'Chiang Mai Ambassador', None),
        ('visit-bob', 'Visit Bob', None),
        ('thenextstep', 'The Next Step', None),
    ]),
]

CARET = '''<svg class="nav-caret" width="14" height="10" viewBox="0 0 14 10" aria-hidden="true">
              <path d="M0 1l7 8 7-8z" fill="currentColor"/>
            </svg>'''

def render_nav(current_slug):
    out = ['<ul class="site-nav__list">']
    for slug, label, children in NAV_ITEMS:
        active = ' class="is-active"' if slug == current_slug else ''
        if children:
            open_cls = ' is-open' if any(c[0] == current_slug for c in children for c in ([c] if len(c) == 2 else [c] + (c[2] or []))) else ''
            out.append(f'<li class="has-children">')
            out.append(f'<a href="/pages/{slug}.html"{active}>{label}</a>')
            out.append(f'<button class="submenu-toggle" aria-expanded="false" aria-label="Toggle submenu">{CARET}</button>')
            out.append('<ul class="sub-menu">')
            for child in children:
                cslug, clabel = child[0], child[1]
                cchildren = child[2] if len(child) > 2 else None
                cactive = ' class="is-active"' if cslug == current_slug else ''
                if cchildren:
                    out.append('<li class="has-children">')
                    out.append(f'<a href="/pages/{cslug}.html"{cactive}>{clabel}</a>')
                    out.append(f'<button class="submenu-toggle" aria-expanded="false" aria-label="Toggle submenu">{CARET}</button>')
                    out.append('<ul class="sub-menu">')
                    for gslug, glabel in cchildren:
                        gactive = ' class="is-active"' if gslug == current_slug else ''
                        out.append(f'<li><a href="/pages/{gslug}.html"{gactive}>{glabel}</a></li>')
                    out.append('</ul></li>')
                else:
                    out.append(f'<li><a href="/pages/{cslug}.html"{cactive}>{clabel}</a></li>')
            out.append('</ul></li>')
        else:
            out.append(f'<li><a href="/pages/{slug}.html"{active}>{label}</a></li>')
    out.append('</ul>')
    return '\n        '.join(out)

HEADER_TEMPLATE = '''<body>
<header class="site-header">
  <div class="container site-header__inner">
    <a href="../index.html" class="site-logo">
      <img src="../images/camp99asia-camp99-asia-logo.webp"
           srcset="../images/camp99asia-camp99-asia-logo.webp 300w, ../images/camp99asia-camp99-asia-logo.webp 450w"
           sizes="(max-width: 300px) 100vw, 300px"
           width="300" height="100" alt="Camp 99">
    </a>
    <button class="nav-toggle" aria-expanded="false" aria-controls="site-nav" aria-label="Toggle Menu">
      <span></span><span></span><span></span>
    </button>
    <nav id="site-nav" class="site-nav" aria-label="Site Navigation">
      {nav}
    </nav>
  </div>
</header>
<main>
'''

FOOTER_TEMPLATE = '''</main>
<footer class="site-footer">
  <div class="container site-footer__inner">
    <div class="site-footer__contact">
      <h3>contact</h3>
      <p>Email&hellip;&hellip;&hellip;&hellip;&hellip;&hellip;&hellip;&hellip;&hellip;&hellip;&hellip;&hellip;&hellip;&hellip;<a href="mailto:info@camp99.asia">info@camp99.asia</a></p>
      <p>Phone Bob Bowling&hellip;&hellip;&hellip;&hellip;&hellip;&hellip;&hellip;&hellip;&hellip;..082-192-1665</p>
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
    <div class="site-footer__links">
      <a href="https://www.paypal.me/DigitalMissionUS" rel="noopener" target="_blank">DONATE NOW with PAYPAL.</a>
      <a href="https://Camp99.asia/tax-deductible-donations/">Tax Deductible Donations - Please Click HERE.</a>
      <a href="https://Camp99.asia/disclaimer/">Disclaimer</a>
    </div>
    <p class="site-footer__copyright">Copyright &copy; 2026 Camp 99. All rights reserved.</p>
  </div>
  <button class="scroll-to-top" aria-label="Scroll to top" hidden>&#8593;</button>
</footer>
<script src="../scripts/main.js"></script>
</body>
</html>
'''

def build_carousel(image_files):
    items = []
    for f in image_files:
        items.append(f'<img class="carousel__item" src="../images/{f}" loading="lazy" alt="Camp 99 asia camp99asia">')
    return f'''<section class="page-gallery-carousel container">
  <div class="carousel" role="region" aria-label="Photo gallery">
    <button class="carousel__btn carousel__btn--prev" aria-label="Previous image">&#8249;</button>
    <div class="carousel__track">
      {chr(10).join(items)}
    </div>
    <button class="carousel__btn carousel__btn--next" aria-label="Next image">&#8250;</button>
  </div>
</section>
'''

def build_page(slug, title, description, hero_img, hero_h1, content_html, hero_subtitle=None):
    head = HEAD_TEMPLATE.format(title=html.escape(title), description=html.escape(description), slug=slug)
    header = HEADER_TEMPLATE.format(nav=render_nav(slug))
    bg_img = f'<img class="page-hero__bg" src="../images/{hero_img}" loading="lazy" alt="">' if hero_img else ''
    subtitle = f'<p class="page-hero__subtitle">{hero_subtitle}</p>' if hero_subtitle else ''
    hero = f'''<section class="page-hero">
  {bg_img}
  <div class="page-hero__content container">
    <span class="page-hero__rule"></span>
    <h1>{html.escape(hero_h1)}</h1>
    {subtitle}
  </div>
</section>
'''
    return head + header + hero + content_html + FOOTER_TEMPLATE
