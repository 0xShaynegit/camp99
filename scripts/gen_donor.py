import sys
sys.path.insert(0, 'scripts')
from build_inner_page import build_page

content = '''<section class="page-content"><div class="page-content__inner">
<p>[give_donor_dashboard]</p>
</div></section>'''

html_out = build_page(
    slug='donor-dashboard',
    title='Donor Dashboard - Camp 99',
    description='Donor Dashboard - [give_donor_dashboard]',
    hero_img='camp99asia-camp99-asia-page-header-banner.webp',
    hero_h1='Donor Dashboard',
    content_html=content,
)
open('pages/donor-dashboard.html', 'w', encoding='utf-8').write(html_out)
print('wrote', len(html_out), 'chars')
