# -*- coding: utf-8 -*-
import sys, re
sys.path.insert(0, 'scripts')
from build_inner_page import build_page

src = open('scripts/_ajtr_original.html', encoding='utf-8').read()
i = src.find('<h2 class="elementor-heading-title elementor-size-medium">')
j = src.find('id="colophon"')
section = src[i:j]

# Walk the section in document order, pulling out headings, paragraphs
# (raw HTML preserved - inline <em>/<a>/etc kept intact), and content images.
# Skip Elementor decorative widgets (dividers, the flower icon graphic) entirely.
token_re = re.compile(
    r'<h2[^>]*>(?P<heading>.*?)</h2>'
    r'|<p>(?P<para>.*?)</p>'
    r'|(?P<img><img[^>]*wp-image-\d+[^>]*>)',
    re.S
)

def img_attr(tag, name):
    m = re.search(name + r'="([^"]*)"', tag)
    return m.group(1) if m else None

blocks = []
for m in token_re.finditer(section):
    if m.group('heading') is not None:
        text = re.sub(r'<br/>', ' ', m.group('heading')).strip()
        blocks.append(('H', text))
    elif m.group('para') is not None:
        blocks.append(('P', m.group('para')))
    elif m.group('img') is not None:
        tag = m.group('img')
        if 'wp-image-959' in tag:  # the small flower divider graphic - skip, purely decorative
            continue
        imgsrc = img_attr(tag, 'src')
        if imgsrc:
            imgsrc = imgsrc.replace('../images/', '')
        blocks.append(('IMG', imgsrc, img_attr(tag, 'width'), img_attr(tag, 'height')))

# First heading is the page title itself (already used as hero_h1) - drop it from the body.
body_blocks = blocks[1:]

content = ['<section class="page-content"><div class="page-content__inner page-content__inner--article">']
for b in body_blocks:
    if b[0] == 'H':
        content.append(f'<h2 class="page-content__subhead">{b[1]}</h2>')
    elif b[0] == 'P':
        content.append(f'<p>{b[1]}</p>')
    elif b[0] == 'IMG':
        _, imgsrc, w, h = b
        content.append(f'<img class="page-content__article-img" src="../images/{imgsrc}" width="{w}" height="{h}" loading="lazy" alt="A Journey to Remember">')
content.append('</div></section>')

html_out = build_page(
    slug='a-journey-to-remember',
    title='A Journey to Remember - Camp 99',
    description='A Journey to Remember - the story of Alice Kern’s return to Bergen-Belsen and Auschwitz, filmed by Robert Bowling in 1995.',
    hero_img='camp99asia-camp99-asia-journey-to-remember-auschwitz-34.webp',
    hero_h1='A Journey to Remember',
    content_html='\n'.join(content),
)
with open('pages/a-journey-to-remember.html', 'w', encoding='utf-8') as f:
    f.write(html_out)
print('wrote', len(html_out), 'chars,', len(body_blocks), 'blocks')
