"""Content for aiwelnesspal.com's generated pages (see build_site.py).

Everything here is public marketing copy, so keep it accurate to the app:
sources are the app's in-app FAQ (lib/screens/faq_screen.dart), the App Store /
Google Play listings, and the privacy policy. American English.
Answers and bodies are HTML fragments.
"""

SITE = 'https://aiwelnesspal.com'
APPLE_ID = '6816496839'
APPLE = 'https://apps.apple.com/us/app/ai-wellness-pal/id6816496839'
PLAY = 'https://play.google.com/store/apps/details?id=com.aiwellnesspal.app'
EMAIL = 'aiwellnesspal@gmail.com'
YOUTUBE_ID = 'PYkPL-Q_1uw'
YOUTUBE_VIDEO = 'https://www.youtube.com/watch?v=PYkPL-Q_1uw'
IOS_RELEASE = '2026-10-05'
PRICE_MONTHLY = '14.99'
PRICE_YEARLY = '89.99'

TAGLINE = 'Your AI wellness companion — a daily plan built around how you actually feel'

HOME_TITLE = 'AI Wellness Pal: AI Wellness Coach App for iPhone & Android'
HOME_DESC = ('AI Wellness Pal is a free AI wellness coach app for iPhone and Android. A 30-second daily check-in '
             'becomes a personalized plan for mood, sleep, nutrition and habits.')

DEFINITION = ('<strong>AI Wellness Pal</strong> is a free AI wellness coach app for iPhone and Android. Each day a '
              '30-second check-in (energy, mood, how your body feels and how much time you have) becomes '
              '<strong>Today’s Plan</strong>: two to four small, doable actions for mood, sleep, movement and '
              'nutrition. An AI companion, the Wellness Pal, helps you follow through, alongside a journal, habit '
              'tracking and nine everyday wellness tools.')
DEFINITION_PLAIN = ('AI Wellness Pal is a free AI wellness coach app for iPhone and Android. Each day a 30-second '
                    'check-in (energy, mood, how your body feels and how much time you have) becomes Today’s Plan: '
                    'two to four small, doable actions for mood, sleep, movement and nutrition. An AI companion, the '
                    'Wellness Pal, helps you follow through, alongside a journal, habit tracking and nine everyday '
                    'wellness tools.')

APP_DESCRIPTION = ('AI Wellness Pal is an AI wellness coach for iPhone and Android: a 30-second daily check-in becomes '
                   'a personalized plan for mood, sleep, nutrition and habits, with an AI Wellness Pal to chat or talk '
                   'with, a guided journal, habit tracking and nine wellness tools (nutrition coach, meal planner, '
                   'calorie budget, hydration coach, sleep coach, meditation, period tracker, body weight and mindful '
                   'travel).')

FEATURE_LIST = [
    'Daily check-in and personalized Today’s Plan',
    'AI Wellness Pal chat and real-time voice conversations (Live Chat Pal)',
    'AI-guided journal and reflections',
    'AI Nutrition Coach: log meals by photo, description or barcode',
    'AI Meal Planner',
    'Calorie Budget (food and exercise)',
    'Hydration Coach with daily water target',
    'Sleep Coach using Apple Health or Health Connect',
    'Meditation Pal: breathing exercises, body scans and stress relief',
    'Period tracker with cycle predictions',
    'Body weight and BMI tracker',
    'Habit builder, challenges, streaks and reminders',
    'Home-screen widgets for iPhone and Android',
]

SCHEMA_SCREENSHOTS = ['01_02_home', '01_03_checkin', '03_05_pal_chat', '10_life_toolkit',
                      '13_hydration_coach', '11_period_tracker', '17_habit_builder', '21_reflections']

LLMS_SUMMARY = '''Key facts:
- Platforms: iPhone (iOS 15.0 or later) and Android (8.0 or later). App Store and Google Play.
- Price: free to download and use, no ads. Optional Premium subscription (US App Store: $14.99/month or $89.99/year, 7-day free trial). Free: daily check-ins and plans, AI journal, habits and challenges, hydration/sleep/period/weight tracking, meditation and breathing, widgets, and 3 Wellness Pal chat messages per day. Premium: unlimited chat, Live Chat Pal real-time voice, AI food analysis (photo/description/barcode), AI meal plans, AI sleep/hydration/calorie insights, the full Wellness Studio and more.
- Launched: App Store on 5 October 2026; Google Play in October 2026.
- Developer: Viraj Dhanushka (independent developer). Support: aiwellnesspal@gmail.com.
- AI: Google Gemini models via Firebase AI Logic. The app asks for permission before any personal information is sent to the AI.
- Privacy: no advertising, no selling of data, no cross-app tracking; accounts and data can be deleted at any time.
- Health data: reads sleep (only) from Apple Health on iPhone or Health Connect on Android, with permission; never writes health data.
- Not a medical device and not medical advice.
- Language: English.'''

# ------------------------------------------------------------------ FAQ

FAQ_LEAD = ('Straight answers about what AI Wellness Pal does, what’s free, how your data is handled and how to get '
            'help. Can’t find something? Email <a href="mailto:aiwellnesspal@gmail.com">aiwellnesspal@gmail.com</a>.')
FAQ_TITLE = 'AI Wellness Pal FAQ: Features, Pricing, Privacy & Support'
FAQ_DESC = ('Answers about AI Wellness Pal: what the AI wellness coach app does, what’s free vs Premium, how your '
            'data and health data are handled, devices, widgets and support.')

Q_WHAT = ('What is AI Wellness Pal?',
          '<p>AI Wellness Pal is a free AI wellness coach app for iPhone and Android. It answers one question each '
          'day: what should I do for my wellbeing right now?</p><p>You do a quick check-in, and the app builds '
          'Today’s Plan: two to four small, doable actions shaped around your energy, mood, body recovery and how '
          'much time you actually have. Everything else in the app supports that: tools to track the day, a Wellness '
          'Pal to talk it through, and progress you can see building up over time.</p>')
Q_FREE = ('Is AI Wellness Pal free?',
          '<p>Yes. AI Wellness Pal is free to download and use on iPhone and Android, with no ads. The free app '
          'includes daily check-ins and Today’s Plan, the AI journal, habits and challenges, hydration, sleep, period '
          'and weight tracking, meditation and breathing sessions, widgets and 3 Wellness Pal chat messages a day.</p>'
          '<p>An optional Premium subscription adds unlimited chat, real-time voice conversations, AI food analysis, '
          'AI meal plans and the other AI coaching inside the toolkit. '
          '<a href="/#pricing">Compare Free and Premium</a>.</p>')
Q_PRICE = ('How much does AI Wellness Pal Premium cost?',
           '<p>On the US App Store, Premium costs $14.99 a month or $89.99 a year, and both plans start with a 7-day '
           'free trial. Prices vary by country and currency; the App Store or Google Play shows the exact price '
           'before you confirm. The subscription renews automatically unless you cancel at least 24 hours before '
           'the end of the current period.</p>')
Q_PREMIUM = ('What do I get with Premium?',
             '<p>Unlimited chat with your Wellness Pal, Live Chat Pal real-time voice conversations, “Discuss” on '
             'your reflections, AI plans for your intentions, and the AI coaching inside the toolkit: nutrition '
             'analysis, meal plans, and sleep, hydration and calorie insights. You also get the full Wellness Studio '
             'library and AI-picked activities refreshed daily. All themes are free for everyone.</p>')
Q_DEVICES = ('Is AI Wellness Pal available on iPhone and Android?',
             f'<p>Yes. Download it from the <a href="{APPLE}">App Store</a> (iPhone, iOS 15.0 or later) or '
             f'<a href="{PLAY}">Google Play</a> (Android 8.0 or later). Sign in with the same account on both and '
             'your data syncs.</p>')
Q_MEDICAL = ('Is AI Wellness Pal medical advice?',
             '<p>No. AI Wellness Pal offers general wellness information and encouragement. It isn’t a medical '
             'device and doesn’t diagnose, treat or replace a doctor, therapist or other qualified professional. AI '
             'responses, calorie estimates and cycle predictions can be wrong, so talk to a healthcare provider about '
             'any health concern.</p><p>If you’re in crisis or thinking about harming yourself, contact your local '
             'emergency number right away. In the US, call or text 988. In the UK, call 111 or Samaritans on 116 123. '
             'Elsewhere, find a helpline at findahelpline.com.</p>')
