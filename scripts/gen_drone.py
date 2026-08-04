import sys
sys.path.insert(0, 'scripts')
from build_inner_page import build_page, build_carousel
import html

marker = '/ 01'
heading = 'DigitalMission Media'
paragraphs_before_image = [
    'My amazing students posing at our excursion to a waterfall!',
]
paragraphs_after = [
    'Sometimes I have been asked to teach three days or a week of classes in Still Photography. (Some folks know that I was the Stills Photographer on the movie, “End of the Spear” and have seen the website for that. I plan to get a page on this Camp 99 website that shows some of those photos in the near future.)',
    'I studied Photography and Art and have worked for three newspapers as a photojournalist. I love to teach people how to take better photos. I’ve taught classes in Chiang Mai for YWAM (Youth With A Mission) at their School of Frontier Media, and also for Project Video, to teach composition and how still cameras work. Here are a few photos from teaching those classes. (Under construction, more photos are on the way… once I find them in another hard drive!)',
]
callout = 'Let me know if I can help you!'

carousel_images = [
    'camp99asia-camp99-asia-ministry-photo-43-2.webp',
    'camp99asia-camp99-asia-photo-class-05.webp',
    'camp99asia-camp99-asia-photo-class-02.webp',
    'camp99asia-camp99-asia-ministry-photo-50.webp',
    'camp99asia-camp99-asia-photo-class-04.webp',
    'camp99asia-camp99-asia-photo-class-03.webp',
    'camp99asia-camp99-asia-photo-class-06.webp',
    'camp99asia-camp99-asia-photo-class-01.webp',
]

content = ['<section class="page-content"><div class="page-content__inner">']
content.append(f'<span class="section-marker">{marker}</span>')
content.append(f'<h2>{heading}</h2>')
content.append('<img class="page-content__figure" src="../images/camp99asia-camp99-asia-ministry-photo-43.webp" width="300" height="288" loading="lazy" alt="Camp 99 asia camp99asia">')
for p in paragraphs_before_image + paragraphs_after:
    content.append(f'<p>{html.escape(p)}</p>')
content.append(f'<p class="page-content__callout">{html.escape(callout)}</p>')
content.append('</div></section>')
content.append(build_carousel(carousel_images))

html_out = build_page(
    slug='drone-images',
    title='Drone Images - Camp 99',
    description='Drone Photos and Videos - DigitalMission Media. Photography class photos and training sessions in Chiang Mai.',
    hero_img='camp99asia-camp99-asia-page-header-banner.webp',
    hero_h1='Drone Photos and Videos',
    content_html='\n'.join(content),
)
open('pages/drone-images.html', 'w', encoding='utf-8').write(html_out)
print('wrote', len(html_out), 'chars')
