import sys
sys.path.insert(0, 'scripts')
from build_inner_page import build_page
import html

paragraphs = [
    'THAILAND is always a top ten best tourist country in the world! And certainly when you factor in cost, you get more days or weeks for your money than many other places like Hawaii, the Caribbean, Japan, or anywhere in Europe.',
    'Most people who visit Thailand will go to 1) The turquoise islands and beaches of the south, 2) Bustling Bangkok with the Royal Palace, floating market, and amazing restaurants, and 3) Chiang Mai in the north country, with our cooler climate, scenic mountains, elephant parks, and fascinating hilltribe villages.',
    'Chiang Mai area is often called the “Colorado Springs of Asia” due to the 250+ mission groups based here. (Also called the “Silicon Valley of mission groups.”) If you visit me I can show you around to a number of other mission groups to get a good overview of what is happening in northern Thailand for Christian schools, children’s homes, Bible Colleges, and outreach efforts. A trip here can be a ‘bucket list” adventure in seeing both “Amazing Thailand” as a tourist, and also what is happening in the missions community, either as a first-time observer, or on a Short Term Mission project. It is VERY safe here and the food is wonderful and healthy, not a worry.',
    'Round-trip airfare runs about $1100 to $1500 (Int’l seating is a bit larger and a full media center will be in the seatback in front of you!) Local expenses are very reasonable: Guesthouse (quaint, garden plants, atmosphere) is $20-30 a night per room (not per person), and a nicer hotel or resort would be $40-60. Meals are just $2 for lunch, and $5-10 for dinner! Also, my house has one A/C room with king-size bed and private bath where you can stay for FREE!',
    'Just do a Google search on Chiang Mai, Bangkok, and/or Beaches of Thailand, and you will get plenty of info. NOTE: Do NOT plan a visit for March or April, it is hot and smokey in the north. May, June, or July are good. (Aug.-Sept. I am likely to be in USA.) October 15th to Feb 1st is best: cool season and no rain! Also lots of festivities in the city and the mountain villages.',
    'Let me know if you are thinking about a trip here, I can help you even more!',
]

content = ['<section class="page-content"><div class="page-content__inner">']
for p in paragraphs:
    content.append(f'<p>{html.escape(p)}</p>')
content.append('<p style="text-align:center;"><a href="http://www.digitalmission.us" rel="noopener" target="_blank" style="font-size:36px;">www.digitalmission.us</a></p>')
content.append('</div></section>')

html_out = build_page(
    slug='visit-bob',
    title='Visit Bob - Camp 99',
    description='THAILAND is always a top ten best tourist country in the world! Visit Bob in Chiang Mai and see northern Thailand.',
    hero_img='camp99asia-camp99-asia-visit-bob-header-banner.webp',
    hero_h1='Visit Bob',
    content_html='\n'.join(content),
)
open('pages/visit-bob.html', 'w', encoding='utf-8').write(html_out)
print('wrote', len(html_out), 'chars')
