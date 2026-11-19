#!/usr/bin/env python3
"""Builds every page of aiwellnesspal.com, in English and 22 other languages.

Run from the repo root after editing tools/site_content.py or i18n/*.json:
    python3 tools/build_site.py

English is written at the site root (/, /features/..., /faq/, /about/) and each
other language under /<lang>/ with the same paths (/es/, /es/features/...).
privacy.html, terms.html and delete-account.html are English-only and never move.

How translation works
    tools/site_content.py (and the page templates below) hold the English text.
    Every visible string goes through T(). The build writes all of them to
    i18n/en.json, keyed by a short slug plus a hash of the English text, and looks
    each key up in i18n/<lang>.json. Changing an English string therefore gives it
    a new key: the old translation stops being used, the page falls back to English
    for that string, and tools/check_site.py reports the key as missing until it is
    translated. Keep HTML tags, links and {placeholders} identical in translations.

Writes (generated, don't edit by hand):
    index.html, features/, faq/, about/ and the same under each /<lang>/,
    i18n/en.json, sitemap.xml, llms.txt, llms-full.txt, and the prompt strings in
    assets/lang.js.

No dependencies beyond Python 3.
"""
import datetime
import hashlib
import html
import json
import re
import subprocess
from pathlib import Path

import site_content as C

ROOT = Path(__file__).resolve().parent.parent
I18N = ROOT / 'i18n'
SITE = C.SITE
TODAY = datetime.date.today().isoformat()
FONT_CSS = 'https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400..800&display=swap'

# code, name in its own language, og:locale. Order = picker order (English first, then by code).
LANGS = [
    ('en', 'English', 'en_US'), ('ar', 'العربية', 'ar_AR'), ('bn', 'বাংলা', 'bn_IN'), ('de', 'Deutsch', 'de_DE'),
    ('es', 'Español', 'es_ES'), ('fr', 'Français', 'fr_FR'), ('hi', 'हिन्दी', 'hi_IN'),
    ('id', 'Bahasa Indonesia', 'id_ID'), ('it', 'Italiano', 'it_IT'), ('ja', '日本語', 'ja_JP'),
    ('ko', '한국어', 'ko_KR'), ('mr', 'मराठी', 'mr_IN'), ('nl', 'Nederlands', 'nl_NL'), ('pl', 'Polski', 'pl_PL'),
    ('pt', 'Português', 'pt_BR'), ('ro', 'Română', 'ro_RO'), ('ru', 'Русский', 'ru_RU'), ('ta', 'தமிழ்', 'ta_IN'),
    ('te', 'తెలుగు', 'te_IN'), ('th', 'ไทย', 'th_TH'), ('tr', 'Türkçe', 'tr_TR'), ('uk', 'Українська', 'uk_UA'),
    ('vi', 'Tiếng Việt', 'vi_VN'),
]
CODES = [c for c, _, _ in LANGS]
NATIVE = {c: n for c, n, _ in LANGS}
OG_LOCALE = {c: o for c, _, o in LANGS}
RTL = {'ar'}

# Pages that exist in every language (path, file relative to the language root).
# English-only pages (legal, account deletion) are listed separately and never get copies.
ENGLISH_ONLY = [('/privacy.html', 'privacy.html'), ('/terms.html', 'terms.html'),
                ('/delete-account.html', 'delete-account.html')]


# ---------------------------------------------------------------- translation

CUR = 'en'          # language being built
EN = {}             # key -> English text, in first-use order (written to i18n/en.json)
TR = {}             # lang -> {key: text}
MISSING = {}        # lang -> set of keys that fell back to English


def plain(fragment):
    """HTML fragment -> plain text (for JSON-LD answers and llms.txt)."""
    t = re.sub(r'<li[^>]*>', '\n- ', fragment)
    t = re.sub(r'</p>\s*<p[^>]*>', '\n\n', t)
    t = re.sub(r'<br\s*/?>', '\n', t)
    t = re.sub(r'<[^>]+>', '', t)
    t = html.unescape(t)
    return re.sub(r'[ \t]+', ' ', re.sub(r'\n{3,}', '\n\n', t)).strip()


def key_for(s):
    words = re.findall(r'[a-z0-9]+', plain(s).lower())[:6]
    return ('-'.join(words)[:40].strip('-') or 'x') + '.' + hashlib.sha1(s.encode()).hexdigest()[:6]


def T(s):
    """The current language's version of English string s (English if missing)."""
    if not s or not s.strip():
        return s
    k = key_for(s)
    EN.setdefault(k, s)
    if CUR == 'en':
        return s
    v = TR.get(CUR, {}).get(k)
    if not v:
        MISSING.setdefault(CUR, set()).add(k)
        return s
    return v


def TB(fragment):
    """A long HTML fragment, translated section by section (split on blank lines)."""
    return '\n\n'.join(T(b) for b in fragment.split('\n\n'))


def load_translations():
    for c in CODES[1:]:
        f = I18N / f'{c}.json'
        TR[c] = json.loads(f.read_text()) if f.exists() else {}


# ---------------------------------------------------------------- paths

def lp(path, lang=None):
    """Site path in a language: '/faq/' -> '/es/faq/'."""
    lang = lang or CUR
    return path if lang == 'en' else f'/{lang}{path}'


def url(path):
    return SITE + path


def lurl(path, lang=None):
    return SITE + lp(path, lang)


LOCALIZABLE = re.compile(r'href="/((?:features/|faq/|about/)[^"]*|#[^"]*|)"')


def localize_links(text):
    """Point internal links at the current language's copy (legal pages and assets stay put)."""
    if CUR == 'en':
        return text
    return LOCALIZABLE.sub(lambda m: f'href="/{CUR}/{m.group(1)}"', text)


# ---------------------------------------------------------------- shared pieces

def esc(s):
    return html.escape(s, quote=True)


def picture(name, alt, sizes='(max-width: 720px) 200px, 260px', eager=False, extra=''):
    """A screenshot as WebP (300w/600w) with the original JPEG as fallback."""
    lazy = 'fetchpriority="high"' if eager else 'loading="lazy"'
    return (f'<picture><source type="image/webp" srcset="/assets/screens/w/{name}-300.webp 300w, '
            f'/assets/screens/w/{name}-600.webp 600w" sizes="{sizes}">'
            f'<img src="/assets/screens/{name}.jpg" alt="{esc(alt)}" width="600" height="1300" '
            f'decoding="async" {lazy}{extra}></picture>')


def icon_img(size_css, cls='', alt=''):
    return (f'<picture><source type="image/webp" srcset="/assets/icon-96.webp 1x, /assets/icon-192.webp 2x">'
            f'<img src="/assets/icon-96.png" alt="{esc(alt)}" width="{size_css}" height="{size_css}"'
            f'{" class=" + chr(34) + cls + chr(34) if cls else ""}></picture>')


def store_buttons(indent='        '):
    return f'''<div class="cta">
{indent}  <a class="btn btn-store" href="{C.APPLE}">
{indent}    <svg aria-hidden="true"><use href="#i-apple"/></svg>
{indent}    <span class="lbl"><small>{T('Download on the')}</small><strong>App Store</strong></span>
{indent}  </a>
{indent}  <a class="btn btn-store" href="{C.PLAY}">
{indent}    <svg aria-hidden="true"><use href="#i-play"/></svg>
{indent}    <span class="lbl"><small>{T('Get it on')}</small><strong>Google Play</strong></span>
{indent}  </a>
{indent}</div>'''


SVG_DEFS = '''<svg width="0" height="0" style="position:absolute" aria-hidden="true">
  <symbol id="i-apple" viewBox="0 0 24 24"><path fill="currentColor" d="M12.152 6.896c-.948 0-2.415-1.078-3.96-1.04-2.04.027-3.91 1.183-4.961 3.014-2.117 3.675-.546 9.103 1.519 12.09 1.013 1.454 2.208 3.09 3.792 3.039 1.52-.065 2.09-.987 3.935-.987 1.831 0 2.35.987 3.96.948 1.637-.026 2.676-1.48 3.676-2.948 1.156-1.688 1.636-3.325 1.662-3.415-.039-.013-3.182-1.221-3.22-4.857-.026-3.04 2.48-4.494 2.597-4.559-1.429-2.09-3.623-2.324-4.39-2.376-2-.156-3.675 1.09-4.61 1.09zM15.53 3.83c.843-1.012 1.4-2.427 1.245-3.83-1.207.052-2.662.805-3.532 1.818-.78.896-1.454 2.338-1.273 3.714 1.338.104 2.715-.688 3.559-1.701"/></symbol>
  <symbol id="i-play" viewBox="0 0 24 24"><path fill="currentColor" d="M22.018 13.298l-3.919 2.218-3.515-3.493 3.543-3.521 3.891 2.202a1.49 1.49 0 0 1 0 2.594zM1.337.924a1.486 1.486 0 0 0-.112.568v21.017c0 .217.045.419.124.6l11.155-11.087L1.337.924zm12.207 10.065l3.258-3.238L3.45.195a1.466 1.466 0 0 0-.946-.179l11.04 10.973zm0 2.067l-11 10.933c.298.036.612-.016.906-.183l13.324-7.54-3.23-3.21z"/></symbol>
  <symbol id="i-check" viewBox="0 0 24 24"><path fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" d="M5 12.5l4.5 4.5L19 7.5"/></symbol>
  <symbol id="i-globe" viewBox="0 0 24 24"><g fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3c2.5 2.6 3.8 5.6 3.8 9s-1.3 6.4-3.8 9c-2.5-2.6-3.8-5.6-3.8-9S9.5 5.6 12 3z"/></g></symbol>
</svg>'''


