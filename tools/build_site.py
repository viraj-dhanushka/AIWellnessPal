#!/usr/bin/env python3
"""Builds aiwelnesspal.com's content pages, sitemap and AI-crawler files.

Run from the repo root after editing tools/site_content.py:
    python3 tools/build_site.py

Writes (generated, don't edit by hand):
    features/index.html, features/<slug>/index.html, faq/index.html,
    about/index.html, sitemap.xml, llms.txt, llms-full.txt
and refreshes the blocks between <!-- BUILD:X --> ... <!-- /BUILD:X --> markers
in index.html (header nav, structured data, FAQ, footer).

No dependencies beyond Python 3.
"""
import datetime
import html
import json
import re
import subprocess
from pathlib import Path

import site_content as C

ROOT = Path(__file__).resolve().parent.parent
SITE = C.SITE
TODAY = datetime.date.today().isoformat()
FONT_CSS = 'https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400..800&display=swap'


# ---------------------------------------------------------------- helpers

def esc(s):
    return html.escape(s, quote=True)


def plain(fragment):
    """HTML fragment -> plain text (for JSON-LD answers and llms.txt)."""
    t = re.sub(r'<li[^>]*>', '\n- ', fragment)
    t = re.sub(r'</p>\s*<p[^>]*>', '\n\n', t)
    t = re.sub(r'<br\s*/?>', '\n', t)
    t = re.sub(r'<[^>]+>', '', t)
    t = html.unescape(t)
    return re.sub(r'[ \t]+', ' ', re.sub(r'\n{3,}', '\n\n', t)).strip()


def url(path):
    return SITE + path


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


def store_buttons():
    return f'''<div class="cta">
          <a class="btn btn-store" href="{C.APPLE}">
            <svg aria-hidden="true"><use href="#i-apple"/></svg>
            <span class="lbl"><small>Download on the</small><strong>App Store</strong></span>
          </a>
          <a class="btn btn-store" href="{C.PLAY}">
            <svg aria-hidden="true"><use href="#i-play"/></svg>
            <span class="lbl"><small>Get it on</small><strong>Google Play</strong></span>
          </a>
        </div>'''


SVG_DEFS = '''<svg width="0" height="0" style="position:absolute" aria-hidden="true">
  <symbol id="i-apple" viewBox="0 0 24 24"><path fill="currentColor" d="M12.152 6.896c-.948 0-2.415-1.078-3.96-1.04-2.04.027-3.91 1.183-4.961 3.014-2.117 3.675-.546 9.103 1.519 12.09 1.013 1.454 2.208 3.09 3.792 3.039 1.52-.065 2.09-.987 3.935-.987 1.831 0 2.35.987 3.96.948 1.637-.026 2.676-1.48 3.676-2.948 1.156-1.688 1.636-3.325 1.662-3.415-.039-.013-3.182-1.221-3.22-4.857-.026-3.04 2.48-4.494 2.597-4.559-1.429-2.09-3.623-2.324-4.39-2.376-2-.156-3.675 1.09-4.61 1.09zM15.53 3.83c.843-1.012 1.4-2.427 1.245-3.83-1.207.052-2.662.805-3.532 1.818-.78.896-1.454 2.338-1.273 3.714 1.338.104 2.715-.688 3.559-1.701"/></symbol>
  <symbol id="i-play" viewBox="0 0 24 24"><path fill="currentColor" d="M22.018 13.298l-3.919 2.218-3.515-3.493 3.543-3.521 3.891 2.202a1.49 1.49 0 0 1 0 2.594zM1.337.924a1.486 1.486 0 0 0-.112.568v21.017c0 .217.045.419.124.6l11.155-11.087L1.337.924zm12.207 10.065l3.258-3.238L3.45.195a1.466 1.466 0 0 0-.946-.179l11.04 10.973zm0 2.067l-11 10.933c.298.036.612-.016.906-.183l13.324-7.54-3.23-3.21z"/></symbol>
  <symbol id="i-check" viewBox="0 0 24 24"><path fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" d="M5 12.5l4.5 4.5L19 7.5"/></symbol>
</svg>'''


