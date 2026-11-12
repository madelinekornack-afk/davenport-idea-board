import json, re, os
from bands import bands_html
B='/Users/madelinekornack/Projects/appfigures-clark/buzz'
clark=open('clark.html').read()
head=clark.split('<div class="wrap">')[0].replace('<title>Clark</title>','<title>Buzz</title>')
NAV='<nav class="tabs"><a href="./">Board</a><a href="clark.html">Clark</a><a href="audit.html">Audit</a><a href="formcheck.html">Form check</a><a class="on" href="buzz.html">Buzz</a><a href="calories.html">Calorie apps</a><a href="bloodwork.html">Bloodwork</a><a href="glp1.html">GLP-1</a><a href="learnai.html">Learn AI</a></nav>'
extra='''
<style>
.line { background: var(--surface); border: 1px solid var(--line); padding: 16px 18px 10px; margin-top: 14px; }
.line h3 { font-size: 19px; }
.line .sub { color: var(--muted); font-size: 13px; margin: 2px 0 8px; }
.line svg { display: block; width: 100%; height: auto; font-family: var(--body); }
.line .ax { stroke: var(--line); stroke-width: 1; }
.line .tk { fill: var(--muted); font-size: 11px; font-family: var(--mono); }
.line .lg { display: flex; gap: 14px; flex-wrap: wrap; font-size: 12.5px; color: var(--muted); margin-top: 6px; }
.line .lg i { display: inline-block; width: 14px; height: 3px; vertical-align: middle; margin-right: 6px; border-radius: 2px; }
.line .pt { fill: var(--surface); stroke-width: 2; }
.line .pt:hover { r: 5; }
.s1 { color: #2a78d6 } .s2 { color: #d9641e } .s3 { color: #2f7a4f } .s4 { color: #7a4fb0 }
.stat { display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 12px; margin-top: 14px; }
.stat div { background: var(--surface); border: 1px solid var(--line); padding: 12px 14px; }
.stat b { display: block; font-family: var(--display); font-size: 26px; font-weight: 700; line-height: 1.1; }
.stat span { font-family: var(--mono); font-size: 11px; letter-spacing: 0.04em; text-transform: uppercase; color: var(--muted); }
</style>
'''
head=head.replace('</style>','</style>'+extra,1)
head=head.replace('</style>','</style>'+'''<style>
table.cmp { width: 100%; border-collapse: collapse; margin-top: 12px; font-size: 13.5px; background: var(--surface); border: 1px solid var(--line); }
table.cmp th, table.cmp td { padding: 7px 10px; text-align: left; border-bottom: 1px solid var(--line); vertical-align: top; }
table.cmp th { font-family: var(--mono); font-size: 11px; letter-spacing: 0.05em; text-transform: uppercase; color: var(--muted); font-weight: 500; }
table.cmp td:nth-child(n+3) { font-family: var(--mono); font-size: 12.5px; font-variant-numeric: tabular-nums; white-space: nowrap; }
table.cmp td.neg { color: #b4452e; } table.cmp td.pos { color: #2f7a4f; font-weight: 700; }
.tablewrap2 { overflow-x: auto; }
</style>''',1)
COL=['#2a78d6','#d9641e','#2f7a4f','#7a4fb0']
def fmt(v,money=False):
    if money: return f"${v/1e6:.1f}M" if v>=1e6 else (f"${v/1e3:.0f}K" if v>=1000 else f"${v:,.0f}")
    return f"{v/1e6:.2f}M" if v>=1e6 else (f"{v/1e3:.0f}K" if v>=1000 else str(int(v)))
