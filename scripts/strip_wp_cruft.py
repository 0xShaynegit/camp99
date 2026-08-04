import re, sys, glob

PATTERNS = [
    r'<meta[^>]*name="generator"[^>]*/?>',
    r'<link[^>]*rel="https://api\.w\.org/"[^>]*/>',
    r'<link[^>]*rel="EditURI"[^>]*/>',
    r'<link[^>]*type="application/json\+oembed"[^>]*/>',
    r'<link[^>]*type="text/xml\+oembed"[^>]*/>',
    r'<link[^>]*type="application/rss\+xml"[^>]*/>',
    r'<link[^>]*rel="shortlink"[^>]*/>',
    r'<link[^>]*rel="alternate"\s+title="JSON"\s+type="application/json"[^>]*/>',
    r'<!--\s*<link[^>]*>\s*-->',
]

TRACKER_PATTERN = re.compile(
    r'<script id="wp-statistics-tracker-js-extra">.*?</script>\s*'
    r'<script id="wp-statistics-tracker-js"[^>]*></script>',
    re.S,
)

def clean(text):
    for pat in PATTERNS:
        text = re.sub(pat, '', text)
    text = TRACKER_PATTERN.sub('', text)
    return text

if __name__ == '__main__':
    files = sys.argv[1:]
    for f in files:
        data = open(f, encoding='utf-8').read()
        before = len(data)
        data = clean(data)
        after = len(data)
        open(f, 'w', encoding='utf-8').write(data)
        print(f, before - after, 'bytes removed')