Q_AI = ('Which AI does AI Wellness Pal use?',
        '<p>The AI features (Wellness Pal chat and voice, journal insights, daily plans, sleep insights and '
        'nutrition analysis) are powered by Google’s Gemini models through Firebase AI Logic. Before any of your '
        'information is sent to the AI, the app shows you what will be shared and asks for your permission. AI '
        'responses can be inaccurate, so use them as guidance, not fact.</p>')
Q_PRIVACY = ('Is my data private? Do you sell it or show ads?',
             '<p>AI Wellness Pal has no ads, doesn’t sell your data and doesn’t track you across other companies’ '
             'apps or websites. Your data is stored in your own private area and isn’t shared with other users. Data '
             'is shared only with the service providers that run the app (such as Firebase for storage and Google '
             'Gemini for AI responses). Read the <a href="/privacy.html">Privacy Policy</a> for details.</p>')
Q_DELETE = ('How do I delete my account and data?',
            '<p>In the app, go to <strong>Settings → Delete Account</strong>. This permanently deletes your account '
            'and its data. If you no longer have the app, <a href="/delete-account.html">request deletion on the '
            'web</a>. Deleting your account doesn’t cancel a subscription, so cancel Premium in your App Store or '
            'Google Play subscriptions first.</p>')
Q_CHECKIN = ('What is the daily check-in?',
             '<p>Three quick steps: your energy (1–5), your mood, and how your body feels plus the time you have '
             'today. You can skip any step and the plan uses what you gave it. Once you’ve checked in, Today’s Plan '
             'is generated within a few seconds. You can also ask your Wellness Pal to “start my check-in” if you’d '
             'rather talk than tap.</p>')

HOME_FAQS = [Q_WHAT, Q_FREE, Q_PRICE, Q_DEVICES, Q_CHECKIN, Q_MEDICAL, Q_AI, Q_PRIVACY]

FAQ_GROUPS = [
    ('About AI Wellness Pal', [
        Q_WHAT, Q_DEVICES, Q_MEDICAL, Q_AI,
        ('Who makes AI Wellness Pal?',
         '<p>AI Wellness Pal is built by Viraj Dhanushka, an independent developer. It launched on the App Store in '
         'October 2026 and on Google Play the same month. <a href="/about/">More about the app</a>.</p>'),
        ('What language is AI Wellness Pal in?',
         '<p>The app is in English. With Live Chat Pal you can speak in other languages, and turn on “Always speak '
         'English” if you want replies in English whatever language you use.</p>'),
        ('Who is AI Wellness Pal for?',
         '<p>Adults (18+) who want a simple daily routine for their wellbeing: people who feel scattered by '
         'too many apps, want small steps that fit their real energy and time, and like having someone to talk '
         'things through with. It’s general wellness support, not a treatment for any condition.</p>'),
    ]),
    ('Pricing & Premium', [
        Q_FREE, Q_PRICE, Q_PREMIUM,
        ('How do I cancel or manage Premium?',
         '<p>On iPhone, go to <strong>Settings → your name → Subscriptions → AI Wellness Pal</strong>. On Android, '
         'open Google Play → <strong>Payments &amp; subscriptions → Subscriptions</strong>. Cancel at least 24 hours '
         'before the end of the current period to avoid the next renewal.</p>'),
        ('How do I restore a purchase on a new phone?',
         '<p>In the app, go to <strong>Settings → Manage Subscription → Restore Purchases</strong>, signed in with '
         'the same Apple ID or Google account you subscribed with. Have a promo code? There’s a “Have a promo code?” '
         'option on the same screen.</p>'),
    ]),
    ('Your day', [
        Q_CHECKIN,
        ('How does Today’s Plan work?',
         '<p>Each action has a checkbox. Tick them off as you go, and when you finish them all you get a small '
         'celebration. If your day changes, ask your Wellness Pal to update the plan (“I’m more tired than I '
         'thought”) and it rebuilds around how you actually feel.</p>'),
        ('What are Wellness Intentions?',
         '<p>Longer-term directions rather than daily tasks, like “sleep better”, “move more” or “feel calmer”. '
         'Your daily plans are shaped by them, and each one tracks its own progress. Premium members can have an '
         'intention broken into gentle daily steps automatically.</p>'),
        ('How do streaks and achievements work?',
         '<p>Your streak counts consecutive days you’ve checked in, with celebrations at 1, 3, 7, 14, 30, 50 and '
         '100 days. Missing a day costs you a day rather than wiping the streak out. Achievements are badges for '
         'streaks, points, intentions, actions, reflections, studio sessions, meditation and challenges, from '
         '“First Sunrise” for your first check-in to “Zen Master” at 100 days.</p>'),
    ]),
    ('Your Wellness Pal', [
        ('How do I talk to my Wellness Pal?',
         '<p>Tap the glowing orb button to open your Pal and start talking. To type instead, open your Pal and tap '
         'the smaller “Chat” orb. Free members get three messages a day; Premium is unlimited. Your three most '
         'recent conversations are kept as cards, and you can turn a useful one into a reflection.</p>'),
        ('What can the Wellness Pal do?',
         '<p>More than talk. It can log water, meals, exercise, weight, a meditation session or a period start; '
         'create habits and set reminders; join challenges; run your check-in; rebuild Today’s Plan; add or remove '
         'Home cards; change your theme or text size; and open any screen. Just ask in your own words.</p>'),
        ('What is Live Chat Pal?',
         '<p>A real-time voice conversation: you talk naturally and your Pal responds as you speak, rather than '
         'waiting for you to finish. It’s a Premium feature, turned on in <strong>Settings → AI Voice</strong>. '
         'With it on, you can also enable “Always listen for Pal” and just say “Hey Pal” while the app is open.</p>'),
        ('How does AI journaling work?',
         '<p>Start a reflection and you’ll get prompts based on how your week has actually gone. Write your entry '
         'and your Pal responds with something supportive and specific. With Premium, tap “Discuss” on any '
         'reflection to talk it through and save anything useful as an Insight.</p>'),
    ]),
    ('Tools & tracking', [
        ('What’s in the Life Toolkit?',
         '<p>Nine tools, reached from the “More” tab: <a href="/features/ai-nutrition-coach/">Nutrition Coach</a>, '
         '<a href="/features/ai-meal-planner/">Meal Planner</a>, <a href="/features/calorie-tracker/">Calorie '
         'Budget</a>, <a href="/features/water-tracker/">Hydration Coach</a>, <a href="/features/sleep-tracker/">'
         'Sleep Coach</a>, <a href="/features/meditation-breathing/">Meditation Pal</a>, '
         '<a href="/features/period-tracker/">Period Tracker</a>, <a href="/features/weight-tracker/">Body '
         'Weight</a> and Mindful Travel.</p>'),
        ('Does AI Wellness Pal work with Apple Health or Health Connect?',
         '<p>Yes, for sleep. The Sleep Coach reads your sleep data from Apple Health on iPhone or Health Connect on '
         'Android, only after you allow it. The app reads sleep only and never writes health data. You can '
         'disconnect at any time in your phone’s settings.</p>'),
        ('What is the Wellness Studio?',
         '<p>Short guided activities for right now, usually 3–12 minutes, in six categories: Breathing Exercises, '
         'Recovery Challenges, Mindfulness Sessions, Wellness Quizzes, Pilates Knowledge Cards and Stress Recovery. '
         'Think Box Breathing, the 4-7-8 Calm Breath, a 5-Minute Stretch Reset or a Body Scan. At least three '
         'activities in each category are free.</p>'),
        ('What are Wellness Reads?',
         '<p>Ten short articles, roughly 3–5 minutes each, on mindfulness, sleep, movement, nutrition, mental health, '
         'stress relief, Pilates and yoga, all free. The app can read any of them aloud in your phone’s voice, and '
         'keeps going in the background with lock-screen controls.</p>'),
    ]),
    ('Widgets, reminders & settings', [
        ('Does AI Wellness Pal have home-screen widgets?',
         '<p>Yes, on iPhone and Android: Today’s Plan (tick actions without opening the app), Today’s Habits, '
         'Wellness Intention, and one for each toolkit tool. Tool widgets flip to show today’s numbers, like your '
         'water progress or cycle day. <a href="/features/home-screen-widgets/">See all widgets</a>.</p>'),
        ('Which notifications will I get?',
         '<p>Only what you ask for. <strong>Settings → Notifications → Notification Preferences</strong> has a '
         'switch for each category: daily check-in, Today’s Plan, meals, hydration, habits and challenges, '
         'meditation, achievements and streaks, and cycle reminders. Meals and hydration start off. A master switch '
         'mutes everything.</p>'),
        ('Can I change how the app looks?',
         '<p>Yes. <strong>Settings → Appearance and Theme</strong> switches light and dark mode and offers six '
         'themes (Clear Sky, Serenity, Lavender, Soft Sand, Morning Glow and Pilates Studio), all free. You can '
         'also scale the text size.</p>'),
        ('Does my data sync across devices?',
         '<p>Yes. Sign in with the same account and your check-ins, plans, reflections, habits, intentions and '
         'settings follow you, on iPhone and Android.</p>'),
    ]),
    ('Privacy & account', [
        Q_PRIVACY, Q_DELETE,
        ('How do I contact support?',
         f'<p>Email <a href="mailto:{EMAIL}">{EMAIL}</a>, or use the <a href="/#feedback">feedback form</a>. '
         'Bug reports and feature ideas are very welcome.</p>'),
    ]),
]

