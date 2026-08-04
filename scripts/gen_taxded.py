import sys
sys.path.insert(0, 'scripts')
from build_inner_page import build_page
import html

content = ['<section class="page-content"><div class="page-content__inner">']
content.append('<p>501(c)(3) tax-deductible donations can be sent to the wonderful CMI folks in Florida.</p>')
content.append('<p>Payable to: &#8220;CMI&#8221;</p>')
content.append('<p>Christian Ministries Inc.<br>&#8453; J. Nixon Daniel, III<br>Beggs &amp; Lane, RLLP<br>501 Commendencia Street<br>Pensacola, FL 32502</p>')
content.append('<p>Please note on separate paper it is for Robert Bowling or DigitalMission.</p>')
content.append('<p class="page-content__callout">THANK YOU so much!</p>')
content.append('</div></section>')

html_out = build_page(
    slug='tax-deductible-donations',
    title='Tax Deductible Donations - Camp 99',
    description='501(c)(3) tax-deductible donations can be sent to the wonderful CMI folks in Florida.',
    hero_img='camp99asia-camp99-asia-donations-header-banner.webp',
    hero_h1='Donations',
    content_html='\n'.join(content),
)
open('pages/tax-deductible-donations.html', 'w', encoding='utf-8').write(html_out)
print('wrote', len(html_out), 'chars')
