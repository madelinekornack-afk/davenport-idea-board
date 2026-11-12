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
# ---- the full field, Nov 11 sweep ----
CF=json.load(open('/Users/madelinekornack/Projects/appfigures-calorie/../appfigures-ideas/calorie_ratings_monthly_us.json')); CFM=CF['months']; CFA=CF['apps']
def fs(pid): return {mm:v for mm,v in zip(CFM,CFA[pid]['new']) if mm<='2026-10' and v>=0}
field=[(a['name'],a['dl30'] or 0,a['rev30'] or 0,a['release'][:4]) for pid,a in CFA.items() if a['rev30'] and pid not in ('280009581858',)]
field.sort(key=lambda r:-r[2])
mx=field[0][2]
rows_html=''.join(f'<div class="row" title="{n}: ${r:,.0f} net revenue, US iPhone, 30 days to Nov 11, {d:,} downloads, app since {y}"><div class="lbl">{n}<small>{y}{(", "+str(round(d/1000))+"K dl") if d else ""}</small></div><div class="track"><i style="width:{100*r/mx:.1f}%"></i></div><div class="val">{"$%.1fM"%(r/1e6) if r>=1e6 else "$%dK"%(r/1e3)}</div></div>' for n,d,r,y in field)
ref=''
field_total=sum(r for _,_,r,_ in field)
def chg(pid):
    n=CFA[pid]['new']; a=sum(n[0:3])/3; b=sum(n[21:24])/3; return a,b,((b/a-1) if a>0 else None)
order=['6013158','337323818982','334409656467','265024508487','5849975','5861283','5969522','11908476640','337202977153','336637125505','42112725269','280330041588','337433311120','6456187','5849513','40913192180','6037940']
trs=''
for pid in order:
    a,b,p=chg(pid); nm=CFA[pid]['name']; y=CFA[pid]['release'][:4]
    cls='pos' if (p is not None and p>0.15) else ('neg' if (p is not None and p<-0.15) else '')
    trs+=f'<tr><td>{nm}</td><td>{y}</td><td>{a:,.0f}</td><td>{b:,.0f}</td><td class="{cls}">{("%+.0f%%"%(p*100)) if p is not None else "from zero"}</td></tr>'
