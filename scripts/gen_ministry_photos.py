import sys
sys.path.insert(0, 'scripts')
from build_inner_page import build_page, build_carousel
from _ministry_photos_list import IMAGES
import html

marker = '/ 01'
paragraphs = [
    'Here are some photos of assorted ministry projects. I love going to the mountain villages to visit the tribal people. Many missions and ministries in Chiang Mai seek to assist, evangelize, and teach the Akha, Karen, Lahu, Lisu, Hmong, and other minority tribal groups in Thailand.',
    'Sometimes I visit villages or churches to help mission groups, and sometimes I visit (and take photos of course!) at the request of friends I know there. I have helped Christian schools, mission groups, individual missionaries, local churches and even done a few weddings… in Chiang Mai and in the mountains.',
    'All of this is FREE since I cannot earn money in Thailand… just helping people in the name of the Lord! (And with financial and prayer support from awesome sponsors… that’s why I often say “We” are helping these people!)',
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
    slug='ministry-photos',
    title='Ministry Photos - Camp 99',
    description='Ministry Photos - DigitalMission Media. Photos of assorted ministry projects with tribal groups in Chiang Mai and northern Thailand.',
    hero_img='camp99asia-camp99-asia-page-header-banner.webp',
    hero_h1='Ministry Photos',
    content_html='\n'.join(content),
)
open('pages/ministry-photos.html', 'w', encoding='utf-8').write(html_out)
print('wrote', len(html_out), 'chars')