def lang_links(path, cls=''):
    """One link per language to this page. '@@' keeps localize_links from touching them."""
    out = []
    for c in CODES:
        cur = ' aria-current="true"' if c == CUR else ''
        out.append(f'<li><a href="@@{lp(path, c)}" hreflang="{c}" lang="{c}" data-lang="{c}"{cur}>{NATIVE[c]}</a></li>')
    return ''.join(out)


def picker(path):
    return f'''<details class="lang-pick">
      <summary aria-label="{esc(T('Language'))}: {NATIVE[CUR]}"><svg aria-hidden="true"><use href="#i-globe"/></svg><span>{CUR.upper()}</span></summary>
      <ul class="lang-menu">{lang_links(path)}</ul>
    </details>'''


def nav(path, active=''):
    items = [('/features/', T('Features')), ('/#demo', T('Demo')), ('/faq/', T('FAQ')), ('/about/', T('About')),
             ('/#support', T('Support'))]
    links = '\n      '.join(
        f'<a href="{h}"{" aria-current=" + chr(34) + "page" + chr(34) if h == active else ""}>{t}</a>' for h, t in items)
    return f'''<header class="nav">
  <div class="wrap">
    <a class="brand" href="/">{icon_img(34)}AI Wellness Pal</a>
    <nav class="nav-links" aria-label="{esc(T('Main'))}">
      {links}
    </nav>
    {picker(path)}
    <a class="btn btn-sm btn-grad" id="get-app" href="{C.APPLE}">{T('Get the app')}</a>
  </div>
</header>'''


def footer(path):
    feats = '\n        '.join(f'<a href="/features/{f["slug"]}/">{esc(T(f["short"]))}</a>' for f in C.FEATURES)
    legal_note = '' if CUR == 'en' else f'\n      <p class="foot-note">{T("Our Privacy Policy and Terms of Use are available in English.")}</p>'
    return f'''<footer class="site-footer">
  <div class="wrap foot-grid">
    <div>
      <a class="brand" href="/">{icon_img(34)}AI Wellness Pal</a>
      <p>{esc(T(C.TAGLINE))}. {T('Free on iPhone and Android.')}</p>
      <p class="foot-stores"><a href="{C.APPLE}">App Store</a> · <a href="{C.PLAY}">Google Play</a></p>
    </div>
    <nav aria-label="{esc(T('Features'))}">
      <p class="foot-h">{T('Features')}</p>
        {feats}
    </nav>
    <nav aria-label="{esc(T('Resources'))}">
      <p class="foot-h">{T('Resources')}</p>
      <a href="/features/">{T('All features')}</a>
      <a href="/faq/">{T('FAQ')}</a>
      <a href="/about/">{T('About')}</a>
      <a href="/#demo">{T('Demo video')}</a>
      <a href="/#support">{T('Support')}</a>
      <a href="/#feedback">{T('Send feedback')}</a>
    </nav>
    <nav aria-label="{esc(T('Legal'))}">
      <p class="foot-h">{T('Legal')}</p>
      <a href="/privacy.html" hreflang="en">{T('Privacy Policy')}</a>
      <a href="/terms.html" hreflang="en">{T('Terms of Use')}</a>
      <a href="/delete-account.html" hreflang="en">{T('Delete your account')}</a>{legal_note}
    </nav>
  </div>
  <nav class="wrap foot-langs" aria-label="{esc(T('Language'))}">
    <p class="foot-h">{T('Language')}</p>
    <ul>{lang_links(path)}</ul>
  </nav>
  <div class="wrap foot-bottom">
    <span>© 2026 Viraj Dhanushka</span>
    <span>{T('Not medical advice. AI Wellness Pal provides general wellness information.')}</span>
  </div>
</footer>'''


def get_app_script():
    return f'''<script>
  // "Get the app" opens Google Play on Android, the App Store elsewhere.
  if (/android/i.test(navigator.userAgent)) document.getElementById('get-app').href = '{C.PLAY}';
</script>'''


def font_links(indent='  '):
    """Fonts load without blocking the first paint (system font shows until then)."""
    return '\n'.join(indent + l for l in [
        '<link rel="preconnect" href="https://fonts.googleapis.com">',
        '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>',
        f'<link rel="preload" as="style" href="{FONT_CSS}">',
        f'<link rel="stylesheet" href="{FONT_CSS}" media="print" onload="this.media=\'all\'">',
        f'<noscript><link rel="stylesheet" href="{FONT_CSS}"></noscript>',
    ])


def alternates(path):
    lines = [f'<link rel="alternate" hreflang="{c}" href="{lurl(path, c)}">' for c in CODES]
    lines.append(f'<link rel="alternate" hreflang="x-default" href="{lurl(path, "en")}">')
    return '\n'.join('  ' + l for l in lines)


def head(title, desc, path, ld, og_type='website', og_title=None, og_desc=None, tw_desc=None, extra='',
         robots='index, follow, max-image-preview:large, max-snippet:-1'):
    og_title, og_desc = og_title or title, og_desc or desc
    tw_desc = tw_desc or og_desc
    d = ' dir="rtl"' if CUR in RTL else ''
    return f'''<!doctype html>
<html lang="{CUR}"{d}>
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{esc(title)}</title>
  <meta name="description" content="{esc(desc)}">
  <meta name="robots" content="{robots}">
  <meta name="author" content="Viraj Dhanushka">
  <meta name="theme-color" content="#0d0f1c">
  <link rel="canonical" href="{lurl(path)}">
{alternates(path)}
  <link rel="icon" type="image/png" href="/assets/favicon.png">
  <link rel="apple-touch-icon" href="/assets/apple-touch-icon.png">
  <link rel="manifest" href="/site.webmanifest">
  <meta name="apple-itunes-app" content="app-id={C.APPLE_ID}">
  <meta property="og:type" content="{og_type}">
  <meta property="og:site_name" content="AI Wellness Pal">
  <meta property="og:locale" content="{OG_LOCALE[CUR]}">
  <meta property="og:title" content="{esc(og_title)}">
  <meta property="og:description" content="{esc(og_desc)}">
  <meta property="og:url" content="{lurl(path)}">
  <meta property="og:image" content="{SITE}/assets/og-image.png">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta property="og:image:alt" content="{esc(T('AI Wellness Pal app: Feel better, one day at a time.'))}">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{esc(og_title)}">
  <meta name="twitter:description" content="{esc(tw_desc)}">
  <meta name="twitter:image" content="{SITE}/assets/og-image.png">
{font_links()}{extra}
  <link rel="stylesheet" href="/landing.css">
  <script type="application/ld+json">
{json.dumps(ld, ensure_ascii=False, indent=2)}
  </script>
</head>'''


def faq_html(faqs):
    return '\n'.join(
        f'''      <details>
        <summary>{esc(T(q))}</summary>
        <div class="a">{T(a)}</div>
      </details>''' for q, a in faqs)


def faq_ld(faqs, page_url):
    return {
        '@type': 'FAQPage',
        '@id': page_url + '#faq',
        'inLanguage': CUR,
        'mainEntity': [{'@type': 'Question', 'name': T(q),
                        'acceptedAnswer': {'@type': 'Answer', 'text': plain(T(a))}} for q, a in faqs],
    }


def crumbs_html(crumbs):
    items = []
    for i, (name, path) in enumerate(crumbs):
        last = i == len(crumbs) - 1
        items.append(f'<li>{esc(name)}</li>' if last else f'<li><a href="{path}">{esc(name)}</a></li>')
    return f'<nav class="crumbs" aria-label="{esc(T("Breadcrumb"))}"><ol>{"".join(items)}</ol></nav>'


def crumbs_ld(crumbs, page_url):
    return {
        '@type': 'BreadcrumbList',
        '@id': page_url + '#breadcrumb',
        'itemListElement': [{'@type': 'ListItem', 'position': i + 1, 'name': n, 'item': lurl(p)}
                            for i, (n, p) in enumerate(crumbs)],
    }


