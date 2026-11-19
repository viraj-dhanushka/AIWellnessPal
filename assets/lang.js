/* Language picker and "View in …?" prompt for aiwellnesspal.com.
 *
 * - Choosing a language in the picker (header or footer) is remembered in
 *   localStorage. Nothing ever redirects automatically.
 * - On English pages, if the visitor chose a language before, or their browser
 *   prefers one the site has, a small dismissible prompt offers that version.
 *   Dismissing it (or choosing English) is remembered.
 * The prompt strings below are filled in by tools/build_site.py.
 */
(function () {
  var PROMPTS = /* BUILD:PROMPTS */{
  "en": {
    "q": "View this page in English?",
    "yes": "English",
    "no": "No thanks"
  },
  "ar": {
    "q": "هل تريد عرض هذه الصفحة بالعربية؟",
    "yes": "العربية",
    "no": "لا، شكرًا"
  },
  "bn": {
    "q": "এই পেজটি কি বাংলায় দেখতে চান?",
    "yes": "বাংলা",
    "no": "না, ধন্যবাদ"
  },
  "de": {
    "q": "Diese Seite auf Deutsch ansehen?",
    "yes": "Deutsch",
    "no": "Nein, danke"
  },
  "es": {
    "q": "¿Ver esta página en español?",
    "yes": "Español",
    "no": "No, gracias"
  },
  "fr": {
    "q": "Voir cette page en français ?",
    "yes": "Français",
    "no": "Non merci"
  },
  "hi": {
    "q": "इस पेज को हिन्दी में देखें?",
    "yes": "हिन्दी",
    "no": "नहीं, धन्यवाद"
  },
  "id": {
    "q": "Lihat halaman ini dalam Bahasa Indonesia?",
    "yes": "Bahasa Indonesia",
    "no": "Tidak, terima kasih"
  },
  "it": {
    "q": "Vuoi vedere questa pagina in italiano?",
    "yes": "Italiano",
    "no": "No, grazie"
  },
  "ja": {
    "q": "このページを日本語で表示しますか？",
    "yes": "日本語",
    "no": "いいえ"
  },
  "ko": {
    "q": "이 페이지를 한국어로 보시겠어요?",
    "yes": "한국어",
    "no": "괜찮아요"
  },
  "mr": {
    "q": "हे पान मराठीत पाहायचे का?",
    "yes": "मराठी",
    "no": "नको, धन्यवाद"
  },
  "nl": {
    "q": "Deze pagina bekijken in het Nederlands?",
    "yes": "Nederlands",
    "no": "Nee, bedankt"
  },
  "pl": {
    "q": "Wyświetlić tę stronę po polsku?",
    "yes": "Polski",
    "no": "Nie, dziękuję"
  },
  "pt": {
    "q": "Ver esta página em português?",
    "yes": "Português",
    "no": "Não, obrigado"
  },
  "ro": {
    "q": "Vrei să vezi această pagină în română?",
    "yes": "Română",
    "no": "Nu, mulțumesc"
  },
  "ru": {
    "q": "Посмотреть эту страницу на русском языке?",
    "yes": "Русский",
    "no": "Нет, спасибо"
  },
  "ta": {
    "q": "இந்தப் பக்கத்தைத் தமிழில் பார்க்கவா?",
    "yes": "தமிழ்",
    "no": "வேண்டாம், நன்றி"
  },
  "te": {
    "q": "ఈ పేజీని తెలుగులో చూడాలనుకుంటున్నారా?",
    "yes": "తెలుగు",
    "no": "వద్దు, ధన్యవాదాలు"
  },
  "th": {
    "q": "ดูหน้านี้เป็นภาษาไทยไหม",
    "yes": "ไทย",
    "no": "ไม่เป็นไร ขอบคุณ"
  },
  "tr": {
    "q": "Bu sayfayı Türkçe görüntülemek ister misin?",
    "yes": "Türkçe",
    "no": "Hayır, teşekkürler"
  },
  "uk": {
    "q": "Переглянути цю сторінку українською?",
    "yes": "Українська",
    "no": "Ні, дякую"
  },
  "vi": {
    "q": "Xem trang này bằng tiếng Việt?",
    "yes": "Tiếng Việt",
    "no": "Không, cảm ơn"
  }
}/* /BUILD:PROMPTS */;
  var LANG_KEY = 'aiwp-lang';
  var OFF_KEY = 'aiwp-lang-prompt-off';

  function get(k) { try { return window.localStorage.getItem(k); } catch (e) { return null; } }
  function set(k, v) { try { window.localStorage.setItem(k, v); } catch (e) {} }

  // Remember the language whenever one is picked.
  document.addEventListener('click', function (e) {
    var a = e.target.closest && e.target.closest('a[data-lang]');
    if (a) set(LANG_KEY, a.getAttribute('data-lang'));
  });

  // Close the header menu on Escape or a click outside it.
  var pickers = document.querySelectorAll('details.lang-pick');
  document.addEventListener('click', function (e) {
    pickers.forEach(function (d) { if (d.open && !d.contains(e.target)) d.open = false; });
  });
  document.addEventListener('keydown', function (e) {
    if (e.key !== 'Escape') return;
    pickers.forEach(function (d) { if (d.open) { d.open = false; d.querySelector('summary').focus(); } });
  });

  // The prompt: English pages only.
  if (document.documentElement.lang !== 'en' || get(OFF_KEY) === '1') return;
  var saved = get(LANG_KEY);
  if (saved === 'en') return;
  var want = saved && PROMPTS[saved] ? saved : null;
  if (!want) {
    var prefs = navigator.languages && navigator.languages.length ? navigator.languages : [navigator.language || ''];
    for (var i = 0; i < prefs.length && !want; i++) {
      var code = String(prefs[i]).toLowerCase().split('-')[0];
      if (code === 'en') return;           // English is preferred over the others: no prompt
      if (PROMPTS[code]) want = code;
    }
  }
  if (!want || want === 'en') return;
  var alt = document.querySelector('link[rel="alternate"][hreflang="' + want + '"]');
  if (!alt) return;
  var href = new URL(alt.href).pathname + location.hash;
  var p = PROMPTS[want];

  var box = document.createElement('div');
  box.className = 'lang-prompt';
  box.setAttribute('role', 'region');
  box.setAttribute('aria-label', p.q);
  box.lang = want;
  box.dir = want === 'ar' ? 'rtl' : 'ltr';
  var text = document.createElement('span');
  text.textContent = p.q;
  var go = document.createElement('a');
  go.href = href;
  go.hreflang = want;
  go.setAttribute('data-lang', want);
  go.textContent = p.yes;
  var no = document.createElement('button');
  no.type = 'button';
  no.setAttribute('aria-label', p.no);
  no.title = p.no;
  no.textContent = '×';
  no.addEventListener('click', function () { set(OFF_KEY, '1'); box.remove(); });
  box.appendChild(text); box.appendChild(go); box.appendChild(no);
  document.body.appendChild(box);
})();
