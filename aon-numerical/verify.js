/* Independent check of gen.js.  node verify.js [tests]
   For every generated statement it recomputes the answer from the data pack with its own code
   (it never trusts the generator's answer), checks the statement text names the same cells,
   numbers and periods the claim uses, and checks the data packs and test mix. */
"use strict";
const G = require("./gen.js");

const N = +process.argv[2] || 20000;
const en = (x, d) => x.toLocaleString("en-GB", { minimumFractionDigits: d, maximumFractionDigits: d });
const FMT = {
  gbp: x => "£" + en(x / 100, 2),
  gbpCode: x => en(x / 100, 2) + " GBP",
  pounds: x => "£" + en(x, 0),
  int: x => String(x),
};
const MULT = { 2: "two", 3: "three", 4: "four", 5: "five", 6: "six", 7: "seven", 8: "eight", 9: "nine" };

function val(P, ref) {
  const [tab, a, b] = ref;
  if (tab === "mail") return P.mail[a][b];
  if (tab === "profit") return (P.profit.total * P.profit.shares[a]) / 100;
  if (tab === "price") return P.price.p[a][b];
  if (tab === "exp") return a === "fc" ? P.exp.fc : P.exp.vc[b];
  if (tab === "hours") return P.hours[a][b];
  if (tab === "emp") return P.emp.cats[a][b];
  throw new Error("unknown ref " + ref);
}
const sum = (P, terms) => terms.reduce((s, t) => s + t.mul * val(P, t.ref), 0);

// Names that must appear in the text for a reference to be the one the text is about.
function namesFor(P, ref) {
  const [tab, a, b] = ref;
  if (tab === "profit") return [P.profit.units[a]];
  if (tab === "price") return [P.price.models[b]];
  if (tab === "hours") return [P.hours.staff[b][1]];
  if (tab === "emp") return [G.CATS[a].noun, "financial year " + P.emp.years[b]];
  if (tab === "exp") return a === "vc" ? [P.exp.qty[b] + " units"] : [];
  return [];
}
const MAIL_KEYS = "bands,nat,intl,svc,exp";

function answerOf(P, st) {
  const c = st.claim, x = st.text;
  if (c.t === "cmp") {
    const L = sum(P, c.l), R = typeof c.r === "number" ? c.r : sum(P, c.r);
    return { ">": L > R, "<": L < R, "==": L === R }[c.op] ? "T" : "F";
  }
  if (c.t === "overtimeSum") return P.hours.actual.reduce((s, a, i) => s + Math.max(0, a - P.hours.agreed[i]), 0) === c.r ? "T" : "F";
  if (c.t === "rise") return P.emp.cats[c.cat].every((v, i, a) => i === 0 || v > a[i - 1]) ? "T" : "F";
  if (c.t === "cs") {
    // A Cannot-say claim must point at information the pack really does not hold.
    const ok = {
      past: st.tab === "mail" ? /years ago/.test(x) && Object.keys(P.mail).join() === MAIL_KEYS : /Last year/.test(x) && Object.keys(P.price).join() === "items,models,p",
      future: /next year/.test(x) && Object.keys(P.mail).join() === MAIL_KEYS,
      volume: /(Most parcels|manufactured .* last month)/.test(x),
      month: c.month !== (st.tab === "profit" ? P.profit.month : P.hours.month) && x.includes(c.month),
      staff: /employees/.test(x) && !("staff" in P.profit),
      pay: /paid/.test(x) && !("pay" in P.hours),
      price: /selling price/.test(x),
      qty: !P.exp.qty.includes(c.qty) && x.includes(c.qty + " units"),
      year: !P.emp.years.includes(c.year) && x.includes("financial year " + c.year),
      parttime: /part-time/.test(x),
      discount: /bulk discount/.test(x),
      fitting: /fitting/.test(x),
    }[c.why];
    return ok ? "C" : "BAD-CS";
  }
  return "UNKNOWN";
}

