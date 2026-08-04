import re, sys

def strip_hidden(section):
    # Remove any elementor-widget wrapper div whose opening tag carries
    # elementor-hidden-desktop (site theme uses show-on-no-breakpoint === never shown)
    pattern = re.compile(
        r'<div class="elementor-element[^"]*elementor-hidden-desktop[^"]*"[^>]*>.*?</div>\s*</div>\s*</div>',
        re.S
    )
    return pattern.sub('', section)

def extract(path):
    data = open(path, encoding='utf-8').read()
    title = re.search(r'<title>([^<]*)</title>', data)
    title = title.group(1) if title else ''
    desc = re.search(r'<meta content="([^"]*)" name="description"', data)
    desc = desc.group(1) if desc else ''

    hero_id_m = re.search(r'elementor-element-([0-9a-f]{6,8}) elementor-section-content-middle', data)
    hero_img = None
    if hero_id_m:
        hero_id = hero_id_m.group(1)
        post_id_m = re.search(r'data-elementor-id="(\d+)"', data)
        if post_id_m:
            try:
                css = open(f'css/post-{post_id_m.group(1)}_b187d0.css', encoding='utf-8').read()
                img_m = re.search(re.escape(hero_id) + r'[^{]*\{[^}]*background-image:url\(\.\./images/([^)]*)\)', css)
                if img_m:
                    hero_img = img_m.group(1)
            except FileNotFoundError:
                pass

    i = data.find('<h1 class="elementor-heading-title')
    k = data.find('id="colophon"')
    section = data[i:k] if i >= 0 and k >= 0 else ''
    section = strip_hidden(section)

    items = []
    pattern = re.compile(
        r'<h([1-6])[^>]*>([^<]*)</h[1-6]>'
        r'|<blockquote><h3><span[^>]*>([^<]*)</span></h3></blockquote>'
        r'|<p>(.*?)</p>'
        r'|<div dir="ltr">([^<]*)</div>'
        r'|<img[^>]*src="([^"]*)"[^>]*width="(\d+)"[^>]*height="(\d+)"',
        re.S
    )
    for m in pattern.finditer(section):
        if m.group(1) is not None:
            items.append(('H' + m.group(1), m.group(2).strip()))
        elif m.group(3) is not None:
            items.append(('CALLOUT', m.group(3).strip()))
        elif m.group(4) is not None:
            txt = re.sub(r'<[^>]+>', ' ', m.group(4)).strip()
            if txt:
                items.append(('P', txt))
        elif m.group(5) is not None:
            txt = m.group(5).strip()
            if txt and txt != '​':
                items.append(('DIV', txt))
        elif m.group(6) is not None:
            items.append(('IMG', m.group(6), m.group(7), m.group(8)))

    return {'title': title, 'desc': desc, 'hero_img': hero_img, 'items': items}

if __name__ == '__main__':
    result = extract(sys.argv[1])
    lines = []
    lines.append('TITLE: ' + result['title'])
    lines.append('DESC: ' + result['desc'][:150])
    lines.append('HERO_IMG: ' + str(result['hero_img']))
    lines.append('---ITEMS---')
    for it in result['items']:
        lines.append(str(it))
    out = '\n'.join(lines)
    sys.stdout.buffer.write(out.encode('utf-8'))
    sys.stdout.buffer.write(b'\n')