def webpage_ld(path, title, desc, crumbs=None, extra=None):
    u = lurl(path)
    d = {
        '@type': 'WebPage', '@id': u + '#webpage', 'url': u, 'name': title, 'description': desc,
        'inLanguage': CUR, 'isPartOf': {'@id': SITE + '/#website'}, 'about': {'@id': SITE + '/#app'},
        'publisher': {'@id': SITE + '/#organization'}, 'dateModified': TODAY,
        'primaryImageOfPage': {'@type': 'ImageObject', 'url': SITE + '/assets/og-image.png'},
    }
    if CUR != 'en':
        d['translationOfWork'] = {'@id': url(path) + '#webpage'}
    if crumbs:
        d['breadcrumb'] = {'@id': u + '#breadcrumb'}
    if extra:
        d.update(extra)
    return d


def final_cta(cls='final'):
    return f'''  <div class="{cls}">
    <picture><source type="image/webp" srcset="/assets/icon-192.webp"><img src="/assets/icon-192.png" alt="{esc(T('AI Wellness Pal app icon'))}" width="88" height="88" loading="lazy"></picture>
    <h2>{T('Start feeling better <span class="grad-text">today</span>')}</h2>
    <p>{T('Free on iPhone and Android.')}</p>
    {store_buttons('    ')}
  </div>'''


def finish(text):
    """Language-specific touches on a whole page."""
    text = localize_links(text).replace('href="@@/', 'href="/')
    if CUR in RTL:
        text = text.replace('→', '←')
    return text


def page(title, desc, path, ld_graph, main, active='', head_kw=None, main_attrs='', scripts=None):
    ld = {'@context': 'https://schema.org', '@graph': ld_graph} if isinstance(ld_graph, list) else ld_graph
    scripts = scripts if scripts is not None else get_app_script()
    body_data = (f' data-music-play="{esc(T("Play music"))}" data-music-pause="{esc(T("Pause music"))}"'
                 f' data-music-play-label="{esc(T("Play background music"))}"'
                 f' data-music-pause-label="{esc(T("Pause background music"))}"') if CUR != 'en' else ''
    return finish(f'''{head(title, desc, path, ld, **(head_kw or {}))}
<body{body_data}>
<div class="glow" aria-hidden="true"><span></span><span></span><span></span></div>
{SVG_DEFS}

{nav(path, active)}

<main{main_attrs}>
{main}
</main>

{footer(path)}

{scripts}
<script src="/assets/lang.js" defer></script>
<script src="/assets/music.js" defer></script>
</body>
</html>
''')


def out(rel):
    return rel if CUR == 'en' else f'{CUR}/{rel}'


def write(rel, content):
    p = ROOT / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content)
    return rel


# ---------------------------------------------------------------- content pages

def related_card(f, cls='card'):
    return (f'<a class="{cls}" href="/features/{f["slug"]}/"><h3>{esc(T(f["short"]))}</h3>'
            f'<p>{esc(T(f["card"]))}</p><span class="more">{T("Learn more →")}</span></a>')


def feature_page(f):
    path = f'/features/{f["slug"]}/'
    short = T(f['short'])
    crumbs = [(T('Home'), '/'), (T('Features'), '/features/'), (short, path)]
    shots = ''
    if f.get('shots'):
        figs = '\n'.join(f'''      <figure>{picture(n, T(cap), sizes='(max-width: 720px) 170px, 220px')}<figcaption>{esc(T(cap))}</figcaption></figure>'''
                         for n, cap in f['shots'])
        shots = f'<div class="prose-shots">\n{figs}\n    </div>'
    related = '\n'.join('      ' + related_card(r) for r in (next(x for x in C.FEATURES if x['slug'] == s) for s in f['related']))
    hero_shot = f'<div class="shot">{picture(f["hero"][0], T(f["hero"][1]), eager=True)}</div>' if f.get('hero') else ''
    title, desc = T(f['title']), T(f['desc'])
    main = f'''  <section class="page-hero">
    <div class="wrap">
      <div>
        {crumbs_html(crumbs)}
        <span class="eyebrow">{esc(T(f["eyebrow"]))}</span>
        <h1>{T(f["h1"])}</h1>
        <p class="lead">{T(f["lead"])}</p>
        {store_buttons()}
      </div>
      {hero_shot}
    </div>
  </section>

  <section class="page-section" style="padding-top:8px">
    <div class="wrap prose">
{TB(f["body"])}
    {shots}
    </div>
  </section>

  <section class="page-section" id="faq">
    <div class="wrap">
      <div class="sec-head"><span class="eyebrow">{T('FAQ')}</span><h2>{esc(T('{feature} questions').replace('{feature}', short))}</h2></div>
      <div class="faq">
{faq_html(f["faqs"])}
      </div>
    </div>
  </section>

  <section class="page-section">
    <div class="wrap">
      <div class="sec-head"><span class="eyebrow">{T('Keep exploring')}</span><h2>{T('Related features')}</h2></div>
      <div class="related">
{related}
      </div>
      <p class="fine"><a href="/features/" style="color:var(--lavender)">{T('See all AI Wellness Pal features →')}</a></p>
    </div>
  </section>

{final_cta()}'''
    graph = [webpage_ld(path, title, desc, crumbs), crumbs_ld(crumbs, lurl(path)), faq_ld(f['faqs'], lurl(path))]
    return write(out(f'features/{f["slug"]}/index.html'), page(title, desc, path, graph, main, '/features/'))


def hub_page():
    path = '/features/'
    crumbs = [(T('Home'), '/'), (T('Features'), path)]
    groups = ''
    for gname, gintro, slugs in C.FEATURE_GROUPS:
        cards = '\n'.join('        ' + related_card(f) for f in (next(x for x in C.FEATURES if x['slug'] == s) for s in slugs))
        groups += f'''
  <section class="page-section">
    <div class="wrap">
      <div class="sec-head"><h2>{esc(T(gname))}</h2><p>{esc(T(gintro))}</p></div>
      <div class="related">
{cards}
      </div>
    </div>
  </section>
'''
    title, desc = T(C.HUB_TITLE), T(C.HUB_DESC)
    main = f'''  <section class="page-hero solo">
    <div class="wrap">
      <div>
        {crumbs_html(crumbs)}
        <span class="eyebrow">{T('Features')}</span>
        <h1>{T('Everything in <span class="grad-text">AI Wellness Pal</span>')}</h1>
        <p class="lead">{T(C.HUB_LEAD)}</p>
        {store_buttons()}
      </div>
    </div>
  </section>
{groups}
{final_cta()}'''
    items = [{'@type': 'ListItem', 'position': i + 1, 'url': lurl(f'/features/{f["slug"]}/'), 'name': T(f['short'])}
             for i, f in enumerate(C.FEATURES)]
    graph = [webpage_ld(path, title, desc, crumbs, {'@type': 'CollectionPage'}), crumbs_ld(crumbs, lurl(path)),
             {'@type': 'ItemList', '@id': lurl(path) + '#list', 'name': T('AI Wellness Pal features'), 'itemListElement': items}]
    return write(out('features/index.html'), page(title, desc, path, graph, main, '/features/'))


def faq_page():
    path = '/faq/'
    crumbs = [(T('Home'), '/'), (T('FAQ'), path)]
    groups = ''.join(f'''
      <div class="faq-group">
        <h2>{esc(T(g))}</h2>
        <div class="faq">
{faq_html(items)}
        </div>
      </div>''' for g, items in C.FAQ_GROUPS)
    all_faqs = [qa for _, items in C.FAQ_GROUPS for qa in items]
    title, desc = T(C.FAQ_TITLE), T(C.FAQ_DESC)
    mail = f'<a href="mailto:{C.EMAIL}" style="color:var(--lavender)">{C.EMAIL}</a>'
    main = f'''  <section class="page-hero solo">
    <div class="wrap">
      <div>
        {crumbs_html(crumbs)}
        <span class="eyebrow">{T('FAQ')}</span>
        <h1>{T('AI Wellness Pal <span class="grad-text">questions &amp; answers</span>')}</h1>
        <p class="lead">{T(C.FAQ_LEAD)}</p>
      </div>
    </div>
  </section>

  <section class="page-section" style="padding-top:8px">
    <div class="wrap">{groups}
      <p class="fine">{T('Still stuck? Email {email}.').replace('{email}', mail)}</p>
    </div>
  </section>

{final_cta()}'''
    graph = [webpage_ld(path, title, desc, crumbs), crumbs_ld(crumbs, lurl(path)), faq_ld(all_faqs, lurl(path))]
    return write(out('faq/index.html'), page(title, desc, path, graph, main, '/faq/'))