def linechart(title, sub, series, money=False, note=''):
    # series: list of (name, {month: value})
    months=sorted({m for _,d in series for m in d})
    W,H,L,R,T,Bm=960,300,56,16,16,36
    allv=[v for _,d in series for v in d.values() if v is not None]
    mx=max(allv) if allv else 1
    def x(i): return L+(W-L-R)*i/max(1,len(months)-1)
    def y(v): return T+(H-T-Bm)*(1-v/mx)
    s=[f'<svg viewBox="0 0 {W} {H}" role="img" aria-label="{title}">']
    for k in range(5):
        v=mx*k/4; yy=y(v); s.append(f'<line class="ax" x1="{L}" y1="{yy:.1f}" x2="{W-R}" y2="{yy:.1f}"/><text class="tk" x="{L-6}" y="{yy+4:.1f}" text-anchor="end">{fmt(v,money)}</text>')
    for i,m in enumerate(months):
        if m.endswith('-01') or m.endswith('-07') or i==0: s.append(f'<text class="tk" x="{x(i):.1f}" y="{H-12}" text-anchor="middle">{m}</text>')
    for si,(name,d) in enumerate(series):
        c=COL[si%4]; pts=[(x(i),y(d[m])) for i,m in enumerate(months) if d.get(m) is not None]
        if not pts: continue
        s.append(f'<path d="M'+' L'.join(f'{px:.1f} {py:.1f}' for px,py in pts)+f'" fill="none" stroke="{c}" stroke-width="2" stroke-linejoin="round"/>')
        for i,m in enumerate(months):
            if d.get(m) is None: continue
            s.append(f'<circle class="pt" cx="{x(i):.1f}" cy="{y(d[m]):.1f}" r="3.5" stroke="{c}"><title>{name}, {m}: {fmt(d[m],money)}</title></circle>')
        lx,ly=pts[-1]; s.append(f'<text x="{min(lx+6,W-4):.1f}" y="{ly+4:.1f}" font-size="12" fill="{c}" text-anchor="{"end" if lx>W-80 else "start"}" dy="{-10 if si%2 else 12}">{name}</text>')
    s.append('</svg>')
    lg=''.join(f'<span><i style="background:{COL[i%4]}"></i>{n}</span>' for i,(n,_) in enumerate(series))
    return f'<div class="line"><h3>{title}</h3><p class="sub">{sub}</p>{"".join(s)}<div class="lg">{lg}</div>{("<p class=none>"+note+"</p>") if note else ""}</div>'

repo=json.load(open(f'{B}/repo.json')); rel=json.load(open(f'{B}/release_downloads_by_month.json')); con=json.load(open(f'{B}/contributors.json'))
names={'4696409368':'Slack','267680453599':'Microsoft Teams','41279274901':'Discord'}
us=json.load(open(f'{B}/est_chat_US.json')); ww=json.load(open(f'{B}/est_chat_WW.json'))
def ser(d,pid,key): return {k[:7]:(int(v[key]) if key=='downloads' else float(v[key])) for k,v in d[pid].items() if not k.startswith('2026-11')}
dl_us=[(names[p],ser(us,p,'downloads')) for p in names]
rev_us=[(names[p],ser(us,p,'revenue')) for p in names if any(float(v['revenue'])>0 for v in us[p].values())]
dl_ww=[(names[p],ser(ww,p,'downloads')) for p in names]
buzz_dl=[('Buzz desktop, GitHub release downloads',{k:v for k,v in rel.items()})]
# extra sections appended from hist if present
hist_path=f'{B}/hist_monthly.json'
hist=json.load(open(hist_path)) if os.path.exists(hist_path) else None
hist_html=''
if hist:
    rat=hist.get('ratings',{}); nm=hist.get('names',{})
    def rs(pid): return {m:v for m,v in rat.get(pid,{}).items() if not m.startswith('2026-11')}
    giants=[(nm.get(p,p),rs(p)) for p in ['4696409368','267680453599','41279274901','280670085405'] if rat.get(p)]
    if giants: hist_html+=linechart('New App Store ratings per month: the giants','A second usage proxy, independent of the download model. People rate apps they keep using.',giants)
    rk=hist.get('ranks',{})
    def rk_s(pid,key): return {m:v for m,v in rk.get(pid,{}).get(key,{}).items()}
    sl=[(nm.get(p,p),rk_s(p,'overall_free')) for p in ['4696409368','267680453599','41279274901'] if rk_s(p,'overall_free')]
    if sl: hist_html+=linechart('Overall US iPhone Top Free rank, monthly average (lower is better)','Where each sits in the whole store, not just its category.',sl,note='Rank axis is inverted in meaning: a rising line means falling in the charts.')


# ---- what is going up instead (chat / AI / community sweep, Nov 11 late) ----
CH=json.load(open('/Users/madelinekornack/Projects/appfigures-ideas/chat_ratings_monthly_us.json')); CM=CH['months']; CA=CH['apps']
def cs(pid): return {m:v for m,v in zip(CM,CA[pid]['new']) if m<='2026-10' and v>=0}
def chg(pid):
    n=CA[pid]['new']; a=sum(n[0:3])/3; b=sum(n[21:24])/3
    return a,b,(b/a-1) if a>0 else None
