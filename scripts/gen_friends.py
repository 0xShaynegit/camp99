import sys
sys.path.insert(0, 'scripts')
from build_inner_page import build_page
import html

marker = '/ 01'
heading = 'Can you help?'
paragraphs = [
    'Five rai is big, over 2.5 acres! If you want to help this ministry by coming out to do improvement projects, maintenance, or gardening, please let me know. We have beautification and painting projects still to do. “Friends of 99” could also use some advisors and you’re welcome to put it on a list of your own ministry efforts in Chiang Mai if you get involved in that way.'
]
callout = 'Thank you if you can help!'

content = ['<section class="page-content"><div class="page-content__inner">']
content.append(f'<span class="section-marker">{marker}</span>')
content.append(f'<h2>{heading}</h2>')
for p in paragraphs:
    content.append(f'<p>{html.escape(p)}</p>')
content.append(f'<p class="page-content__callout">{html.escape(callout)}</p>')
content.append('</div></section>')

html_out = build_page(
    slug='friends-of-camp-99',
    title='Friends of Camp 99 - Camp 99',
    description='FRIENDS OF CAMP 99 – Five rai is big, over 2.5 acres! If you want to help this ministry by coming out to do improvement projects, maintenance, or gardening, please let us know.',
    hero_img='camp99asia-camp99-asia-friends-header-banner.webp',
    hero_h1='Friends of Camp 99',
    content_html='\n'.join(content),
)
open('pages/friends-of-camp-99.html', 'w', encoding='utf-8').write(html_out)
print('wrote', len(html_out), 'chars')
