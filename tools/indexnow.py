#!/usr/bin/env python3
"""Tells IndexNow search engines (Bing, Yandex, Seznam, Naver...) which pages changed.

Run after the site is deployed:
    python3 tools/indexnow.py            # submits every URL in sitemap.xml
    python3 tools/indexnow.py /faq/ /    # submits only these paths
The key file (<key>.txt in the repo root) proves the site owns the key.
"""
import json
import re
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
HOST = 'aiwelnesspal.com'
key_files = [p for p in ROOT.glob('*.txt') if re.fullmatch(r'[0-9a-f]{32}\.txt', p.name)]
assert len(key_files) == 1, 'expected exactly one IndexNow key file in the repo root'
KEY = key_files[0].stem

if len(sys.argv) > 1:
    urls = [f'https://{HOST}{p}' for p in sys.argv[1:]]
else:
    urls = re.findall(r'<loc>([^<]+)</loc>', (ROOT / 'sitemap.xml').read_text())

body = json.dumps({'host': HOST, 'key': KEY, 'keyLocation': f'https://{HOST}/{KEY}.txt', 'urlList': urls}).encode()
req = urllib.request.Request('https://api.indexnow.org/indexnow', data=body,
                             headers={'Content-Type': 'application/json; charset=utf-8'})
with urllib.request.urlopen(req, timeout=30) as r:
    print(r.status, r.reason, '-', len(urls), 'URLs submitted')