def about_page():
    path = '/about/'
    crumbs = [(T('Home'), '/'), (T('About'), path)]
    rows = '\n'.join(f'          <tr><th scope="row">{esc(T(k))}</th><td>{T(v)}</td></tr>' for k, v in C.FACTS)
    title, desc = T(C.ABOUT_TITLE), T(C.ABOUT_DESC)
    main = f'''  <section class="page-hero solo">
    <div class="wrap">
      <div>
        {crumbs_html(crumbs)}
        <span class="eyebrow">{T('About')}</span>
        <h1>{T('About <span class="grad-text">AI Wellness Pal</span>')}</h1>
        <p class="lead">{T(C.DEFINITION)}</p>
      </div>
    </div>
  </section>

  <section class="page-section" style="padding-top:8px">
    <div class="wrap prose">
      <h2>{T('Key facts')}</h2>
      <table class="facts">
        <tbody>
{rows}
        </tbody>
      </table>
{TB(C.ABOUT_BODY)}
    </div>
  </section>

{final_cta()}'''
    graph = [webpage_ld(path, title, desc, crumbs, {'@type': 'AboutPage'}), crumbs_ld(crumbs, lurl(path))]
    return write(out('about/index.html'), page(title, desc, path, graph, main, '/about/'))


# ---------------------------------------------------------------- home page

HOME_OG_TITLE = 'AI Wellness Pal: your personal AI wellness coach'
HOME_OG_DESC = ('Daily check-ins, personalized plans, guided reflections and an AI Wellness Pal to talk things '
                'through. Free on the App Store and Google Play.')
HOME_TW_DESC = 'Daily check-ins, personalized plans, guided reflections and an AI Wellness Pal to talk things through.'

ICONS = {
    'sun': '<circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/>',
    'chat': '<path d="M21 12a8 8 0 0 1-11.6 7.1L4 20l1-4.6A8 8 0 1 1 21 12z"/>',
    'book': '<path d="M4 19.5V5a2 2 0 0 1 2-2h12v18H6a2 2 0 0 1-2-1.5z"/><path d="M8 7h6M8 11h6"/>',
    'camera': '<path d="M3 9a2 2 0 0 1 2-2h2l1.5-2h7L17 7h2a2 2 0 0 1 2 2v9a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/><circle cx="12" cy="13" r="3.5"/>',
    'fork': '<path d="M4 3v8a3 3 0 0 0 6 0V3M7 3v18M17 21V3c-2.5 1-4 3.5-4 7v3h4"/>',
    'flame': '<path d="M12 3c1 3 4 4.5 4 9a4 4 0 0 1-8 0c0-2 1-3 2-4 0 2 1 3 2 3 0-3-1-5 0-8z"/><path d="M6 15a6 6 0 0 0 12 0"/>',
    'drop': '<path d="M12 3s6 6.5 6 11a6 6 0 0 1-12 0c0-4.5 6-11 6-11z"/>',
    'moon': '<path d="M20 14.5A8.5 8.5 0 1 1 9.5 4a7 7 0 0 0 10.5 10.5z"/>',
    'person': '<circle cx="12" cy="5" r="2"/><path d="M12 8v5M6 20l3-4h6l3 4M5 12l7 1 7-1"/>',
    'heart': '<path d="M12 21s-7-4.5-7-10a4 4 0 0 1 7-2.6A4 4 0 0 1 19 11c0 5.5-7 10-7 10z"/>',
    'scale': '<rect x="3" y="4" width="18" height="16" rx="3"/><path d="M8 10a4 4 0 0 1 8 0M12 10l1.5-2"/>',
    'plane': '<path d="M2 16l20-6-2.5-2.5L13 9 8 4 6 5l3 6-4 1.5L3 11l-1 1z"/><path d="M3 20h18"/>',
}

HOME_CORE = [
    ('ai-wellness-coach', 'sun', 'Daily check-ins',
     'Log energy, mood and recovery in seconds. Your answers shape a personalized plan for the day.'),
    ('ai-wellness-chat', 'chat', 'Your Wellness Pal',
     'Chat about stress, motivation or habits. Your Pal learns from your check-ins and journal to give relevant guidance.'),
    ('ai-journal', 'book', 'Guided reflections',
     'A private journal with thoughtful prompts. Spot patterns and see what actually helps you feel better.'),
]
HOME_TOOLKIT = [
    ('ai-nutrition-coach', 'camera', 'AI Nutrition Coach',
     'Log meals by photo, description or barcode and get an instant AI estimate of calories and macros.'),
    ('ai-meal-planner', 'fork', 'AI Meal Planner',
     'A day, a week or a month of meals built around your goal and diet style, with a grocery list to match.'),
    ('calorie-tracker', 'flame', 'AI Calorie Budget',
     'See intake and exercise together so you always know your daily energy balance.'),
    ('water-tracker', 'drop', 'AI Hydration Coach',
     'Track your water against a smart daily target, with quick add and a hydration streak to keep you going.'),
    ('sleep-tracker', 'moon', 'Sleep Coach',
     'Understand your sleep: connect Apple Health or Health Connect (read-only) for sleep scores, stages and recovery insights.'),
    ('meditation-breathing', 'person', 'Meditation Pal',
     'Breathe, meditate and find your calm with guided breathing, body scans and step-by-step stress relief.'),
    ('period-tracker', 'heart', 'Period Tracker',
     'Log your cycle, see predictions for your next period and fertile window, and get phase-based tips.'),
    ('weight-tracker', 'scale', 'Body Weight',
     'Track weight and BMI over time with a clear trend chart and your full weigh-in history.'),
    (None, 'plane', 'Mindful Travel',
     'AI wellness guidance for every trip, so you can keep feeling good while you’re away.'),
]
HOME_SHOTS = [
    ('01_00_onboard', 'Onboarding: less overthinking, focus on what matters most today'),
    ('01_01_onboard', 'Onboarding: know your energy with quick daily check-ins'),
    ('01_03_checkin', 'Daily check-in asking how your energy is today'),
    ('05_reminder', 'Setting a reminder time for a wellness action'),
    ('06_profile', 'Profile with personal details and preferred wellness methods'),
    ('07_action_detail', 'Plank and core challenge action details with a how-to guide'),
    ('08_add_habit', 'Adding a custom habit with frequency and target'),
    ('09_habit_formed', 'Achievement unlocked celebration for forming a habit'),
    ('10_life_toolkit', 'Life toolkit with period tracker, body weight, hydration, calorie and meal planning tools'),
    ('11_period_tracker', 'Period tracker with cycle day, predictions and phase tips'),
    ('12_body_weight', 'Body weight tracker with trend chart and BMI'),
    ('13_hydration_coach', 'Hydration coach with daily water goal and quick add'),
    ('14_wellness_studio', 'Wellness studio with short breathing exercises'),
    ('15_wellness_reads', 'Wellness reads on sleep, movement, nutrition and mental health'),
    ('16_wellness_intention', 'Setting a new wellness intention'),
    ('17_habit_builder', 'Habit builder with starter habits and challenges'),
    ('18_habit_list', 'Habit builder list of active habits'),
    ('19_challenges', 'Wellness challenges in progress, like a 14-day sleep routine'),
    ('21_reflections', 'Guided wellness reflections and pinned conversations in light mode'),
    ('22_home_light', 'Home screen in light mode with AI insight and nutrition progress'),
]
HELP_SHAPE = 'Help shape <span class="grad-text">what\'s next</span>'
FEEDBACK_TYPES = ['Idea or feature request', 'Something isn\'t working', 'Something I love', 'Other']

# Messages the feedback form's script shows (the form still posts the same fields to the same Worker).
FORM_MSGS = {
    'sending': 'Sending…',
    'send': 'Send feedback',
    'invalid': 'Please choose a feedback type and write your message. If you add an email, check it’s valid.',
    'turnstile': 'Please complete the verification check above the button.',
    'failed': 'Sorry, we couldn’t send your feedback. Please check your connection and try again.',
    'thanks': 'Thanks. Your feedback has been sent.',
    'thanksName': 'Thanks, {name}. Your feedback has been sent.',
    'reply': 'We’ll reply to {email}.',
    'video': 'AI Wellness Pal complete walkthrough',
}


def home_card(slug, icon, title, text, indent='        '):
    ico = (f'<div class="ico"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" '
           f'stroke-linecap="round" stroke-linejoin="round">{ICONS[icon]}</svg></div>')
    if slug:
        return f'''{indent}<a class="card reveal" href="/features/{slug}/">
{indent}  {ico}
{indent}  <h3>{T(title)}</h3>
{indent}  <p>{T(text)}</p>
{indent}  <span class="more">{T('Learn more →')}</span>
{indent}</a>'''
    return f'''{indent}<article class="card reveal">
{indent}  {ico}
{indent}  <h3>{T(title)}</h3>
{indent}  <p>{T(text)}</p>
{indent}</article>'''


