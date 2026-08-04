import sys
sys.path.insert(0, 'scripts')
from build_inner_page import build_page, build_carousel
from _pcp_list import IMAGES
import html

marker = '/ 01'
paragraphs = [
    'Occasionally I am asked by missionaries or other Christian people to make a photo portrait, either for their website or, often times, to go on a “Prayer Card” that they will have printed and take home and distribute to sponsors when they are speaking at churches or having information groups about what they do in Thailand.',
    'And of course I sometimes take portraits that will go in digital format, like a slide show or video program.',
    'You’ll also see some photos below that I took at a friend’s wedding, and a few shots of some graduating “Soccer team Seniors” at a local Christian international school.',
    'Remember, I don’t (cannot) work for money in Thailand and do these projects for free because of kind-hearted people who sponsor me from the USA! Here are a few samples of these photos taken of Westerners in our area.',
]
callout = 'Let me know if I can help you!'

content = ['<section class="page-content"><div class="page-content__inner">']
content.append(f'<span class="section-marker">{marker}</span>')
for p in paragraphs:
    content.append(f'<p>{html.escape(p)}</p>')
content.append(f'<p class="page-content__callout">{html.escape(callout)}</p>')
content.append('</div></section>')
content.append(build_carousel(IMAGES))

html_out = build_page(
    slug='prayer-card-portraits',
    title='Prayer Card Portraits - Camp 99',
    description='Prayer Card Portraits - DigitalMission Media. Portrait photography for missionaries prayer cards and support materials.',
    hero_img='camp99asia-camp99-asia-page-header-banner.webp',
    hero_h1='Prayer Card Portraits',
    content_html='\n'.join(content),
)
open('pages/prayer-card-portraits.html', 'w', encoding='utf-8').write(html_out)
print('wrote', len(html_out), 'chars')