# ------------------------------------------------------------------ About page

ABOUT_TITLE = 'About AI Wellness Pal: Key Facts, Developer & Contact'
ABOUT_DESC = ('Key facts about AI Wellness Pal, the AI wellness coach app for iPhone and Android: what it does, who '
              'makes it, launch dates, pricing, AI provider, privacy and contact.')

FACTS = [
    ('What it is', 'An AI wellness coach app: a daily check-in becomes a personalized plan, supported by an AI '
                   'companion, a journal, habits and nine wellness tools.'),
    ('Platforms', f'iPhone (iOS 15.0 or later) on the <a href="{APPLE}">App Store</a>; Android (8.0 or later) on '
                  f'<a href="{PLAY}">Google Play</a>'),
    ('Launched', 'App Store: 5 October 2026. Google Play: October 2026.'),
    ('Category', 'Health &amp; Fitness'),
    ('Price', 'Free, with no ads. Optional Premium subscription: $14.99/month or $89.99/year on the US App Store, '
              'with a 7-day free trial (prices vary by country).'),
    ('Free plan', 'Daily check-ins and Today’s Plan, AI journal, habits and challenges, hydration, sleep, period and '
                  'weight tracking, meditation and breathing, widgets, and 3 Wellness Pal messages a day'),
    ('Premium', 'Unlimited Wellness Pal chat, Live Chat Pal real-time voice, AI food analysis (photo, description or '
                'barcode), AI meal plans, AI sleep, hydration and calorie insights, “Discuss” and weekly reflections, '
                'AI steps for intentions, and the full Wellness Studio'),
    ('AI', 'Google Gemini models via Firebase AI Logic, with permission asked before personal information is sent'),
    ('Health data', 'Reads sleep only, from Apple Health (iPhone) or Health Connect (Android), with permission. '
                    'Never writes health data.'),
    ('Privacy', 'No ads, no data selling, no cross-app tracking. Delete your account and data anytime.'),
    ('Language', 'English'),
    ('Age', 'For adults 18 and over'),
    ('Developer', 'Viraj Dhanushka, independent developer'),
    ('Contact', f'<a href="mailto:{EMAIL}">{EMAIL}</a>'),
    ('Website', '<a href="https://aiwelnesspal.com/">aiwelnesspal.com</a>'),
]

ABOUT_BODY = f'''      <h2>Why AI Wellness Pal exists</h2>
      <p>Most wellness apps hand you the same plan as everyone else. AI Wellness Pal asks how you’re actually doing
      first. Every morning a 30-second check-in captures your energy, your mood, how your body feels and how much time
      you genuinely have. Then your Pal builds Today’s Plan: two to four small, doable actions shaped around that
      answer. Exhausted with fifteen minutes free? You get a very different day than when you’re rested with an
      hour.</p>
      <p>Everything else in the app supports that daily plan: tools to track meals, water, sleep, cycles and weight,
      a habit builder with challenges, a guided journal, and a Wellness Pal you can chat or talk with when you need
      it.</p>

      <h2>Who builds it</h2>
      <p>AI Wellness Pal is designed and built by <strong>Viraj Dhanushka</strong>, an independent developer. Feedback
      goes straight to the person who builds the app, and shapes what comes next. Send ideas, bugs or praise through
      the <a href="/#feedback">feedback form</a> or by email.</p>

      <h2>How the AI is used, and its limits</h2>
      <p>The AI features use Google’s Gemini models through Firebase AI Logic. Before any of your information is sent
      to the AI, the app shows you what will be shared and asks for your permission. AI responses, calorie estimates
      and cycle predictions can be wrong; AI Wellness Pal provides general wellness information and is not a medical
      device or a substitute for professional care.</p>

      <h2>Privacy commitments</h2>
      <ul>
        <li>No advertising, no selling of data, and no tracking across other companies’ apps or websites.</li>
        <li>Health data is read only with your permission (sleep only) and never written back.</li>
        <li>Delete your account and data at any time, in the app or <a href="/delete-account.html">on the web</a>.</li>
      </ul>
      <p>Full details are in the <a href="/privacy.html">Privacy Policy</a> and <a href="/terms.html">Terms of Use</a>.</p>

      <h2>Press and media</h2>
      <p>You’re welcome to use the app icon and screenshots on this site when writing about AI Wellness Pal. The
      <a href="/assets/icon.png">512 × 512 app icon</a> and <a href="/#screens">app screenshots</a> are linked here; for
      anything else, email <a href="mailto:{EMAIL}">{EMAIL}</a>.</p>
'''

# ------------------------------------------------------------------ Features hub

HUB_TITLE = 'AI Wellness Pal Features: AI Coach, Journal, Trackers & Widgets'
HUB_DESC = ('Every AI Wellness Pal feature: daily check-ins and plans, AI chat, journaling, habits, and tools for meals, calories, water, sleep, meditation, periods and weight.')
HUB_LEAD = ('One app for your daily wellbeing: a check-in that becomes a plan, an AI companion to talk with, and '
            'focused tools for the parts of life you want to look after. Here’s everything it does.')


# ------------------------------------------------------------------ Feature pages
# Each: slug, short (nav/footer label), card (one line), title, desc (meta), eyebrow, h1 (HTML),
# lead (HTML), hero (screenshot, alt), shots [(screenshot, caption)], body (HTML), faqs, related.

F_COACH = dict(
    slug='ai-wellness-coach', short='Daily check-in & plan',
    card='A 30-second check-in becomes Today’s Plan: two to four small actions that fit your energy and time.',
    title='Daily Wellness Check-in & Personalized Plan | AI Wellness Pal',
    desc=('Check in for 30 seconds (energy, mood, body, time) and AI Wellness Pal builds Today’s Plan: two to four '
          'small, doable actions for mood, sleep, movement and nutrition.'),
    eyebrow='Daily check-in · Today’s Plan',
    h1='A daily wellness plan built around <span class="grad-text">how you actually feel</span>',
    lead=('AI Wellness Pal starts every day with a 30-second check-in, then turns your answers into Today’s Plan: two '
          'to four small, doable actions for mood, sleep, movement and nutrition. Free on iPhone and Android.'),
    hero=('01_03_checkin', 'AI Wellness Pal daily check-in asking how your energy is today'),
    shots=[('01_02_home', 'Home: today’s focus, energy and plan'),
           ('07_action_detail', 'Each action has a step-by-step guide'),
           ('16_wellness_intention', 'Intentions shape your daily plans')],
    body="""      <h2>Why a check-in first</h2>
      <p>Most wellness apps hand you the same plan as everyone else. AI Wellness Pal asks how you’re actually doing
      first, because the right next step depends on it. Exhausted with fifteen minutes free? You get a very different
      day than when you’re rested with an hour.</p>

      <h2>How the daily check-in works</h2>
      <ol>
        <li><strong>Energy:</strong> pick a level from 1 to 5, from “Completely Drained” to “Fully Energized”.</li>
        <li><strong>Mood:</strong> how you feel emotionally right now.</li>
        <li><strong>Body and time:</strong> how your body feels (your recovery) and how much time you have today.</li>
      </ol>
      <p>You can skip any step and the plan uses what you gave it. Prefer to talk? Ask your Wellness Pal to “start my
      check-in”. Once you’ve checked in, <strong>Today’s Plan</strong> is ready within a few seconds.</p>

      <h2>What’s in Today’s Plan</h2>
      <p>Two to four actions, each with a time estimate and a checkbox: think a short Pilates session, a few minutes
      of recovery stretches or a breathing exercise. Open any action for a friendly step-by-step guide, and set a
      one-time reminder if you want a nudge to do your plan later today. Tick actions off as you go; finish them all
      and you get a small celebration.</p>
      <p>Days change. If you’re more tired than you thought, tell your Wellness Pal and it rebuilds the plan around how
      you actually feel.</p>

      <h2>Plans that follow your bigger goals</h2>
      <p>Wellness Intentions are longer-term directions like “sleep better”, “move more” or “feel calmer”. Your daily
      plans are shaped by them, and each intention tracks its own progress. With Premium, an intention can be broken
      into gentle daily steps automatically.</p>

      <h2>Progress you can see</h2>
      <p>Your streak counts the days you check in, with celebrations at 1, 3, 7, 14, 30, 50 and 100 days. Missing a
      day costs you a day rather than wiping the streak out. Achievements mark milestones from your first check-in
      (“First Sunrise”) to 100 days (“Zen Master”), and the Today’s Plan widget lets you tick actions straight from
      your home screen.</p>""",
    faqs=[
        ('How long does the daily check-in take?',
         '<p>About 30 seconds: three quick steps for energy, mood, and how your body feels plus the time you have. '
         'You can skip any step.</p>'),
        ('Is the daily check-in and plan free?',
         '<p>Yes. Daily check-ins and Today’s Plan are part of the free app on iPhone and Android. Premium adds '
         'extras like unlimited Wellness Pal chat, real-time voice and AI steps for your intentions.</p>'),
        ('What if my day changes after I get my plan?',
         '<p>Ask your Wellness Pal to update it, for example “I’m more tired than I thought”, and it rebuilds Today’s '
         'Plan around how you actually feel.</p>'),
        ('Can I get a reminder to do my plan?',
         '<p>Yes. Set a one-time reminder for later today from Today’s Plan and AI Wellness Pal will nudge you at that '
         'time. You choose which notifications you get in <strong>Settings → Notifications</strong>.</p>'),
    ],
    related=['ai-wellness-chat', 'habit-tracker', 'home-screen-widgets'],
)

