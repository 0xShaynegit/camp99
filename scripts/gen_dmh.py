# -*- coding: utf-8 -*-
import sys
sys.path.insert(0, 'scripts')
from build_inner_page import build_page

inner = open('scripts/_dmh_inner.html', encoding='utf-8').read()

content = f'''<section class="page-content"><div class="page-content__inner page-content__wall">
{inner}
</div></section>'''

html_out = build_page(
    slug='digital-mission-home',
    title='Digital Mission Home - Camp 99',
    description='DigitalMission Home - photography, video, journalism, and media work in Chiang Mai, Thailand.',
    hero_img=None,
    hero_h1='Digital Mission Home',
    content_html=content,
)
with open('pages/digital-mission-home.html', 'w', encoding='utf-8') as f:
    f.write(html_out)
print('wrote', len(html_out), 'chars')