def nav(active=''):
    items = [('/features/', 'Features'), ('/#demo', 'Demo'), ('/faq/', 'FAQ'), ('/about/', 'About'), ('/#support', 'Support')]
    links = '\n      '.join(
        f'<a href="{h}"{" aria-current=" + chr(34) + "page" + chr(34) if h == active else ""}>{t}</a>' for h, t in items)
    return f'''<header class="nav">
  <div class="wrap">
    <a class="brand" href="/">{icon_img(34)}AI Wellness Pal</a>
    <nav class="nav-links" aria-label="Main">
      {links}
    </nav>
    <a class="btn btn-sm btn-grad" id="get-app" href="{C.APPLE}">Get the app</a>
  </div>
</header>'''


def footer():
    feats = '\n        '.join(f'<a href="/features/{f["slug"]}/">{esc(f["short"])}</a>' for f in C.FEATURES)
    return f'''<footer class="site-footer">
  <div class="wrap foot-grid">
    <div>
      <a class="brand" href="/">{icon_img(34)}AI Wellness Pal</a>
      <p>{esc(C.TAGLINE)}. Free on iPhone and Android.</p>
      <p class="foot-stores"><a href="{C.APPLE}">App Store</a> · <a href="{C.PLAY}">Google Play</a></p>
    </div>
    <nav aria-label="Features">
      <p class="foot-h">Features</p>
        {feats}
    </nav>
    <nav aria-label="Resources">
      <p class="foot-h">Resources</p>
      <a href="/features/">All features</a>
      <a href="/faq/">FAQ</a>
      <a href="/about/">About</a>
      <a href="/#demo">Demo video</a>
      <a href="/#support">Support</a>
      <a href="/#feedback">Send feedback</a>
    </nav>
    <nav aria-label="Legal">
      <p class="foot-h">Legal</p>
      <a href="/privacy.html">Privacy Policy</a>
      <a href="/terms.html">Terms of Use</a>
      <a href="/delete-account.html">Delete your account</a>
    </nav>
  </div>
  <div class="wrap foot-bottom">
    <span>© 2026 Viraj Dhanushka</span>
    <span>Not medical advice. AI Wellness Pal provides general wellness information.</span>
  </div>
</footer>'''


GET_APP_SCRIPT = f'''<script>
  // "Get the app" opens Google Play on Android, the App Store elsewhere.
  if (/android/i.test(navigator.userAgent)) document.getElementById('get-app').href = '{C.PLAY}';
</script>'''


def head(title, desc, path, ld, og_type='website', robots='index, follow, max-image-preview:large, max-snippet:-1'):
    return f'''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{esc(title)}</title>
  <meta name="description" content="{esc(desc)}">
  <meta name="robots" content="{robots}">
  <meta name="author" content="Viraj Dhanushka">
  <meta name="theme-color" content="#0d0f1c">
  <link rel="canonical" href="{url(path)}">
  <link rel="icon" type="image/png" href="/assets/favicon.png">
  <link rel="apple-touch-icon" href="/assets/apple-touch-icon.png">
  <link rel="manifest" href="/site.webmanifest">
  <meta name="apple-itunes-app" content="app-id={C.APPLE_ID}">
  <meta property="og:type" content="{og_type}">
  <meta property="og:site_name" content="AI Wellness Pal">
  <meta property="og:locale" content="en_US">
  <meta property="og:title" content="{esc(title)}">
  <meta property="og:description" content="{esc(desc)}">
  <meta property="og:url" content="{url(path)}">
  <meta property="og:image" content="{SITE}/assets/og-image.png">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta property="og:image:alt" content="AI Wellness Pal app: Feel better, one day at a time.">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{esc(title)}">
  <meta name="twitter:description" content="{esc(desc)}">
  <meta name="twitter:image" content="{SITE}/assets/og-image.png">
{font_links()}
  <link rel="stylesheet" href="/landing.css">
  <script type="application/ld+json">
{json.dumps(ld, ensure_ascii=False, indent=2)}
  </script>
</head>'''


def font_links(indent='  '):
    """Fonts load without blocking the first paint (system font shows until then)."""
    return '\n'.join(indent + l for l in [
        '<link rel="preconnect" href="https://fonts.googleapis.com">',
        '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>',
        f'<link rel="preload" as="style" href="{FONT_CSS}">',
        f'<link rel="stylesheet" href="{FONT_CSS}" media="print" onload="this.media=\'all\'">',
        f'<noscript><link rel="stylesheet" href="{FONT_CSS}"></noscript>',
    ])


