import sys
sys.path.insert(0, 'scripts')
from build_inner_page import build_page, build_carousel
import html

marker = '/ 01'
paragraphs = [
    'In looking through a lot of photos to add to the DigitalMission Media part of The Next Step website I ran across a lot of ME, doing different things here in Thailand. So I’ve included a slide show of “Bob in Thailand”, or we could call it it “Out and About in Thailand.” I love going to the beautiful mountains in my 4×4 Ford Ranger pick-up truck. And it’s often cooler up there! I’ll be looking to add even more photos of my time here in the near future. Any questions about what I’m doing, or how you can help? Just send me an email at eBob777@yahoo.com.'
]
callout = 'Let me know if I can help you!'

carousel_images = [
    'camp99asia-camp99-asia-bob-on-the-go-34.webp',
    'camp99asia-camp99-asia-bob-on-the-go-04.webp',
    'camp99asia-camp99-asia-ministry-photo-53.webp',
    'camp99asia-camp99-asia-bob-on-the-go-02.webp',
    'camp99asia-camp99-asia-bob-on-the-go-07.webp',
    'camp99asia-camp99-asia-bob-on-the-go-12.webp',
    'camp99asia-camp99-asia-bob-on-the-go-40.webp',
    'camp99asia-camp99-asia-bob-on-the-go-28.webp',
    'camp99asia-camp99-asia-bob-on-the-go-14.webp',
    'camp99asia-camp99-asia-bob-on-the-go-32.webp',
    'camp99asia-camp99-asia-bob-on-the-go-01.webp',
    'camp99asia-camp99-asia-bob-on-the-go-06.webp',
    'camp99asia-camp99-asia-bob-on-the-go-26.webp',
    'camp99asia-camp99-asia-bob-on-the-go-19.webp',
    'camp99asia-camp99-asia-bob-on-the-go-38.webp',
    'camp99asia-camp99-asia-bob-on-the-go-20.webp',
    'camp99asia-camp99-asia-bob-on-the-go-36.webp',
    'camp99asia-camp99-asia-ministry-photo-04.webp',
    'camp99asia-camp99-asia-bob-on-the-go-09.webp',
    'camp99asia-camp99-asia-bob-on-the-go-35.webp',
    'camp99asia-camp99-asia-bob-on-the-go-17.webp',
]

content = ['<section class="page-content"><div class="page-content__inner">']
content.append(f'<span class="section-marker">{marker}</span>')
content.append('<h2>DigitalMission Media</h2>')
for p in paragraphs:
    content.append(f'<p>{html.escape(p)}</p>')
content.append(f'<p class="page-content__callout">{html.escape(callout)}</p>')
content.append('</div></section>')
content.append(build_carousel(carousel_images))

html_out = build_page(
    slug='bob-on-the-go',
    title='Bob on the go - Camp 99',
    description='Bob on the go - photos of Bob out and about in Thailand, DigitalMission Media.',
    hero_img='camp99asia-camp99-asia-page-header-banner.webp',
    hero_h1='Bob on the go',
    content_html='\n'.join(content),
)
open('pages/bob-on-the-go.html', 'w', encoding='utf-8').write(html_out)
print('wrote', len(html_out), 'chars')