def home_main():
    phone_sizes = '(max-width: 720px) 200px, (max-width: 960px) 230px, 270px'
    shots = '\n'.join(
        f'      <picture><source type="image/webp" srcset="/assets/screens/w/{n}-300.webp 300w, /assets/screens/w/{n}-600.webp 600w" '
        f'sizes="(max-width: 720px) 190px, 230px"><img src="/assets/screens/{n}.jpg" alt="{esc(T(a))}" width="600" height="1300" '
        f'loading="lazy" decoding="async"></picture>' for n, a in HOME_SHOTS)
    options = '\n'.join(f'              <option value="{esc(o)}">{esc(T(o))}</option>' for o in FEEDBACK_TYPES)
    support_mail = f'<a class="grad-text" href="mailto:{C.EMAIL}?subject=AI%20Wellness%20Pal%20support">{C.EMAIL}</a>'
    gh = 'https://github.com/viraj-dhanushka/AIWellnessPal/issues'
    legal_note = '' if CUR == 'en' else ' ' + T('Our Privacy Policy and Terms of Use are available in English.')
    return f'''  <!-- Hero -->
  <section class="hero">
    <div class="wrap">
      <div>
        <span class="pill"><span class="dot"></span>{T('Now on the App Store and Google Play')}</span>
        <h1><span class="h1-kicker">{T('AI Wellness Pal · AI wellness coach app')}</span>{T('Feel better,<br><span class="grad-text">one day at a time.</span>')}</h1>
        <p class="lead">{T('<strong>AI Wellness Pal</strong> is a free AI wellness coach for iPhone and Android. A 30-second daily check-in becomes a personalized plan for mood, sleep, nutrition and habits — with an AI Wellness Pal to talk things through whenever you need it.')}</p>
        {store_buttons()}
        <div class="hero-meta">
          <span><svg><use href="#i-check"/></svg>{T('Free to download')}</span>
          <span><svg><use href="#i-check"/></svg>{T('No ads, no data selling')}</span>
          <span><svg><use href="#i-check"/></svg>{T('Delete your data anytime')}</span>
        </div>
      </div>
      <div class="phones" aria-hidden="true">
        <div class="phone back"><picture><source type="image/webp" srcset="/assets/screens/w/03_05_pal_chat-300.webp 300w, /assets/screens/w/03_05_pal_chat-600.webp 600w" sizes="{phone_sizes}"><img src="/assets/screens/03_05_pal_chat.jpg" alt="" width="600" height="1300" decoding="async"></picture></div>
        <div class="phone front"><picture><source type="image/webp" srcset="/assets/screens/w/01_02_home-300.webp 300w, /assets/screens/w/01_02_home-600.webp 600w" sizes="{phone_sizes}"><img src="/assets/screens/01_02_home.jpg" alt="" width="600" height="1300" fetchpriority="high"></picture></div>
      </div>
    </div>
  </section>

  <!-- How it works -->
  <section id="how" style="padding-top:40px">
    <div class="wrap">
      <div class="sec-head reveal">
        <span class="eyebrow">{T('How it works')}</span>
        <h2>{T('One check-in. <span class="grad-text">A plan that fits today.</span>')}</h2>
        <p>{T("Most wellness apps hand you the same plan as everyone else. AI Wellness Pal asks how you're actually doing first.")}</p>
      </div>
      <ol class="how reveal">
        <li><h3>{T('Check in (30 seconds)')}</h3><p>{T('Rate your energy, pick your mood, and say how your body feels and how much time you have. Skip anything you like.')}</p></li>
        <li><h3>{T("Get Today's Plan")}</h3><p>{T("Two to four small, doable actions shaped around your answers. Exhausted with fifteen minutes free? You get a very different day than when you're rested with an hour.")}</p></li>
        <li><h3>{T('Follow through with your Pal')}</h3><p>{T('Tick actions off, track water, meals, sleep and habits, and talk things through with your AI Wellness Pal when you need it.')}</p></li>
      </ol>
    </div>
  </section>

  <!-- Demo video -->
  <section id="demo">
    <div class="wrap">
      <div class="sec-head reveal">
        <span class="eyebrow">{T('See it in action')}</span>
        <h2>{T('Watch the <span class="grad-text">demo</span>')}</h2>
        <p>{T('A complete walkthrough of the app: check-ins, daily plans, the Wellness Pal chat, the toolkit and more.')}</p>
      </div>
      <div class="video reveal" id="video">
        <button type="button" aria-label="{esc(T('Play the AI Wellness Pal walkthrough video'))}">
          <img src="https://i.ytimg.com/vi/{C.YOUTUBE_ID}/hqdefault.jpg" alt="" width="480" height="360" loading="lazy" decoding="async">
          <span class="play"><svg viewBox="0 0 24 24"><path fill="currentColor" d="M7 4.5v15l12.5-7.5z"/></svg></span>
        </button>
      </div>
    </div>
  </section>

  <!-- Features -->
  <section id="features">
    <div class="wrap">
      <div class="sec-head reveal">
        <span class="eyebrow">{T('Everything in one place')}</span>
        <h2>{T('Your whole wellbeing, <span class="grad-text">gently guided</span>')}</h2>
        <p>{T('Small, doable actions that fit your energy, your time and your day.')}</p>
      </div>
      <div class="grid">
{chr(10).join(home_card(*c) for c in HOME_CORE)}
      </div>

      <div class="toolkit-head reveal">
        <span class="eyebrow">{T('The Life Toolkit')}</span>
        <h3>{T('Nine tools for <span class="grad-text">every part of life</span>')}</h3>
        <p>{T('From meals and water to sleep, cycles and travel. Open any tool from the More tab, and pin your favorites to your Home screen.')} <a href="/features/" style="color:var(--lavender)">{T('See every feature →')}</a></p>
      </div>
      <div class="grid toolkit">
{chr(10).join(home_card(*c) for c in HOME_TOOLKIT)}
      </div>
    </div>
  </section>

  <!-- Screenshots -->
  <section id="screens" aria-labelledby="screens-title" style="padding-top:0">
    <div class="wrap">
      <div class="shots-head reveal">
        <div>
          <span class="eyebrow">{T('Take a look inside')}</span>
          <h2 id="screens-title">{T('Made for <span class="grad-text">real days</span>')}</h2>
        </div>
        <div class="shots-nav">
          <button class="btn btn-icon" type="button" data-dir="-1" aria-label="{esc(T('Previous screenshots'))}"><svg viewBox="0 0 24 24"><path fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" d="M15 5l-7 7 7 7"/></svg></button>
          <button class="btn btn-icon" type="button" data-dir="1" aria-label="{esc(T('Next screenshots'))}"><svg viewBox="0 0 24 24"><path fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" d="M9 5l7 7-7 7"/></svg></button>
        </div>
      </div>
    </div>
    <div class="shots reveal" tabindex="0" aria-label="{esc(T('App screenshots, scroll sideways'))}">
{shots}
    </div>
  </section>

  <!-- Wellness Garden -->
  <section id="garden" aria-labelledby="garden-title">
    <div class="wrap">
      <div class="sec-head reveal">
        <span class="eyebrow">{T('Wellness Garden')}</span>
        <h2 id="garden-title">{T('Your habits grow <span class="grad-text">a garden</span>')}</h2>
        <p>{T('Every real step you take for yourself helps something grow. It turns building habits into something you look forward to opening, and it never punishes you for a missed day.')}</p>
      </div>
      <div class="garden-grid reveal">
        <figure class="garden-shot garden-main"><picture><source type="image/webp" srcset="/assets/screens/w/23_garden-640.webp 640w, /assets/screens/w/23_garden-1280.webp 1280w" sizes="(max-width: 720px) 92vw, 1100px"><img src="/assets/screens/23_garden.jpg" alt="{esc(T('The Wellness Garden in AI Wellness Pal, with flower planters, a gardener on the path, coins and a 10-day count'))}" width="1280" height="590" loading="lazy" decoding="async"></picture></figure>
        <figure class="garden-shot"><picture><source type="image/webp" srcset="/assets/screens/w/24_garden_gifts-640.webp 640w, /assets/screens/w/24_garden_gifts-1280.webp 1280w" sizes="(max-width: 720px) 92vw, 540px"><img src="/assets/screens/24_garden_gifts.jpg" alt="{esc(T('Garden gifts: one gift for every day you show up, with a chest at the end of each round'))}" width="1280" height="590" loading="lazy" decoding="async"></picture></figure>
        <figure class="garden-shot"><picture><source type="image/webp" srcset="/assets/screens/w/25_garden_map-640.webp 640w, /assets/screens/w/25_garden_map-1280.webp 1280w" sizes="(max-width: 720px) 92vw, 540px"><img src="/assets/screens/25_garden_map.jpg" alt="{esc(T('Garden map with Meadow, Zen garden, Greenhouse and Seaside places that open as you level up'))}" width="1280" height="590" loading="lazy" decoding="async"></picture></figure>
      </div>
      <ul class="garden-points reveal">
        <li><h3>{T('Grows when you show up')}</h3><p>{T('Your garden grows a little each day you show up and keeps everything it grows. Habits become seeds you plant, and finished habits grow fruit to pick.')}</p></li>
        <li><h3>{T('Streaks without the stress')}</h3><p>{T('Missed a day? Nothing is lost. Your level only goes up, and when you come back everything has waited for you. On a tired day, the tiny version of a habit counts just the same.')}</p></li>
        <li><h3>{T('A daily reason to come back')}</h3><p>{T('Open a garden gift for every day you show up, earn coins for check-ins, habits and water, and spend them on plants and decorations.')}</p></li>
        <li><h3>{T('Something new to discover')}</h3><p>{T('Dress up your companions, meet garden visitors, plant a private mood flower with each check-in and unlock new places like the Greenhouse and Seaside as you level up.')}</p></li>
      </ul>
    </div>
  </section>

  <!-- Free vs Premium -->
  <section id="pricing">
    <div class="wrap">
      <div class="sec-head reveal">
        <span class="eyebrow">{T('Pricing')}</span>
        <h2>{T('Free to use. <span class="grad-text">Premium when you want more.</span>')}</h2>
        <p>{T('The core app is free on iPhone and Android, with no ads. Premium adds unlimited AI and voice.')}</p>
      </div>
      <div class="pricing reveal">
        <div class="plan">
          <h3>{T('Free')}</h3>
          <p class="price">{T('$0, no ads')}</p>
          <ul>
            <li>{T("<strong>Daily check-ins</strong> and a personalized Today's Plan")}</li>
            <li>{T('An <strong>AI journal</strong> with guided reflections')}</li>
            <li>{T('<strong>3 Wellness Pal messages</strong> a day')}</li>
            <li>{T('Habits, challenges, reminders and streaks')}</li>
            <li>{T('Hydration, sleep, period and weight tracking, plus a calorie budget')}</li>
            <li>{T('Meditation, breathing and body scans, and every theme')}</li>
            <li>{T('Home-screen widgets')}</li>
          </ul>
        </div>
        <div class="plan premium">
          <h3>{T('Premium')}</h3>
          <p class="price">{T('7-day free trial, then monthly or yearly')}</p>
          <ul>
            <li>{T('<strong>Unlimited</strong> Wellness Pal chat')}</li>
            <li>{T('<strong>Live Chat Pal</strong>: real-time voice conversations')}</li>
            <li>{T('<strong>AI food analysis</strong> from a photo, description or barcode, and <strong>AI meal plans</strong>')}</li>
            <li>{T('AI sleep, hydration and calorie insights, and weather-aware water goals')}</li>
            <li>{T('“Discuss” your reflections and AI steps for your intentions')}</li>
            <li>{T('The full Wellness Studio library')}</li>
          </ul>
        </div>
      </div>
      <p class="fine">{T('On the US App Store, Premium is $14.99 a month or $89.99 a year. Prices vary by country and are shown in the App Store or Google Play before you subscribe. Cancel anytime in your store subscriptions.')}</p>
    </div>
  </section>

  <!-- FAQ (from tools/site_content.py) -->
  <section id="faq">
    <div class="wrap">
      <div class="sec-head reveal">
        <span class="eyebrow">{T('FAQ')}</span>
        <h2>{T('Questions, <span class="grad-text">answered</span>')}</h2>
      </div>
      <div class="faq">
{faq_html(C.HOME_FAQS)}
      </div>
      <p class="fine"><a href="/faq/" style="color:var(--lavender)">{T('See all questions →')}</a></p>
    </div>
  </section>

  <!-- Feedback -->
  <section id="feedback">
    <div class="wrap">
      <div class="feedback-card reveal">
        <div>
          <span class="eyebrow">{T('Feedback')}</span>
          <h2>{T(HELP_SHAPE)}</h2>
          <p>{T('Love something, missing something, or found a bug? Tell us. Every message is read, and your ideas shape the next update.')}</p>
          <ol class="steps">
            <li><strong>{T('Share your thoughts')}</strong>{T('Ideas, bugs, praise: all of it helps.')}</li>
            <li><strong>{T("Leave your email if you'd like a reply")}</strong>{T("It's optional, and only used to answer you.")}</li>
            <li><strong>{T('Enjoying the app?')}</strong>{T('A quick review helps others find it:')} <a href="{C.APPLE}?action=write-review">App Store</a> · <a href="{C.PLAY}&amp;showAllReviews=true">Google Play</a></li>
          </ol>
        </div>
        <div class="request-wrap">
        <form class="request" id="feedback-form" action="https://api.aiwellnesspal.com/submit?form=feedback" method="POST" novalidate>
          <input class="hp" type="text" name="_honey" tabindex="-1" autocomplete="off" aria-hidden="true">
          <div class="field">
            <label for="f-type">{T('What kind of feedback?')}</label>
            <select id="f-type" name="type" required>
              <option value="">{T('Choose one')}</option>
{options}
            </select>
          </div>
          <div class="field">
            <label for="f-platform">{T('Which device?')} <span class="hint">{T('(optional)')}</span></label>
            <select id="f-platform" name="platform">
              <option value="">{T('Choose one')}</option>
              <option>iPhone</option>
              <option>Android</option>
            </select>
          </div>
          <div class="field">
            <label for="f-note">{T('Your feedback')}</label>
            <textarea id="f-note" name="message" required></textarea>
          </div>
          <div class="field">
            <label for="f-name">{T('Name')} <span class="hint">{T('(optional)')}</span></label>
            <input id="f-name" name="name" type="text" autocomplete="name">
          </div>
          <div class="field">
            <label for="f-email">{T('Email')} <span class="hint">{T("(optional, if you'd like a reply)")}</span></label>
            <input id="f-email" name="email" type="email" autocomplete="email" placeholder="you@example.com">
          </div>
          <div class="cf-turnstile" data-sitekey="0x4AAAAAAFeATWxgyA2X7qGo" data-theme="dark" data-size="flexible"></div>
          <div class="form-alert" role="alert" hidden></div>
          <button class="btn btn-grad" type="submit"><span class="spinner" aria-hidden="true"></span><span class="btn-label">{T(FORM_MSGS['send'])}</span></button>
        </form>
        <div class="request-done" id="feedback-done" tabindex="-1" hidden>
          <div class="done-icon"><svg viewBox="0 0 24 24"><use href="#i-check"/></svg></div>
          <h3>{T('Thank you!')}</h3>
          <p id="done-msg">{T(FORM_MSGS['thanks'])}</p>
          <button class="btn" type="button" id="feedback-again">{T('Send more feedback')}</button>
        </div>
        </div>
      </div>
    </div>
  </section>

  <!-- Support (App Store Connect support URL points to this page) -->
  <section id="support">
    <div class="wrap">
      <div class="sec-head reveal">
        <span class="eyebrow">{T('Support')}</span>
        <h2>{T('Here to <span class="grad-text">help</span>')}</h2>
        <p>{T('Need help, found a bug, or have a question? Email {email} and we’ll get back to you. You can also <a class="grad-text" href="{github}">report a bug on GitHub</a>.').replace('{email}', support_mail).replace('{github}', gh)}</p>
      </div>
      <div class="support-grid">
        <article class="card reveal">
          <h3>{T('Delete your account')}</h3>
          <p>{T('In the app, go to <strong>Settings → Delete Account</strong>. This permanently deletes your account and all of your data. No longer have the app? <a href="/delete-account.html">Request deletion on the web</a>.')}</p>
        </article>
        <article class="card reveal">
          <h3>{T('Manage or cancel Premium')}</h3>
          <p>{T('On iPhone, go to <strong>Settings → your name → Subscriptions → AI Wellness Pal</strong>. On Android, open Google Play → <strong>Payments &amp; subscriptions → Subscriptions</strong>. To restore Premium on a new device, use <strong>Restore Purchases</strong> in the app.')}</p>
        </article>
        <article class="card reveal">
          <h3>{T('Connect or disconnect sleep data')}</h3>
          <p>{T('On iPhone, go to <strong>Settings → Health → Data Access &amp; Devices → AI Wellness Pal</strong>. On Android, open <strong>Health Connect → App permissions → AI Wellness Pal</strong>.')}</p>
        </article>
        <article class="card reveal">
          <h3>{T('Not medical advice')}</h3>
          <p>{T('AI Wellness Pal offers general wellness information and is not a substitute for professional medical advice. If you are in crisis or have a medical emergency, call your local emergency number immediately.')}</p>
        </article>
      </div>
      <p class="notice">{T('Read our <a href="/privacy.html">Privacy Policy</a> and <a href="/terms.html">Terms of Use</a>.')}{legal_note}</p>
    </div>
  </section>

  <!-- Final CTA -->
{final_cta('final reveal')}'''


