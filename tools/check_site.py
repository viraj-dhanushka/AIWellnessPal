#!/usr/bin/env python3
"""Pre-publish checks for aiwellnesspal.com. Run from the repo root:
    python3 tools/check_site.py
Exits non-zero if anything needs fixing.
"""
import json
import re
import sys
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE = 'https://aiwellnesspal.com'
SKIP_DIRS = {'.git', '.firebase', 'node_modules', 'cloudflare', 'tools', '.wrangler', 'i18n'}
sys.path.insert(0, str(Path(__file__).resolve().parent))
from build_site import CODES, RTL, ENGLISH_ONLY  # noqa: E402
ENGLISH_ONLY_FILES = {rel for _, rel in ENGLISH_ONLY} | {'404.html'}
TAG = re.compile(r'<(/?[a-zA-Z0-9]+)')
HREF = re.compile(r'href="([^"]*)"')
PLACEHOLDER = re.compile(r'\{[a-z]+\}')


def check_translations(errors, warns):
    """Every language file has every English key, non-empty, with the same tags, links and placeholders."""
    en = json.loads((ROOT / 'i18n' / 'en.json').read_text())
    for c in CODES[1:]:
        f = ROOT / 'i18n' / f'{c}.json'
        if not f.exists():
            errors.append(f'i18n/{c}.json: missing (no translations for {c})')
            continue
        tr = json.loads(f.read_text())
        missing = [k for k in en if not (tr.get(k) or '').strip()]
        if missing:
            errors.append(f'i18n/{c}.json: {len(missing)} missing translation keys, e.g. {missing[:3]}')
        if '@prompt' not in tr:
            errors.append(f'i18n/{c}.json: missing "@prompt" (the "View this page in …?" sentence)')
        extra = [k for k in tr if k not in en and not k.startswith('@')]
        if extra:
            warns.append(f'i18n/{c}.json: {len(extra)} unused keys (English changed?), e.g. {extra[:3]}')
        for k, e in en.items():
            t = tr.get(k)
            if not t:
                continue
            if sorted(HREF.findall(e)) != sorted(HREF.findall(t)):
                errors.append(f'i18n/{c}.json: {k}: links differ from English')
            if sorted(PLACEHOLDER.findall(e)) != sorted(PLACEHOLDER.findall(t)):
                errors.append(f'i18n/{c}.json: {k}: placeholders differ from English')
            if sorted(TAG.findall(e)) != sorted(TAG.findall(t)):
                warns.append(f'i18n/{c}.json: {k}: HTML tags differ from English')


class Page(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.links, self.ids, self.imgs, self.ld = [], set(), [], []
        self.h1 = 0
        self.title = ''
        self.meta = {}
        self.canonical = None
        self.lang = None
        self.dir = None
        self.hreflang = {}
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
        if tag == 'link' and a.get('rel') == 'alternate' and a.get('hreflang'):
            self.hreflang[a['hreflang']] = a.get('href')
        if tag == 'html':
            self.lang, self.dir = a.get('lang'), a.get('dir')
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
        if not p.lang:
            errors.append(f'{name}: <html> has no lang attribute')
        top = name.split('/')[0]
        lang = top if top in CODES[1:] else 'en'
        if p.lang and p.lang != lang:
            errors.append(f'{name}: lang="{p.lang}" but the page is in /{lang}/')
        if (lang in RTL) != (p.dir == 'rtl'):
            errors.append(f'{name}: dir={p.dir!r} is wrong for {lang}')
        if name not in ENGLISH_ONLY_FILES and not noindex:
            want_langs = set(CODES) | {'x-default'}
            if set(p.hreflang) != want_langs:
                errors.append(f'{name}: hreflang links missing for {sorted(want_langs - set(p.hreflang))}')
            for hl, href in p.hreflang.items():
                r = resolve(href, here)
                if r and not r[0].exists():
                    errors.append(f'{name}: hreflang {hl} -> {href} does not exist')
                elif r and r[0] in parsed and parsed[r[0]].hreflang != p.hreflang:
                    errors.append(f'{name}: hreflang set not reciprocal with {href}')
            if p.hreflang.get(p.lang) != p.canonical:
                errors.append(f'{name}: canonical is not its own hreflang ({p.lang})')
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
            if lang == 'en' and not (15 <= len(p.title) <= 70):
                warns.append(f'{name}: title length {len(p.title)}: {p.title!r}')
            d = p.meta.get('description', '')
            if lang == 'en' and not (70 <= len(d) <= 170):
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
    locs = set(re.findall(r'<loc>([^<]+)</loc>', sm))
    for loc in locs:
        r = resolve(loc, '/')
        if r and not r[0].exists():
            errors.append(f'sitemap.xml: {loc} does not exist')
    for f, p in parsed.items():
        if 'noindex' not in p.meta.get('robots', '') and f.name != '404.html' and SITE + page_path(f) not in locs:
            errors.append(f'sitemap.xml: {page_path(f)} is not listed')
    check_translations(errors, warns)
    # Every script the site is translated into needs a font stack (system fallbacks are fine).
    css = (ROOT / 'landing.css').read_text()
    for c in ('ar', 'ja', 'ko', 'th', 'hi', 'mr', 'bn', 'ta', 'te'):
        if f':lang({c}) body' not in css:
            errors.append(f'landing.css: no font stack for {c}')
    for w in warns:
        print('warn:', w)
    for e in errors:
        print('ERROR:', e)
    print(f'{len(files)} pages checked, {len(errors)} errors, {len(warns)} warnings')
    sys.exit(1 if errors else 0)


if __name__ == '__main__':
    main()
