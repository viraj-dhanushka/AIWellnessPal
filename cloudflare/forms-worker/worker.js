/**
 * AI Wellness Pal form relay (Cloudflare Worker, served at api.aiwelnesspal.com).
 *
 * The website's feedback and account-deletion forms post here. This Worker:
 *   1. only accepts requests from the site's own origins,
 *   2. verifies the Cloudflare Turnstile token (blocks bots),
 *   3. emails the submission to the support inbox through Cloudflare Email
 *      Routing (the SEB "send email" binding). No third-party form service.
 *
 * Needs:
 *   - Secret TURNSTILE_SECRET (Turnstile widget secret key)
 *   - Email Routing enabled on aiwelnesspal.com with TO_ADDRESS verified as a
 *     destination, and a "Send email" binding named SEB on this Worker.
 */
import { EmailMessage } from 'cloudflare:email';

const FROM_ADDRESS = 'forms@aiwelnesspal.com';
const TO_ADDRESS = 'aiwellnesspal@gmail.com';

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

    // Plain text fields only, capped; skip control fields and the token.
    const fields = [];
    for (const [key, value] of data) {
      if (key.startsWith('_') || key === 'cf-turnstile-response' || typeof value !== 'string') continue;
      if (fields.length >= MAX_FIELDS) break;
      fields.push([key, value.slice(0, MAX_FIELD_LENGTH)]);
    }
    const email = String(data.get('email') || '').trim();
    const replyTo = /^[^\s@<>",;]+@[^\s@<>",;]+\.[^\s@<>",;]+$/.test(email) ? email : '';

    const body =
      `New submission from ${origin}\n\n` +
      fields.map(([k, v]) => `${label(k)}:\n${v || '—'}`).join('\n\n') +
      `\n\nSent ${new Date().toUTCString()}\n`;

    try {
      await env.SEB.send(new EmailMessage(FROM_ADDRESS, TO_ADDRESS, mime(subject, body, replyTo)));
    } catch (e) {
      console.error('send_email failed', e && e.message);
      return json({ success: 'false', message: 'Email could not be sent' }, 502, cors);
    }
    return json({ success: 'true' }, 200, cors);
  },
};

function label(key) {
  return key.replace(/[_-]+/g, ' ').replace(/^\w/, (c) => c.toUpperCase());
}

/** Minimal RFC 5322 message; subject/body base64 so any language is safe. */
function mime(subject, body, replyTo) {
  const headers = [
    `From: "AI Wellness Pal Forms" <${FROM_ADDRESS}>`,
    `To: <${TO_ADDRESS}>`,
    replyTo ? `Reply-To: <${replyTo}>` : null,
    `Subject: =?UTF-8?B?${b64(subject)}?=`,
    `Date: ${new Date().toUTCString()}`,
    `Message-ID: <${crypto.randomUUID()}@aiwelnesspal.com>`,
    'MIME-Version: 1.0',
    'Content-Type: text/plain; charset=UTF-8',
    'Content-Transfer-Encoding: base64',
  ].filter(Boolean);
  const encoded = b64(body).replace(/.{1,76}/g, '$&\r\n');
  return headers.join('\r\n') + '\r\n\r\n' + encoded;
}

function b64(text) {
  const bytes = new TextEncoder().encode(text);
  let bin = '';
  for (let i = 0; i < bytes.length; i += 0x8000) bin += String.fromCharCode(...bytes.subarray(i, i + 0x8000));
  return btoa(bin);
}

function json(obj, status, headers) {
  return new Response(JSON.stringify(obj), {
    status,
    headers: { 'Content-Type': 'application/json', ...headers },
  });
}
