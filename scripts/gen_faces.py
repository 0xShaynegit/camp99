import sys
sys.path.insert(0, 'scripts')
from build_inner_page import build_page, build_carousel
import html

marker = '/ 01'
callout = 'Let me know if I can help you!'

carousel_images = [
    'camp99asia-camp99-asia-portrait-08.webp',
    'camp99asia-camp99-asia-portrait-13.webp',
    'camp99asia-camp99-asia-portrait-11.webp',
    'camp99asia-camp99-asia-portrait-07.webp',
    'camp99asia-camp99-asia-photo-class-02.webp',
    'camp99asia-camp99-asia-portrait-24.webp',
    'camp99asia-camp99-asia-portrait-27.webp',
    'camp99asia-camp99-asia-portrait-18.webp',
    'camp99asia-camp99-asia-portrait-16.webp',
    'camp99asia-camp99-asia-portrait-01.webp',
    'camp99asia-camp99-asia-portrait-12.webp',
    'camp99asia-camp99-asia-portrait-21.webp',
    'camp99asia-camp99-asia-portrait-20.webp',
    'camp99asia-camp99-asia-portrait-17.webp',
    'camp99asia-camp99-asia-portrait-23.webp',
    'camp99asia-camp99-asia-portrait-14.webp',
    'camp99asia-camp99-asia-portrait-10.webp',
    'camp99asia-camp99-asia-portrait-06.webp',
    'camp99asia-camp99-asia-portrait-15.webp',
    'camp99asia-camp99-asia-portrait-19.webp',
    'camp99asia-camp99-asia-portrait-09.webp',
    'camp99asia-camp99-asia-portrait-05.webp',
    'camp99asia-camp99-asia-portrait-02.webp',
    'camp99asia-camp99-asia-portrait-25.webp',
    'camp99asia-camp99-asia-portrait-03.webp',
    'camp99asia-camp99-asia-portrait-04.webp',
    'camp99asia-camp99-asia-portrait-22.webp',
    'camp99asia-camp99-asia-portrait-26.webp',
]

content = ['<section class="page-content"><div class="page-content__inner">']
content.append(f'<span class="section-marker">{marker}</span>')
content.append(f'<p class="page-content__callout">{html.escape(callout)}</p>')
content.append('</div></section>')
content.append(build_carousel(carousel_images))

html_out = build_page(
    slug='faces-of-thailand',
    title='Faces of Thailand - Camp 99',
    description='Faces of Thailand - DigitalMission Media. A gallery of portrait photography from Chiang Mai and northern Thailand.',
    hero_img='camp99asia-camp99-asia-page-header-banner.webp',
    hero_h1='Faces of Thailand',
    content_html='\n'.join(content),
)
open('pages/faces-of-thailand.html', 'w', encoding='utf-8').write(html_out)
print('wrote', len(html_out), 'chars')