def faq_html(faqs):
    return '\n'.join(
        f'''      <details>
        <summary>{esc(q)}</summary>
        <div class="a">{a}</div>
      </details>''' for q, a in faqs)


def faq_ld(faqs, page_url):
    return {
        '@type': 'FAQPage',
        '@id': page_url + '#faq',
        'mainEntity': [{'@type': 'Question', 'name': q,
                        'acceptedAnswer': {'@type': 'Answer', 'text': plain(a)}} for q, a in faqs],
    }


def crumbs_html(crumbs):
    items = []
    for i, (name, path) in enumerate(crumbs):
        last = i == len(crumbs) - 1
        items.append(f'<li>{esc(name)}</li>' if last else f'<li><a href="{path}">{esc(name)}</a></li>')
    return f'<nav class="crumbs" aria-label="Breadcrumb"><ol>{"".join(items)}</ol></nav>'


def crumbs_ld(crumbs, page_url):
    return {
        '@type': 'BreadcrumbList',
        '@id': page_url + '#breadcrumb',
        'itemListElement': [{'@type': 'ListItem', 'position': i + 1, 'name': n, 'item': url(p)}
                            for i, (n, p) in enumerate(crumbs)],
    }


def webpage_ld(path, title, desc, crumbs=None, extra=None):
    u = url(path)
    d = {
        '@type': 'WebPage', '@id': u + '#webpage', 'url': u, 'name': title, 'description': desc,
        'inLanguage': 'en', 'isPartOf': {'@id': SITE + '/#website'}, 'about': {'@id': SITE + '/#app'},
        'publisher': {'@id': SITE + '/#organization'}, 'dateModified': TODAY,
        'primaryImageOfPage': {'@type': 'ImageObject', 'url': SITE + '/assets/og-image.png'},
    }
    if crumbs:
        d['breadcrumb'] = {'@id': u + '#breadcrumb'}
    if extra:
        d.update(extra)
    return d


def final_cta(title='Start feeling better <span class="grad-text">today</span>', sub='Free on iPhone and Android.'):
    return f'''  <div class="final">
    <picture><source type="image/webp" srcset="/assets/icon-192.webp"><img src="/assets/icon-192.png" alt="AI Wellness Pal app icon" width="88" height="88" loading="lazy"></picture>
    <h2>{title}</h2>
    <p>{sub}</p>
    {store_buttons()}
  </div>'''


def page(title, desc, path, ld_graph, main, active=''):
    ld = {'@context': 'https://schema.org', '@graph': ld_graph}
    return f'''{head(title, desc, path, ld)}
<body>
<div class="glow" aria-hidden="true"><span></span><span></span><span></span></div>
{SVG_DEFS}

{nav(active)}

<main>
{main}
</main>

{footer()}

{GET_APP_SCRIPT}
</body>
</html>
'''


def write(rel, content):
    p = ROOT / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content)
    return rel


# ---------------------------------------------------------------- pages

