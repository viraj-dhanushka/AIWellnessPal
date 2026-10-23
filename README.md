# AI Wellness Pal — website

Source for **[aiwelnesspal.com](https://aiwelnesspal.com/)**, the website of **AI Wellness Pal**, a free AI wellness coach app for iPhone and Android.

AI Wellness Pal turns a 30-second daily check-in (energy, mood, how your body feels and how much time you have) into a personalized plan for mood, sleep, nutrition and habits, with an AI Wellness Pal to chat or talk with, a guided journal, habit tracking and nine everyday wellness tools.

- Download: [App Store](https://apps.apple.com/us/app/ai-wellness-pal/id6816496839) · [Google Play](https://play.google.com/store/apps/details?id=com.aiwellnesspal.app)
- Learn more: [Features](https://aiwelnesspal.com/features/) · [FAQ](https://aiwelnesspal.com/faq/) · [About](https://aiwelnesspal.com/about/)
- Support: aiwellnesspal@gmail.com

## How the site is built

Static HTML hosted on GitHub Pages. No framework.

| Path | What it is |
|---|---|
| `index.html` | Home page (hand-written; blocks between `<!-- BUILD:X -->` markers are generated) |
| `features/`, `faq/`, `about/` | **Generated** content pages — edit `tools/site_content.py`, not the HTML |
| `privacy.html`, `terms.html`, `delete-account.html` | Legal pages (their URLs are used by the app and the stores — never move them) |
| `landing.css` | Styles for the home and content pages (`style.css` is for the legal pages) |
| `sitemap.xml`, `llms.txt`, `llms-full.txt` | **Generated** sitemap and AI-assistant summaries |
| `robots.txt` | Crawler rules (search and AI-search crawlers are welcome) |
| `cloudflare/forms-worker/` | Cloudflare Worker that checks Turnstile and emails the website's forms |
| `tools/` | Build scripts (below) |

### Updating content

```bash
python3 tools/build_site.py        # rebuild generated pages, sitemap and llms files
python3 tools/optimize_images.py   # after adding/replacing screenshots or the icon (needs Pillow)
```

After deploying, `python3 tools/indexnow.py` tells Bing and other IndexNow search engines what changed.
