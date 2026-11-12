"""Revenue potential by market penetration, 1% / 10% / 50%, for the Appfigures-backed ideas.
Two framings per idea: share of a measured or sourced revenue pool, and share of the Maxinomics audience buying at a price."""
AUD=850_000
BANDS=[0.01,0.10,0.50]
def m(v):
    if v>=1e9: return f"${v/1e9:.1f}B"
    if v>=1e6: return f"${v/1e6:.1f}M" if v<10e6 else f"${v/1e6:.0f}M"
    if v>=1e3: return f"${v/1e3:.0f}K"
    return f"${v:,.0f}"
def n(v): return f"{v/1e6:.2f}M" if v>=1e6 else (f"{v/1e3:.0f}K" if v>=1000 else str(int(v)))
IDEAS={
 'buzz.html': dict(
   title='Buzz, or a product on top of it',
   pools=[('Slack revenue, about $3B (Benioff, Salesforce FY26 call; not a reported line item)',3.0e9),('Discord revenue, about $560M (third-party 2025 estimate; others say up to $950M)',5.6e8),('Team collaboration software category, $21.5B (IMARC, 2025; other firms say up to $40B)',2.15e10)],
   price=120, price_note='$10 per seat per month, Slack Pro is about $8.75, Discord Nitro $9.99',
   read='The honest pool for Buzz is none of these: agent-native team chat is a category with no revenue yet. Slack is the comparable because it is the product a Buzz customer would stop paying for. One percent of Slack is a $30M company. The audience framing is weaker here than anywhere else on the board: 850K people who watch explainer videos are not 850K teams, so the realistic buyer count is a few thousand small teams and the people running agents at home.'),
 'calories.html': dict(
   title='Health copilot (idea 3), measured against the calorie apps',
   pools=[('MyFitnessPal + Cal AI, worldwide iOS net revenue, last 12 months, measured',1.78e8),('MyFitnessPal + Cal AI, US iPhone only, measured',1.29e8),('Nutrition apps category, $4.8B (from the Oct 24 market map on the card; analyst figure, scope varies)',4.8e9)],
   price=60, price_note='$60 a year; Cal AI sells at about $30 to $60, MyFitnessPal Premium at $80',
   read='Cal AI took 28% of the measured two-app pool in two years from a standing start, so 10% is not a fantasy band in this category; it is roughly what a newcomer with a real hook and paid acquisition has done. The audience framing is strong: the people who watch Maxinomics are the people who track things, and 1% of them at $60 is a half-million-dollar business on its own.'),
 'glp1.html': dict(
   title='GLP-1 / peptide tracker (idea 7)',
   pools=[('MeAgain + Shotsy, US iPhone net revenue, annualized from the 30-day estimate, measured',6.8e6),('Whole tracker category incl. peptides and the long tail, US iPhone, estimated',8.0e6),('Same, worldwide, applying the 1.4x worldwide-to-US ratio seen on the calorie apps',1.1e7)],
   price=50, price_note='$50 a year; MeAgain and Shotsy earn about $7 to $14 per download',
   read='This is the smallest pool on the board. Fifty percent of the entire US iPhone tracker category is a $4M business, and the leader already has it. The only band that pays here is the audience one, and only if the product is the food-plus-labs layer the card describes rather than another log: 1% of the audience at $50 is more than Shotsy makes today.'),
 'bloodwork.html': dict(
   title='Buy into something like Rythm (idea 8)',
   pools=[('Function Health, about $100M to $130M a year (Sacra run-rate Feb 2025; third-party)',1.15e8),('US direct-to-consumer lab testing, about $2B (Meticulous Research 2025 base, derived from its 2032 projection)',2.0e9),('Global direct-to-consumer lab testing, $3.8B (Towards Healthcare, 2025)',3.78e9)],
   price=948, price_note='$79 a month, Rythm\'s price; Function is $365 to $499 a year',
   read='Read these as revenue generated for the partner, not for the group; what the group gets is the equity or affiliate share it negotiates. That is the point: 1% of the audience on a $79-a-month panel is an $8M-a-year customer base, which is about 7% of Function\'s whole business and more than any single marketing channel a company that size has. That is the number to put in front of Rythm or Superpower.'),
 'learnai.html': dict(
   title='Nora, learn AI by doing (idea 6)',
   pools=[('Learn-AI apps on the App Store: no measurable pool. Not one of 74 apps clears the download model',0),('Coursera, all subjects, US iPhone net revenue, annualized, measured, for scale',4.7e6),('Executive and professional AI training is sold off-store (Maven cohorts $500 to $2,000, Section, corporate L&D); no reliable public size',0)],
   price=300, price_note='$300 one-time; creator courses sell at $200 to $500, cohort courses at $500 to $2,000',
   read='There is no App Store pool to take a share of, which is why the audience framing is the whole model here. At creator-course conversion rates (1% to 3% of an engaged audience buy), Nora is a $2.5M to $7.5M product if it is sold to the Maxinomics audience directly, and the 10% band is the ceiling a well-run cohort business reaches over several years, not a launch number.'),
}
def bands_html(fn):
    d=IDEAS.get(fn)
    if not d: return ''
    rows=''
    for lbl,pool in d['pools']:
        if pool: rows+=f'<tr><td>{lbl}</td>'+''.join(f'<td>{m(pool*b)}</td>' for b in BANDS)+'</tr>'
        else: rows+=f'<tr><td>{lbl}</td><td colspan="3" style="color:var(--muted)">no pool to size</td></tr>'
    p=d['price']
    arow='<tr><td><b>Maxinomics audience, 850K subscribers</b>, buying at '+d['price_note']+'</td>'+''.join(f'<td><b>{m(AUD*b*p)}</b><br><small>{n(AUD*b)} buyers</small></td>' for b in BANDS)+'</tr>'
    return f'''
<section>
  <h2>Revenue potential by penetration: 1%, 10%, 50%</h2>
  <p class="lede" style="color:var(--muted);max-width:72ch;margin-top:0">{d['title']}. Annual revenue at each penetration band, against the pools that can be sized and against the audience. Gross revenue, not profit, and the 50% band is there for scale, not as a plan.</p>
  <div class="tablewrap2"><table class="cmp"><thead><tr><th>Pool</th><th>1%</th><th>10%</th><th>50%</th></tr></thead><tbody>{rows}{arow}</tbody></table></div>
  <div class="read">
    <div class="hot"><b>Read</b>{d['read']}</div>
    <div><b>How to read the bands</b>Creator-sold products convert 1% to 3% of an engaged audience, so the 1% row is the realistic case, 10% is a multi-year ceiling, and 50% is the size of the whole audience spending, which no product reaches. Category pools are third-party estimates whose definitions vary; the measured rows are Appfigures iOS net revenue and understate anything sold on the web.</div>
  </div>
</section>'''