def feature_page(f):
    path = f'/features/{f["slug"]}/'
    crumbs = [('Home', '/'), ('Features', '/features/'), (f['short'], path)]
    shots = ''
    if f.get('shots'):
        figs = '\n'.join(f'''      <figure>{picture(n, cap, sizes='(max-width: 720px) 170px, 220px')}<figcaption>{esc(cap)}</figcaption></figure>'''
                         for n, cap in f['shots'])
        shots = f'<div class="prose-shots">\n{figs}\n    </div>'
    related = '\n'.join(
        f'''      <a class="card" href="/features/{r["slug"]}/"><h3>{esc(r["short"])}</h3><p>{esc(r["card"])}</p><span class="more">Learn more →</span></a>'''
        for r in (next(x for x in C.FEATURES if x['slug'] == s) for s in f['related']))
    hero_shot = f'<div class="shot">{picture(f["hero"][0], f["hero"][1], eager=True)}</div>' if f.get('hero') else ''
    main = f'''  <section class="page-hero">
    <div class="wrap">
      <div>
        {crumbs_html(crumbs)}
        <span class="eyebrow">{esc(f["eyebrow"])}</span>
        <h1>{f["h1"]}</h1>
        <p class="lead">{f["lead"]}</p>
        {store_buttons()}
      </div>
      {hero_shot}
    </div>
  </section>

  <section class="page-section" style="padding-top:8px">
    <div class="wrap prose">
{f["body"]}
    {shots}
    </div>
  </section>

  <section class="page-section" id="faq">
    <div class="wrap">
      <div class="sec-head"><span class="eyebrow">FAQ</span><h2>{esc(f["short"])} questions</h2></div>
      <div class="faq">
{faq_html(f["faqs"])}
      </div>
    </div>
  </section>

  <section class="page-section">
    <div class="wrap">
      <div class="sec-head"><span class="eyebrow">Keep exploring</span><h2>Related features</h2></div>
      <div class="related">
{related}
      </div>
      <p class="fine"><a href="/features/" style="color:var(--lavender)">See all AI Wellness Pal features →</a></p>
    </div>
  </section>

{final_cta()}'''
    graph = [webpage_ld(path, f['title'], f['desc'], crumbs), crumbs_ld(crumbs, url(path)), faq_ld(f['faqs'], url(path))]
    return write(f'features/{f["slug"]}/index.html', page(f['title'], f['desc'], path, graph, main, '/features/'))


def hub_page():
    path = '/features/'
    crumbs = [('Home', '/'), ('Features', path)]
    groups = ''
    for gname, gintro, slugs in C.FEATURE_GROUPS:
        cards = '\n'.join(
            f'''        <a class="card" href="/features/{f["slug"]}/"><h3>{esc(f["short"])}</h3><p>{esc(f["card"])}</p><span class="more">Learn more →</span></a>'''
            for f in (next(x for x in C.FEATURES if x['slug'] == s) for s in slugs))
        groups += f'''
  <section class="page-section">
    <div class="wrap">
      <div class="sec-head"><h2>{esc(gname)}</h2><p>{esc(gintro)}</p></div>
      <div class="related">
{cards}
      </div>
    </div>
  </section>
'''
    main = f'''  <section class="page-hero solo">
    <div class="wrap">
      <div>
        {crumbs_html(crumbs)}
        <span class="eyebrow">Features</span>
        <h1>Everything in <span class="grad-text">AI Wellness Pal</span></h1>
        <p class="lead">{C.HUB_LEAD}</p>
        {store_buttons()}
      </div>
    </div>
  </section>
{groups}
{final_cta()}'''
    items = [{'@type': 'ListItem', 'position': i + 1, 'url': url(f'/features/{f["slug"]}/'), 'name': f['short']}
             for i, f in enumerate(C.FEATURES)]
    graph = [webpage_ld(path, C.HUB_TITLE, C.HUB_DESC, crumbs, {'@type': 'CollectionPage'}), crumbs_ld(crumbs, url(path)),
             {'@type': 'ItemList', '@id': url(path) + '#list', 'name': 'AI Wellness Pal features', 'itemListElement': items}]
    return write('features/index.html', page(C.HUB_TITLE, C.HUB_DESC, path, graph, main, '/features/'))


def faq_page():
    path = '/faq/'
    crumbs = [('Home', '/'), ('FAQ', path)]
    groups = ''.join(f'''
      <div class="faq-group">
        <h2>{esc(g)}</h2>
        <div class="faq">
{faq_html(items)}
        </div>
      </div>''' for g, items in C.FAQ_GROUPS)
    all_faqs = [qa for _, items in C.FAQ_GROUPS for qa in items]
    main = f'''  <section class="page-hero solo">
    <div class="wrap">
      <div>
        {crumbs_html(crumbs)}
        <span class="eyebrow">FAQ</span>
        <h1>AI Wellness Pal <span class="grad-text">questions &amp; answers</span></h1>
        <p class="lead">{C.FAQ_LEAD}</p>
      </div>
    </div>
  </section>

  <section class="page-section" style="padding-top:8px">
    <div class="wrap">{groups}
      <p class="fine">Still stuck? Email <a href="mailto:{C.EMAIL}" style="color:var(--lavender)">{C.EMAIL}</a>.</p>
    </div>
  </section>

{final_cta()}'''
    graph = [webpage_ld(path, C.FAQ_TITLE, C.FAQ_DESC, crumbs), crumbs_ld(crumbs, url(path)), faq_ld(all_faqs, url(path))]
    return write('faq/index.html', page(C.FAQ_TITLE, C.FAQ_DESC, path, graph, main, '/faq/'))


