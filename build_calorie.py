import json, re
from bands import bands_html
D='/Users/madelinekornack/Projects/appfigures-calorie'
exec(open('build_buzz.py').read().split("repo=json.load")[0].replace("<title>Buzz</title>","<title>Calorie apps</title>").replace('<a class="on" href="buzz.html">Buzz</a><a href="calories.html">Calorie apps</a>','<a href="buzz.html">Buzz</a><a class="on" href="calories.html">Calorie apps</a>'))
NAMES={'6013158':'MyFitnessPal','337323818982':'Cal AI'}
us=json.load(open(f'{D}/raw_monthly_us_v2.json')); ww=json.load(open(f'{D}/raw_monthly_ww_v2.json')); rat=json.load(open(f'{D}/raw_ratings_v2.json'))
def ser(d,pid,key):
    return {k[:7]:(int(v[key]) if key in('downloads','new_total') else float(v[key])) for k,v in d[pid].items() if not k.startswith('2026-11')}
dl_us=[(NAMES[p],ser(us,p,'downloads')) for p in NAMES]
rev_us=[(NAMES[p],ser(us,p,'revenue')) for p in NAMES]
rev_ww=[(NAMES[p],ser(ww,p,'revenue')) for p in NAMES]
dl_ww=[(NAMES[p],ser(ww,p,'downloads')) for p in NAMES]
rt=[(NAMES[p],ser(rat,p,'new_total')) for p in NAMES]
def win(s,a,b): return sum(v for m,v in s.items() if a<=m<=b)
A1,B1,A0,B0='2025-11','2026-10','2024-11','2025-10'
def pct(c,p): return f"{100*(c/p-1):+.0f}%"
T={}
for p,n in NAMES.items():
    T[n]=dict(us_dl=win(ser(us,p,'downloads'),A1,B1), us_dl0=win(ser(us,p,'downloads'),A0,B0),
              us_rev=win(ser(us,p,'revenue'),A1,B1), us_rev0=win(ser(us,p,'revenue'),A0,B0),
              ww_dl=win(ser(ww,p,'downloads'),A1,B1), ww_dl0=win(ser(ww,p,'downloads'),A0,B0),
              ww_rev=win(ser(ww,p,'revenue'),A1,B1), ww_rev0=win(ser(ww,p,'revenue'),A0,B0),
              rt=win(ser(rat,p,'new_total'),A1,B1), rt0=win(ser(rat,p,'new_total'),A0,B0))
    T[n]['ppd']=T[n]['us_rev']/T[n]['us_dl']
m,c=T['MyFitnessPal'],T['Cal AI']
last=max(dl_us[0][1]); 
def M(v): return f"${v/1e6:.0f}M"
def K(v): return f"{v/1e6:.2f}M" if v>=1e6 else f"{v/1e3:.0f}K"
tbl=f'''<table class="cmp"><thead><tr><th></th><th>MyFitnessPal</th><th>Cal AI</th></tr></thead><tbody>
<tr><td>US downloads</td><td>{K(m['us_dl'])} <small>{pct(m['us_dl'],m['us_dl0'])}</small></td><td class="w">{K(c['us_dl'])} <small>{pct(c['us_dl'],c['us_dl0'])}</small></td></tr>
<tr><td>US net revenue</td><td class="w">{M(m['us_rev'])} <small>{pct(m['us_rev'],m['us_rev0'])}</small></td><td>{M(c['us_rev'])} <small>{pct(c['us_rev'],c['us_rev0'])}</small></td></tr>
<tr><td>Worldwide downloads</td><td class="w">{K(m['ww_dl'])} <small>{pct(m['ww_dl'],m['ww_dl0'])}</small></td><td>{K(c['ww_dl'])} <small>{pct(c['ww_dl'],c['ww_dl0'])}</small></td></tr>
<tr><td>Worldwide net revenue</td><td class="w">{M(m['ww_rev'])} <small>{pct(m['ww_rev'],m['ww_rev0'])}</small></td><td>{M(c['ww_rev'])} <small>{pct(c['ww_rev'],c['ww_rev0'])}</small></td></tr>
<tr><td>Revenue per US download</td><td class="w">${m['ppd']:.2f}</td><td>${c['ppd']:.2f}</td></tr>
<tr><td>New App Store ratings</td><td class="w">{K(m['rt'])} <small>{pct(m['rt'],m['rt0'])}</small></td><td>{K(c['rt'])} <small>{pct(c['rt'],c['rt0'])}</small></td></tr>
</tbody></table>'''
# markets, Oct25-Sep26 vs prior (from the Oct 26 pull)
import csv
rows=list(csv.DictReader(open(f'{D}/mfp_calai_countries.csv')))
mk=['US','GB','CA','AU','DE','FR','ES']; mn={'US':'US','GB':'UK','CA':'Canada','AU':'Australia','DE':'Germany','FR':'France','ES':'Spain'}
g={}
for r in rows:
    if r['country'] in mk: g[(r['app'],r['country'])]=100*(int(r['downloads_oct25_sep26'])/int(r['downloads_oct24_sep25'])-1)