F_CHAT = dict(
    slug='ai-wellness-chat', short='Wellness Pal AI chat',
    card='Chat or talk with an AI companion that knows your check-ins, and can log, plan and remind for you.',
    title='AI Wellness Chat & Voice Companion | AI Wellness Pal',
    desc=('Chat or talk with your Wellness Pal, an AI companion that learns from your check-ins and journal. It can '
          'log water and meals, set reminders and rebuild your daily plan.'),
    eyebrow='Wellness Pal · AI chat and voice',
    h1='An AI wellness companion you can <span class="grad-text">talk things through with</span>',
    lead=('Your Wellness Pal is the AI inside AI Wellness Pal. Chat or talk about stress, motivation, energy or '
          'habits. It learns from your check-ins and journal, so its guidance is personal, and it can do things in '
          'the app for you.'),
    hero=('03_05_pal_chat', 'Live voice conversation with the Wellness Pal in AI Wellness Pal'),
    shots=[],
    body="""      <h2>Chat or talk, whichever suits you</h2>
      <p>Tap the glowing orb button to open your Pal and start talking. To type instead, tap the smaller “Chat” orb
      beside it. Your chats are saved alongside your spoken conversations, and tapping a saved chat picks it back up
      where you left it. Free members get three messages a day; Premium is unlimited.</p>

      <h2>Live Chat Pal: real-time voice (Premium)</h2>
      <p>Live Chat Pal is a real-time voice conversation: you talk naturally and your Pal responds as you speak,
      rather than waiting for you to finish. Turn it on in <strong>Settings → AI Voice</strong>. With it on, you can
      also enable “Always listen for Pal” and just say <strong>“Hey Pal”</strong> while the app is open. Choose the
      voice you like, and turn on “Always speak English” if you want replies in English whatever language you
      speak.</p>

      <h2>It does things, not just talks</h2>
      <p>Ask in your own words and your Pal can:</p>
      <ul>
        <li>log water, meals, exercise, weight, a meditation session or a period start;</li>
        <li>create habits, set reminders and join challenges;</li>
        <li>run your check-in or rebuild Today’s Plan when your day changes;</li>
        <li>add or remove cards on your Home screen, or change your theme or text size;</li>
        <li>open any screen in the app.</li>
      </ul>

      <h2>Conversations that turn into insight</h2>
      <p>Your three most recent conversations are kept as cards: long-press the orb button to see them. They aren’t
      saved as journal entries automatically; if one was worth keeping, tap “Generate Reflection” to turn it into a
      reflection you can revisit.</p>

      <h2>Personal, private and honest about its limits</h2>
      <p>The Wellness Pal is powered by Google’s Gemini models. Before any of your information is shared with the
      AI, the app shows you what will be sent and asks your permission. Your Pal offers general wellness support, not
      therapy or medical advice. If you’re in crisis, contact your local emergency number; in the US you can call or
      text 988.</p>""",
    faqs=[
        ('Is the Wellness Pal chat free?',
         '<p>Yes: free members get three Wellness Pal messages a day. Premium makes chat unlimited and adds Live Chat '
         'Pal, the real-time voice conversation.</p>'),
        ('Can the Wellness Pal replace a therapist?',
         '<p>No. It’s a supportive AI companion for everyday wellbeing, not a therapist or a medical service. For '
         'mental-health concerns, talk to a qualified professional; in a crisis, contact your local emergency '
         'number.</p>'),
        ('Does my Wellness Pal remember me?',
         '<p>It learns from your check-ins and journal to make its guidance relevant, and keeps your three most recent '
         'conversations so you can pick them up again.</p>'),
        ('What does “Hey Pal” do?',
         '<p>With Live Chat Pal (Premium) and “Always listen for Pal” turned on, saying “Hey Pal” while the app is open '
         'starts a voice conversation hands-free.</p>'),
    ],
    related=['ai-journal', 'ai-wellness-coach', 'meditation-breathing'],
)

F_JOURNAL = dict(
    slug='ai-journal', short='AI journal & reflections',
    card='Guided prompts based on your real week, and supportive, specific responses from your Pal.',
    title='AI Journal App with Guided Reflections | AI Wellness Pal',
    desc=('Journal with prompts based on how your week actually went. Your Wellness Pal responds with something '
          'supportive and specific, and helps you see what really helps.'),
    eyebrow='Reflection · AI journal',
    h1='An AI journal that asks <span class="grad-text">the right questions</span>',
    lead=('Guided reflections in AI Wellness Pal give you prompts based on how your week has actually gone. Write in '
          'your own words and your Wellness Pal responds with something supportive and specific.'),
    hero=('21_reflections', 'Guided wellness reflection prompts in the AI Wellness Pal journal'),
    shots=[],
    body="""      <h2>Prompts from your real week</h2>
      <p>A blank page is hard. Start a reflection and you get prompts drawn from your recent check-ins, energy and
      sleep, like:</p>
      <ul>
        <li>“What’s weighing on my mind today?”</li>
        <li>“How have my sleep and energy been lately?”</li>
        <li>“What would help me feel more balanced right now?”</li>
      </ul>

      <h2>Responses that are specific, not generic</h2>
      <p>Write your entry and your Wellness Pal responds with something supportive and specific to what you wrote,
      not a stock affirmation. Over time your reflections help you spot patterns and see what actually helps you
      feel better.</p>

      <h2>Go deeper with Premium</h2>
      <p>Open any reflection and tap <strong>Discuss</strong> to talk it through properly with your Pal, then save
      anything useful that comes out of it as an <strong>Insight</strong> you can come back to. Write three or more
      reflections in a week and Premium also gives you a <strong>Weekly Reflection</strong> summary.</p>

      <h2>Turn conversations into reflections</h2>
      <p>Had a good conversation with your Pal? Tap “Generate Reflection” and it becomes a journal entry, so the
      thinking you did isn’t lost.</p>

      <h2>Private by design</h2>
      <p>Your journal is stored in your own private area of your account and isn’t shared with other users. AI
      Wellness Pal has no ads and doesn’t sell your data. When a reflection is sent to the AI for a response, the app
      asks your permission first.</p>""",
    faqs=[
        ('Is the AI journal free?',
         '<p>Yes. Guided reflections and AI responses are part of the free app. Premium adds “Discuss”, a full '
         'conversation about any reflection, and a Weekly Reflection summary.</p>'),
        ('Is my journal private?',
         '<p>Yes. Entries are stored in your own private area and never shared with other users, and the app has no '
         'ads and doesn’t sell data. See the <a href="/privacy.html">Privacy Policy</a>.</p>'),
        ('What is an Insight?',
         '<p>Something useful you save while discussing a reflection with your Pal, so you can revisit it later.</p>'),
    ],
    related=['ai-wellness-chat', 'meditation-breathing', 'ai-wellness-coach'],
)

