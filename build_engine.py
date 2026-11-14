#!/usr/bin/env python3
"""The engine tab: the explainer for the project the group ended up on at the Nov 11 Davenport session.
Source: the Minutes AI notes and the full transcript of the session. Writes engine.html.
Reuses the Clark tab's page shell (styles, diagram, caps, read grid) so it matches the rest of the board."""
import re
clark=open('clark.html').read()
head=clark.split('<div class="wrap">')[0].replace('<title>Clark</title>','<title>The engine</title>')
head=head.replace('</style>','''</style>
<style>
.big { font-size: 17px; max-width: 72ch; margin: 14px 0 0; }
.big b { font-weight: 600; }
.steps { counter-reset: s; display: grid; gap: 10px; margin-top: 14px; }
.step { background: var(--surface); border: 1px solid var(--line); padding: 14px 16px 14px 58px; position: relative; font-size: 14px; }
.step::before { counter-increment: s; content: counter(s); position: absolute; left: 16px; top: 10px; font-family: var(--display); font-size: 30px; font-weight: 700; color: var(--accent); }
.step b { display: block; font-family: var(--display); font-size: 18px; font-weight: 700; margin-bottom: 2px; }
.step .when { font-family: var(--mono); font-size: 11px; letter-spacing: 0.04em; text-transform: uppercase; color: var(--muted); margin-left: 8px; }
table.plan { min-width: 0; }
table.plan td { font-size: 14px; }
table.plan td:first-child { font-weight: 600; }
table.plan td.who, table.plan td.when { font-family: var(--mono); font-size: 12.5px; color: var(--muted); }
table.plan td.when { white-space: nowrap; }
.q { background: var(--surface); border: 1px solid var(--line); border-left: 3px solid var(--accent); padding: 12px 14px; font-size: 14px; }
.q b { display: block; font-weight: 600; margin-bottom: 2px; }
.links a { margin-right: 14px; }
.cap .st.plan { color: var(--muted); }
.roles { display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 12px; margin-top: 14px; }
.roles div { background: var(--surface); border: 1px solid var(--line); padding: 14px 16px; font-size: 14px; }
.roles b { display: block; font-family: var(--display); font-size: 20px; font-weight: 700; margin-bottom: 6px; }
.roles ul { margin: 0; padding-left: 18px; }
.roles li { margin: 3px 0; }
table.plan td.num { text-align: right; font-family: var(--mono); font-size: 12.5px; white-space: nowrap; }
.caps.two { grid-template-columns: repeat(auto-fit, minmax(380px, 1fr)); }
@media (max-width: 560px) { .caps.two { grid-template-columns: 1fr; } }
</style>''',1)
TABS=[('engine.html','The engine'),('./','Board'),('clark.html','Clark'),('audit.html','Audit'),('formcheck.html','Form check'),('buzz.html','Buzz'),('calories.html','Calorie apps'),('bloodwork.html','Bloodwork'),('glp1.html','GLP-1'),('learnai.html','Learn AI')]
NAV='<nav class="tabs">'+''.join(f'<a{" class=on" if h=="engine.html" else ""} href="{h}">{t}</a>' for h,t in TABS)+'</nav>'

def box(x,y,w,h,t,m,cls='box'):
    return f'<rect class="{cls}" x="{x}" y="{y}" width="{w}" height="{h}" rx="6"/><text class="t" x="{x+12}" y="{y+19}" text-anchor="start">{t}</text><text class="m" x="{x+12}" y="{y+36}" text-anchor="start">{m}</text>'
def arrow(x1,y1,x2,y2,later=False):
    return f'<path class="arrow{" later" if later else ""}" d="M{x1} {y1} L{x2} {y2}"/>'

