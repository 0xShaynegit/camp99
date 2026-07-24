import os
from PIL import Image

IMG_DIR = os.path.join(os.path.dirname(__file__), '..', 'images')
MAX_WIDTH = 1600
QUALITY = 78

total_before = 0
total_after = 0
changed = 0

for fname in os.listdir(IMG_DIR):
    if not fname.lower().endswith(('.webp', '.png', '.jpg', '.jpeg')):
        continue
    path = os.path.join(IMG_DIR, fname)
    before = os.path.getsize(path)
    total_before += before

    try:
        im = Image.open(path)
    except Exception as e:
        print('SKIP (open failed):', fname, e)
        total_after += before
        continue

    orig_mode = im.mode
    w, h = im.size
    resized = False
    if w > MAX_WIDTH:
        new_h = round(h * MAX_WIDTH / w)
        im = im.resize((MAX_WIDTH, new_h), Image.LANCZOS)
        resized = True

    if im.mode in ('RGBA', 'LA') or (im.mode == 'P' and 'transparency' in im.info):
        im = im.convert('RGBA')
    elif im.mode != 'RGB':
        im = im.convert('RGB')

    save_kwargs = {'quality': QUALITY, 'method': 6}
    if fname.lower().endswith('.webp'):
        im.save(path, 'WEBP', **save_kwargs)
    else:
        im.save(path, quality=QUALITY, optimize=True)

    after = os.path.getsize(path)
    total_after += after
    if after < before or resized:
        changed += 1
        print(f'{fname}: {before//1024}KB -> {after//1024}KB' + (' (resized)' if resized else ''))

print()
print(f'Files touched: {changed}')
print(f'Total before: {total_before/1024/1024:.1f} MB')
print(f'Total after:  {total_after/1024/1024:.1f} MB')
print(f'Saved: {(total_before-total_after)/1024/1024:.1f} MB')