function textErrors(P, st) {
  const c = st.claim, x = st.text, errs = [];
  if (/(?:^A|\sa) (?:[aeiou]|8|11 |18 )/.test(x)) errs.push("article: a/an");
  if (/(?:^An|\san) (?![aeiou]|8|11 |18 )/.test(x)) errs.push("article: an before consonant");
  if (c.t !== "cmp") return errs;
  if (typeof c.r === "number" && !x.includes(FMT[c.fmt](c.r))) errs.push("value " + FMT[c.fmt](c.r) + " not in text");
  const refs = c.l.concat(typeof c.r === "number" ? [] : c.r).map(t => t.ref);
  for (const ref of refs) for (const nm of namesFor(P, ref)) if (!x.includes(nm)) errs.push("missing name " + nm);
  if (st.tab === "price") for (const ref of refs) { const it = P.price.items[ref[1]]; if (!x.includes(it.one) && !x.includes(it.many)) errs.push("missing item " + it.one); }
  if (c.w !== undefined) {
    if (!x.includes(c.w + " kilo")) errs.push("weight not in text");
    const band = P.mail.bands.findIndex(([lo, hi]) => c.w >= lo && c.w <= hi);
    for (const ref of refs) if (ref[0] === "mail" && ref[1] !== "exp" && ref[2] !== band) errs.push("weight " + c.w + " used the wrong band");
    const intl = refs.some(r => r[1] === "intl");
    if (intl !== /^International/.test(x)) errs.push("national/international mismatch");
    for (const ref of refs) if (ref[1] === "exp" && !x.includes("'" + P.mail.svc[ref[2]] + "'")) errs.push("service name missing");
  }
  if (c.q !== undefined && !x.includes(P.exp.qty[c.q] + " units")) errs.push("quantity missing");
  if (st.tab === "exp") {
    const words = { fc: /fixed cost/, vc: /variable cost/ };
    const kinds = refs.map(r => r[1]);
    if (kinds.includes("fc") && kinds.includes("vc") && c.op === "==" && !/total cost/.test(x)) errs.push("fc+vc should be total cost");
    if (kinds.length === 1 && !words[kinds[0]].test(x)) errs.push("cost type wording");
  }
  if (c.month && !x.includes(c.month)) errs.push("month missing");
  if (c.n && !x.toLowerCase().includes(MULT[c.n] + " ")) errs.push("count word missing");
  // Order: the left-hand entity is named before the right-hand one.
  const ord = (a, b) => { const i = x.indexOf(a), j = x.indexOf(b); if (a !== b && (i < 0 || j < 0 || i > j)) errs.push("order " + a + " / " + b); };
  if (c.unit2 !== undefined) ord(P.profit.units[c.unit], P.profit.units[c.unit2]);
  if (c.emp2 !== undefined) ord(P.hours.staff[c.emp][1], P.hours.staff[c.emp2][1]);
  if (c.model2 !== undefined) ord("'" + P.price.models[c.model] + "'", "'" + P.price.models[c.model2] + "'");
  if (c.year2 !== undefined) ord("financial year " + c.year, "financial year " + c.year2);
  // Comparison words match the operator.
  if (c.op === ">" && !/(more|higher)/.test(x)) errs.push("'>' without more/higher");
  if (c.op === "<" && !/(less|fewer)/.test(x)) errs.push("'<' without less/fewer");
  if (c.op === "==" && /(more than|fewer than|less than|higher than)/.test(x) && st.template !== "price-difference") errs.push("'==' with a comparison word");
  return errs;
}

