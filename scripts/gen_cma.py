import sys
sys.path.insert(0, 'scripts')
from build_inner_page import build_page
import html

links = [
    ('http://www.chiangmaiambassador.com/best-chiang-mai/', 'The Best Chiang Mai Resources'),
    ('https://chiangmaiambassador.com/pages/living-better-in-thailand', 'Living Better in Thailand'),
    ('https://www.chiangmaiambassador.com/guides/chiang-mai-festivals', 'Chiang Mai Festivals Guide'),
]

content = ['<section class="page-content"><div class="page-content__inner">']
content.append('<h2>Chiang Mai Ambassador and the Best Resources in Chiang Mai and Getting Connected</h2>')
content.append('<p>Here are some useful resources from the Chiang Mai Ambassador</p>')
content.append('<ul class="page-content__linklist">')
for href, label in links:
    content.append(f'<li><a href="{href}" rel="noopener" target="_blank">{html.escape(label)}</a></li>')
content.append('</ul>')
content.append('</div></section>')

html_out = build_page(
    slug='chiang-mai-ambassador',
    title='Chiang Mai Ambassador - Camp 99',
    description='Chiang Mai Ambassador - useful resources from the Chiang Mai Ambassador for getting connected in Chiang Mai.',
    hero_img='camp99asia-camp99-asia-chiang-mai-ambassador-partner.webp',
    hero_h1='Chiang Mai Ambassador',
    content_html='\n'.join(content),
)
open('pages/chiang-mai-ambassador.html', 'w', encoding='utf-8').write(html_out)
print('wrote', len(html_out), 'chars')
