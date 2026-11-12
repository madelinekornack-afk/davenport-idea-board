import json, csv, re
from bands import bands_html
K='/Users/madelinekornack/Projects/appfigures-ideas'
prefix=open('build_buzz.py').read().split("repo=json.load")[0]
TABS=[('./','Board'),('clark.html','Clark'),('audit.html','Audit'),('formcheck.html','Form check'),('buzz.html','Buzz'),('calories.html','Calorie apps'),('bloodwork.html','Bloodwork'),('glp1.html','GLP-1'),('learnai.html','Learn AI')]
def nav(active): return '<nav class="tabs">'+''.join(f'<a{" class=on" if h==active else ""} href="{h}">{t}</a>' for h,t in TABS)+'</nav>'
rows=list(csv.DictReader(open(f'{K}/keywords_us30d.psv'),delimiter='|'))
byid={}
for r in rows: byid.setdefault(r['af_id'],r)
R=json.load(open(f'{K}/ratings_monthly_us.json')); months=R['months']; apps=R['apps']
def rs(pid, upto='2026-10'):
    a=apps[pid]; return {m:v for m,v in zip(months,a['new']) if m<=upto and v>=0}
def money(v): return f"${v/1e6:.1f}M" if v>=1e6 else (f"${v/1e3:.0f}K" if v>=1000 else f"${v:,.0f}")
def num(v): return f"{v/1e6:.2f}M" if v>=1e6 else (f"{v/1e3:.0f}K" if v>=1000 else str(int(v)))
def bars(title, sub, items, key='rev', note=''):
    # items: list of (name, dl, rev, blurb)
    vals=[(n,dl,rv,b) for n,dl,rv,b in items]
    mx=max((rv if key=='rev' else dl) for n,dl,rv,b in vals) or 1
    tot=sum((rv if key=='rev' else dl) for n,dl,rv,b in vals)
    out=[]
    for n,dl,rv,b in vals:
        v=rv if key=='rev' else dl
        small=f'<small>{num(dl)} dl</small>' if key=='rev' and dl else (f'<small>{money(rv)}</small>' if key=='dl' and rv else '')
        t=f"{n}: {money(rv) if key=='rev' else num(dl)+' downloads'}, US iPhone, 30 days. {b}"
        out.append(f'<div class="row" title="{t}"><div class="lbl">{n}{small}</div><div class="track"><i style="width:{100*v/mx:.1f}%"></i></div><div class="val">{money(v) if key=="rev" else num(v)}</div></div>')
    lab='net revenue' if key=='rev' else 'downloads'
    return f'<div class="chart"><h3>{title} <span style="font-family:var(--mono);font-size:12px;color:var(--muted);font-weight:400">· {lab}, group total {money(tot) if key=="rev" else num(tot)}</span></h3><p class="sub">{sub}</p><div class="rows">{"".join(out)}</div>{("<p class=none>"+note+"</p>") if note else ""}</div>'
def page(fn, title, eyebrow, h1, lede, body_html, foot):
    g={}
    exec(prefix.replace("<title>Buzz</title>",f"<title>{title}</title>"), g)
    head=g['head'].replace('</style>','</style>'+CSS2,1)
    html=head+f'<div class="wrap">\n{nav(fn)}\n<header>\n  <div class="eyebrow">{eyebrow}</div>\n  <h1>{h1}</h1>\n  <p class="lede">{lede}</p>\n</header>\n{body_html}\n{bands_html(fn)}\n<div class="foot">{foot} <a href="./">Back to the board.</a></div>\n</div>\n</body>\n</html>\n'
    open(fn,'w').write(html); print('wrote',fn,len(html))