F_MEDITATE = dict(
    slug='meditation-breathing', short='Meditation & breathing',
    card='Box breathing, 4-7-8, body scans and stress relief in 1 to 15 minutes, all free in Meditation Pal.',
    title='Meditation & Breathing Exercises App | AI Wellness Pal',
    desc=('Calm down in minutes with Box Breathing, 4-7-8, body scans and step-by-step stress relief in Meditation Pal, plus quick Wellness Studio activities. Free.'),
    eyebrow='Meditation Pal · Wellness Studio',
    h1='Breathe, meditate and <span class="grad-text">find your calm</span> in minutes',
    lead=('Meditation Pal in AI Wellness Pal gives you guided breathing, body scans, meditation sessions and '
          'step-by-step stress relief in 1 to 15 minutes, all free, plus a Wellness Studio of quick activities.'),
    hero=('14_wellness_studio', 'Breathing exercises in the AI Wellness Pal Wellness Studio'),
    shots=[('15_wellness_reads', 'Wellness Reads, ready to read aloud'),
           ('19_challenges', 'Join a 14-day meditation challenge')],
    body="""      <h2>Breathing you can follow</h2>
      <p>Choose <strong>Box</strong>, <strong>4-7-8</strong>, <strong>Calm</strong> or <strong>Stress Relief</strong>
      breathing for 1, 3, 5 or 10 minutes. An animated breathing orb and gentle haptic cues tell you when to breathe
      in, hold and breathe out, so you can close your eyes.</p>

      <h2>Body scans and meditation sessions</h2>
      <p>Body scans in four lengths (Quick 5 minutes, Stress Release 8, Sleep 10 and Full 15) and ten meditation
      sessions across nine themes, each 5 to 15 minutes, guided by a calming timer with breathing cues. There are
      wind-down sessions for bedtime too.</p>

      <h2>Stress relief, step by step</h2>
      <p>Five short exercises that walk you through calming down when stress spikes, one step at a time.</p>

      <h2>Reminders, progress and badges</h2>
      <p>Set meditation reminders for the days and times that suit you (like a morning, afternoon or bedtime
      session), track your sessions and minutes, earn meditation badges, and join the 14-Day Meditation Challenge.
      Your Wellness Pal can log a session for you too.</p>

      <h2>Wellness Studio</h2>
      <p>Thirty quick activities of 3 to 12 minutes in six categories: Breathing Exercises, Recovery Challenges,
      Mindfulness Sessions, Wellness Quizzes, Pilates Knowledge Cards and Stress Recovery. Three in every category are
      free, like Box Breathing, a 5-Minute Stretch Reset, a Body Scan Meditation and the Stress Awareness Quiz.
      Premium unlocks the rest, plus personalized picks.</p>

      <h2>Wellness Reads</h2>
      <p>Ten short articles on mindfulness, sleep, movement, nutrition, mental health, stress relief, Pilates and yoga,
      all free. The app can read any of them aloud in your phone’s voice, and keeps reading in the background with
      lock-screen controls.</p>""",
    faqs=[
        ('Are the meditation and breathing exercises free?',
         '<p>Yes. Every Meditation Pal session (breathing, body scans, meditations and stress relief) is free, and so '
         'are three activities in each Wellness Studio category. Premium unlocks the full Studio and personalized '
         'recommendations.</p>'),
        ('Are the sessions narrated?',
         '<p>Meditation Pal sessions are guided by a timer, a breathing animation and haptic cues rather than '
         'recorded narration. Wellness Reads can be read aloud by your phone’s voice.</p>'),
        ('How long are the sessions?',
         '<p>Breathing sessions run 1 to 10 minutes, body scans and meditations 5 to 15 minutes, and Studio '
         'activities 3 to 12 minutes.</p>'),
    ],
    related=['ai-journal', 'sleep-tracker', 'habit-tracker'],
)

F_PERIOD = dict(
    slug='period-tracker', short='Period tracker',
    card='Log your cycle, see your next period and fertile window, and get tips for each phase.',
    title='Period Tracker with Cycle Predictions & Phase Tips | AI Wellness Pal',
    desc=('Track your cycle in AI Wellness Pal: log period starts, see your cycle day and phase, your predicted next '
          'period and fertile window, and get gentle tips for each phase.'),
    eyebrow='Life Toolkit · Period Tracker',
    h1='A period tracker that fits <span class="grad-text">into your whole day</span>',
    lead=('Log your period starts and AI Wellness Pal shows your cycle day, current phase, predicted next period and '
          'estimated fertile window, with tips for each phase and plans that adapt to it.'),
    hero=('11_period_tracker', 'Period tracker showing cycle day 3 of 28 in the menstrual phase'),
    shots=[],
    body="""      <h2>Your cycle at a glance</h2>
      <p>Log the first day of each period and the tracker shows where you are: your <strong>cycle day</strong>, the
      current <strong>phase</strong> (menstrual, follicular, ovulation or luteal), when your <strong>next period</strong>
      is likely, and an estimated <strong>ovulation date and fertile window</strong>. If a period is late, it tells
      you how many days.</p>

      <h2>Predictions that learn your rhythm</h2>
      <p>Set your usual cycle and period length to start. As you log more periods, predictions use the average of
      your own logged cycles, so they reflect your rhythm rather than a textbook 28 days.</p>

      <h2>Tips for each phase, and a plan that adapts</h2>
      <p>Each phase comes with gentle tips, like resting and being kind to yourself, with light movement, warmth and
      hydration during your period. Your daily plan adapts to the phase too.</p>

      <h2>Reminders and widgets</h2>
      <p>Turn on cycle reminders in your notification preferences (they appear once you’ve logged period data), and
      add the Period Tracker widget to see your phase and cycle day on your home screen. You can also just tell your
      Wellness Pal “my period started today”.</p>

      <p class="note">Predictions are estimates and aren’t suitable for contraception or conception planning. Talk to
      a healthcare provider about your cycle or any concerns.</p>""",
    faqs=[
        ('Is the period tracker free?',
         '<p>Yes. Logging periods, predictions, phases and tips are part of the free app on iPhone and Android.</p>'),
        ('How does AI Wellness Pal predict my next period?',
         '<p>It adds your average cycle length to your last logged period start. With two or more logged periods, it '
         'uses the average gap between your own cycles; otherwise it uses the cycle length you set.</p>'),
        ('Can I use it for birth control or to get pregnant?',
         '<p>No. Predictions are estimates and aren’t suitable for contraception or conception planning. Talk to a '
         'healthcare provider.</p>'),
    ],
    related=['weight-tracker', 'sleep-tracker', 'ai-wellness-coach'],
)

F_WEIGHT = dict(
    slug='weight-tracker', short='Weight & BMI tracker',
    card='Log weigh-ins in kg or lb and see your trend, change over time and BMI.',
    title='Weight & BMI Tracker with Trend Chart | AI Wellness Pal',
    desc=('Log your weight in kg or lb and see your trend over time, your change since you started, your lowest and '
          'highest weigh-ins and your BMI, all in AI Wellness Pal.'),
    eyebrow='Life Toolkit · Body Weight',
    h1='Track your weight and BMI <span class="grad-text">without the obsession</span>',
    lead=('Body Weight in AI Wellness Pal keeps a simple record of your weigh-ins with a trend chart, your overall '
          'change and your BMI, so you see the direction, not just the daily wobble.'),
    hero=('12_body_weight', 'Body weight tracker with trend chart and BMI in AI Wellness Pal'),
    shots=[],
    body="""      <h2>Simple weigh-ins</h2>
      <p>Log a weigh-in in a couple of taps, in <strong>kilograms or pounds</strong>. Or just tell your Wellness Pal
      your weight and it logs it for you.</p>

      <h2>See the trend, not the noise</h2>
      <p>Weight moves day to day. The trend chart shows the direction over time, alongside your current weight, the
      change since your first entry, your lowest and highest weigh-ins and how many entries you’ve logged. Your full
      history is there to scroll back through.</p>

      <h2>Body Mass Index</h2>
      <p>Add your height once and your BMI is calculated from your latest weigh-in, shown with its category. BMI is
      a rough screening number, not a measure of health on its own, so treat it as one signal among many.</p>

      <h2>Part of the bigger picture</h2>
      <p>Weight sits next to your nutrition, calorie budget and habits in the same app, and the Body Weight widget
      can show your current weight and recent change on your home screen.</p>""",
    faqs=[
        ('Is the weight tracker free?',
         '<p>Yes. Logging weigh-ins, the trend chart and BMI are part of the free app.</p>'),
        ('Can I use pounds instead of kilograms?',
         '<p>Yes, switch between kg and lb at any time.</p>'),
        ('How is BMI calculated?',
         '<p>From your latest weigh-in and the height you add, using the standard BMI formula and adult categories. '
         'It’s a general screening measure, not a diagnosis.</p>'),
    ],
    related=['calorie-tracker', 'ai-nutrition-coach', 'habit-tracker'],
)