d=['<svg viewBox="0 0 1040 470" role="img" aria-label="The engine: sources flow into Clark and Tally, which clean and link everything at write time into one stack per customer; products sit on top">',
'<defs><marker id="ah" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0 L10 5 L0 10 z" fill="var(--muted)"/></marker></defs>',
'<text class="h" x="20" y="24" text-anchor="start">1 · What comes in</text>',
'<text class="h" x="300" y="24" text-anchor="start">2 · The engine, at write time</text>',
'<text class="h" x="760" y="24" text-anchor="start">3 · Products on top</text>',
box(20,40,230,46,'Email','Gmail, by Google sign-in'),
box(20,100,230,46,'Transactions','Plaid webhooks, every bank and card'),
box(20,160,230,46,'Files','local embedding model on the Mac; next'),
box(20,220,230,46,'Property data','Orca: work orders, vendors, tenants'),
box(20,280,230,46,'Statements and K-1s','brokerages, 401(k), the tax pile; later'),
'<rect class="core" x="300" y="40" width="420" height="370" rx="8"/>',
box(316,56,388,46,'Clark: email','vectorized plus keyword search; spots receipts','box'),
box(316,116,388,46,'Tally: money','stage 1 names the merchant, stage 2 types the money','box'),
box(316,176,388,46,'Link','receipt to transaction, person to thread, invoice to job','box'),
box(316,236,388,46,'Normalize and classify once','47 economic types, cleaned aliases, confidence scores','box'),
box(316,296,388,46,'One index per customer','its own AWS stack; nobody shares a table','box'),
'<text class="m" x="316" y="372" text-anchor="start">Node and Python on AWS. Cleaned on arrival, so every later question is fast and cheap.</text>',
'<text class="m" x="316" y="390" text-anchor="start">Open by API, CLI and MCP. No lock-in to one chat app.</text>',
box(760,40,260,54,'Orca statement reconciliation','first; Jason at WSPM is the guinea pig','box'),
box(760,108,260,54,'The executive record','$1,000 a month; 100 customers is $1.2M','box'),
box(760,176,260,54,'Tax season, pre-assembled','the pain that started it; a December question','box'),
box(760,244,260,54,'Your own agent','Claude Code, Cowork, a terminal','box'),
box(760,312,260,54,'The Mac app, on its own','email and money in one window; Nov 12','box'),
arrow(250,63,300,63),arrow(250,123,300,123),arrow(250,183,300,183,True),arrow(250,243,300,243),arrow(250,303,300,303,True),
arrow(720,110,760,67),arrow(720,160,760,135),arrow(720,210,760,203,True),arrow(720,260,760,271),arrow(720,300,760,339,True),
'<text class="m" x="20" y="445" text-anchor="start">Dashed: not built or not decided yet. Solid: running for Phil today, multi-tenant in progress.</text>',
'</svg>']
DIAGRAM=''.join(d)