def cfmt(v): return f"{v/1e6:.2f}M" if v>=1e6 else (f"{v/1e3:.1f}K" if v>=1000 else f"{v:.0f}")
order=['336744124021','337819614201','337924427373','337365095251','338665378456','336597891347','336758442084','5893317','31932595429','40188328711','6756611','280670085405','212786893','263458146435','4696409368','267680453599','41279274901','9334987','336594876475','124714775577','336853432807','5980590','6603280','212710021']
trs=[]
for pid in order:
    a,b,p=chg(pid); nm=CA[pid]['name']; g=CA[pid]['group']
    if pid=='338665378456': cell='launched Sep 2026: 111K, then 300K'
    elif p is None: cell='from zero'
    else: cell=f'{p*100:+.0f}%'
    cls='pos' if (p is not None and p>0.15) else ('neg' if (p is not None and p<-0.15) else '')
    trs.append(f'<tr><td>{nm}</td><td>{g}</td><td>{cfmt(a)}</td><td>{cfmt(b)}</td><td class="{cls}">{cell}</td></tr>')
replace_tbl='<div class="tablewrap2"><table class="cmp"><thead><tr><th>App</th><th>Group</th><th>New ratings / mo, Nov 24 to Jan 25</th><th>Aug to Oct 2026</th><th>Change</th></tr></thead><tbody>'+''.join(trs)+'</tbody></table></div>'
replace_html=f"""
<section>
  <h2>If Discord is going down, what is going up?</h2>
  <p class="lede" style="color:var(--muted);max-width:72ch;margin-top:0">Same measure for 30 apps: new US App Store ratings per month, Nov 2024 to Oct 2026, from a keyword sweep of messengers, AI assistants, streaming and community apps on Nov 11. Ratings are the usage proxy the download model cannot hide, and on this measure Discord has not moved at all.</p>
  {linechart('AI assistants: new ratings per month','ChatGPT went from 100K a month to 1M. Gemini and Grok from near zero to 100K+. Muse from Meta launched in September and did 300K in its second month.',[('ChatGPT',cs('336744124021')),('Google Gemini',cs('337819614201')),('Grok',cs('337924427373')),('Muse from Meta',cs('338665378456'))])}
  {linechart('Chat with people: new ratings per month','WhatsApp flat, Signal flat, Telegram flat, Messenger down by two thirds.',[('WhatsApp',cs('5893317')),('Messenger (Meta)',cs('6756611')),('Signal',cs('40188328711')),('Telegram',cs('31932595429'))])}
  {linechart('Where Discord lives: community and streaming','Discord is flat at about 27K a month for two years. Twitch and Reddit are drifting down. Kick, the Twitch rival, went from nothing to 5K a month in November 2025 and held.',[('Discord',cs('41279274901')),('Twitch',cs('9334987')),('Reddit',cs('124714775577')),('Kick',cs('336594876475'))])}
  {replace_tbl}
  <div class="read">
    <div class="hot"><b>Nothing in chat is replacing Discord</b>Every messenger is flat or down. WhatsApp, Signal and Telegram have the same rating velocity they had two years ago; Messenger has lost two thirds; Google Chat half; GroupMe and Google Meet are at zero. Discord itself is flat on ratings, which means its 40% download drop is mostly the install model and the gaming cycle, not people leaving.</div>
    <div class="hot"><b>What went up is talking to models</b>ChatGPT's new ratings went from 100K a month to 1M. Gemini 5x. Grok from zero to 100K. Claude from 2K to 36K at the March 2026 peak. Muse from Meta is the biggest launch in the sweep, 2.7M US installs in 30 days. Across the same two years that is the only category on the phone that grew by an order of magnitude.</div>
    <div><b>The one human-chat exception is streaming</b>Kick went from 80 ratings a month to 5,600 when it started paying streamers in late 2025, and is now at 530K US installs a month to Twitch's 320K. That is share moving inside a category, which is what Buzz would have to do in team chat.</div>
    <div><b>What this says for Buzz</b>Attention did not move to a better chat app. It moved to a chat window with an agent on the other side. Buzz is the one product in this group that puts agents and people in the same channels, so the growth story is not "beat Slack," it is "be where the two kinds of chat meet." That is also the strongest argument on this board for building on it.</div>
  </div>
  <div class="read">
    <div><b>Caveats</b>Ratings count people who rate, so a prompt change moves the line (Slack's jump in Aug 2025, Labcorp's in May 2026 on the Bloodwork tab). The AI apps' curves are so steep that no prompt change explains them. Messenger's decline could partly be Meta moving ratings prompts to Instagram.</div>
    <div><b>Method</b>Keyword Inspector searches for whatsapp, telegram, signal, messenger, chatgpt, claude, gemini, character ai, twitch, kick, reddit, discord, group chat, community, zoom, threads, steam, voice chat; then one ratings call for 30 apps, Nov 2024 to Nov 2026, US. Raw data in <code>~/Projects/appfigures-ideas/chat_*</code>.</div>
  </div>
</section>
"""

