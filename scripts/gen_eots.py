# -*- coding: utf-8 -*-
import sys, re
sys.path.insert(0, 'scripts')
from build_inner_page import build_page, build_carousel

data = open('pages/end-of-the-spear.html', encoding='utf-8').read()

# --- hero title + pull-quote ---
hero_h1 = 'END of the SPEAR'
hero_subtitle = '&#8220;Without question, this is one of the most compelling stories of the 20th century&#8221;'

# --- carousel (top of page) ---
carousel_images = [
    'camp99asia-camp99-asia-end-of-the-spear-32.webp',
    'camp99asia-camp99-asia-end-of-the-spear-16.webp',
    'camp99asia-camp99-asia-end-of-the-spear-14.webp',
    'camp99asia-camp99-asia-end-of-the-spear-15.webp',
    'camp99asia-camp99-asia-end-of-the-spear-34.webp',
    'camp99asia-camp99-asia-end-of-the-spear-25.webp',
    'camp99asia-camp99-asia-end-of-the-spear-23.webp',
    'camp99asia-camp99-asia-end-of-the-spear-03.webp',
    'camp99asia-camp99-asia-end-of-the-spear-39.webp',
]

# --- main article body: from "On the set" heading through "The women reach out" section ---
start = data.find('On the set  of &quot;End of the Spear&quot;')
if start == -1:
    start = data.find('>On the set  of')
end_marker = data.find('HE IS NO FOOL WHO GIVES UP')
section = data[start:end_marker] if start != -1 and end_marker != -1 else ''

def img_attr(tag, name):
    m = re.search(name + r'="([^"]*)"', tag)
    return m.group(1) if m else None

token_re = re.compile(
    r'<h[23][^>]*>(?P<heading>.*?)</h[23]>'
    r'|<p>(?P<para>.*?)</p>'
    r'|(?P<img><img[^>]*wp-image-\d+[^>]*>)',
    re.S
)
blocks = []
for m in token_re.finditer(section):
    if m.group('heading') is not None:
        blocks.append(('H', re.sub(r'<br/>', ' ', m.group('heading')).strip()))
    elif m.group('para') is not None:
        blocks.append(('P', m.group('para')))
    elif m.group('img') is not None:
        tag = m.group('img')
        imgsrc = img_attr(tag, 'src')
        if imgsrc:
            imgsrc = imgsrc.replace('../images/', '')
        blocks.append(('IMG', imgsrc, img_attr(tag, 'width') or '800', img_attr(tag, 'height') or '600'))

body = ['<section class="page-content"><div class="page-content__inner page-content__inner--article">']
# first block is the "On the set..." heading itself
first = True
for b in blocks:
    if b[0] == 'H':
        tag = 'h2' if first else 'h3'
        body.append(f'<{tag} class="page-content__subhead">{b[1]}</{tag}>')
        first = False
    elif b[0] == 'P':
        body.append(f'<p>{b[1]}</p>')
    elif b[0] == 'IMG':
        _, imgsrc, w, h = b
        if imgsrc:
            body.append(f'<img class="page-content__article-img" src="../images/{imgsrc}" width="{w}" height="{h}" loading="lazy" alt="End of the Spear">')
body.append(f'<p class="page-content__callout">&#8220;He is no fool who gives up what he cannot keep, to gain what he cannot lose.&#8221;</p>')
body.append('</div></section>')

# --- closing "Related Books" section ---
books_html = '''<section class="page-content"><div class="page-content__inner page-content__inner--article">
<h3 class="page-content__subhead">End of the Spear Related Books</h3>
<p><a href="https://www.amazon.com/End-Spear-Steve-Saint-ebook/dp/B00DW9NCSS/" rel="noopener" target="_blank"><i>End of the Spear</i></a>, by Steve Saint &mdash; <a href="https://www.amazon.com/Through-Gates-Splendor-Elisabeth-Elliot-ebook/dp/B007V699S0/" rel="noopener" target="_blank"><i>Through Gates of Splendor</i></a>, by Elisabeth Elliot</p>
<p><a href="https://www.amazon.com/Jungle-Pilot-Martyred-Missionary-Ecuador-ebook/dp/B06WLP8PH6/" rel="noopener" target="_blank"><i>Jungle Pilot</i></a>, by Nate Saint &mdash; <a href="https://www.amazon.com/Savage-My-Kinsman-True-Story/dp/0892830999/" rel="noopener" target="_blank"><i>The Savage, My Kinsman</i></a>, by Elisabeth Elliot</p>
<p style="opacity:0.7;font-size:22px;">All photos copyright 2004, Every Tribe Entertainment. Photos by Robert Bowling.</p>
</div></section>'''

content = '\n'.join(body) + '\n' + build_carousel(carousel_images) + '\n' + books_html

html_out = build_page(
    slug='end-of-the-spear',
    title='End of the Spear - Camp 99',
    description='END of the SPEAR - a magazine article by Robert Bowling on the set of "End of the Spear", the movie based on actual events.',
    hero_img=None,
    hero_h1=hero_h1,
    hero_subtitle=hero_subtitle,
    content_html=content,
)
with open('pages/end-of-the-spear.html', 'w', encoding='utf-8') as f:
    f.write(html_out)
print('wrote', len(html_out), 'chars,', len(blocks), 'body blocks')