field_tbl='<div class="tablewrap2"><table class="cmp"><thead><tr><th>App</th><th>Since</th><th>New ratings / mo, Nov 24 to Jan 25</th><th>Aug to Oct 2026</th><th>Change</th></tr></thead><tbody>'+trs+'</tbody></table></div>'
field_lines1=linechart('New App Store ratings per month: the old guard','MyFitnessPal, Lose It!, MyNetDiary and Cronometer. January is the resolution spike for all of them.',[('MyFitnessPal',fs('6013158')),('Lose It!',fs('5861283')),('MyNetDiary',fs('5849975')),('Cronometer',fs('265024508487'))])
field_lines2=linechart('New App Store ratings per month: the AI-photo newcomers','Cal AI against the three clones behind it. Cal AI is down 73% from its January 2026 peak; Calo is the only one still rising.',[('Cal AI',fs('337323818982')),('Numify',fs('337202977153')),('BitePal',fs('337433311120')),('Calo',fs('336637125505'))])
extra2='''<style>
table.cmp { width: 100%; border-collapse: collapse; margin-top: 12px; font-size: 14px; background: var(--surface); border: 1px solid var(--line); }
table.cmp th, table.cmp td { padding: 8px 12px; text-align: left; border-bottom: 1px solid var(--line); }
table.cmp th { font-family: var(--mono); font-size: 11px; letter-spacing: 0.05em; text-transform: uppercase; color: var(--muted); font-weight: 500; }
table.cmp td:not(:first-child) { font-family: var(--mono); font-size: 13px; font-variant-numeric: tabular-nums; }
table.cmp td.w { font-weight: 700; }
table.cmp td small { color: var(--muted); font-size: 11px; margin-left: 4px; }
table.cmp td.neg { color: #b4452e; } table.cmp td.pos { color: #2f7a4f; font-weight: 700; }
.tablewrap2 { overflow-x: auto; }
</style>'''
head=head.replace('</style>','</style>'+extra2,1)
lastm='Oct 2026'
SUB_WW="After Apple's cut. MFP is a $10M-to-$18M-a-month business on the phone; Cal AI peaked at $4.2M in January 2026."
SUB_US="About three quarters of both apps' revenue is American."
body=f'''<div class="wrap">
{NAV}
<header>
  <div class="eyebrow">Ideas 3 and 4 on the board · a better Cal AI, and the health copilot on top of it · Appfigures competitor tracking, pulled Oct 26 and refreshed Nov 11</div>
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
  <div class="chart"><h3>Every calorie and diet app that makes money on US iPhone, 30 days to Nov 11 <span style="font-family:var(--mono);font-size:12px;color:var(--muted);font-weight:400">· net revenue, field total {fmt(field_total,True)}</span></h3><p class="sub">Keyword Inspector searches by name for Noom, WeightWatchers, Lifesum, Yazio, fatsecret, Lose It, Cronometer, MacroFactor and Carb Manager, plus "calorie counter", "macro tracker" and "food scanner". Yuka (a label scanner, $512K) is left out.</p><div class="rows">{rows_html}</div><p class="none"><b>Read.</b> MyFitnessPal is half the field on its own and nothing sits between it and Cal AI. WeightWatchers makes $605K a month from 1,270 downloads: a legacy subscriber base, not a growing app. Noom, Lifesum, Yazio and fatsecret, the names people assume are big, are small on US iPhone. MacroFactor earns more per download than anyone. The AI-photo clones together make about 60% of Cal AI.</p></div>
  {field_tbl}
  {field_lines1}
  {field_lines2}
  <div class="read">
    <div class="hot"><b>Cal AI is not the front of a wave</b>Its new ratings are down 73% from January 2026 (23K a month to 5.9K in October). Numify and BitePal each spiked past 5,000 a month in early 2026 and have faded by two thirds. Calo is the only AI-photo app still growing, from 53 a month to about 2,000.</div>
    <div><b>The old guard is holding</b>MyNetDiary has doubled its ratings pace in two years, Cronometer and Noom are flat, Lose It! is up on a March 2026 spike. WeightWatchers and Lifesum are the ones fading. Nobody in the field is going away; the newcomers are not taking the incumbents' users, they are adding and then churning their own.</div>
  </div>
  <div class="read">
    <div><b>Who buys ads</b>On "calorie counter", MFP had 43% of Apple Ads impressions, Lose It 27%, Cal AI 15%, and Cal AI had been absent for about a month at the time of the pull. On "cal ai", a look-alike called Calor AI had taken 20% of the impressions on Cal AI's own name.</div>
    <div><b>What this says for idea 4</b>A newcomer can take the download lead in this category in a year, and the money is real: Cal AI cleared {M(c['ww_rev'])} on iOS in twelve months. But its growth has turned over, the photo-logging clones behind it are tiny, and MFP's revenue barely moved. The open ground is not another logger; it is the thing that sits on top of one, which is the health copilot pitch, and the reason the board scores its market 5 and its edge 2.</div>
  </div>
  <div class="read">
    <div><b>Scope</b>iPhone, App Store only. Android and web are not here. Cal AI is owned by Viral Development, not MFP; MFP belongs to Francisco Partners.</div>
    <div><b>Method</b>MFP and Cal AI are two of the plan's five tracked competitors, so their monthly history comes through the API at no credit cost. Country splits are from the Oct 26 pull and run Oct 2025 to Sep 2026. The field chart, table and ratings lines are from a Keyword Inspector sweep by app name on Nov 11 plus one ratings call for 20 apps. Raw data in <code>~/Projects/appfigures-calorie</code> and <code>~/Projects/appfigures-ideas/calorie_*</code>.</div>
  </div>
</section>

{bands_html('calories.html')}
<div class="foot">Built Oct 26, refreshed Nov 11 with the full field, 2026 for the Davenport session. <a href="./">Back to the board.</a></div>
</div>
</body>
</html>
'''
open('calories.html','w').write(head+body)
print('ok', {k:(round(v) if isinstance(v,float) else v) for k,v in m.items()}, {k:(round(v) if isinstance(v,float) else v) for k,v in c.items()})
print('ratings last', rt[0][1]['2026-10'], rt[1][1]['2026-10'], 'first', rt[0][1]['2024-10'], rt[1][1]['2024-10'])
print('US dl 2026', {k:v for k,v in dl_us[1][1].items() if k>='2026-01'})