HOME_SCRIPT = '''<script>
  var M = __MSGS__;

  // Load the YouTube player only when someone presses play (faster page, no tracking until then).
  document.querySelector('#video button').addEventListener('click', function () {
    var f = document.createElement('iframe');
    f.src = 'https://www.youtube-nocookie.com/embed/__YT__?autoplay=1&rel=0&modestbranding=1&playsinline=1&hl=' + document.documentElement.lang;
    f.title = M.video;
    f.allow = 'accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share';
    f.allowFullscreen = true;
    f.referrerPolicy = 'strict-origin-when-cross-origin';
    this.replaceWith(f);
  });

  // Fade sections in as they scroll into view.
  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); } });
    }, { threshold: 0.12 });
    document.querySelectorAll('.reveal').forEach(function (el) { io.observe(el); });
  } else {
    document.querySelectorAll('.reveal').forEach(function (el) { el.classList.add('in'); });
  }

  // Screenshot gallery arrows: scroll by roughly one screen's worth of images (mirrored for right-to-left).
  (function () {
    var strip = document.querySelector('.shots');
    var btns = document.querySelectorAll('.shots-nav button');
    var rtl = document.documentElement.dir === 'rtl' ? -1 : 1;
    function update() {
      var pos = Math.abs(strip.scrollLeft);
      btns[0].disabled = pos <= 4;
      btns[1].disabled = pos + strip.clientWidth >= strip.scrollWidth - 4;
    }
    btns.forEach(function (b) {
      b.addEventListener('click', function () {
        strip.scrollBy({ left: rtl * Number(b.dataset.dir) * strip.clientWidth * 0.8, behavior: 'smooth' });
      });
    });
    strip.addEventListener('scroll', update, { passive: true });
    window.addEventListener('resize', update);
    requestAnimationFrame(update);
  })();

  // "Get the app" goes to Google Play on Android, the App Store elsewhere.
  if (/android/i.test(navigator.userAgent)) {
    document.getElementById('get-app').href = '__PLAY__';
  }

  // Load Cloudflare Turnstile (the form's bot check) only when the form is about to be used.
  (function () {
    var loaded = false;
    function load() {
      if (loaded) return; loaded = true;
      var sc = document.createElement('script');
      sc.src = 'https://challenges.cloudflare.com/turnstile/v0/api.js'; sc.async = true;
      document.head.appendChild(sc);
    }
    var target = document.getElementById('feedback');
    if ('IntersectionObserver' in window) {
      var tio = new IntersectionObserver(function (es) { if (es.some(function (e) { return e.isIntersecting; })) { load(); tio.disconnect(); } }, { rootMargin: '600px 0px' });
      tio.observe(target);
    } else { load(); }
    target.addEventListener('focusin', load);
    if (location.hash === '#feedback') load();
  })();

  // Feedback form: posts to the Cloudflare Worker (cloudflare/forms-worker), which checks Turnstile and emails it.
  var form = document.getElementById('feedback-form');
  var done = document.getElementById('feedback-done');
  var alertBox = form.querySelector('.form-alert');
  var btn = form.querySelector('button[type=submit]');
  var btnLabel = btn.querySelector('.btn-label');

  function showAlert(msg) { alertBox.textContent = msg; alertBox.hidden = false; }
  function setSending(on) {
    btn.disabled = on; btn.classList.toggle('sending', on);
    btnLabel.textContent = on ? M.sending : M.send;
  }

  form.addEventListener('input', function (e) {
    if (e.target.validity && e.target.validity.valid) e.target.removeAttribute('aria-invalid');
  });

  form.addEventListener('submit', function (e) {
    e.preventDefault();
    alertBox.hidden = true;
    // Required fields, plus the optional email when one was typed.
    var invalid = Array.prototype.filter.call(form.querySelectorAll('[required], input[type=email]'), function (el) {
      var bad = !el.checkValidity();
      if (bad) el.setAttribute('aria-invalid', 'true'); else el.removeAttribute('aria-invalid');
      return bad;
    });
    if (invalid.length) {
      showAlert(M.invalid);
      invalid[0].focus();
      return;
    }
    // Turnstile adds this hidden field once the visitor passes the check.
    var tsField = form.querySelector('[name="cf-turnstile-response"]');
    if (!tsField || !tsField.value) {
      showAlert(M.turnstile);
      return;
    }
    var name = form.elements.namedItem('name').value.trim();
    var email = form.elements.namedItem('email').value.trim();
    setSending(true);
    fetch(form.action, { method: 'POST', body: new FormData(form), headers: { Accept: 'application/json' } })
      .then(function (r) { return r.json().catch(function () { return {}; }).then(function (d) { return { ok: r.ok, d: d }; }); })
      .then(function (res) {
        if (!res.ok || String(res.d.success) !== 'true') throw new Error(res.d.message || 'Request failed');
        form.reset();
        var msg = name ? M.thanksName.replace('{name}', name.split(' ')[0]) : M.thanks;
        if (email) msg += ' ' + M.reply.replace('{email}', email);
        document.getElementById('done-msg').textContent = msg;
        form.hidden = true;
        done.hidden = false;
        done.focus();
      })
      .catch(function (err) {
        // The Worker's own verification messages are English; show ours in the page's language.
        var vmsg = /verification/i.test(err && err.message);
        showAlert(vmsg ? (document.documentElement.lang === 'en' ? err.message : M.turnstile) : M.failed);
      })
      .finally(function () {
        setSending(false);
        // Tokens are single-use: get a fresh one for the next attempt.
        if (window.turnstile) turnstile.reset(form.querySelector('.cf-turnstile'));
      });
  });

  document.getElementById('feedback-again').addEventListener('click', function () {
    done.hidden = true;
    form.hidden = false;
    form.querySelector('select').focus();
  });
</script>'''


