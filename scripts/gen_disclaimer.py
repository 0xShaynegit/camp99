import sys
sys.path.insert(0, 'scripts')
from build_inner_page import build_page
import html

paragraphs = [
    'Hello, we are Camp99, we love helping people and I created this website as a resource for just that. The information is provided by Camp99 and while we try to keep the information useful, correct and up to date, we make no representations or warranties of any kind, express or implied, regarding the completeness, reliability, accuracy, suitability or availability with respect to the website or the information, products, services, or related graphics contained on the website for any purpose. Any reliance you place on such information here is strictly at your own risk.',
    'In no event will I be liable for any loss or damage including without limitation, indirect or consequential loss or damage, or any loss or damage whatsoever arising from loss of data or profits arising out of, or in connection with, the use of this website.',
    'Through this website you are able to link to other websites which are not under the control of Camp99. I have no control over the nature, content and availability of those sites. The inclusion of any links does not necessarily imply a recommendation or endorse the views expressed within them.',
    'Every effort is made to keep the website up and running smoothly. However, Camp99 takes no responsibility for, and will not be liable for, the website being temporarily unavailable due to technical issues beyond our control.',
]

content = ['<section class="page-content"><div class="page-content__inner">']
for p in paragraphs:
    content.append(f'<p>{html.escape(p)}</p>')
content.append('</div></section>')

html_out = build_page(
    slug='disclaimer',
    title='Disclaimer - Camp 99',
    description='Disclaimer - the information on this website is provided by Camp99 in good faith, but we make no warranties about its completeness or accuracy.',
    hero_img='camp99asia-camp99-asia-page-header-banner.webp',
    hero_h1='Disclaimer',
    content_html='\n'.join(content),
)
open('pages/disclaimer.html', 'w', encoding='utf-8').write(html_out)
print('wrote', len(html_out), 'chars')