body=f'''<div class="wrap">
{NAV}
<header>
  <div class="eyebrow">Idea 8 on the board · Maddy, Nov 11 · Block's open-source project · the group runs 63 agents on it</div>
  <h1>Buzz</h1>
  <p class="lede">Buzz is Block's open-source team chat for people and AI agents, built on Nostr: a relay, a desktop app and a CLI. Created on GitHub in March 2026, first release in May. The group runs its own relay with 63 agents across 181 channels and has written its own fixes for the gaps. The question on this tab: is anyone else using it, and are the chat giants losing anything to it?</p>
</header>

<section>
  <h2>Is anyone using Buzz?</h2>
  <div class="stat">
    <div><b>{repo["stargazers_count"]:,}</b><span>GitHub stars</span></div>
    <div><b>{repo["forks_count"]:,}</b><span>forks</span></div>
    <div><b>{len(con)}</b><span>contributors</span></div>
    <div><b>125</b><span>releases since May 3</span></div>
    <div><b>{sum(rel.values())/1e6:.2f}M</b><span>desktop downloads, all releases</span></div>
    <div><b>{repo["open_issues_count"]:,}</b><span>open issues</span></div>
  </div>
  {linechart('Buzz desktop downloads by month','GitHub release asset downloads, every platform. Includes auto-updates, so each month is new installs plus existing users updating.',buzz_dl,note='Peak was June, the first full month after launch. October is a sixth of that. With updates counted, a falling line means fewer people updating, which is the closest thing to a user count GitHub gives.')}
  <div class="read">
    <div class="hot"><b>Read</b>The star count says developers noticed; the download curve says they are not staying. 468K downloads in June to 74K in October, with releases still shipping weekly. Buzz is not on any app store, so Appfigures has nothing on it; this is the whole public signal.</div>
    <div><b>What the group adds</b>Everything on the Buzz card: the mention bridge, the roster, channel staffing, the busy-agent rule. Those are the fixes a daily user needs and a 129-contributor project has not shipped.</div>
  </div>
</section>

<section>
  <h2>Are the giants slipping?</h2>
  <p class="lede" style="color:var(--muted);max-width:72ch;margin-top:0">Slack, Teams and Discord, 24 months of modeled iPhone downloads and net revenue, from Appfigures competitor tracking pulled tonight. Caveat up front: Slack and Teams seats are bought by IT departments on the web, so phone installs are a usage proxy, not a sales number.</p>
  {linechart('US iPhone downloads per month','Slack and Teams are free apps bought elsewhere; Discord sells Nitro in-app.',dl_us)}
  {linechart('Worldwide iPhone downloads per month','Same three, all countries.',dl_ww)}
  {linechart('US iPhone net revenue per month','Only Discord monetizes on the phone. Teams started charging in-app this year.',rev_us,money=True)}
  {hist_html}
  <div class="read">
    <div class="hot"><b>Slack is flat, not falling</b>About 200K US installs a month for two years, 440K to 630K worldwide, with September 2026 among the highest months in the series. No sign of mobile erosion.</div>
    <div class="hot"><b>Teams is flat with a spring spike</b>Around 1M US a month, spiking to 2.2M in May 2025. Nothing in 2026 reads as decline.</div>
    <div><b>Discord: fewer installs, more money</b>US downloads are down about 40% from the July 2025 peak, while in-app revenue doubled to $8.3M a month. It is monetizing an installed base, not growing one.</div>
    <div><b>What this says for Buzz</b>Nothing has moved. Buzz's own download curve is falling faster than any giant's. If share moves, it will be in a new category, agent-native team chat, where none of the three giants compete today, and where the group's daily use is the edge.</div>
  </div>
  <div class="read">
    <div><b>Scope</b>iPhone only. Android, desktop and web, where most Slack and Teams usage lives, are not here.</div>
    <div><b>Method</b>Slack, Teams and Discord added as tracked competitors tonight with the plan's free slots, then pulled through the API: monthly, US and worldwide, Nov 2024 to Oct 2026. GitHub data from the public API. No credits used. Raw data in <code>~/Projects/appfigures-clark/buzz</code>.</div>
  </div>
</section>

{replace_html}
{bands_html('buzz.html')}
<div class="foot">Built Nov 11, 2026 for the Davenport session. <a href="./">Back to the board.</a></div>
</div>
</body>
</html>
'''
open('buzz.html','w').write(head+body)
print('buzz.html written', 'with hist' if hist else 'without hist')