def about_page():
    path = '/about/'
    crumbs = [('Home', '/'), ('About', path)]
    rows = '\n'.join(f'          <tr><th scope="row">{esc(k)}</th><td>{v}</td></tr>' for k, v in C.FACTS)
    main = f'''  <section class="page-hero solo">
    <div class="wrap">
      <div>
        {crumbs_html(crumbs)}
        <span class="eyebrow">About</span>
        <h1>About <span class="grad-text">AI Wellness Pal</span></h1>
        <p class="lead">{C.DEFINITION}</p>
      </div>
    </div>
  </section>

  <section class="page-section" style="padding-top:8px">
    <div class="wrap prose">
      <h2>Key facts</h2>
      <table class="facts">
        <tbody>
{rows}
        </tbody>
      </table>
{C.ABOUT_BODY}
    </div>
  </section>

{final_cta()}'''
    graph = [webpage_ld(path, C.ABOUT_TITLE, C.ABOUT_DESC, crumbs, {'@type': 'AboutPage'}), crumbs_ld(crumbs, url(path))]
    return write('about/index.html', page(C.ABOUT_TITLE, C.ABOUT_DESC, path, graph, main, '/about/'))


# ---------------------------------------------------------------- home page blocks

def home_ld():
    app = {
        '@type': 'MobileApplication', '@id': SITE + '/#app', 'name': 'AI Wellness Pal', 'url': SITE + '/',
        'description': C.APP_DESCRIPTION, 'abstract': C.TAGLINE,
        'image': SITE + '/assets/icon.png',
        'screenshot': [SITE + f'/assets/screens/{n}.jpg' for n in C.SCHEMA_SCREENSHOTS],
        'operatingSystem': 'iOS 15.0 or later, Android 8.0 or later',
        'applicationCategory': 'HealthApplication', 'applicationSubCategory': 'Wellness',
        'featureList': C.FEATURE_LIST,
        'offers': [
            {'@type': 'Offer', 'name': 'Free', 'price': '0', 'priceCurrency': 'USD'},
            {'@type': 'Offer', 'name': 'Premium Monthly (US App Store)', 'price': C.PRICE_MONTHLY, 'priceCurrency': 'USD',
             'description': 'Auto-renewing subscription with a 7-day free trial.'},
            {'@type': 'Offer', 'name': 'Premium Yearly (US App Store)', 'price': C.PRICE_YEARLY, 'priceCurrency': 'USD',
             'description': 'Auto-renewing subscription with a 7-day free trial.'},
        ],
        'isAccessibleForFree': True, 'inLanguage': 'en', 'datePublished': C.IOS_RELEASE,
        'installUrl': [C.APPLE, C.PLAY], 'downloadUrl': [C.APPLE, C.PLAY], 'sameAs': [C.APPLE, C.PLAY],
        'author': {'@id': SITE + '/#founder'}, 'publisher': {'@id': SITE + '/#organization'},
        'softwareHelp': {'@type': 'WebPage', 'url': SITE + '/faq/'},
        'video': {'@id': SITE + '/#demo-video'},
    }
    return {'@context': 'https://schema.org', '@graph': [
        {'@type': 'WebSite', '@id': SITE + '/#website', 'url': SITE + '/', 'name': 'AI Wellness Pal',
         'alternateName': ['AI Wellness Pal app', 'aiwelnesspal.com'], 'inLanguage': 'en',
         'publisher': {'@id': SITE + '/#organization'}},
        {'@type': 'Organization', '@id': SITE + '/#organization', 'name': 'AI Wellness Pal', 'url': SITE + '/',
         'logo': {'@type': 'ImageObject', 'url': SITE + '/assets/icon.png', 'width': 512, 'height': 512},
         'email': C.EMAIL, 'founder': {'@id': SITE + '/#founder'},
         'contactPoint': {'@type': 'ContactPoint', 'contactType': 'customer support', 'email': C.EMAIL, 'availableLanguage': 'en'},
         'sameAs': [C.APPLE, C.PLAY]},
        {'@type': 'Person', '@id': SITE + '/#founder', 'name': 'Viraj Dhanushka', 'jobTitle': 'Founder and developer',
         'worksFor': {'@id': SITE + '/#organization'}},
        webpage_ld('/', C.HOME_TITLE, C.HOME_DESC, extra={'@type': 'WebPage', 'mainEntity': {'@id': SITE + '/#app'}}),
        app,
        {'@type': 'VideoObject', '@id': SITE + '/#demo-video', 'name': 'AI Wellness Pal – App demo',
         'description': 'A quick tour of AI Wellness Pal: daily check-ins, personalized plans, the Wellness Pal chat and more.',
         'thumbnailUrl': f'https://i.ytimg.com/vi/{C.YOUTUBE_ID}/maxresdefault.jpg',
         'embedUrl': f'https://www.youtube-nocookie.com/embed/{C.YOUTUBE_ID}',
         'contentUrl': C.YOUTUBE_VIDEO, 'uploadDate': '2026-10-01T07:05:01-07:00'},
        faq_ld(C.HOME_FAQS, SITE + '/'),
    ]}