F_HABIT = dict(
    slug='habit-tracker', short='Habits & challenges',
    card='Build habits on your schedule with reminders, streaks and multi-day challenges.',
    title='Habit Tracker with Reminders, Streaks & Challenges | AI Wellness Pal',
    desc=('Build healthy habits in AI Wellness Pal: daily, weekday or custom schedules, reminders, streaks and challenges for water, walking, meditation, sugar and sleep.'),
    eyebrow='Habit Builder · Challenges',
    h1='Build habits that stick, <span class="grad-text">one small win at a time</span>',
    lead=('The Habit Builder in AI Wellness Pal turns good intentions into a routine: habits on your own schedule, '
          'optional reminders, streaks, and multi-day challenges with achievements when you finish.'),
    hero=('17_habit_builder', 'Habit Builder with popular challenges in AI Wellness Pal'),
    shots=[('08_add_habit', 'Create a habit with a target'),
           ('19_challenges', 'Multi-day challenges'),
           ('09_habit_formed', 'Celebrate each habit formed')],
    body="""      <h2>Habits on your schedule</h2>
      <p>Create a habit from a suggestion or from scratch, link it to a tool like the Hydration Coach or Calorie
      Budget, and set how often it happens: <strong>every day, weekdays, weekends or custom days</strong>. Add a target
      and unit if it helps, such as steps, litres, minutes or calories.</p>

      <h2>Reminders that show up on time</h2>
      <p>Give any habit an optional reminder time. If you’ve already done it today, today’s reminder is skipped, and
      it comes back tomorrow. You can also ask your Wellness Pal to “remind me to stretch at 7 pm”.</p>

      <h2>Challenges with an end point</h2>
      <p>A challenge is a multi-day commitment you join and log each day. Current challenges include:</p>
      <ul>
        <li><strong>7-Day Hydration Challenge</strong>: drink your daily water target for seven days in a row;</li>
        <li><strong>30-Day Walking Challenge</strong>: reach your daily step target;</li>
        <li><strong>14-Day Meditation Challenge</strong>: meditate at least five minutes a day;</li>
        <li><strong>Cut Back on Sugar Challenge</strong>: reduce added sugar for seven days;</li>
        <li><strong>14-Day Sleep Routine</strong>: be in bed before 11 pm for 14 nights.</li>
      </ul>
      <p>Finishing a challenge earns points and unlocks an achievement.</p>

      <h2>Tick habits off from your home screen</h2>
      <p>The Today’s Habits widget shows what’s left today with checkboxes you can tap without opening the app, on
      iPhone and Android.</p>""",
    faqs=[
        ('Is the habit tracker free?',
         '<p>Yes. Habits, reminders, streaks, challenges and the Today’s Habits widget are part of the free app.</p>'),
        ('Can a habit repeat only on some days?',
         '<p>Yes: every day, weekdays, weekends, or custom days of the week.</p>'),
        ('What’s the difference between a habit and a challenge?',
         '<p>A habit is part of your routine with its own schedule and optional reminder. A challenge is a multi-day '
         'commitment with an end point, like the 30-Day Walking Challenge, and finishing it unlocks an '
         'achievement.</p>'),
    ],
    related=['ai-wellness-coach', 'water-tracker', 'home-screen-widgets'],
)

F_WIDGETS = dict(
    slug='home-screen-widgets', short='Home-screen widgets',
    card='Today’s plan, habits and every tool on your home screen, on iPhone and Android.',
    title='Wellness Widgets for iPhone & Android Home Screens | AI Wellness Pal',
    desc=('AI Wellness Pal widgets put Today’s Plan, habits, water, nutrition, calories, cycle and weight on your iPhone or Android home screen, tickable without opening the app.'),
    eyebrow='Widgets · iPhone and Android',
    h1='Your wellbeing, <span class="grad-text">right on your home screen</span>',
    lead=('AI Wellness Pal’s widgets show today’s plan, habits and wellness tools at a glance, and let you tick things '
          'off without opening the app, on both iPhone and Android.'),
    hero=None,
    shots=[],
    images=['/assets/widgets.jpg'],
    body="""      <figure class="wide-figure"><picture><source type="image/webp" srcset="/assets/widgets.webp"><img src="/assets/widgets.jpg" alt="AI Wellness Pal home-screen widgets: Today’s Plan, Today’s Habits, Hydration Coach, Period Tracker, Body Weight and Nutrition Coach" width="1280" height="664" loading="lazy" decoding="async"></picture><figcaption>Widget previews: Today’s Plan, Today’s Habits and a few of the tool widgets</figcaption></figure>

      <h2>Plan and habits widgets</h2>
      <ul>
        <li><strong>Today’s Plan</strong>: today’s focus and actions, with checkboxes you can tick from the home
        screen and progress for the day.</li>
        <li><strong>Today’s Habits</strong>: what’s left today, ready to tick off.</li>
        <li><strong>Wellness Intention</strong>: your current intention’s tasks and progress.</li>
      </ul>

      <h2>A widget for every tool</h2>
      <p>Small widgets for the Life Toolkit: Hydration Coach, Nutrition Coach, Meal Planner, Calorie Budget, Period
      Tracker, Body Weight, Sleep Coach, Meditation Pal and Mindful Travel. Tap one to jump straight into that tool.</p>
      <p>Tool widgets with data have a <strong>flip button</strong> that turns the tile over to show today’s numbers:
      water progress, calories and macros, kcal left, your cycle phase and day, your current weight, or today’s meals
      (with arrows to browse them).</p>

      <h2>Made to match your home screen</h2>
      <p>Each widget has its own light and dark switch, so you can match it to your wallpaper. Widgets update as you
      use the app.</p>

      <h2>How to add a widget</h2>
      <p><strong>iPhone:</strong> long-press an empty area of your home screen, tap <strong>+</strong>, search for
      “AI Wellness Pal”, choose a widget and size, and tap Add Widget.</p>
      <p><strong>Android:</strong> long-press your home screen, tap <strong>Widgets</strong>, find AI Wellness Pal and
      drag the widget you want onto your home screen.</p>""",
    faqs=[
        ('Are the widgets free?',
         '<p>Yes. All widgets are part of the free app on iPhone and Android.</p>'),
        ('Can I tick off actions from the widget?',
         '<p>Yes. The Today’s Plan and Today’s Habits widgets have checkboxes that work without opening the app.</p>'),
        ('Why does my widget look out of date?',
         '<p>Your phone decides how often widgets refresh, so they can lag a little. Opening the app syncs them '
         'immediately, including anything you ticked from the home screen.</p>'),
    ],
    related=['ai-wellness-coach', 'habit-tracker', 'water-tracker'],
)

