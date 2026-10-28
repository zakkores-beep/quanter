/* Independent check of verbal.js.  node verify-verbal.js [tests]   (MUTATE=1 flips answers to prove the checks bite)
   For every statement it re-derives the answer from the world facts and the rendered tab text (never from the
   generator's label), checks every "Cannot say" detail is absent from all six tabs, checks that the facts a
   True/False answer relies on are really printed in the tabs, and checks the test mix. */
"use strict";
const V = require("./verbal.js");
const N = +process.argv[2] || 20000;
const WORDS = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten", "eleven", "twelve"];

function allText(tabs) { return Object.values(tabs).flat().map(p => p.h + ". " + p.t).join("\n"); }
function tabText(tabs, key) { return tabs[key].map(p => p.h + ". " + p.t).join("\n"); }
const person = (W, name) => W.board.find(p => p.name === name);

// The truth for a path, read from the world and confirmed against the printed text. undefined = the tabs do not say.
function truth(W, tabs, path) {
  const [k, x] = path, T = allText(tabs);
  switch (k) {
    case "divRole": { const d = W.divs.find(v => v.code === x); return d && d.role; }
    case "withdraw": return /will not withdraw from this sector/.test(T) ? "no" : undefined;
    case "umbrellaOverlap": return /Some members of the umbrella organisation are simultaneously members/.test(T) ? "some" : undefined;
    case "contact": return x === W.divs[1].code && /Every client has their own contact person/.test(T) ? "yes" : undefined;
    case "chair": return W.board[0].name;
    case "prevRole": { const p = person(W, x); return p.career === "A" || p.career === "B" ? p.prevRole : undefined; }
    case "prevCity": return person(W, x).city;
    case "freesFor": return W.sale.freesFor;
    case "saleCountry": return W.sale.country;
    case "replaced": return /Some of these services were replaced by online banking/.test(T) ? "some" : undefined;
    case "acqNat": return W.acq.nat;
    case "acqName": return W.acq.name;
    case "duty": return W.duties[x];
    case "informs": return /inform the Supervisory Board about the situation of the group on a regular basis/.test(T) ? "regularly" : undefined;
    case "strategyApproval": return /major decisions relating to the company's strategy are brought before the Supervisory Board in order to be approved/.test(T) ? "Supervisory Board" : undefined;
    case "period": return W.period;
    case "bcWho": return /supports self-employed people and family businesses/.test(T) ? "self-employed people and family businesses" : undefined;
    case "experts": return /optionally accompany repositioning efforts/.test(T) ? "optionally" : undefined;
    case "projectsInclude": return /All products and services are designed either for regional or national projects/.test(T) ? ["regional", "national"] : undefined;
    case "hedge": return /offer the chance of high returns/.test(T) ? "chance" : undefined;
    case "amSegment": return W.amCountries.includes(x) ? "big corporations" : undefined;
    case "realEstateIn": {
      if (W.foRegions.includes(x) && /In countries where it offers options, .* also offers real estate funds/.test(T)) return "yes";
      if ((T.match(/real estate funds?/g) || []).length > 1 || regionMentioned(tabs, x)) return "AMBIGUOUS";   // only the options rule may mention them
      return undefined;
    }
    case "converseRule": return undefined;
    case "hq": return W.hq;
    case "divClients": return W.divs.find(v => v.code === x).clients;
    case "returns": return W.returns;
    case "costs": return W.costs;
    case "rights": return W.rights;
    case "invOthers": return W.invOthers;
    case "boardYears": return person(W, x).boardYears;
    case "dirMinusBoard": { const p = person(W, x); return p.dirYears - p.boardYears; }
    default: throw new Error("unknown path " + k);
  }
}
const num = (W, tabs, v) => (Array.isArray(v) ? truth(W, tabs, v) : v);