lc=None
CSS2='''<style>
table.cmp { width: 100%; border-collapse: collapse; margin-top: 12px; font-size: 13.5px; background: var(--surface); border: 1px solid var(--line); }
table.cmp th, table.cmp td { padding: 8px 10px; text-align: left; border-bottom: 1px solid var(--line); vertical-align: top; }
table.cmp th { font-family: var(--mono); font-size: 11px; letter-spacing: 0.05em; text-transform: uppercase; color: var(--muted); font-weight: 500; }
table.cmp td:nth-child(2), table.cmp td:nth-child(3), table.cmp td:nth-child(4), table.cmp td:nth-child(5) { font-family: var(--mono); font-size: 12.5px; font-variant-numeric: tabular-nums; white-space: nowrap; }
table.cmp td.w { font-weight: 700; }
.tablewrap2 { overflow-x: auto; }
</style>'''
g={}; exec(prefix, g); linechart=g['linechart']
METHOD='<div class="read"><div><b>Scope</b>US, iPhone, App Store only. Android, web sign-ups and web billing are not here, and most of these companies sell on the web, so revenue understates them.</div><div><b>Estimates</b>Appfigures models downloads from ranks and ratings. Apps below its threshold show as "not modeled," which means small, not zero.</div><div><b>Method</b>Keyword Inspector searches in a signed-in session on Nov 11, top 15 results per keyword with 30-day US estimates for the top 10, plus the ratings report for every app named here, Nov 2024 to Nov 2026. No credits, no tracking slots. Raw data in <code>~/Projects/appfigures-ideas</code>.</div></div>'

# ---------------- BLOODWORK (idea 9) ----------------
bw_bars=bars('Who is on the phone: at-home testing and biomarker apps, US iPhone, 30 days to Nov 11','Only four of the nineteen apps in the sweep clear the download model. None sells in-app; all of them bill on the web.',[
 ('Rythm Health',112937,0,'launched Oct 7, 2026; $79 monthly panel'),
 ('Function Health',16594,0,'$499/yr, 100+ biomarkers twice a year'),
 ('MyQuest (Quest)',116343,0,'the lab incumbent, results portal'),
 ('MyLabcorp',142810,0,'the other lab incumbent'),
],key='dl',note='<b>Not modeled.</b> Superpower (Jan 2026), InsideTracker, Everlywell, LetsGetChecked, Health3, BloodTrends, Carrot Care, Vector, Node Health, Bryan Johnson\'s Blueprint and Don\'t Die. Being below the model on a Nov 11 pull means fewer than roughly 10K US installs a month.')
bw_lines=linechart('New App Store ratings per month: the three that look like Rythm','Ratings are the one signal the download model cannot hide. Function peaked in January 2026; Rythm is one month old.',[('Function Health',rs('337641328340')),('Superpower',rs('338450597779')),('Rythm Health',rs('338707346013'))])
bw_lines2=linechart('The legacy at-home test companies, same measure','Everlywell and LetsGetChecked, the 2015-era kit companies, on the phone.',[('Everlywell',rs('335569086222')),('LetsGetChecked',rs('281953720053')),('InsideTracker',rs('304718626849'))],note='Everlywell\'s October value is an Appfigures recount and is dropped; its run rate is about 100 ratings a month, flat for two years. LetsGetChecked is under 20 and falling. InsideTracker is dead on mobile.')
bw_tbl='''<div class="tablewrap2"><table class="cmp"><thead><tr><th>Company</th><th>App since</th><th>US downloads, 30d</th><th>New ratings, Oct 2026</th><th>All-time ratings</th><th>Read</th></tr></thead><tbody>
<tr><td>Rythm Health</td><td>Oct 2026</td><td class="w">113K</td><td>47 (253 so far in Nov)</td><td>300</td><td>Biggest launch in the category; the ratings lag the installs, which reads as paid acquisition. Verify before believing the 113K.</td></tr>
<tr><td>Function Health</td><td>Aug 2024</td><td>17K</td><td>340</td><td>25K</td><td>Scaled, then slowed: new ratings fell from 2,056 in Jan 2026 to 340 in Oct, a sixth of the peak.</td></tr>
<tr><td>Superpower</td><td>Jan 2026</td><td>not modeled</td><td>169</td><td>1.8K</td><td>Early. Grew to 344 a month in June, half that now.</td></tr>
<tr><td>Everlywell</td><td>Aug 2022</td><td>not modeled</td><td>~100</td><td>10K</td><td>Flat for two years.</td></tr>
<tr><td>LetsGetChecked</td><td>Jan 2020</td><td>not modeled</td><td>12</td><td>9.5K</td><td>Fading.</td></tr>
<tr><td>InsideTracker</td><td>Jun 2020</td><td>not modeled</td><td>1</td><td>342</td><td>Nothing on mobile.</td></tr>
<tr><td>Quest, Labcorp</td><td>2014, 2018</td><td>116K, 143K</td><td>16K, 17K</td><td>528K, 112K</td><td>The labs everyone else resells. Labcorp turned on a ratings prompt in May 2026.</td></tr>
</tbody></table></div>'''
bw_body=f'''
<section>
  <h2>The field</h2>
  {bw_tbl}
  {bw_bars}
</section>
<section>
  <h2>Who is growing</h2>
  {bw_lines}
  {bw_lines2}
  <div class="read">
    <div class="hot"><b>Rythm is the one with momentum</b>Its app went live on October 7 and the model already puts it at 113K US installs in 30 days, more than Function has done in any month. The ratings have not caught up (300 total), so part of that is a launch campaign. Either way it is the newest and fastest-moving company of its kind, which is what a distribution partner wants.</div>
    <div class="hot"><b>Function has peaked on the phone</b>It is the scaled player (25K ratings, $499 a year, reported $2.5B valuation in 2025) and its monthly new ratings are down six-fold from January. A company that size does not need Maxinomics; it needs a growth story, which is a different conversation.</div>
    <div><b>Superpower is the early one</b>Launched the app in January, 1.8K ratings, growth stalled in the summer. It is the company most likely to trade equity for an audience that converts.</div>
    <div><b>The 2015 cohort never made the phone work</b>Everlywell, LetsGetChecked and InsideTracker have nothing happening in the App Store. Apple Ads on "at home blood test": nobody is buying. The category is being re-founded, not fought over.</div>
  </div>
</section>
<section>
  <h2>What this says for idea 9</h2>
  <div class="read">
    <div class="hot"><b>Three first conversations</b>1. Rythm: the product on the card, one month in, with the install curve of a company that is spending to grow and would rather not. 2. Superpower: early and stalled, the classic audience-for-equity fit. 3. Function: only if the ask is a content partnership, not equity.</div>
    <div><b>What to verify before any of them</b>Whether Rythm's 113K is organic or bought (ask for their install source split), what each pays per acquired customer today, and whether a Maxinomics video converts at a tenth of that. One sponsored video with a tracking link answers all three for under $10K of opportunity cost.</div>
    <div><b>What the data cannot say</b>Revenue. All of these bill on the web, so the App Store shows installs and nothing else. Function has disclosed numbers publicly; the others have not.</div>
  </div>
  {METHOD}
</section>'''
page('bloodwork.html','Bloodwork','Idea 9 on the board · buy into something like Rythm · Appfigures sweep, Nov 11','At-home bloodwork: who to call first','Idea 9 is to take a stake in a company like Rythm and bring Maxinomics as distribution instead of building a clone. This tab answers the whiteboard question on the card: which three companies deserve a first conversation? Every at-home testing, biomarker and longevity app the Keyword Inspector returns, with two years of ratings velocity for the ones that matter.',bw_body,'Built Nov 11, 2026 for the Davenport session.')