F_NUTRITION = dict(
    slug='ai-nutrition-coach', short='AI nutrition coach',
    card='Snap, describe or scan a meal for an AI estimate of calories, macros, fiber and a food quality score.',
    title='AI Food Tracker: Calories & Macros from a Photo | AI Wellness Pal',
    desc=('Snap a photo, describe your meal or scan a barcode, and AI Wellness Pal’s Nutrition Coach estimates '
          'calories, protein, carbs, fat and fiber, with a food quality score.'),
    eyebrow='Life Toolkit · Nutrition Coach',
    h1='Snap a meal. <span class="grad-text">Know what’s on your plate.</span>',
    lead=('The AI Nutrition Coach in AI Wellness Pal estimates calories and macros from a photo, a quick description '
          'or a barcode, keeps a simple food diary, and nudges you toward your daily goals.'),
    hero=('22_home_light', 'Today’s nutrition progress on the AI Wellness Pal home screen'),
    shots=[],
    body="""      <h2>Four ways to log a meal</h2>
      <ul>
        <li><strong>Take a photo</strong> of your plate for instant analysis.</li>
        <li><strong>Choose a photo</strong> from your gallery.</li>
        <li><strong>Describe it</strong> in your own words, like “2 egg hoppers and milk tea”.</li>
        <li><strong>Scan a barcode</strong> on packaged food. Products are looked up in Open Food Facts, per serving
        where available, otherwise per 100 g.</li>
      </ul>
      <p>You can also ask your Wellness Pal to log a meal for you.</p>

      <h2>What you get for every meal</h2>
      <p>An estimate of <strong>calories, protein, carbs, fat and fiber</strong> (plus sugar and sodium), the foods it
      detected and the portion size, a <strong>Food Quality Score</strong> from 0 to 100, and two to four short
      insights about the meal.</p>

      <h2>A food diary organized by meal</h2>
      <p>Meals are grouped into Breakfast, Lunch, Dinner and Snacks, so you can see your day at a glance. Edit or
      delete an entry any time, or send a meal from the Meal Planner straight to your diary.</p>

      <h2>Daily goals and coach insights</h2>
      <p>Set daily goals for calories, protein, carbs and fat (they start at 2,000 kcal, 90 g, 250 g and 65 g). Coach
      insights point out what to adjust, like “You are below your protein goal today”, with simple food ideas.</p>

      <h2>Connected to the rest of your day</h2>
      <p>Logged meals count toward your <a href="/features/calorie-tracker/">Calorie Budget</a> automatically, and the
      Nutrition Coach widget can flip to show today’s calories and macros on your home screen.</p>

      <h2>What’s free and what’s Premium</h2>
      <p>AI food analysis (photo, description and barcode) is part of Premium, which starts with a 7-day free trial.
      Your goals, food diary and coach insights are free.</p>

      <p class="note">Calories and nutrients are AI estimates and may be inaccurate. Use them as guidance, not fact;
      this isn’t medical or dietary advice. For health concerns, talk to a qualified professional.</p>""",
    faqs=[
        ('Is the AI nutrition coach free?',
         '<p>The food diary, daily goals and coach insights are free. Logging meals with AI analysis by photo, '
         'description or barcode is a Premium feature, with a 7-day free trial.</p>'),
        ('How accurate are the calorie estimates?',
         '<p>They’re AI estimates from a photo or description, so they can be off, especially for mixed dishes and '
         'portion sizes. Barcode lookups use the product’s published values from Open Food Facts. Treat the numbers as '
         'a guide.</p>'),
        ('Can I log food without taking a photo?',
         '<p>Yes. Describe the meal in a sentence, scan a barcode, or ask your Wellness Pal to log it.</p>'),
        ('Which foods can the barcode scanner find?',
         '<p>Packaged foods listed in Open Food Facts, the open food database. If a product isn’t found, you can '
         'describe it instead.</p>'),
    ],
    related=['calorie-tracker', 'ai-meal-planner', 'water-tracker'],
)

F_MEALS = dict(
    slug='ai-meal-planner', short='AI meal planner',
    card='A day, a week or a month of meals built around your goal, diet and calorie target, with a grocery list.',
    title='AI Meal Planner: Weekly Meal Plans & Grocery Lists | AI Wellness Pal',
    desc=('Daily, weekly or monthly meal plans around your goal, diet style and calorie target, with macros for every meal and a grocery list. AI Wellness Pal Premium.'),
    eyebrow='Life Toolkit · Meal Planner (Premium)',
    h1='Meal plans built around <span class="grad-text">your goals and your food</span>',
    lead=('Tell the AI Meal Planner about yourself and how you like to eat, and it plans breakfast, lunch, dinner and '
          'a snack for a day, a week or a month, with macros for every meal and a grocery list to match.'),
    hero=('10_life_toolkit', 'The AI Wellness Pal Life Toolkit with the AI Meal Planner, AI Calorie Budget and AI Nutrition Coach'),
    shots=[],
    body="""      <h2>Start with you</h2>
      <p>Your plan is built from a short profile: age, height, current and goal weight, activity level, your country
      or food culture, a daily calorie target (between 1,200 and 5,000 kcal), and your wellness goal, such as weight
      loss, muscle building, better energy, better sleep or stress management.</p>

      <h2>Pick a diet style</h2>
      <p>Standard, Vegetarian, Vegan, Local Cuisine, Budget-Friendly, High Protein or Low Carb.</p>

      <h2>Choose how far ahead to plan</h2>
      <ul>
        <li><strong>Daily:</strong> one day of meals.</li>
        <li><strong>Weekly:</strong> seven days of meals.</li>
        <li><strong>Monthly:</strong> 30 days built from a seven-day rotation.</li>
      </ul>

      <h2>Every meal, explained</h2>
      <p>Each day has breakfast, lunch, dinner and a snack. Every meal shows its calories, protein, carbs and fat,
      with a one-line reason it fits your goal, and each plan comes with a few AI insights. Don’t like the plan?
      Regenerate it.</p>

      <h2>A grocery list in one tap</h2>
      <p>Turn a plan into a combined shopping list, grouped into vegetables, fruits, proteins, dairy, grains and
      pantry items, and tick things off as you shop.</p>

      <h2>From plan to plate</h2>
      <p>Log a planned meal to your <a href="/features/ai-nutrition-coach/">food diary</a> in one tap, save favorites,
      and add the Meal Planner widget to browse today’s meals from your home screen.</p>

      <h2>Premium</h2>
      <p>Generating meal plans is part of AI Wellness Pal Premium, which starts with a 7-day free trial. Setting up
      your profile is free.</p>

      <p class="note">Calories and nutrients are AI estimates and may be inaccurate. This isn’t medical or dietary
      advice; if you have a medical condition, allergies or specific dietary needs, check with a qualified
      professional.</p>""",
    faqs=[
        ('Is the AI meal planner free?',
         '<p>Meal plan generation is a Premium feature, with a 7-day free trial. You can set up your profile for '
         'free.</p>'),
        ('Can it plan vegetarian or vegan meals?',
         '<p>Yes. Choose Vegetarian or Vegan, or another style such as High Protein, Low Carb, Budget-Friendly or '
         'Local Cuisine.</p>'),
        ('Does it make a shopping list?',
         '<p>Yes. It turns your plan into a grocery list grouped by type, which you can tick off as you shop.</p>'),
        ('Can it handle food allergies?',
         '<p>There isn’t an allergy setting yet, so always check ingredients yourself. If you have allergies or a '
         'medical diet, talk to a qualified professional.</p>'),
    ],
    related=['ai-nutrition-coach', 'calorie-tracker', 'weight-tracker'],
)

F_CALORIES = dict(
    slug='calorie-tracker', short='Calorie budget',
    card='Food and exercise in one place: your daily budget, what you’ve eaten, what you’ve burned and what’s left.',
    title='Calorie Budget Tracker: Food & Exercise Together | AI Wellness Pal',
    desc=('Set a daily calorie budget for losing, maintaining or gaining weight, log exercise, and see calories eaten, '
          'burned and remaining with AI Wellness Pal’s Calorie Budget.'),
    eyebrow='Life Toolkit · Calorie Budget',
    h1='Your daily calorie budget, <span class="grad-text">food and exercise together</span>',
    lead=('Calorie Budget in AI Wellness Pal puts what you eat next to what you burn, so you always know how much of '
          'today’s budget is left.'),
    hero=('10_life_toolkit', 'The AI Wellness Pal Life Toolkit with the AI Meal Planner, AI Calorie Budget and AI Nutrition Coach'),
    shots=[],
    body="""      <h2>A budget that matches your goal</h2>
      <p>Your daily budget starts from the calorie target in your Meal Planner profile (2,000 kcal by default) and
      adjusts for your goal: Weight Loss (−500 kcal), Maintenance, Weight Gain (+400 kcal) or Muscle Building
      (+300 kcal). Prefer your own number? Type it in; budgets stay between 1,200 and 5,000 kcal.</p>

      <h2>Eaten, burned and what’s left</h2>
      <p>A simple ring shows your budget, what you’ve eaten and what you’ve burned. What’s left is your budget minus
      what you’ve eaten, plus what you’ve burned. Meals you log in the <a href="/features/ai-nutrition-coach/">Nutrition
      Coach</a> are counted automatically.</p>

      <h2>Log exercise in seconds</h2>
      <p>Pick an activity (walking, running, cycling, yoga, Pilates, strength training or other) and the minutes.
      Enter the calories yourself, or let the app estimate them from the activity and time. You can also just tell
      your Wellness Pal “I walked for 30 minutes”.</p>

      <h2>See your week</h2>
      <p>Today’s timeline lists every meal and workout (and you can edit them), a goal streak counts the days you
      stay within budget, and a seven-day chart shows how the week is going.</p>

      <h2>AI prediction (Premium)</h2>
      <p>With Premium, Calorie Budget predicts where today is heading, your chance of staying on goal, and gives a few
      tailored insights.</p>

      <p class="note">Calorie numbers are estimates. This isn’t medical or dietary advice.</p>""",
    faqs=[
        ('Is the calorie budget tracker free?',
         '<p>Yes. Your budget, goal modes, exercise logging, timeline, streak and seven-day chart are free. AI '
         'predictions and insights are Premium, and logging meals with AI food analysis uses the Premium Nutrition '
         'Coach.</p>'),
        ('How is my daily calorie budget set?',
         '<p>From the daily calorie target in your Meal Planner profile, adjusted for your goal (for example −500 '
         'kcal for weight loss). You can also type your own budget, from 1,200 to 5,000 kcal.</p>'),
        ('Does it import workouts from Apple Health or Health Connect?',
         '<p>Not at the moment. Log exercise in the app or ask your Wellness Pal to log it for you.</p>'),
    ],
    related=['ai-nutrition-coach', 'weight-tracker', 'ai-meal-planner'],
)

