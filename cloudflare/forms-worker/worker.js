/**
 * AI Wellness Pal form relay (Cloudflare Worker, served at api.aiwelnesspal.com).
 *
 * The website's feedback and account-deletion forms post here instead of to
 * FormSubmit directly. This Worker:
 *   1. only accepts requests from the site's own origins,
 *   2. verifies the Cloudflare Turnstile token (blocks bots),
 *   3. forwards the fields to FormSubmit using a destination that never appears
 *      in the page source (FORMSUBMIT_ID secret), so bots can't skip steps 1-2.
 *
 * Secrets (set with `npx wrangler secret put <NAME>`):
 *   TURNSTILE_SECRET  Turnstile widget secret key
 *   FORMSUBMIT_ID     FormSubmit destination, e.g. aiwellnesspal+forms@gmail.com
 */

const ALLOWED_ORIGINS = [
  'https://aiwelnesspal.com',
  'https://www.aiwelnesspal.com',
  'https://ai-wellness-pal-8f537.web.app',
  'https://ai-wellness-pal-8f537.firebaseapp.com',
];

// ?form=<key> → email subject. Anything else is rejected.
const FORMS = {
  feedback: 'AI Wellness Pal – Feedback',
  delete: 'AI Wellness Pal – ACCOUNT DELETION REQUEST',
};

const MAX_FIELD_LENGTH = 5000;
const MAX_FIELDS = 20;

export default {
  async fetch(request, env) {
    const origin = request.headers.get('Origin') || '';
    const allowed = ALLOWED_ORIGINS.includes(origin);
    const cors = allowed ? { 'Access-Control-Allow-Origin': origin, Vary: 'Origin' } : {};

    if (request.method === 'OPTIONS') {
      return new Response(null, {
        status: allowed ? 204 : 403,
        headers: {
          ...cors,
          'Access-Control-Allow-Methods': 'POST',
          'Access-Control-Allow-Headers': 'Accept, Content-Type',
          'Access-Control-Max-Age': '86400',
        },
      });
    }

    const url = new URL(request.url);
    if (request.method !== 'POST' || url.pathname !== '/submit') {
      return json({ success: 'false', message: 'Not found' }, 404, cors);
    }
    if (!allowed) return json({ success: 'false', message: 'Forbidden' }, 403, cors);

    const subject = FORMS[url.searchParams.get('form')];
    if (!subject) return json({ success: 'false', message: 'Unknown form' }, 400, cors);

    let data;
    try {
      data = await request.formData();
    } catch {
      return json({ success: 'false', message: 'Bad request' }, 400, cors);
    }

    // Honeypot filled in: pretend it worked, send nothing.
    if (data.get('_honey')) return json({ success: 'true' }, 200, cors);

    const token = data.get('cf-turnstile-response');
    if (!token) {
      return json({ success: 'false', message: 'Please complete the verification check.' }, 400, cors);
    }
    const verify = await fetch('https://challenges.cloudflare.com/turnstile/v0/siteverify', {
      method: 'POST',
      body: new URLSearchParams({
        secret: env.TURNSTILE_SECRET,
        response: token,
        remoteip: request.headers.get('CF-Connecting-IP') || '',
      }),
    });
    const outcome = await verify.json().catch(() => ({}));
    if (!outcome.success) {
      return json({ success: 'false', message: 'Verification failed. Please try again.' }, 403, cors);
    }

    // Rebuild the payload: only plain text fields, capped, no FormSubmit
    // control fields from the client (those are set here).
    const out = new FormData();
    out.set('_subject', subject);
    out.set('_template', 'table');
    out.set('_captcha', 'false');
    let count = 0;
    for (const [key, value] of data) {
      if (key.startsWith('_') || key === 'cf-turnstile-response' || typeof value !== 'string') continue;
      if (++count > MAX_FIELDS) break;
      out.append(key, value.slice(0, MAX_FIELD_LENGTH));
    }
    const email = data.get('email');
    if (typeof email === 'string' && email.includes('@')) out.set('_replyto', email);

    const res = await fetch(`https://formsubmit.co/ajax/${encodeURIComponent(env.FORMSUBMIT_ID)}`, {
      method: 'POST',
      body: out,
      headers: {
        Accept: 'application/json',
        // FormSubmit ties a form to the site it's used on.
        Origin: 'https://aiwelnesspal.com',
        Referer: 'https://aiwelnesspal.com/',
      },
    });
    const body = await res.json().catch(() => ({}));
    const ok = res.ok && String(body.success) === 'true';
    return json({ success: ok ? 'true' : 'false', message: body.message || '' }, ok ? 200 : 502, cors);
  },
};

function json(obj, status, headers) {
  return new Response(JSON.stringify(obj), {
    status,
    headers: { 'Content-Type': 'application/json', ...headers },
  });
}