body=f'''<div class="wrap">
{NAV}
<header>
  <div class="eyebrow">The project, on one page · decided at the Nov 11 Davenport session, updated from Buzz and the group text through Nov 12 · ideas 1, 2 and 7 on the board</div>
  <h1>The engine</h1>
  <p class="lede">Clark and Tally together: one place where your email, your money and your files are cleaned, classified and linked the moment they arrive, so anything asked later is instant. It is not sold on its own. Products sit on top of it, and the first one is for Orca. This page is the whole project: what it is, what already runs, what has to be built and by whom, what it costs and earns, who else is in the field, and what is still undecided.</p>
  <p class="quote"><b>Phil, Nov 11:</b> "That is what every single business is. It is trying to make someone's high entropy environment that's a pain in the ass to work in into lower entropy. And then you sell that order to the customer."</p>
</header>

<section>
  <h2>In plain words</h2>
  <p class="big">Every business you have ever paid sells order. A car is 30,000 parts sold as one thing. A property manager sells a calm month to an owner who would otherwise be chasing invoices. <b>The engine is the machine that makes order out of a person's or a company's mess</b>, and the mess today is email, bank transactions and files. Phil has been building it for himself under two names: <b>Clark</b> for email and <b>Tally</b> for money. On Nov 11 the three of you agreed that the engine is the thing worth building, that it is never the product, and that the products stack on top of it in a set order.</p>
  <div class="read">
    <div><b>Why it feels different from Claude on its own</b>Most agents work at read time. You ask, and the model searches, scrapes and reads raw text for minutes. The engine works at write time. Every email and transaction is cleaned, named, typed and linked when it lands, so a question is a lookup, not an expedition. Steve's own version: "You have to solve the data layer before you can do the harness really well."</div>
    <div><b>Why it is not a feature Google or Anthropic ships tomorrow</b>Phil looked: Google does not vector-index free Gmail because the compute costs more than the account earns. A chat app would have to pull in all of your mail, money and files and store them. The engine does exactly that, for a price, on infrastructure that belongs to one customer.</div>
    <div class="hot"><b>Why not the health app</b>Phil: "We all agree that a health app is out." Steve has Mercury for salary and Orca for the long game; a third context is impossible. Anything new must feed Orca, "two birds, one stone." The engine does: the first product is for Steve's customers.</div>
  </div>
</section>

<section>
  <h2>How it fits together</h2>
  <div class="diagram">{DIAGRAM}</div>
</section>

<section>
  <h2>What exists today</h2>
  <p class="lede" style="color:var(--muted);max-width:72ch;margin-top:0">Running on Phil's own stack unless marked. The <a href="clark.html">Clark</a> and <a href="audit.html">Audit</a> tabs have the long versions.</p>
  <div class="caps">
    <div class="cap"><span class="st live">Built, in use</span><b>Email, searchable</b>Vectorized search over the whole inbox plus keyword index. "Find the other emails where they talk about the same thing."</div>
    <div class="cap"><span class="st live">Built, in use</span><b>Transactions, normalized</b>Every charge resolved to the real merchant and typed as one of 47 kinds of money. 94 to 95 percent at Phil's.</div>
    <div class="cap"><span class="st live">Built, in use</span><b>Receipts matched to charges</b>Emails feed the transaction pipeline as evidence, which is how Amazon and PayPal line items get itemized. Since Nov 12, every transaction email pins itself to its transaction.</div>
    <div class="cap"><span class="st live">Built, in use</span><b>Files, classified</b>Statements, K-1s and brokerage PDFs sorted and linked to the transactions and emails they belong to.</div>
    <div class="cap"><span class="st live">Built, in use</span><b>Browser history, searchable</b>Every page opened, in the same index, searchable by what it was about. Maddy's test case: Sarah and Dan's wedding website.</div>
    <div class="cap"><span class="st live">Built, in use</span><b>One sign-in, open to any agent</b>Email, Plaid and files connected once. Reachable from a terminal, Claude Code, Cowork or any agent over MCP. No assistant laid on top.</div>
    <div class="cap"><span class="st live">Built, in use</span><b>One stack per customer</b>A CloudFormation template spins up isolated infrastructure per customer. Built for one customer so far: Phil.</div>
    <div class="cap"><span class="st live">Built, Nov 12</span><b>The Mac app</b>Email and transactions in one native window, with each purchase's paperwork attached. Phil's own copy; not yet shared.</div>
    <div class="cap"><span class="st live">Proof</span><b>Taxes in 90 minutes, FSA claims</b>Phil filed with a K-1, wash sales and a closed Fidelity rollover; the system found the IRA distribution in email from an account closed the year before. Maddy's own version found every FSA-eligible expense across transactions and email and filed the claims.</div>
    <div class="cap"><span class="st live">Built, in use (Orca)</span><b>The verified maintenance record</b>Orca holds work orders, vendor invoices, dispatch and technician location for Jason's and Kyle's shops. Kyle queries it from Claude Code; Jason runs his day through Cowork connected to Orca, AppFolio and his email.</div>
    <div class="cap"><span class="st next">Design concept</span><b>The statement audit</b>Steve's owner-side design: read any PM statement, know the contract, check every charge, catch paying twice, build the dispute pack. Exists as a concept, not iterated; flipped to the manager's side on Nov 11.</div>
    <div class="cap"><span class="st next">In progress</span><b>Multi-tenant</b>Built for one email address and one person. Builds for the multi-account version were running on Nov 11.</div>
  </div>
</section>

<section>
  <h2>The two halves, as Phil described them</h2>
  <div class="caps two">
    <div class="cap"><span class="st live">Running</span><b>Tally: money</b>Plaid pushes each bank and card transaction into a pipeline the moment it posts. <b>Stage 1</b> cleans the name. A fast model reasons over the cryptic descriptor and gives a confidence score. Low confidence sends a second model to the web, with account numbers and names stripped first, to find out that "paddle viewstax" is a software vendor. The result is saved as a machine-cleaned alias, and nobody is asked to confirm it. Amazon direct and Amazon Marketplace come out as different vendors. <b>Stage 2</b> says what kind of money it is: a merchant purchase, Maddy sending Phil money, a card payoff, a transfer between accounts, a brokerage deposit or withdrawal. 47 economic types, none of which Plaid supplies. Phil hand-labelled 450 of his own transactions to tune it. Accuracy is 94 to 95 percent.</div>
    <div class="cap"><span class="st live">Running</span><b>Clark: email</b>Every message is ingested, vectorized and stored next to a keyword index, so search is meaning plus exact terms, not Gmail's Boolean operators. "Morning Brew contract" finds the 2023 thread with Devin Emery about pay, before any contract existed, even though the word contract is not in it. Clark also watches for receipts and passes candidates to Tally, which attaches the receipt to the exact transaction.</div>
    <div class="cap"><span class="st next">Next</span><b>Files, then the rest</b>A lightweight embedding model runs on the Mac or PC and indexes the local disk, which Spotlight cannot do inside PDFs and decks. After that, Slack and browser history. Health and wearables are a later layer, not a product.</div>
    <div class="cap"><span class="st live">Running</span><b>One stack per customer</b>Email and transactions are the most private data a person has, so no customer shares a database. A CloudFormation template spins up a full isolated stack for each one; a prompt injection against SQL cannot reach anyone else's table. The team can still sign in through SSO to run it. Phil's own stack costs about $350 a month unoptimized, which is the number the $1,000 price has to clear.</div>
  </div>
</section>

<section>
  <h2>Since the session: Nov 12</h2>
  <div class="read">
    <div><b>Phil: the Mac app</b>Email and transactions are now one native Mac app. The email side hands transaction emails to Tally as they arrive, and Tally pins each to its transaction: order confirmed, subscription notice, return. Every purchase keeps its own paperwork. "The GUI part will be useful even by itself and I'm pretty excited to have it ready for me personally, so that's usually a good sign." Steve: "sort of sounds like that alone could almost be a product?" Phil: "very well might be." It is drawn as a fourth product above, dashed, until the group decides.</div>
    <div><b>Steve, the morning after</b>"Confident in the direction and wanna dig in asap." His reason for raising PropFlow on the night: they and many others take shortcuts for a flashy product and lean on Claude with a thin harness, which is likely the root cause of their problems. Orca gives their product a better foundation; "so would the Max pipeline." And: "while you don't own the source data with the Max pipeline, you do own the way it's stored and indexed, which is prob the next best thing."</div>
    <div class="hot"><b>Steve's build-or-buy challenge</b>Managed memory services sell this layer with nothing to run; he found mem0. He runs Orca on Supabase and writes no CRUD endpoints. So is starting with infrastructure and figuring out the product the right order? Usually the product comes first and build-versus-buy falls out of it. His proposed test: pick one AI feature for Orca, build it on a managed service, build it again on Clark when it is ready, and compare. Carried to December below, and on the build list.</div>
    <div><b>Phil: urgency</b>"With the urgency of onboarding you guys, I'm moving much harder to get it fully up for multiple users." Builds for multi-tenant were already running on the night.</div>
  </div>
</section>

<section>
  <h2>The products, in the order you agreed</h2>
  <div class="steps">
    <div class="step"><b>Statement reconciliation for property managers, on Orca <span class="when">first</span></b>The scenario Phil walked through: an owner's bill is $10,000 above a normal month and the manager has to explain why. Today that is a scramble across vendor threads, invoices and tenant tickets. With work orders in Orca and email and payments in the engine, the explanation assembles itself: the furnace was serviced four times before it was fixed, here are the four invoices, here is the thread. Same machine for 50-owner month ends. The checks, from Steve's design: each line against the contract (a 10 percent markup billed at 15, a coordination fee that is not in the agreement, a repair above the approval limit), vendor invoice against what the owner was charged, the same repair on the same unit months apart, and this month against every prior statement. What the owner gets: per-property spend all time, a maintenance history that does not vanish when they switch managers, and the explanation with the evidence attached. Sold through the manager as a PM-branded portal, which is what landlords on BiggerPockets actually asked for and what avoids selling against Orca's own customers. Jason at WSPM is the guinea pig; Kyle at Green Street already queries Orca from Claude Code. ProFlow, the "AI property manager" Jason pays $1,200 a month, turned out to be a voice harness that had to build on Orca's webhooks to do anything about maintenance. This is board idea 2 and the <a href="audit.html">Audit</a> tab.</div>
    <div class="step"><b>The executive system of record <span class="when">second</span></b>White glove, $1,000 a month, for the operators Maxinomics already reaches: people with several entities, real estate, deal flow, eight financial institutions and no order in any of it. Phil's number: 100 customers is $1.2M a year, with no funding. Steve's reaction to the price was the customer's: "Shut up and take my money." The pitch is privacy and portability. It is on your own infrastructure, we cannot see it, and you can take the data anywhere. This is board idea 1 and the <a href="clark.html">Clark</a> tab.</div>
    <div class="step"><b>Tax season, pre-assembled <span class="when">third</span></b>The pain that started all of it. Phil spent an evening finding a five-year-old Fidelity 401(k) withdrawal to offset an IRS letter. Steve spent two and a half hours with Claude driving a browser through Schwab and old returns, stuck on login screens. A $1,500 CPA still makes you collect the documents. With a year of transactions and statements already typed and linked, the return is itemized before filing season opens. Board idea 7. Open question for December: a feature of the record, or the hook that sells it.</div>
  </div>
</section>

<section>
  <h2>Who does what</h2>
  <div class="roles">
    <div><b>Phil</b><ul><li>Builds and runs the engine: Clark, Tally, the per-customer stack, the Mac app.</li><li>Multi-tenant and multi-lane ingestion inside two weeks, then the web onboarding page.</li><li>Hands Steve the repos once multi-tenant passes.</li><li>Owns the executive-record and tax layers; brings the audience that buys them.</li></ul></div>
    <div><b>Steve</b><ul><li>Owns Orca and the two live property-management customers.</li><li>Brings Jason's WSPM data as the first test and decides how finished the engine must be before Jason touches it.</li><li>Designs the reconciliation product on Orca (the audit design concept is his).</li><li>Runs the build-or-buy test: one Orca feature on a managed service, then on Clark.</li><li>Keeps the SEO loop running for Orca demos.</li></ul></div>
    <div><b>Maddy</b><ul><li>Second user of the engine in December, on her own mail and money, after building her own version for FSA claims.</li><li>Keeps this board and the record: the Nov 11 transcript, the Buzz channel Phil asked everyone to keep the conversation in.</li><li>Market and competitor research: Appfigures, the research tabs, the comparables.</li><li>Distribution: the 850K Maxinomics audience is where the executive-record and tax buyers are.</li></ul></div>
  </div>
</section>

<section>
  <h2>The money</h2>
  <div class="tablewrap"><table class="plan">
    <thead><tr><th>Layer</th><th>Buyer</th><th class="num">Price</th><th class="num">1% of the audience</th><th>What that number rests on</th></tr></thead>
    <tbody>
      <tr><td>Orca statement reconciliation</td><td class="who">property managers, via Orca</td><td class="num">$240 / owner / yr</td><td class="num">$2.0M</td><td>Board idea 2. Owner-side landlord software earns nothing on the App Store; the money is on the PM side (Buildium, AppFolio, DoorLoop, Yardi), which is the side Orca already sells to.</td></tr>
      <tr><td>The executive record</td><td class="who">executives, family offices</td><td class="num">$1,000 / mo</td><td class="num">$102M (scale only)</td><td>Board idea 1. Phil's real target is 100 customers, $1.2M a year, no funding. Steve's reaction was the customer's: "Shut up and take my money."</td></tr>
      <tr><td>Tax season, pre-assembled</td><td class="who">anyone with a K-1 or a brokerage account</td><td class="num">$300 / yr</td><td class="num">$2.5M</td><td>Board idea 7. A CPA is $800 to $3,000; TurboTax is a weekend. Seasonal unless it is the moment that sells the record.</td></tr>
      <tr><td>The Mac app, if it is a product</td><td class="who">consumers</td><td class="num">$100 to 200 / yr</td><td class="num">not scored</td><td>The five Plaid budgeting apps clear $3.8M a month on US iPhone alone (Rocket Money $1.2M). None uses email as evidence. Receipt matching on its own earns $32K a month; the data layer on its own earns nothing.</td></tr>
      <tr><td>Cost to run</td><td class="who">per customer stack</td><td class="num">$350 / mo</td><td class="num"></td><td>Phil's own stack, unoptimized. The $1,000 price clears it; the $240 and $300 layers only work on shared or much cheaper infrastructure, which is a December question.</td></tr>
    </tbody>
  </table></div>
  <p style="color:var(--muted);font-size:13px;max-width:72ch">1 percent of the audience is the board's standard column: 850K subscribers, 1 percent buying, times the price. It sizes the channel, not the forecast. The executive-record cell is scale only, since nobody expects 8,500 executives at $12,000 a year.</p>
</section>

<section>
  <h2>Who else is building it</h2>
  <p class="lede" style="color:var(--muted);max-width:72ch;margin-top:0">What came up in the room, plus the competitor map Fable built in Buzz the same night from Steve's handoff, with each claim checked against press coverage rather than filings.</p>
  <div class="tablewrap"><table class="plan">
    <thead><tr><th>Group</th><th>Who</th><th>What the sources support</th></tr></thead>
    <tbody>
      <tr><td>Platforms</td><td class="who">Microsoft Work IQ; OpenAI company knowledge</td><td>Work IQ sits on Microsoft Graph (people, documents, activity, relationships); agent APIs GA June 2026, a read-only memory profile for agents over MCP due December 2026. OpenAI's company knowledge retrieves at question time with citations, the design the engine replaces.</td></tr>
      <tr><td>Enterprise context</td><td class="who">Glean; Jedify</td><td>Glean maps people, content and activity, with 100-seat minimums. Jedify raised $24M in June 2026 to arm agents with business context.</td></tr>
      <tr><td>Learned memory</td><td class="who">Engram</td><td>Trains a model on an organization's information, so the knowledge lives in weights, not a store. $98M at launch, Microsoft, Notion and Harvey as partners. The opposite design: no evidence row to cite.</td></tr>
      <tr><td>Personal assistants</td><td class="who">Instinct</td><td>$250M at $2.5B in August 2026, then $1B at $10B in September. One profile says still pre-revenue. One teardown says it keeps markdown in git. Steve: "basically what's on our chalkboard" was Supermemory, not this.</td></tr>
      <tr><td>Relationship CRMs</td><td class="who">Affinity</td><td>Builds people and company records from email and calendar as its core product. The handoff missed this group.</td></tr>
      <tr><td>Finance</td><td class="who">Digits; Ramp; Brex</td><td>Digits attaches emailed receipts to transactions and learns vendors, and says month one needs heavy review. Ramp matches above 90 percent and fails on same vendor, same amount, adjacent days. The receipt half of Tally exists for small businesses.</td></tr>
      <tr><td>Developer memory</td><td class="who">Supermemory; Hyperspell; mem0</td><td>Seed-stage, sold to developers, billed by the token. mem0 is the one Steve raised on Nov 12 as the buy option.</td></tr>
    </tbody>
  </table></div>
  <div class="read">
    <div class="hot"><b>The gap, as Fable put it</b>Every component exists as a product, but each incumbent owns one source and wants to be the hub. Nobody joins bank transactions, email and product data into one link table with a reason and a confidence on every row, for a company too small for Glean and not on Microsoft. The defensible piece is not the entity table (Affinity builds that from a mailbox, Microsoft Graph ships with 365). It is the link between money and mail with evidence on each row, for a business on Google Workspace plus a bank feed, which neither Microsoft's December release nor Digits reaches today.</div>
    <div><b>The platform risk, still open</b>Steve's standing worry is that Anthropic ships the feature. The answer on the night was the architecture: write-time processing on one isolated stack per customer is not what a chat app ships, and the first customers are property managers who will never sign up for Instinct. Two moves to watch: Microsoft's agent memory profile in December, and Digits' email intake for companies that move their books there.</div>
    <div><b>A second opinion, from Claude itself</b>Steve asked Fable whether the design was sound. It said the warehouse is "buildable with standard parts" and that no product gives it ready made, that it mostly helps questions about clients, operations and money rather than code, and it pulled four recent failures from its own lessons file that an index would have prevented: a misidentified site visitor, a wrong client price, a missed Green Street purchase, a question already answered in an unread email.</div>
  </div>
</section>

<section>
  <h2>What has to be built, in order</h2>
  <div class="tablewrap"><table class="plan">
    <thead><tr><th>Step</th><th>Who</th><th>Status</th><th>What it unlocks</th></tr></thead>
    <tbody>
      <tr><td>Multi-tenant on AWS</td><td class="who">Phil</td><td class="when">in progress, builds running Nov 11</td><td>More than one email address and one person on the pipeline. Everything below waits on it.</td></tr>
      <tr><td>Multi-lane email ingestion</td><td class="who">Phil</td><td class="when">inside two weeks, by about Nov 25</td><td>Thousands of messages a day in parallel. Two to three days of agent builds plus QA.</td></tr>
      <tr><td>Web onboarding page</td><td class="who">Phil</td><td class="when">after the two above</td><td>Google sign-in and Plaid on one screen, so Maddy and Steve connect in 15 to 20 minutes without the CLI.</td></tr>
      <tr><td>Repos to Steve</td><td class="who">Phil</td><td class="when">once multi-tenant passes</td><td>Steve reads the code, not just the product.</td></tr>
      <tr><td>Maddy and Steve on their own stacks</td><td class="who">all three</td><td class="when">first two weeks of December, in person</td><td>The engine tested on three people's real mail and money before Phil and Maddy leave around Dec 20.</td></tr>
      <tr><td>Orca data into the engine</td><td class="who">Steve, Phil</td><td class="when">not started</td><td>Work orders, vendor invoices and tenant mail indexed next to the bank feed. Jason's WSPM data is the first load. Steve is still deciding how finished it must be before Jason sees it.</td></tr>
      <tr><td>The reconciliation product on Orca</td><td class="who">Steve</td><td class="when">not started; design concept exists</td><td>The checks above, run every month, with the owner explanation assembled. The first thing anyone sells on the engine.</td></tr>
      <tr><td>Build-or-buy test</td><td class="who">Steve</td><td class="when">proposed Nov 12</td><td>One Orca AI feature on a managed memory service, then on Clark. Settles whether the engine has to be built in-house.</td></tr>
      <tr><td>Files and the event graph</td><td class="who">Phil</td><td class="when">next, after multi-tenant</td><td>Local files indexed by an on-device embedding model; who said what, when, which decision replaced which, for the revenue-share statement case.</td></tr>
      <tr><td>The executive record as a service</td><td class="who">Phil, Maddy</td><td class="when">after December</td><td>White-glove onboarding, the three demo questions (a contract renegotiation brief, tax documents assembled, last week's expenses submitted), a price page. Buyers come from the channel.</td></tr>
      <tr><td>Tax season, pre-assembled</td><td class="who">Phil</td><td class="when">December decision</td><td>A feature of the record or the hook that sells it. Either way it needs a year of typed transactions and matched documents, which the engine is already collecting.</td></tr>
      <tr><td>The Mac app, decided</td><td class="who">all three</td><td class="when">December decision</td><td>Phil's own tool today. Whether it ships as a consumer product next to the executive record.</td></tr>
    </tbody>
  </table></div>
</section>

<section>
  <h2>Carried to December</h2>
  <div class="caps">
    <div class="q"><b>Build or buy (Steve, Nov 12)</b>One Orca AI feature built on a managed memory service, then again on Clark, side by side. Fable's framing of the same question: count a week of questions the agent gets wrong because of identity or link errors first. If the count is small, the store does not earn its upkeep.</div>
    <div class="q"><b>Margin per customer</b>$350 a month to run Phil's stack against a $1,000 price, before optimization. Digital Ocean or a leaner template could change the number.</div>
    <div class="q"><b>Accounting depth</b>Tally types the economics, not the ledger. Mercury spent six months and an acquisition on categorization against 300-ledger charts of accounts. Owner statements may need the ledger.</div>
    <div class="q"><b>How finished before Jason</b>Steve's call. A guinea pig who hits a rough edge is still a customer who hit a rough edge.</div>
    <div class="q"><b>Tax: feature or hook</b>Phil's instinct is that tax is the pain everyone recognizes. Whether it is the first thing a customer hears about or the third is undecided.</div>
    <div class="q"><b>Things mentioned, not scored</b>Per-project token tracking (Phil burned a weekly ChatGPT allocation in two days), the Sentry to Buzz auto-fix loop, PostHog session replays feeding a morning review, and sensors as the system of record for physical things. See the <a href="./">board</a> footer.</div>
  </div>
</section>

<div class="foot">Written Nov 12, 2026 from the Nov 11 Davenport session transcript, updated Nov 14 from Buzz #product-ideas and the group text through Nov 12. Speaker A is Steve, B is Phil, C is Maddy. <span class="links"><a href="./">Board</a> <a href="clark.html">Clark</a> <a href="audit.html">Audit</a></span></div>
</div>
</body>
</html>
'''
open('engine.html','w').write(head+body)
print('engine.html', len(head+body))