# ---------------- GLP-1 (idea 8) ----------------
g_rev=bars('GLP-1 and peptide trackers that make money, US iPhone, 30 days to Nov 11','Of 62 tracker apps the sweep returned, seven clear the download model and three clear the revenue model.',[
 ('MeAgain: GLP-1 Tracker',49698,380303,'Apr 2025; shot log, weight, food, AI coach'),
 ('Shotsy GLP-1 Tracker',13572,184986,'May 2024; the original, shot log and side effects'),
 ('PeptidePal',0,52846,'Apr 2026; peptide dosing calculator, downloads not modeled'),
],key='rev',note='<b>Downloads only, no revenue modeled:</b> Peptide Tracker Log & Reminder 18K, Mochi Health 13K (telehealth prescriber, not a tracker), Dosely 3.5K, Pep AI 813. <b>Not modeled at all:</b> the other 55, including Glapp, DreamMe, Glippy, Zepbound & Mounjaro Tracker, Ozempic Tracker, GLP Buddy, Dosiva, GLPal, GLPro, Free.Well, Klick, Glo, Curely, PenPal, Holt, Dosley, TrimRx, Blum, Ozzy, OzemPro, SlimShot, Slimming, WeTide, Shoty, Dosia, JabJourney and the rest.')
g_lines=linechart('New App Store ratings per month: the two leaders','MeAgain passed Shotsy in June 2026 and has held about 4,500 a month since. Shotsy has been flat at about 2,000 for a year.',[('MeAgain',rs('338158184377')),('Shotsy',rs('337413541786')),('Mochi Health (telehealth)',rs('337437955321'))])
g_lines2=linechart('The 2025 and 2026 launches','Every tracker launched in the last two years that got past 300 ratings. Spikes are paid campaigns; none has held.',[('PeptidePal',rs('338527961650')),('DreamMe (pet)',rs('338420395998')),('Peptide Tracker Log',rs('338535105022')),('Zepbound & Mounjaro Tracker',rs('337852539544'))],note='Glapp (the one on the card) peaked at 207 in June and is at 81. Glippy, Free.Well, GLPTracker, OzemPro and Dosely are all under 200 a month. The other 40-odd 2025 and 2026 launches have fewer than ten ratings each.')
g_tbl='''<div class="tablewrap2"><table class="cmp"><thead><tr><th>Launch year</th><th>Trackers in the sweep</th><th>Cleared the download model</th><th>Cleared the revenue model</th></tr></thead><tbody>
<tr><td>2023 and earlier</td><td>5</td><td>0</td><td>0</td></tr>
<tr><td>2024</td><td>9</td><td class="w">1 (Shotsy)</td><td class="w">1 (Shotsy)</td></tr>
<tr><td>2025</td><td>9</td><td class="w">1 (MeAgain)</td><td class="w">1 (MeAgain)</td></tr>
<tr><td>2026</td><td class="w">25</td><td>4 (PeptidePal, Peptide Tracker Log, Dosely, Pep AI)</td><td>1 (PeptidePal)</td></tr>
<tr><td>no date (not in the estimate set)</td><td>14</td><td>0</td><td>0</td></tr>
</tbody></table></div>'''
g_body=f'''
<section>
  <h2>The field: 62 trackers, two businesses</h2>
  {g_tbl}
  {g_rev}
  <div class="read">
    <div class="hot"><b>Two winners, $565K a month between them</b>MeAgain and Shotsy make about $6.8M a year on US iPhone combined. That is the whole category's in-app revenue. Both buy Apple Ads on "glp-1 tracker" and "ozempic," and so does MyFitnessPal, which now ranks for "glp1" organically: the incumbent is moving in.</div>
    <div><b>Twenty-five trackers launched in 2026</b>Up from nine in 2025. Four cleared the download model and one makes money. The shot-log-plus-reminder app is a solved problem with a two-year head start, and the long tail proves it.</div>
    <div><b>The one new thing that worked is peptides, briefly</b>PeptidePal and Peptide Tracker Log both launched in spring 2026 and both spiked to 800 to 1,700 ratings a month in June and July, then fell by 80%. There is demand for peptide dosing that the GLP-1 apps do not serve, and nobody has held it.</div>
  </div>
</section>
<section>
  <h2>Who is growing</h2>
  {g_lines}
  {g_lines2}
</section>
<section>
  <h2>What this says for idea 8</h2>
  <div class="read">
    <div class="hot"><b>The card was right: another shot log is dead on arrival</b>Twenty-five of them shipped this year and one makes money. Steve's "would likely crush" has to mean the layer the trackers lack: the regimen compared against bloodwork, food and labs in one place, which MeAgain is already inching toward with an AI coach.</div>
    <div><b>The market is real but small on the phone</b>About $7M a year in the US App Store for the top two, with MeAgain still growing at 4,500 ratings a month. The money in GLP-1 is in prescribing (Mochi Health went from 229 to 2,000 ratings a month in a year) and in the drugs, not the log.</div>
    <div><b>Where the audience helps</b>GLP-1 users skew to the income band Maxinomics has, and the peptide spike says the Bryan Johnson crowd is in there too. That is a distribution edge for a Rythm-style partner (idea 9) as much as for a tracker.</div>
  </div>
  {METHOD}
</section>'''
page('glp1.html','GLP-1 trackers','Idea 8 on the board · peptide / GLP-1 regimen tracker · Appfigures sweep, Nov 11','GLP-1 and peptide trackers: 62 apps, two businesses','The card said "GLP-1 dose trackers are already a pile" without numbers. Here are the numbers: every tracker the Keyword Inspector returns for eight GLP-1, Ozempic, semaglutide, tirzepatide and peptide terms, who makes money, who is growing, and how many launched this year.',g_body,'Built Nov 11, 2026 for the Davenport session.')

