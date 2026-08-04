import sys
sys.path.insert(0, 'scripts')
from build_inner_page import build_page
import html

marker = '/ 01'
paragraphs = [
    'THREE SAMPLE VIDEOS: First for an International Church picnic. All photos and video shot and edited by Robert Bowling. Several of my video projects cannot be shown online because they deal with Human Trafficking issues and are not allowed on the internet, only shown ‘live’ by speakers or pastors. (And sometimes we upload to Youtube but put the setting on Private, thus it is not searchable to public, but it is shareable to friends.)',
    'This is a good representation of my media work that is put on websites and also shown during support-raising trips during church services and information gatherings. A video link is also handy to put into e-newsletters!',
]
callout = 'Let me know if I can help you!'

videos = [
    ('https://www.youtube.com/embed/2aePlIC18L8?controls=1&rel=0&playsinline=0&cc_load_policy=0&autoplay=0', 'Camp 99 and DigitalMission Media', 'Church picnic at Camp 99 using my gimbal/steadicam and my DJI drone!'),
    ('https://www.youtube.com/embed/jmXetSOpmIE?controls=1&rel=0&playsinline=0&cc_load_policy=0&autoplay=0', 'Seed of Hope Christmas', 'This video was done as a “Thank You” to USA folks who help sponsor these tribal kids.'),
    ('https://www.youtube.com/embed/wNn6ZITjKq0?controls=1&rel=0&playsinline=0&cc_load_policy=0&autoplay=0', 'Sending Hope Girls Home', 'This video was produced for a home that helps at-risk Hilltribe girls.'),
]

content = ['<section class="page-content"><div class="page-content__inner">']
content.append(f'<span class="section-marker">{marker}</span>')
for p in paragraphs:
    content.append(f'<p>{html.escape(p)}</p>')
content.append('</div></section>')

content.append('<section class="page-content__videos container">')
for src, title, caption in videos:
    content.append(f'<p style="text-align:center;">{html.escape(caption)}</p>')
    content.append(f'''<div class="video-wrapper">
  <iframe class="video-wrapper__frame" src="{src}" title="{html.escape(title)}" loading="lazy"
          allow="accelerometer; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>
</div>''')
content.append(f'<p class="page-content__callout" style="max-width:900px;margin:0 auto;">{html.escape(callout)}</p>')
content.append('</section>')

html_out = build_page(
    slug='sample-video-projects',
    title='Sample Video Projects - Camp 99',
    description='Sample Video Projects - DigitalMission Media. Three sample videos of media work in Chiang Mai, Thailand.',
    hero_img='camp99asia-camp99-asia-page-header-banner.webp',
    hero_h1='Sample Video Projects',
    content_html='\n'.join(content),
)
open('pages/sample-video-projects.html', 'w', encoding='utf-8').write(html_out)
print('wrote', len(html_out), 'chars')