def home_ld():
    app = {
        '@type': 'MobileApplication', '@id': SITE + '/#app', 'name': 'AI Wellness Pal', 'url': SITE + '/',
        'description': T(C.APP_DESCRIPTION), 'abstract': T(C.TAGLINE),
        'image': SITE + '/assets/icon.png',
        'screenshot': [SITE + f'/assets/screens/{n}.jpg' for n in C.SCHEMA_SCREENSHOTS],
        'operatingSystem': 'iOS 15.0 or later, Android 8.0 or later',
        'applicationCategory': 'HealthApplication', 'applicationSubCategory': 'Wellness',
        'featureList': [T(x) for x in C.FEATURE_LIST],
        'offers': [
            {'@type': 'Offer', 'name': 'Free', 'price': '0', 'priceCurrency': 'USD'},
            {'@type': 'Offer', 'name': 'Premium Monthly (US App Store)', 'price': C.PRICE_MONTHLY, 'priceCurrency': 'USD',
             'description': 'Auto-renewing subscription with a 7-day free trial.'},
            {'@type': 'Offer', 'name': 'Premium Yearly (US App Store)', 'price': C.PRICE_YEARLY, 'priceCurrency': 'USD',
             'description': 'Auto-renewing subscription with a 7-day free trial.'},
        ],
        'isAccessibleForFree': True, 'inLanguage': CODES, 'datePublished': C.IOS_RELEASE,
        'installUrl': [C.APPLE, C.PLAY], 'downloadUrl': [C.APPLE, C.PLAY], 'sameAs': [C.APPLE, C.PLAY],
        'author': {'@id': SITE + '/#founder'}, 'publisher': {'@id': SITE + '/#organization'},
        'softwareHelp': {'@type': 'WebPage', 'url': lurl('/faq/')},
        'video': {'@id': SITE + '/#demo-video'},
    }
    return {'@context': 'https://schema.org', '@graph': [
        {'@type': 'WebSite', '@id': SITE + '/#website', 'url': SITE + '/', 'name': 'AI Wellness Pal',
         'alternateName': ['AI Wellness Pal app', 'aiwellnesspal.com', 'aiwelnesspal.com'], 'inLanguage': CODES,
         'publisher': {'@id': SITE + '/#organization'}},
        {'@type': 'Organization', '@id': SITE + '/#organization', 'name': 'AI Wellness Pal', 'url': SITE + '/',
         'logo': {'@type': 'ImageObject', 'url': SITE + '/assets/icon.png', 'width': 512, 'height': 512},
         'email': C.EMAIL, 'founder': {'@id': SITE + '/#founder'},
         'contactPoint': {'@type': 'ContactPoint', 'contactType': 'customer support', 'email': C.EMAIL, 'availableLanguage': 'en'},
         'sameAs': [C.APPLE, C.PLAY]},
        {'@type': 'Person', '@id': SITE + '/#founder', 'name': 'Viraj Dhanushka', 'jobTitle': 'Founder and developer',
         'worksFor': {'@id': SITE + '/#organization'}},
        webpage_ld('/', T(C.HOME_TITLE), T(C.HOME_DESC), extra={'@type': 'WebPage', 'mainEntity': {'@id': SITE + '/#app'}}),
        app,
        {'@type': 'VideoObject', '@id': SITE + '/#demo-video', 'name': 'AI Wellness Pal – Complete Walkthrough',
         'description': 'A complete walkthrough of AI Wellness Pal: daily check-ins, personalized plans, the Wellness Pal chat, the Life Toolkit and more.',
         'thumbnailUrl': f'https://i.ytimg.com/vi/{C.YOUTUBE_ID}/hqdefault.jpg',
         'embedUrl': f'https://www.youtube-nocookie.com/embed/{C.YOUTUBE_ID}',
         'contentUrl': C.YOUTUBE_VIDEO, 'uploadDate': '2026-11-18T07:46:21-08:00', 'inLanguage': 'en'},
        faq_ld(C.HOME_FAQS, lurl('/')),
    ]}