// Independent country -> region map: a "new" region in a Cannot-say statement must not contain any country the tabs name.
const COUNTRY_REGION = { Japan: "Asia", Singapore: "Asia", India: "Asia", "Hong Kong": "Asia", Brazil: "South America", Mexico: "South America", Argentina: "South America", Chile: "South America", Peru: "South America", "South Africa": "Africa" };
function regionMentioned(tabs, region) { const T = allText(tabs); return Object.entries(COUNTRY_REGION).some(([c, r]) => r === region && T.includes(c)); }
function evalAtom(W, tabs, a, text, errs) {
  const T = allText(tabs).toLowerCase();
  if (a.k === "novel") { if (T.includes(a.say.toLowerCase())) errs.push(`"${a.say}" is in the tabs, so it is not Cannot say`);
    if (regionMentioned(tabs, a.say)) errs.push(`a country in ${a.say} is named in the tabs`); if (!text.toLowerCase().includes(a.say.toLowerCase())) errs.push("novel detail not in statement"); return "C"; }
  if (a.k === "cmp") {
    const l = num(W, tabs, a.l), r = num(W, tabs, a.r);
    if (typeof l !== "number" || typeof r !== "number") return "C";
    for (const v of [a.l, a.r]) if (Array.isArray(v) && !text.includes(v[1])) errs.push("person missing: " + v[1]);
    if (!Array.isArray(a.r) && !text.includes(" " + WORDS[a.r] + " year")) errs.push("number not in statement");
    if (a.l[0] === "boardYears" && !tabText(tabs, "board").includes(WORDS[l] + " years")) errs.push("board years not printed");
    return { "==": l === r, ">": l > r, "<": l < r }[a.op] ? "T" : "F";
  }
  const tv = truth(W, tabs, a.path);
  if (tv === undefined) return "C";
  if (tv === "AMBIGUOUS") { errs.push("ambiguous: another tab may imply the answer"); return "C"; }
  if (a.k === "has") { if (!T.includes(String(a.say).toLowerCase()) && tv.includes(a.say)) errs.push("listed item not printed"); return tv.includes(a.say) ? "T" : "C"; }
  if (a.k === "only") return !tv.includes(a.say) ? "C" : tv.length > 1 ? "F" : "T";
  if (a.path[0] === "projectsInclude") return tv.includes(a.say) ? "T" : "F";   // "All ... either regional or national": anything else contradicts
  if (typeof tv === "string" && /^[A-Z]/.test(tv) && !T.includes(tv.toLowerCase())) errs.push("truth not printed: " + tv);
  return tv === a.say ? "T" : "F";
}
function answerOf(W, tabs, st, errs) {
  const r = st.atoms.map(a => evalAtom(W, tabs, a, st.text, errs));
  return r.includes("F") ? "F" : r.includes("C") ? "C" : "T";
}
function grammar(s) {
  const e = [];
  if (/(?:^A|\sa) (?:[aeiouAEIOU])/.test(s) && !/a (?:one|uni|Euro|use)/.test(s)) e.push("a/an");
  if (/\b(undefined|null|NaN)\b/.test(s)) e.push("undefined value");
  if (/\s\s|\s[.,]/.test(s)) e.push("spacing");
  return e;
}

const stats = {}; let bad = 0, shown = 0, total = 0; const mix = { T: 0, F: 0, C: 0 };
const fail = (m, st) => { bad++; if (shown++ < 15) console.log("FAIL", m, st ? "| " + st.template + " | " + st.text : ""); };
for (let s = 1; s <= N; s++) {
  const t = V.makeVerbalTest(s, 18);
  if (process.env.MUTATE) for (const st of t.items) st.answer = { T: "F", F: "C", C: "T" }[st.answer];
  for (const p of Object.values(t.tabs).flat()) for (const e of grammar(p.h + ". " + p.t)) fail("tab: " + e + " | " + p.t.slice(0, 80));
  const per = { T: 0, F: 0, C: 0 }, perTab = {};
  for (const st of t.items) {
    const errs = [], want = answerOf(t.world, t.tabs, st, errs);
    errs.push(...grammar(st.text));
    const r = stats[st.template] || (stats[st.template] = { n: 0, ok: 0, T: 0, F: 0, C: 0 });
    r.n++; total++;
    if (want !== st.answer) fail(`answer gen=${st.answer} verifier=${want}`, st);
    else if (errs.length) fail(errs.join("; "), st);
    else r.ok++;
    r[st.answer]++; per[st.answer]++; mix[st.answer]++; perTab[st.tab] = (perTab[st.tab] || 0) + 1;
  }
  if (t.items.length !== 18 || new Set(t.items.map(i => i.text)).size !== 18) fail("count/duplicates in test " + s);
  if (Object.keys(perTab).length !== 6 || Object.values(perTab).some(v => v !== 3)) fail("tab mix " + JSON.stringify(perTab));
  if (per.C < 6 || per.C > 10 || per.T < 3 || per.F < 3) fail("answer mix " + JSON.stringify(per));
  if (s <= 30 && !process.env.MUTATE && JSON.stringify(V.makeVerbalTest(s, 18)) !== JSON.stringify(t)) fail("not deterministic");
}
console.log("template                 statements  verified    T     F     C");
for (const [k, r] of Object.entries(stats).sort()) console.log(k.padEnd(24), String(r.n).padStart(9), String(r.ok).padStart(9), String(r.T).padStart(5), String(r.F).padStart(5), String(r.C).padStart(5));
console.log(`\n${N} tests, ${total} statements, ${bad} failures. Answer mix: True ${(100 * mix.T / total).toFixed(1)}%, False ${(100 * mix.F / total).toFixed(1)}%, Cannot say ${(100 * mix.C / total).toFixed(1)}%.`);
process.exit(bad ? 1 : 0);