mt='<table class="cmp"><thead><tr><th>Downloads, Oct 2025 to Sep 2026 vs the year before</th><th>MyFitnessPal</th><th>Cal AI</th></tr></thead><tbody>'
for cc in mk:
    a,b=g[('MyFitnessPal',cc)],g[('Cal AI',cc)]
    mt+=f'<tr><td>{mn[cc]}</td><td class="{"neg" if a<0 else "pos"}">{a:+.0f}%</td><td class="{"neg" if b<0 else "pos"}">{b:+.0f}%</td></tr>'
mt+='</tbody></table>'
# rest of category, US iPhone last 30 days as of Oct 26 (Keyword Inspector)
cat=[('MyFitnessPal',None,round(m['us_rev']/12/1e3),'owned by Francisco Partners; bought Cal AI? no, separate'),]
cat=[('MacroFactor',58,1300,'macro coach, adaptive targets'),('Cronometer',158,764,'micronutrients, the nerd favorite'),('MyNetDiary',84,697,'old-guard logger'),('Lose It!',66,633,'old-guard logger, 2008'),('Numify',51,347,'AI photo logging'),('Calo',59,264,'AI photo logging'),('Foodvisor',45,237,'AI photo logging, French'),('BitePal',23,86,'AI photo logging')]
mx=max(r[2] for r in cat)
rows_html=''.join(f'<div class="row" title="{n}: ${r:,}K net revenue, US iPhone, 30 days, {d}K downloads. {t}"><div class="lbl">{n}<small>{d}K dl</small></div><div class="track"><i style="width:{100*r/mx:.1f}%"></i></div><div class="val">{"$%.1fM"%(r/1000) if r>=1000 else "$%dK"%r}</div></div>' for n,d,r,t in cat)
ref=f'<div class="row ref" title="For scale: Cal AI, monthly average over the last 12 months (tracked, not from the keyword sweep)"><div class="lbl">Cal AI, 12-mo avg<small>{int(c["us_dl"]/12/1e3)}K dl</small></div><div class="track"><i style="width:100%"></i></div><div class="val">${c["us_rev"]/12/1e6:.1f}M</div></div>'
extra2='''<style>
table.cmp { width: 100%; border-collapse: collapse; margin-top: 12px; font-size: 14px; background: var(--surface); border: 1px solid var(--line); }
table.cmp th, table.cmp td { padding: 8px 12px; text-align: left; border-bottom: 1px solid var(--line); }
table.cmp th { font-family: var(--mono); font-size: 11px; letter-spacing: 0.05em; text-transform: uppercase; color: var(--muted); font-weight: 500; }
table.cmp td:not(:first-child) { font-family: var(--mono); font-size: 13px; font-variant-numeric: tabular-nums; }
table.cmp td.w { font-weight: 700; }
table.cmp td small { color: var(--muted); font-size: 11px; margin-left: 4px; }
table.cmp td.neg { color: #b4452e; } table.cmp td.pos { color: #2f7a4f; }
</style>'''
head=head.replace('</style>','</style>'+extra2,1)
lastm='Oct 2026'
SUB_WW="After Apple's cut. MFP is a $10M-to-$18M-a-month business on the phone; Cal AI peaked at $4.2M in January 2026."
SUB_US="About three quarters of both apps' revenue is American."
body=f'''<div class="wrap">
{NAV}
<header>
  <div class="eyebrow">Idea 3 on the board · Health copilot · Appfigures competitor tracking, pulled Oct 26 and refreshed Nov 11</div>
  <h1>Calorie apps: MyFitnessPal vs Cal AI</h1>
  <p class="lede">The incumbent and the AI-photo newcomer, 24 months of modeled iPhone downloads, revenue and ratings, plus the rest of the category from a keyword sweep. The question for the health copilot: is a new entrant winning here, and what does it earn when it does?</p>
</header>

<section>
  <h2>Last 12 months, Nov 2025 to Oct 2026, against the year before</h2>
  {tbl}
  <div class="read">
    <div class="hot"><b>The crossover already happened</b>Cal AI has out-downloaded MyFitnessPal in the US every month since October 2025. In {lastm} it was {K(dl_us[1][1]['2026-10'])} to {K(dl_us[0][1]['2026-10'])}.</div>
    <div class="hot"><b>MFP still makes about {m['ww_rev']/c['ww_rev']:.0f}x the money</b>It earns ${m['ppd']:.0f} per US download against Cal AI's ${c['ppd']:.0f}. MFP's downloads fell {pct(m['ww_dl'],m['ww_dl0'])[1:]} worldwide while revenue fell only {pct(m['ww_rev'],m['ww_rev0'])[1:]}: it is squeezing more out of the base it has.</div>
    <div><b>Cal AI's growth is slowing</b>US downloads were +43% a year ago on the Oct 26 pull. On the refreshed window they are {pct(c['us_dl'],c['us_dl0'])}, and every month since January 2026 has been below the one before. The January spike was its best month ever and it has not held any of it.</div>
  </div>
</section>

<section>
  <h2>Month by month</h2>
  {linechart('US iPhone downloads per month','Appfigures estimates, Oct 2024 to Oct 2026. January is New Year resolutions for both.',dl_us)}
  {linechart('Worldwide iPhone net revenue per month',SUB_WW,rev_ww,money=True)}
  {linechart('US iPhone net revenue per month',SUB_US,rev_us,money=True)}
  {linechart('New App Store ratings per month','A usage proxy independent of the download model. MFP spiked to 97K in January 2026 and is rising again this fall; Cal AI has fallen from 37K a month in October 2025 to 8K.',rt)}
</section>

<section>
  <h2>Where the growth is</h2>
  {mt}
  <div class="read">
    <div class="hot"><b>English-speaking only</b>Cal AI grew in the US, UK, Canada and Australia and shrank in Germany, France and Spain. MFP shrank everywhere. The AI-photo pitch has not travelled outside English yet.</div>
    <div><b>US share</b>73% of Cal AI's revenue and 72% of MFP's comes from the US. Whoever builds here is building for Americans first.</div>
  </div>
</section>

<section>
  <h2>The rest of the category</h2>
  <div class="chart"><h3>Calorie and macro loggers, US iPhone, 30 days to Oct 26 <span style="font-family:var(--mono);font-size:12px;color:var(--muted);font-weight:400">· net revenue</span></h3><p class="sub">From Keyword Inspector searches on "calorie counter", "macro tracker" and "food scanner". Only the top ten results per search carry estimates.</p><div class="rows">{ref}{rows_html}</div><p class="none"><b>Read.</b> MacroFactor has the best revenue per download after MFP: 58K downloads to $1.3M. The AI-photo clones (Numify, Calo, Foodvisor, BitePal) together make less than a quarter of Cal AI, which makes Cal AI the category's one breakout rather than the front of a wave. Cronometer gets the most downloads of the group and converts worst.</p></div>
  <div class="read">
    <div><b>Who buys ads</b>On "calorie counter", MFP had 43% of Apple Ads impressions, Lose It 27%, Cal AI 15%, and Cal AI had been absent for about a month at the time of the pull. On "cal ai", a look-alike called Calor AI had taken 20% of the impressions on Cal AI's own name.</div>
    <div><b>What this says for idea 3</b>A newcomer can take the download lead in this category in a year, and the money is real: Cal AI cleared {M(c['ww_rev'])} on iOS in twelve months. But its growth has turned over, the photo-logging clones behind it are tiny, and MFP's revenue barely moved. The open ground is not another logger; it is the thing that sits on top of one, which is the health copilot pitch, and the reason the board scores its market 5 and its edge 2.</div>
  </div>
  <div class="read">
    <div><b>Scope</b>iPhone, App Store only. Android and web are not here. Cal AI is owned by Viral Development, not MFP; MFP belongs to Francisco Partners.</div>
    <div><b>Method</b>MFP and Cal AI are two of the plan's five tracked competitors, so their monthly history comes through the API at no credit cost (three requests tonight). Country splits are from the Oct 26 pull and run Oct 2025 to Sep 2026. The category sweep is from the Keyword Inspector on Oct 26. Raw data in <code>~/Projects/appfigures-calorie</code>.</div>
  </div>
</section>

{bands_html('calories.html')}
<div class="foot">Built Oct 26, refreshed Nov 11, 2026 for the Davenport session. <a href="./">Back to the board.</a></div>
</div>
</body>
</html>
'''
open('calories.html','w').write(head+body)
print('ok', {k:(round(v) if isinstance(v,float) else v) for k,v in m.items()}, {k:(round(v) if isinstance(v,float) else v) for k,v in c.items()})
print('ratings last', rt[0][1]['2026-10'], rt[1][1]['2026-10'], 'first', rt[0][1]['2024-10'], rt[1][1]['2024-10'])
print('US dl 2026', {k:v for k,v in dl_us[1][1].items() if k>='2026-01'})