# ---------------- LEARN AI (idea 7, Nora) ----------------
l_bars=bars('Anything that sells "learn AI" on the phone, US iPhone, 30 days to Nov 11','Of 74 learn-AI, prompt and AI-course apps in the sweep, zero clear the download model. The only apps with estimates on these keywords are platforms and a homework bot.',[
 ('Coursera',22381,390494,'the course platform; AI is one shelf'),
 ('DataCamp',0,2903,'data and AI courses, bills on the web'),
 ('Khan Academy',48914,0,'free'),
 ('Gauth: AI Study Companion',276532,627831,'students photographing homework, not executives'),
],key='rev',note='<b>Not modeled, all 74 of them:</b> Sololearn\'s Learn AI, Learn AI: AI Tools Mastery, Coursiv, DeepLearning.AI, Skilario, Kairo, Curio, explainx, Cyberminds, Cosmo (CodeSignal), Noesion, Prompt Dojo, PromptCraft, Learn AI Prompt Engineering, AI Academy, AI From Zero, UnlockAI, Pawsitive AI, Iro, mainio, Skiller, sqills, Tixu, kju.ai and the rest. Thirty-three of the 74 launched in 2026.')
l_lines=linechart('New App Store ratings per month: the only learn-AI apps with any','Coursiv is the one that got past 1,000 in a month; it bought that in spring and is at 70 now.',[('Coursiv',rs('338493082422')),('Cosmo (CodeSignal)',rs('338283711940')),('Skilario',rs('338609422855')),('Learn AI: AI Tools Mastery',rs('338170449413'))],note='Everything else named above has between zero and six ratings all time. DeepLearning.AI, Andrew Ng\'s brand, launched an app in July and has 54.')
l_lines2=linechart('For scale: the platforms','Coursera and Khan Academy on the same measure. Flat, and two orders of magnitude above the AI-specific apps.',[('Coursera',rs('39787288099')),('Khan Academy',rs('25282702')),('DataCamp',rs('280442838525'))])
l_body=f'''
<section>
  <h2>The field: 74 apps, none with traction</h2>
  {l_bars}
  <div class="read">
    <div class="hot"><b>Nobody has made "learn AI" work as an app</b>Seventy-four apps rank for the terms, thirty-three of them launched this year, and not one clears Appfigures' download threshold. The best of them, Coursiv, ran a paid spike to 1,311 ratings in May 2026 and is at 70. Andrew Ng's DeepLearning.AI app has 54 ratings in four months.</div>
    <div><b>Who buys the ads instead</b>On "learn ai" the Apple Ads buyers are Learna (an English-learning app), DataCamp, and then Gemini, Claude and ChatGPT themselves. The labs are bidding on the phrase, which says the "learning" happens inside the chatbot, not in a course app.</div>
    <div><b>Where the money on these keywords is</b>Gauth, a homework-photo bot for students, makes $628K a month. Coursera makes $390K across every subject. "Learn AI" as a phone purchase is a student behavior, not an executive one.</div>
  </div>
</section>
<section>
  <h2>Who is growing</h2>
  {l_lines}
  {l_lines2}
</section>
<section>
  <h2>What this says for Nora, idea 7</h2>
  <div class="read">
    <div class="hot"><b>Open field, wrong shelf</b>There is no incumbent to displace, which supports the edge score. But the App Store is also telling you that the buyer Nora is for, a senior person who wants to learn by doing, does not go to the App Store for it. They buy a cohort course, a newsletter, a workshop, or they watch a video, which is where Maxinomics already is.</div>
    <div><b>What that means for the build</b>Nora as a Maxinomics product (a paid series, exercises delivered by email and in a browser, a Buzz channel to do them in) fits the data. Nora as an iOS app with in-app purchase would be the seventy-fifth entry in a category where the seventy-fourth has six ratings.</div>
    <div><b>Market score</b>Stays at 3. The market is real and the audience is in it, but it is off-store, so none of it shows up in the data here. Pricing comps are Maven cohorts ($500 to $2,000) and Section's AI courses, not $9.99 a month.</div>
  </div>
  {METHOD}
</section>'''
page('learnai.html','Learn AI apps','Idea 7 on the board · Nora, learn AI by doing · Appfigures sweep, Nov 11','Learn-AI apps: 74 of them, none with traction','Nora moved to rank 6 on the argument that the Maxinomics audience is the buyer. This tab checks whether anyone sells AI education on the phone today and what it earns: every app the Keyword Inspector returns for eight learn-AI, prompt-engineering and AI-course terms, with two years of ratings for the ones that have any.',l_body,'Built Nov 11, 2026 for the Davenport session.')