F_WATER = dict(
    slug='water-tracker', short='Water tracker',
    card='A daily water target that fits you, one-tap logging, a hydration score and streaks.',
    title='Water Tracker & Hydration Coach App | AI Wellness Pal',
    desc=('Track your water with a daily target that fits your body and activity, one-tap logging, a hydration score, '
          'streaks and optional weather-aware goals in AI Wellness Pal.'),
    eyebrow='Life Toolkit · Hydration Coach',
    h1='Drink enough water, <span class="grad-text">without overthinking it</span>',
    lead=('The Hydration Coach in AI Wellness Pal sets a daily water target that fits you, makes logging a single tap, '
          'and shows how consistently you’re hitting it.'),
    hero=('13_hydration_coach', 'Hydration Coach with daily water goal and quick add in AI Wellness Pal'),
    shots=[('19_challenges', 'The 7-Day Hydration Challenge')],
    body="""      <h2>A target that fits you</h2>
      <p>Your daily goal starts at about 35 ml of water per kilogram of body weight (from your profile), adjusted for
      your profile and activity level, and kept between 1.8 and 4.5 liters. No weight set? It starts at 2.5 liters.
      You can set your own target any time and switch back to automatic.</p>

      <h2>Weather-aware hydration (Premium)</h2>
      <p>Hot or humid day? Set your location and the Hydration Coach adds up to an extra liter to your goal, based on
      the “feels like” temperature.</p>

      <h2>One-tap logging</h2>
      <p>Quick-add 100, 200, 250, 500 or 750 ml, or a full liter, or enter a custom amount. Or just tell your
      Wellness Pal “log a glass of water”.</p>

      <h2>Score, streaks and your week</h2>
      <ul>
        <li>A <strong>hydration score</strong> from 0 to 100 that rewards drinking enough, drinking consistently and
        spreading it through the day.</li>
        <li>Streak milestones like <strong>Hydration Hero</strong> (7 days) and <strong>Hydration Champion</strong>
        (30 days).</li>
        <li>A timeline of today’s drinks and a seven-day view of how often you met your goal.</li>
      </ul>

      <h2>Reminders, challenges and widgets</h2>
      <p>Turn on hydration reminders in your notification preferences (they start off), join the 7-Day Hydration
      Challenge, and add the Hydration Coach widget to see today’s progress on your home screen. With Premium you also
      get AI insights about your drinking patterns.</p>""",
    faqs=[
        ('Is the water tracker free?',
         '<p>Yes. Logging, your automatic or custom goal, the hydration score, streaks and the weekly view are free. '
         'Weather-aware goals and AI insights are Premium.</p>'),
        ('How much water should I drink a day?',
         '<p>The Hydration Coach starts at about 35 ml per kilogram of body weight, adjusted for your profile and '
         'activity, between 1.8 and 4.5 liters. Needs vary, so follow your doctor’s advice if you have a health '
         'condition.</p>'),
        ('Can I track water in ounces?',
         '<p>Not yet. Amounts are in milliliters and liters.</p>'),
        ('Does it remind me to drink water?',
         '<p>Yes, if you want it to. Turn on hydration reminders in <strong>Settings → Notifications → Notification '
         'Preferences</strong>; they’re off by default.</p>'),
    ],
    related=['habit-tracker', 'ai-nutrition-coach', 'home-screen-widgets'],
)

F_SLEEP = dict(
    slug='sleep-tracker', short='Sleep coach',
    card='A sleep score, sleep stages and the habits behind them, from Apple Health or Health Connect.',
    title='Sleep Tracker with Apple Health & Health Connect | AI Wellness Pal',
    desc=('See your sleep score, sleep stages and what affects them. AI Wellness Pal’s Sleep Coach reads sleep from '
          'Apple Health or Health Connect (read-only) and adds AI insights.'),
    eyebrow='Life Toolkit · Sleep Coach',
    h1='Understand your sleep, <span class="grad-text">then improve it</span>',
    lead=('The Sleep Coach reads your sleep from Apple Health on iPhone or Health Connect on Android and turns it into '
          'a simple score, your sleep stages, and the everyday habits that affect them.'),
    hero=None,
    shots=[],
    body="""      <h2>Connect once, read-only</h2>
      <p>Tap <strong>Connect Apple Health</strong> (iPhone) or <strong>Connect Health Connect</strong> (Android) and allow
      sleep access. The Sleep Coach reads sleep only (time asleep and awake, deep, REM, light and time in bed) and
      never writes anything back. Until you connect, it shows clearly labelled sample data so you can see how it
      works.</p>

      <h2>Your sleep score</h2>
      <p>Each night gets a score from 0 to 100, rated Great (85+), Good (70+) or Fair (50+). It weighs how long you
      slept (seven to nine hours is ideal), how much was deep and REM sleep, how efficiently you slept, and how
      consistent your schedule is.</p>

      <h2>Sleep stages</h2>
      <p>See how the night split between Awake, REM, Core and Deep sleep, with the share of each.</p>

      <h2>What affects your sleep</h2>
      <p>Sleep factors connect your night to your day, using what you’ve logged in the app: hydration, exercise,
      dinner timing and caffeine. A food and sleep card and a seven-day history help you spot patterns.</p>

      <h2>AI Sleep Insight (Premium)</h2>
      <p>With Premium you get a personalized summary of your sleep and what’s contributing to it, plus a “Try this
      tonight” suggestion you can add to your routine. Sleep summaries are sent to Google Gemini only after you give
      permission, and are never used for advertising.</p>

      <h2>Build better sleep habits</h2>
      <p>Join the 14-Day Sleep Routine challenge (in bed before 11 pm), and wind down with a sleep body scan or
      breathing session in <a href="/features/meditation-breathing/">Meditation Pal</a>.</p>

      <p class="note">The Sleep Coach offers general wellness information. If you have ongoing sleep problems, talk to a
      doctor.</p>""",
    faqs=[
        ('Is the sleep tracker free?',
         '<p>Yes. Connecting Apple Health or Health Connect, your sleep score, stages, sleep factors and history are '
         'free. The AI Sleep Insight is Premium.</p>'),
        ('Do I need a smartwatch?',
         '<p>The Sleep Coach uses the sleep data already in Apple Health or Health Connect, which can come from a '
         'watch, a sleep-tracking app or your phone. The more detailed that data, the more detailed your stages.</p>'),
        ('Does AI Wellness Pal write to Apple Health or Health Connect?',
         '<p>No. It only reads your sleep data, with your permission, and you can disconnect at any time in your '
         'phone’s settings.</p>'),
        ('How is the sleep score calculated?',
         '<p>From four things: duration (seven to nine hours is ideal), deep and REM sleep, sleep efficiency and '
         'schedule consistency, combined into a 0 to 100 score.</p>'),
    ],
    related=['meditation-breathing', 'ai-wellness-coach', 'water-tracker'],
)

FEATURES = [F_COACH, F_CHAT, F_JOURNAL, F_NUTRITION, F_MEALS, F_CALORIES, F_WATER, F_SLEEP,
            F_MEDITATE, F_PERIOD, F_WEIGHT, F_HABIT, F_WIDGETS]
FEATURE_GROUPS = [
    ('Your daily core', 'The check-in, plan and companion at the heart of the app.',
     ['ai-wellness-coach', 'ai-wellness-chat', 'ai-journal', 'habit-tracker']),
    ('Food and body', 'Track what you eat, your energy balance and your weight.',
     ['ai-nutrition-coach', 'ai-meal-planner', 'calorie-tracker', 'weight-tracker']),
    ('Rest, calm and cycle', 'Sleep, hydration, mindfulness and your cycle.',
     ['sleep-tracker', 'water-tracker', 'meditation-breathing', 'period-tracker']),
    ('On your home screen', 'See and tick things off without opening the app.',
     ['home-screen-widgets']),
]