def home_page():
    msgs = {k: T(v) for k, v in FORM_MSGS.items()}
    script = (HOME_SCRIPT.replace('__MSGS__', json.dumps(msgs, ensure_ascii=False))
              .replace('__YT__', C.YOUTUBE_ID).replace('__PLAY__', C.PLAY))
    extra = ('\n  <link rel="preload" as="image" type="image/webp" href="/assets/screens/w/01_02_home-600.webp" '
             'imagesrcset="/assets/screens/w/01_02_home-300.webp 300w, /assets/screens/w/01_02_home-600.webp 600w" '
             'imagesizes="(max-width: 720px) 200px, (max-width: 960px) 230px, 270px">\n'
             '  <noscript><style>.reveal { opacity: 1; transform: none; }</style></noscript>')
    head_kw = dict(og_title=T(HOME_OG_TITLE), og_desc=T(HOME_OG_DESC), tw_desc=T(HOME_TW_DESC), extra=extra)
    html_ = page(T(C.HOME_TITLE), T(C.HOME_DESC), '/', home_ld(), home_main(), head_kw=head_kw,
                 main_attrs=' id="top"', scripts=script)
    return write(out('index.html'), html_)


# ---------------------------------------------------------------- language prompt strings

def update_lang_js():
    """Fill the per-language 'View this page in …?' strings in assets/lang.js."""
    global CUR
    prompts = {}
    for c in CODES:
        CUR = c
        # Each language file has its own whole sentence under '@prompt' (names the language naturally).
        q = TR.get(c, {}).get('@prompt') or T('View this page in {language}?').replace('{language}', NATIVE[c])
        prompts[c] = {'q': q,
                      'yes': NATIVE[c], 'no': T('No thanks')}
    CUR = 'en'
    p = ROOT / 'assets' / 'lang.js'
    t = p.read_text()
    pat = re.compile(r'(/\* BUILD:PROMPTS \*/)(.*?)(/\* /BUILD:PROMPTS \*/)', re.S)
    assert pat.search(t), 'BUILD:PROMPTS marker missing in assets/lang.js'
    t = pat.sub(lambda m: m.group(1) + json.dumps(prompts, ensure_ascii=False, indent=2) + m.group(3), t, count=1)
    p.write_text(t)


# ---------------------------------------------------------------- sitemap + llms

def lastmod(rel):
    """Last commit date of a file; today if it has uncommitted changes."""
    try:
        dirty = subprocess.run(['git', 'status', '--porcelain', '--', rel], cwd=ROOT, capture_output=True, text=True).stdout.strip()
        if dirty:
            return TODAY
        d = subprocess.run(['git', 'log', '-1', '--format=%cs', '--', rel], cwd=ROOT, capture_output=True, text=True).stdout.strip()
        return d or TODAY
    except Exception:
        return TODAY


def sitemap(pages):
    out_ = ['<?xml version="1.0" encoding="UTF-8"?>',
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" '
            'xmlns:image="http://www.google.com/schemas/sitemap-image/1.1" '
            'xmlns:xhtml="http://www.w3.org/1999/xhtml">']
    for path, rel, images, langs in pages:
        for c in langs:
            out_.append('  <url>')
            out_.append(f'    <loc>{lurl(path, c)}</loc>')
            out_.append(f'    <lastmod>{lastmod(rel if c == "en" else c + "/" + rel)}</lastmod>')
            if len(langs) > 1:
                for a in langs:
                    out_.append(f'    <xhtml:link rel="alternate" hreflang="{a}" href="{lurl(path, a)}"/>')
                out_.append(f'    <xhtml:link rel="alternate" hreflang="x-default" href="{lurl(path, "en")}"/>')
            for img in images:
                out_.append(f'    <image:image><image:loc>{SITE}{img}</image:loc></image:image>')
            out_.append('  </url>')
    out_.append('</urlset>')
    (ROOT / 'sitemap.xml').write_text('\n'.join(out_) + '\n')


def llms():
    feats = '\n'.join(f'- [{f["short"]}]({url("/features/" + f["slug"] + "/")}): {f["card"]}' for f in C.FEATURES)
    langs = '\n'.join(f'- [{NATIVE[c]}]({lurl("/", c)})' for c in CODES[1:])
    short = f'''# AI Wellness Pal

> {C.DEFINITION_PLAIN}

{C.LLMS_SUMMARY}

## Key pages
- [Home]({SITE}/): overview, demo video, pricing, FAQ
- [All features]({SITE}/features/)
- [FAQ]({SITE}/faq/): answers about features, pricing, privacy and devices
- [About]({SITE}/about/): key facts (developer, launch dates, platforms, pricing, AI provider)
- [Privacy Policy]({SITE}/privacy.html)
- [Terms of Use]({SITE}/terms.html)
- [Delete your account]({SITE}/delete-account.html)

## Features
{feats}

## Download
- [App Store (iPhone)]({C.APPLE})
- [Google Play (Android)]({C.PLAY})

## Other languages
This site is also available in 22 other languages, with the same pages under /<language code>/ (for example {SITE}/es/faq/). The Privacy Policy and Terms of Use are English only.
{langs}

## Optional
- [Full text for AI assistants]({SITE}/llms-full.txt)
- [Demo video]({C.YOUTUBE_VIDEO})
'''
    (ROOT / 'llms.txt').write_text(short)

    parts = [f'# AI Wellness Pal — full reference\n\n{C.DEFINITION_PLAIN}\n\nWebsite: {SITE}/\n',
             '## Key facts\n' + '\n'.join(f'- {k}: {plain(v)}' for k, v in C.FACTS) + '\n']
    for f in C.FEATURES:
        parts.append(f'## {f["short"]}\nPage: {url("/features/" + f["slug"] + "/")}\n\n{plain(f["lead"])}\n\n{plain(f["body"])}\n\n'
                     + '\n\n'.join(f'Q: {q}\nA: {plain(a)}' for q, a in f['faqs']) + '\n')
    parts.append('## Frequently asked questions\n' + '\n\n'.join(
        f'Q: {q}\nA: {plain(a)}' for _, items in C.FAQ_GROUPS for q, a in items) + '\n')
    (ROOT / 'llms-full.txt').write_text('\n'.join(parts))


# ---------------------------------------------------------------- main

def build_language(c):
    global CUR
    CUR = c
    written = [home_page(), hub_page(), faq_page(), about_page()]
    written += [feature_page(f) for f in C.FEATURES]
    CUR = 'en'
    return written


def main():
    load_translations()
    written = []
    for c in CODES:
        written += build_language(c)
    update_lang_js()
    I18N.mkdir(exist_ok=True)
    (I18N / 'en.json').write_text(json.dumps(EN, ensure_ascii=False, indent=1) + '\n')

    pages = [('/', 'index.html', [f'/assets/screens/{n}.jpg' for n in C.SCHEMA_SCREENSHOTS] + ['/assets/og-image.png'], CODES),
             ('/features/', 'features/index.html', [], CODES),
             ('/faq/', 'faq/index.html', [], CODES),
             ('/about/', 'about/index.html', ['/assets/icon.png'], CODES)]
    for f in C.FEATURES:
        imgs = ([f'/assets/screens/{f["hero"][0]}.jpg'] if f.get('hero') else []) + [f'/assets/screens/{n}.jpg' for n, _ in f.get('shots', [])]
        imgs += f.get('images', [])
        pages.append((f'/features/{f["slug"]}/', f'features/{f["slug"]}/index.html', list(dict.fromkeys(imgs)), CODES))
    pages += [(p, rel, [], ['en']) for p, rel in ENGLISH_ONLY]
    sitemap(pages)
    llms()
    print(f'built: {len(written)} pages in {len(CODES)} languages, {len(EN)} strings in i18n/en.json, '
          'sitemap.xml, llms.txt, llms-full.txt')
    if MISSING:
        total = sum(len(v) for v in MISSING.values())
        print(f'untranslated (shown in English): {total} strings across {len(MISSING)} languages; '
              'run tools/check_site.py for details')


if __name__ == '__main__':
    main()