def replace_block(text, name, content):
    pat = re.compile(rf'(<!-- BUILD:{name} -->)(.*?)(<!-- /BUILD:{name} -->)', re.S)
    assert pat.search(text), f'marker BUILD:{name} missing in index.html'
    return pat.sub(lambda m: f'{m.group(1)}\n{content}\n{m.group(3)}', text, count=1)


def update_home():
    p = ROOT / 'index.html'
    t = p.read_text()
    t = replace_block(t, 'LD', '  <script type="application/ld+json">\n'
                      + json.dumps(home_ld(), ensure_ascii=False, indent=2) + '\n  </script>')
    t = replace_block(t, 'NAV', nav())
    t = replace_block(t, 'FAQ', faq_html(C.HOME_FAQS))
    t = replace_block(t, 'FOOTER', footer())
    p.write_text(t)
    return 'index.html'


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
    out = ['<?xml version="1.0" encoding="UTF-8"?>',
           '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" '
           'xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">']
    for path, rel, images in pages:
        out.append('  <url>')
        out.append(f'    <loc>{url(path)}</loc>')
        out.append(f'    <lastmod>{lastmod(rel)}</lastmod>')
        for img in images:
            out.append(f'    <image:image><image:loc>{SITE}{img}</image:loc></image:image>')
        out.append('  </url>')
    out.append('</urlset>')
    (ROOT / 'sitemap.xml').write_text('\n'.join(out) + '\n')


def llms():
    feats = '\n'.join(f'- [{f["short"]}]({url("/features/" + f["slug"] + "/")}): {f["card"]}' for f in C.FEATURES)
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

def main():
    written = [update_home(), hub_page(), faq_page(), about_page()]
    written += [feature_page(f) for f in C.FEATURES]
    pages = [('/', 'index.html', [f'/assets/screens/{n}.jpg' for n in C.SCHEMA_SCREENSHOTS] + ['/assets/og-image.png']),
             ('/features/', 'features/index.html', []),
             ('/faq/', 'faq/index.html', []),
             ('/about/', 'about/index.html', ['/assets/icon.png'])]
    for f in C.FEATURES:
        imgs = ([f'/assets/screens/{f["hero"][0]}.jpg'] if f.get('hero') else []) + [f'/assets/screens/{n}.jpg' for n, _ in f.get('shots', [])]
        imgs += f.get('images', [])
        pages.append((f'/features/{f["slug"]}/', f'features/{f["slug"]}/index.html', list(dict.fromkeys(imgs))))
    pages += [('/privacy.html', 'privacy.html', []), ('/terms.html', 'terms.html', []),
              ('/delete-account.html', 'delete-account.html', [])]
    sitemap(pages)
    llms()
    print('built:', len(written), 'pages + sitemap.xml, llms.txt, llms-full.txt')


if __name__ == '__main__':
    main()
