import sys, re
sys.path.insert(0, 'scripts')
from build_inner_page import HEAD_TEMPLATE, HEADER_TEMPLATE, FOOTER_TEMPLATE, render_nav
import html as htmlmod

def swap(slug):
    path = f'pages/{slug}.html'
    data = open(path, encoding='utf-8').read()

    title_m = re.search(r'<title>([^<]*)</title>', data)
    title = title_m.group(1) if title_m else slug
    desc_m = re.search(r'<meta content="([^"]*)" name="description"', data)
    desc = desc_m.group(1) if desc_m else title

    content_start = data.find('<div class="tns-article">')
    # end right after the last </script> that precedes the WP article-close comment
    marker = data.find('<!-- #post-')
    tail_before_marker = data[:marker]
    content_end = tail_before_marker.rfind('</script>') + len('</script>')

    content = data[content_start:content_end]
    # fix any lingering ../images or ../pages references - already relative correctly since
    # this file already lives in pages/, so ../ prefixes are already correct as-is.

    head = HEAD_TEMPLATE.format(title=htmlmod.escape(title), description=htmlmod.escape(desc), slug=slug)
    header = HEADER_TEMPLATE.format(nav=render_nav(slug))

    out = head + header + content + '\n' + FOOTER_TEMPLATE
    open(path, 'w', encoding='utf-8').write(out)
    print(slug, '->', len(out), 'chars')

if __name__ == '__main__':
    for slug in sys.argv[1:]:
        swap(slug)
