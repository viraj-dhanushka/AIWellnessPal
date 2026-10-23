#!/usr/bin/env python3
"""Pre-publish checks for aiwelnesspal.com. Run from the repo root:
    python3 tools/check_site.py
Exits non-zero if anything needs fixing.
"""
import json
import re
import sys
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE = 'https://aiwelnesspal.com'
SKIP_DIRS = {'.git', '.firebase', 'node_modules', 'cloudflare', 'tools', '.wrangler'}


class Page(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.links, self.ids, self.imgs, self.ld = [], set(), [], []
        self.h1 = 0
        self.title = ''
        self.meta = {}
        self.canonical = None
        self._in = None
        self._buf = ''

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if 'id' in a:
            self.ids.add(a['id'])
        if tag == 'a' and 'href' in a:
            self.links.append(a['href'])
        if tag in ('img', 'source', 'script', 'link') and (a.get('src') or a.get('href') or a.get('srcset')):
            for v in (a.get('src'), a.get('href') if tag == 'link' and a.get('rel') in ('stylesheet', 'icon', 'apple-touch-icon', 'manifest', 'preload') else None):
                if v:
                    self.links.append(v)
            if a.get('srcset'):
                self.links += [p.strip().split(' ')[0] for p in a['srcset'].split(',')]
        if tag == 'img':
            self.imgs.append(a)
        if tag == 'h1':
            self.h1 += 1
        if tag == 'meta' and a.get('name'):
            self.meta[a['name']] = a.get('content', '')
        if tag == 'link' and a.get('rel') == 'canonical':
            self.canonical = a.get('href')
        if tag == 'title' or (tag == 'script' and a.get('type') == 'application/ld+json'):
            self._in, self._buf = tag, ''

    def handle_data(self, data):
        if self._in:
            self._buf += data

    def handle_endtag(self, tag):
        if self._in == tag:
            if tag == 'title':
                self.title = self._buf.strip()
            else:
                self.ld.append(self._buf)
            self._in = None


def page_path(f):
    rel = f.relative_to(ROOT).as_posix()
    return '/' + (rel[:-len('index.html')] if rel.endswith('index.html') else rel)


def resolve(href, here):
    """Local file for an internal URL (or None if external / not checkable)."""
    if href.startswith(('mailto:', 'tel:', 'javascript:', 'data:')):
        return None
    if href.startswith(SITE):
        href = href[len(SITE):] or '/'
    elif re.match(r'^[a-z]+:', href) or href.startswith('//'):
        return None
    path, _, frag = href.partition('#')
    path = path.split('?')[0]
    if not path:
        target = here
    elif path.startswith('/'):
        target = path
    else:
        base = here if here.endswith('/') else here.rsplit('/', 1)[0] + '/'
        target = base + path
    f = ROOT / target.lstrip('/')
    if target.endswith('/'):
        f = f / 'index.html'
    return f, frag


def main():
    errors, warns = [], []
    files = [f for f in ROOT.rglob('*.html') if not (set(f.relative_to(ROOT).parts) & SKIP_DIRS)]
    parsed = {}
    for f in files:
        p = Page()
        p.feed(f.read_text())
        parsed[f] = p
    for f, p in parsed.items():
        here = page_path(f)
        name = f.relative_to(ROOT).as_posix()
        text = f.read_text()
        noindex = 'noindex' in p.meta.get('robots', '')
        if 'TODO' in text:
            errors.append(f'{name}: contains TODO')
        for blk in p.ld:
            try:
                json.loads(blk)
            except Exception as e:
                errors.append(f'{name}: invalid JSON-LD ({e})')
        if not noindex:
            if p.h1 != 1:
                errors.append(f'{name}: {p.h1} <h1> elements (want 1)')
            if not (15 <= len(p.title) <= 70):
                warns.append(f'{name}: title length {len(p.title)}: {p.title!r}')
            d = p.meta.get('description', '')
            if not (70 <= len(d) <= 170):
                warns.append(f'{name}: description length {len(d)}')
            want = SITE + here
            if p.canonical != want:
                errors.append(f'{name}: canonical {p.canonical!r} != {want!r}')
        for img in p.imgs:
            if 'alt' not in img:
                errors.append(f'{name}: <img src={img.get("src")}> has no alt')
        for href in p.links:
            r = resolve(href, here)
            if not r:
                continue
            target, frag = r
            if not target.exists():
                errors.append(f'{name}: broken link {href}')
            elif frag and target.suffix == '.html' and target in parsed and frag not in parsed[target].ids:
                errors.append(f'{name}: missing anchor #{frag} in {target.relative_to(ROOT)}')
    sm = (ROOT / 'sitemap.xml').read_text()
    for loc in re.findall(r'<loc>([^<]+)</loc>', sm):
        r = resolve(loc, '/')
        if r and not r[0].exists():
            errors.append(f'sitemap.xml: {loc} does not exist')
    for w in warns:
        print('warn:', w)
    for e in errors:
        print('ERROR:', e)
    print(f'{len(files)} pages checked, {len(errors)} errors, {len(warns)} warnings')
    sys.exit(1 if errors else 0)


if __name__ == '__main__':
    main()