function packErrors(P) {
  const e = [];
  const sh = P.profit.shares;
  if (sh.reduce((a, b) => a + b, 0) !== 100 || new Set(sh).size !== 4 || sh.some(s => s % 5 || s < 5)) e.push("shares");
  P.emp.total.forEach((t, j) => { if (t !== P.emp.cats.reduce((a, c) => a + c[j], 0)) e.push("emp total"); });
  if (P.emp.axisMax < Math.max(...P.emp.total) || P.emp.cats.flat().some(v => v < 1)) e.push("emp axis/values");
  if (!P.exp.vc.every((v, i, a) => i === 0 || v < a[i - 1]) || P.exp.axisMax * 100 < P.exp.fc + P.exp.vc[0]) e.push("expenses");
  const b = P.mail.bands;
  for (let i = 0; i < 3; i++) { if (b[i][0] > b[i][1]) e.push("band"); if (i && b[i][0] <= b[i - 1][1]) e.push("bands overlap"); }
  if (!(P.mail.nat[0] < P.mail.nat[1] && P.mail.nat[1] < P.mail.nat[2])) e.push("national prices");
  for (let m = 0; m < 2; m++) if (new Set(P.price.p.map(r => r[m])).size !== 6) e.push("price column");
  if (P.price.p.some(r => r[0] === r[1])) e.push("price row");
  if (P.hours.actual.some(a => a <= 0)) e.push("hours");
  return e;
}

const stats = {}, mix = { C: 0, T: 0, F: 0 };
let bad = 0, shown = 0, tests = 0;
const fail = (msg, st) => { bad++; if (shown++ < 15) console.log("FAIL", msg, "|", st ? st.template + " | " + st.text : ""); };
for (let s = 1; s <= N; s++) {
  const t = G.makeTest(s, 18);
  tests++;
  // MUTATE=1 corrupts every answer (True<->False, Cannot say->True) to prove the checks catch it.
  if (process.env.MUTATE) for (const st of t.items) st.answer = { T: "F", F: "T", C: "T" }[st.answer];
  for (const e of packErrors(t.pack)) fail("pack: " + e);
  if (t.items.length !== 18) fail("count " + t.items.length);
  const perTab = {}, per = { C: 0, T: 0, F: 0 };
  for (const st of t.items) {
    const want = answerOf(t.pack, st);
    const errs = textErrors(t.pack, st);
    if (want === "C" && errs.length) { fail(errs.join("; "), st); continue; }
    const r = stats[st.template] || (stats[st.template] = { n: 0, ok: 0, T: 0, F: 0, C: 0 });
    r.n++;
    if (want !== st.answer) fail(`answer gen=${st.answer} verifier=${want}`, st);
    else if (errs.length) fail(errs.join("; "), st);
    else r.ok++;
    r[st.answer]++; per[st.answer]++; mix[st.answer]++;
    perTab[st.tab] = (perTab[st.tab] || 0) + 1;
  }
  if (new Set(t.items.map(i => i.text)).size !== 18) fail("duplicate statement in test " + s);
  if (Object.values(perTab).some(v => v !== 3) || Object.keys(perTab).length !== 6) fail("tab mix " + JSON.stringify(perTab));
  if (per.C < 3 || per.C > 7 || per.T < 4 || per.F < 4) fail("answer mix " + JSON.stringify(per));
  if (s <= 50 && !process.env.MUTATE && JSON.stringify(G.makeTest(s, 18)) !== JSON.stringify(t)) fail("not deterministic");
}

console.log("template                       statements  verified   T     F     C");
for (const [k, r] of Object.entries(stats).sort()) console.log(k.padEnd(30), String(r.n).padStart(9), String(r.ok).padStart(9), String(r.T).padStart(6), String(r.F).padStart(6), String(r.C).padStart(6));
const total = Object.values(stats).reduce((a, r) => a + r.n, 0);
console.log(`\n${tests} tests, ${total} statements, ${bad} failures. Answer mix: True ${(100 * mix.T / total).toFixed(1)}%, False ${(100 * mix.F / total).toFixed(1)}%, Cannot say ${(100 * mix.C / total).toFixed(1)}%.`);
process.exit(bad ? 1 : 0);
