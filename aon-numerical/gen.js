/* Aon-style numerical statements: data pack + True / False / Cannot say statements.
   Pure logic, no DOM. Runs in the page and in Node (verify.js).
   Money is kept in integer pence to avoid floating-point errors. */
(function (root) {
"use strict";

function mulberry32(a) {
  return function () {
    a |= 0; a = (a + 0x6D2B79F5) | 0;
    let t = Math.imul(a ^ (a >>> 15), 1 | a);
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}
function Rng(seed) {
  const r = mulberry32(seed);
  const g = {
    f: r,
    int: (a, b) => a + Math.floor(r() * (b - a + 1)),
    pick: a => a[Math.floor(r() * a.length)],
    chance: p => r() < p,
    shuffle(a) { a = a.slice(); for (let i = a.length - 1; i > 0; i--) { const j = Math.floor(r() * (i + 1)); [a[i], a[j]] = [a[j], a[i]]; } return a; },
  };
  g.others = (n, i) => [...Array(n).keys()].filter(x => x !== i);
  return g;
}

/* ---------- formatting ---------- */
function commas(s) { const [i, d] = s.split("."); return i.replace(/\B(?=(\d{3})+(?!\d))/g, ",") + (d !== undefined ? "." + d : ""); }
const gbp = p => "£" + commas((p / 100).toFixed(2));            // pence -> £1,234.50
const gbpCode = p => commas((p / 100).toFixed(2)) + " GBP";       // pence -> 1.00 GBP
const pounds = n => "£" + commas(String(n));                      // whole pounds -> £900,000
const WORDS = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten", "eleven", "twelve"];
const word = n => (n <= 12 ? WORDS[n] : String(n));
const cap = s => s[0].toUpperCase() + s.slice(1);
const MONTHS = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];
function niceMax(v, step) { return Math.ceil((v * 1.08) / step) * step; }

/* ---------- data pack ---------- */
const ITEMS = [
  { name: "Headlights", one: "headlight", many: "headlights" },
  { name: "Fog lights", one: "fog light", many: "fog lights" },
  { name: "Tail light", one: "tail light", many: "tail lights" },
  { name: "Front indicator", one: "front indicator", many: "front indicators" },
  { name: "Rear indicator", one: "rear indicator", many: "rear indicators" },
  { name: "Battery", one: "battery", many: "batteries" },
  { name: "Wiper blades", one: "wiper blade", many: "wiper blades" },
  { name: "Brake pads", one: "brake pad set", many: "brake pad sets" },
  { name: "Side mirror", one: "side mirror", many: "side mirrors" },
  { name: "Air filter", one: "air filter", many: "air filters" },
];
const MODEL_PAIRS = [["Coupé", "Combi"], ["Saloon", "Estate"], ["Roadster", "Hatchback"], ["City", "Tourer"]];
const UNIT_SETS = [["Factory 1", "Factory 2", "Factory 3", "Factory 4"], ["Plant A", "Plant B", "Plant C", "Plant D"], ["Site North", "Site South", "Site East", "Site West"]];
const STAFF = [["Ms", "Stratford"], ["Mr", "Newman"], ["Ms", "Dasgupta"], ["Mr", "Sanders"], ["Ms", "Lee"], ["Mr", "Wilson"], ["Ms", "Okafor"], ["Mr", "Novak"], ["Ms", "Brennan"], ["Mr", "Haddad"], ["Ms", "Kowalski"], ["Mr", "Tanaka"]];
const CATS = [
  { label: "Apprentices", noun: "apprentices" },
  { label: "Back office", noun: "back-office employees" },
  { label: "Front office", noun: "front-office employees" },
];
const BAND_SETS = [[[1, 7], [8, 15], [16, 20]], [[1, 5], [6, 12], [13, 20]], [[1, 3], [4, 10], [11, 25]], [[1, 4], [5, 10], [11, 20]]];
const SERVICES = ["Express", "Express before 9 a.m.", "Express Sunday"];

function makePack(g) {
  // 1. Mail order
  const bands = g.pick(BAND_SETS);
  const nat = [g.int(45, 95) * 10]; nat.push(nat[0] + g.int(5, 45) * 10); nat.push(nat[1] + g.int(1, 40) * 10);
  const intl = [g.int(70, 120) * 10]; intl.push(intl[0] + g.int(5, 40) * 10); intl.push(intl[1] + g.int(10, 80) * 10);
  const e0 = g.int(10, 18) * 100 + g.pick([0, 50]), e1 = e0 + g.int(8, 16) * 100 + g.pick([0, 50]), e2 = e1 + g.int(10, 30) * 100;
  const mail = { bands, nat, intl, svc: SERVICES.slice(), exp: [e0, e1, e2] };

  // 2. Profit shares (multiples of 5, distinct, sum 100)
  let shares;
  do {
    shares = [g.int(1, 12), g.int(1, 12), g.int(1, 12)].map(x => x * 5);
    shares.push(100 - shares.reduce((a, b) => a + b, 0));
  } while (shares[3] < 5 || new Set(shares).size < 4);
  const profit = { units: g.pick(UNIT_SETS), shares, total: g.pick([1000000, 1500000, 2000000, 2500000, 3000000, 4000000, 5000000, 6000000, 8000000]), month: g.pick(MONTHS) };

  // 3. Price list (whole pounds, stored in pence)
  const items = g.shuffle(ITEMS).slice(0, 6), models = g.pick(MODEL_PAIRS);
  let prices;
  do {
    prices = items.map(() => { const a = g.int(25, 95); let b; do { b = a + g.int(-18, 18); } while (b === a || b < 20); return [a * 100, b * 100]; });
  } while (new Set(prices.map(p => p[0])).size < 6 || new Set(prices.map(p => p[1])).size < 6);
  const price = { items, models, p: prices };

  // 4. Expenses per unit: fixed constant, variable falling, total = fixed + variable (total not labelled)
  const qty = [100, 200, 300, 400, 500, 600];
  const fc = g.int(5, 12) * 100 + g.pick([0, 50]);
  let vc;
  do {
    const v0 = g.int(10, 16) * 100 + g.pick([0, 50]), a = 0.6 + g.f() * 0.4;
    vc = qty.map((q, i) => Math.round(v0 * Math.pow(1 / (i + 1), a)));
  } while (!vc.every((v, i) => i === 0 || v < vc[i - 1]) || vc[5] < 150 || vc.includes(fc));
  const exp = { qty, fc, vc, axisMax: niceMax((fc + vc[0]) / 100, 5) };

  // 5. Working hours
  const [part, full] = g.pick([[85, 175], [80, 160], [90, 180]]);
  const staff = g.shuffle(STAFF).slice(0, 6);
  let agreed, actual;
  do {
    agreed = staff.map(() => (g.chance(0.35) ? part : full));
    actual = agreed.map(a => (g.chance(0.18) ? a : a + g.int(-16, 12)));
  } while (new Set(agreed).size < 2 || !actual.some((x, i) => x > agreed[i]) || !actual.some((x, i) => x < agreed[i]));
  const hours = { staff, agreed, actual, month: g.pick(MONTHS) };

  // 6. Employees by financial year
  const y0 = g.int(3, 7), years = [y0, y0 + 1, y0 + 2, y0 + 3];
  const walk = (start, lo, hi) => { const s = [start]; for (let i = 1; i < 4; i++) s.push(Math.max(1, s[i - 1] + g.int(lo, hi))); return s; };
  const cats = [walk(g.int(3, 8), -1, 3), walk(g.int(10, 20), -2, 4), walk(g.int(26, 40), -3, 2)];
  const total = years.map((_, j) => cats[0][j] + cats[1][j] + cats[2][j]);
  const emp = { years, cats, total, axisMax: niceMax(Math.max(...total), 10) };

  return { mail, profit, price, exp, hours, emp };
}

/* ---------- statement helpers ---------- */
// Pick a false value: a "trap" decoy (a real number from the wrong cell) or a near miss.
function falseVal(g, v, decoys, nears) {
  const ds = decoys.filter(d => d !== v && d > 0);
  if (ds.length && g.chance(0.55)) return g.pick(ds);
  for (let i = 0; i < 20; i++) { const x = v + g.pick([-1, 1]) * g.pick(nears); if (x > 0 && x !== v) return x; }
  return v + nears[0];
}
const T = (ref, mul) => ({ ref, mul: mul || 1 });
function S(tab, kind, text, answer, claim, expl) { return { tab, kind, text, answer, claim, expl }; }
function bandIdx(P, w) { return P.mail.bands.findIndex(([lo, hi]) => w >= lo && w <= hi); }
function weightIn(g, P, b) { const [lo, hi] = P.mail.bands[b]; return g.int(lo, hi); }
const bandTxt = (P, b) => `${P.mail.bands[b][0]}–${P.mail.bands[b][1]} kg`;
const otherMonth = (g, m) => g.pick(MONTHS.filter(x => x !== m));
const poss = t => (t === "Ms" ? "her" : "his");
// "a" or "an" for the next word: an air filter, an 8 kilo parcel, an 11 / 18 kilo parcel.
const art = w => (/^(?:[aeiou]|8|11\b|18\b)/i.test(String(w)) ? "an " : "a ") + w;

/* ---------- templates ----------
   Each template: (g, P, want) -> statement or null.  want is "T" or "F"; Cannot-say templates ignore it.
   claim is a machine-checkable description used by verify.js; answer is the generator's own verdict. */
const TEMPLATES = {
  mail: [
    { id: "mail-national", kind: "lookup", f(g, P, want) {
      const b = g.int(0, 2), w = weightIn(g, P, b), v = P.mail.nat[b];
      const x = want === "T" ? v : falseVal(g, v, [P.mail.nat[(b + 1) % 3], P.mail.intl[b]], [10, 20, 50, 100]);
      return S("mail", "lookup", `National delivery of ${art(w)} kilo parcel costs ${gbp(x)}.`, x === v ? "T" : "F",
        { t: "cmp", w, l: [T(["mail", "nat", b])], op: "==", r: x, fmt: "gbp" },
        `${w} kg falls in the ${bandTxt(P, b)} band. National price: ${gbp(v)}.`);
    } },
    { id: "mail-national-express", kind: "two-step", f(g, P, want) {
      const b = g.int(0, 2), s = g.int(0, 2), w = weightIn(g, P, b), v = P.mail.nat[b] + P.mail.exp[s];
      const x = want === "T" ? v : falseVal(g, v, [P.mail.nat[b] + P.mail.exp[(s + 1) % 3], P.mail.nat[(b + 1) % 3] + P.mail.exp[s], P.mail.nat[b] + P.mail.intl[b] + P.mail.exp[s]], [100, 1000, 50]);
      return S("mail", "two-step", `National delivery of ${art(w)} kilo parcel, including the surcharge for the '${P.mail.svc[s]}' service, costs ${gbp(x)}.`, x === v ? "T" : "F",
        { t: "cmp", w, svc: s, l: [T(["mail", "nat", b]), T(["mail", "exp", s])], op: "==", r: x, fmt: "gbp" },
        `${bandTxt(P, b)} national ${gbp(P.mail.nat[b])} + '${P.mail.svc[s]}' ${gbp(P.mail.exp[s])} = ${gbp(v)}.`);
    } },
    { id: "mail-international", kind: "two-step", f(g, P, want) {
      const b = g.int(0, 2), w = weightIn(g, P, b), v = P.mail.nat[b] + P.mail.intl[b];
      const x = want === "T" ? v : falseVal(g, v, [P.mail.intl[b], P.mail.nat[b] + P.mail.intl[(b + 1) % 3]], [10, 100, 50]);
      return S("mail", "two-step", `International delivery of ${art(w)} kilo parcel costs ${gbp(x)}.`, x === v ? "T" : "F",
        { t: "cmp", w, l: [T(["mail", "nat", b]), T(["mail", "intl", b])], op: "==", r: x, fmt: "gbp" },
        `The international surcharge is added on top of the national price: ${gbp(P.mail.nat[b])} + ${gbp(P.mail.intl[b])} = ${gbp(v)}.`);
    } },
    { id: "mail-international-express", kind: "three-step", f(g, P, want) {
      const b = g.int(0, 2), s = g.int(0, 2), w = weightIn(g, P, b), v = P.mail.nat[b] + P.mail.intl[b] + P.mail.exp[s];
      const x = want === "T" ? v : falseVal(g, v, [P.mail.intl[b] + P.mail.exp[s], P.mail.nat[b] + P.mail.exp[s], P.mail.nat[b] + P.mail.intl[b] + P.mail.exp[(s + 1) % 3]], [100, 1000]);
      return S("mail", "three-step", `International delivery of ${art(w)} kilo parcel, including the '${P.mail.svc[s]}' service, costs ${gbp(x)}.`, x === v ? "T" : "F",
        { t: "cmp", w, svc: s, l: [T(["mail", "nat", b]), T(["mail", "intl", b]), T(["mail", "exp", s])], op: "==", r: x, fmt: "gbp" },
        `${gbp(P.mail.nat[b])} national + ${gbp(P.mail.intl[b])} international surcharge + ${gbp(P.mail.exp[s])} '${P.mail.svc[s]}' = ${gbp(v)}.`);
    } },
    { id: "mail-cs", kind: "cannot say", cs: true, f(g, P) {
      const b = g.int(0, 2), w = weightIn(g, P, b), v = P.mail.nat[b], m = g.int(0, 2);
      const text = [
        `National delivery of ${art(w)} kilo parcel cost ${gbp(v - g.int(1, 9) * 10)} ${word(g.int(2, 4))} years ago.`,
        `From next year, international delivery of ${art(w)} kilo parcel will cost ${gbp(v + P.mail.intl[b] + g.int(1, 9) * 10)}.`,
        `Most parcels sent by the company weigh between ${P.mail.bands[b][0]} and ${P.mail.bands[b][1]} kilos.`,
      ][m];
      return S("mail", "cannot say", text, "C", { t: "cs", why: ["past", "future", "volume"][m], w },
        ["The table shows current prices only, not past ones.", "The table shows current prices only, not future ones.", "The table shows prices, not how many parcels are sent."][m]);
    } },
  ],

  profit: [
    { id: "profit-value", kind: "lookup", f(g, P, want) {
      const i = g.int(0, 3), pr = P.profit, v = pr.shares[i] * pr.total / 100;
      const x = want === "T" ? v : falseVal(g, v, g.others(4, i).map(j => pr.shares[j] * pr.total / 100), [pr.total / 20, pr.total / 10]);
      return S("profit", "lookup", `${pr.units[i]} generated a profit of ${pounds(x)} in ${pr.month}.`, x === v ? "T" : "F",
        { t: "cmp", unit: i, month: pr.month, l: [T(["profit", i])], op: "==", r: x, fmt: "pounds" },
        `${pr.units[i]} has the ${pr.shares[i]}% slice: ${pr.shares[i]}% × ${pounds(pr.total)} = ${pounds(v)}.`);
    } },
    { id: "profit-pair", kind: "two-step", f(g, P, want) {
      const pr = P.profit, [i, j] = g.shuffle([0, 1, 2, 3]).slice(0, 2), v = (pr.shares[i] + pr.shares[j]) * pr.total / 100;
      const x = want === "T" ? v : falseVal(g, v, [(100 - pr.shares[i] - pr.shares[j]) * pr.total / 100], [pr.total / 20, pr.total / 10]);
      return S("profit", "two-step", `Together, ${pr.units[i]} and ${pr.units[j]} generated a profit of ${pounds(x)} in ${pr.month}.`, x === v ? "T" : "F",
        { t: "cmp", unit: i, unit2: j, month: pr.month, l: [T(["profit", i]), T(["profit", j])], op: "==", r: x, fmt: "pounds" },
        `${pr.shares[i]}% + ${pr.shares[j]}% = ${pr.shares[i] + pr.shares[j]}% of ${pounds(pr.total)} = ${pounds(v)}.`);
    } },
    { id: "profit-more-than-two", kind: "comparison", f(g, P, want) {
      const pr = P.profit;
      for (let k = 0; k < 12; k++) {
        const [i, j, l] = g.shuffle([0, 1, 2, 3]).slice(0, 3), a = pr.shares[i], bc = pr.shares[j] + pr.shares[l];
        if (a === bc || (a > bc) !== (want === "T")) continue;
        return S("profit", "comparison", `${pr.units[i]} generated more profit than ${pr.units[j]} and ${pr.units[l]} combined in ${pr.month}.`, a > bc ? "T" : "F",
          { t: "cmp", unit: i, unit2: j, unit3: l, month: pr.month, l: [T(["profit", i])], op: ">", r: [T(["profit", j]), T(["profit", l])] },
          `Compare shares: ${a}% vs ${pr.shares[j]}% + ${pr.shares[l]}% = ${bc}%.`);
      }
      return null;
    } },
    { id: "profit-ratio", kind: "comparison", f(g, P, want) {
      const pr = P.profit, k = g.pick([2, 3]);
      const pairs = [];
      for (let i = 0; i < 4; i++) for (let j = 0; j < 4; j++) if (i !== j && (pr.shares[i] === k * pr.shares[j]) === (want === "T") && pr.shares[i] > pr.shares[j]) pairs.push([i, j]);
      if (!pairs.length) return null;
      const [i, j] = g.pick(pairs), ok = pr.shares[i] === k * pr.shares[j];
      return S("profit", "comparison", `In ${pr.month}, ${pr.units[i]}'s profit was exactly ${k === 2 ? "twice" : "three times"} that of ${pr.units[j]}.`, ok ? "T" : "F",
        { t: "cmp", unit: i, unit2: j, month: pr.month, l: [T(["profit", i])], op: "==", r: [T(["profit", j], k)] },
        `${pr.shares[i]}% vs ${pr.shares[j]}%: ${pr.shares[i]} ÷ ${pr.shares[j]} = ${+(pr.shares[i] / pr.shares[j]).toFixed(2)}.`);
    } },
    { id: "profit-cs", kind: "cannot say", cs: true, f(g, P) {
      const pr = P.profit, i = g.int(0, 3), j = g.pick(g.others(4, i)), om = otherMonth(g, pr.month), m = g.int(0, 2);
      const text = [
        `${pr.units[i]} generated a higher profit in ${om} than in ${pr.month}.`,
        `In ${om}, ${pr.units[i]} generated a profit of ${pounds(pr.shares[i] * pr.total / 100)}.`,
        `${pr.units[i]} has more employees than ${pr.units[j]}.`,
      ][m];
      return S("profit", "cannot say", text, "C", { t: "cs", why: m < 2 ? "month" : "staff", month: om },
        m < 2 ? `The chart only covers ${pr.month}.` : "The chart shows profit shares, not staff numbers.");
    } },
  ],

  price: [
    { id: "price-lookup", kind: "lookup", f(g, P, want) {
      const pl = P.price, i = g.int(0, 5), m = g.int(0, 1), v = pl.p[i][m];
      const x = want === "T" ? v : falseVal(g, v, [pl.p[i][1 - m], pl.p[(i + 1) % 6][m]], [100, 200, 500]);
      return S("price", "lookup", `According to the price list, ${art(pl.items[i].one)} for the '${pl.models[m]}' model costs ${gbp(x)}.`, x === v ? "T" : "F",
        { t: "cmp", item: i, model: m, l: [T(["price", i, m])], op: "==", r: x, fmt: "gbp" },
        `${pl.items[i].name}, '${pl.models[m]}' column: ${gbp(v)}.`);
    } },
    { id: "price-difference", kind: "two-step", f(g, P, want) {
      const pl = P.price, i = g.int(0, 5), m = g.int(0, 1), d = pl.p[i][m] - pl.p[i][1 - m];
      let x;
      if (want === "T") { if (d <= 0) return null; x = d; }
      else x = d > 0 ? falseVal(g, d, [], [100, 200, 300]) : -d;     // wrong amount, or right amount in the wrong direction
      return S("price", "two-step", `According to the price list, ${art(pl.items[i].one)} for the '${pl.models[m]}' model costs ${gbpCode(x)} more than ${art(pl.items[i].one)} for the '${pl.models[1 - m]}' model.`, d === x ? "T" : "F",
        { t: "cmp", item: i, model: m, model2: 1 - m, l: [T(["price", i, m]), T(["price", i, 1 - m], -1)], op: "==", r: x, fmt: "gbpCode" },
        `${gbp(pl.p[i][m])} − ${gbp(pl.p[i][1 - m])} = ${d < 0 ? "−" : ""}${gbp(Math.abs(d))}${d < 0 ? ` (it is cheaper, not dearer)` : ""}.`);
    } },
    { id: "price-multiple", kind: "two-step", f(g, P, want) {
      const pl = P.price, i = g.int(0, 5), m = g.int(0, 1), n = g.int(2, 9), v = n * pl.p[i][m];
      const x = want === "T" ? v : falseVal(g, v, [n * pl.p[i][1 - m], (n + 1) * pl.p[i][m], (n - 1) * pl.p[i][m]], [100, 1000]);
      return S("price", "two-step", `${cap(word(n))} ${pl.items[i].many} for the '${pl.models[m]}' model cost ${gbp(x)} in total.`, x === v ? "T" : "F",
        { t: "cmp", item: i, model: m, n, l: [T(["price", i, m], n)], op: "==", r: x, fmt: "gbp" },
        `${n} × ${gbp(pl.p[i][m])} = ${gbp(v)}.`);
    } },
    { id: "price-compare-multiples", kind: "comparison", f(g, P, want) {
      const pl = P.price;
      for (let k = 0; k < 15; k++) {
        const i = g.int(0, 5), j = g.int(0, 5), m = g.int(0, 1), n1 = g.int(2, 8), n2 = g.int(2, 8);
        const a = n1 * pl.p[i][m], b = n2 * pl.p[j][1 - m];
        if (a === b || (a > b) !== (want === "T") || (i === j && n1 === n2)) continue;
        return S("price", "comparison", `${cap(word(n1))} ${pl.items[i].many} for the '${pl.models[m]}' model cost more than ${word(n2)} ${pl.items[j].many} for the '${pl.models[1 - m]}' model.`, a > b ? "T" : "F",
          { t: "cmp", item: i, item2: j, model: m, model2: 1 - m, n: n1, n2, l: [T(["price", i, m], n1)], op: ">", r: [T(["price", j, 1 - m], n2)] },
          `${n1} × ${gbp(pl.p[i][m])} = ${gbp(a)} vs ${n2} × ${gbp(pl.p[j][1 - m])} = ${gbp(b)}.`);
      }
      return null;
    } },
    { id: "price-cs", kind: "cannot say", cs: true, f(g, P) {
      const pl = P.price, i = g.int(0, 5), j = g.int(0, 5), m = g.int(0, 1), k = g.int(0, 2);
      const text = [
        `With a bulk discount, ${word(g.int(4, 9))} ${pl.items[i].many} of the '${pl.models[m]}' type cost the same as ${word(g.int(4, 9))} ${pl.items[j].many} for the '${pl.models[1 - m]}' model without a bulk discount.`,
        `Including fitting, ${art(pl.items[i].one)} for the '${pl.models[m]}' model costs ${gbp(pl.p[i][m] + g.int(2, 6) * 500)}.`,
        `Last year, ${art(pl.items[i].one)} for the '${pl.models[m]}' model cost ${gbp(pl.p[i][m] - g.int(1, 5) * 100)}.`,
      ][k];
      return S("price", "cannot say", text, "C", { t: "cs", why: ["discount", "fitting", "past"][k] },
        ["The price list says nothing about a bulk discount.", "The price list says nothing about fitting costs.", "The price list shows current prices only."][k]);
    } },
  ],

  exp: [
    { id: "exp-fixed", kind: "lookup", f(g, P, want) {
      const e = P.exp, q = g.int(0, 5), v = e.fc;
      const x = want === "T" ? v : falseVal(g, v, [e.vc[q], e.fc + e.vc[q]], [50, 100]);
      return S("exp", "lookup", `The fixed cost per unit if ${e.qty[q]} units were to be manufactured is ${gbp(x)}.`, x === v ? "T" : "F",
        { t: "cmp", q, l: [T(["exp", "fc"])], op: "==", r: x, fmt: "gbp" },
        `Read the fc line (dark blue) at ${e.qty[q]}: ${gbp(v)}.`);
    } },
    { id: "exp-variable", kind: "lookup", f(g, P, want) {
      const e = P.exp, q = g.int(0, 5), v = e.vc[q];
      const x = want === "T" ? v : falseVal(g, v, [e.fc, e.vc[q === 5 ? 4 : q + 1]], [50, 100]);
      return S("exp", "lookup", `The variable cost per unit for a quantity of ${e.qty[q]} units is ${gbp(x)}.`, x === v ? "T" : "F",
        { t: "cmp", q, l: [T(["exp", "vc", q])], op: "==", r: x, fmt: "gbp" },
        `Read the vc line (light blue) at ${e.qty[q]}: ${gbp(v)}.`);
    } },
    { id: "exp-total-per-unit", kind: "two-step", f(g, P, want) {
      const e = P.exp, q = g.int(0, 5), v = e.fc + e.vc[q];
      const x = want === "T" ? v : falseVal(g, v, [e.vc[q], e.fc + e.vc[q === 0 ? 1 : q - 1]], [50, 100, 1000]);
      return S("exp", "two-step", `The total cost per unit for a quantity of ${e.qty[q]} units is ${gbp(x)}.`, x === v ? "T" : "F",
        { t: "cmp", q, l: [T(["exp", "fc"]), T(["exp", "vc", q])], op: "==", r: x, fmt: "gbp" },
        `The c line has no labels, so add: fc ${gbp(e.fc)} + vc ${gbp(e.vc[q])} = ${gbp(v)}.`);
    } },
    { id: "exp-vc-vs-fc", kind: "comparison", f(g, P, want) {
      const e = P.exp, opts = [0, 1, 2, 3, 4, 5].filter(q => (e.vc[q] > e.fc) === (want === "T"));
      if (!opts.length) return null;
      const q = g.pick(opts);
      return S("exp", "comparison", `For a quantity of ${e.qty[q]} units, the variable cost per unit is higher than the fixed cost per unit.`, e.vc[q] > e.fc ? "T" : "F",
        { t: "cmp", q, l: [T(["exp", "vc", q])], op: ">", r: [T(["exp", "fc"])] },
        `vc ${gbp(e.vc[q])} vs fc ${gbp(e.fc)}.`);
    } },
    { id: "exp-cs", kind: "cannot say", cs: true, f(g, P) {
      const e = P.exp, q = g.int(0, 5), k = g.int(0, 2), far = g.pick([700, 800, 1000]);
      const text = [
        `The selling price per unit for a quantity of ${e.qty[q]} units is ${gbp(e.fc + e.vc[q] + g.int(2, 8) * 100)}.`,
        `For a quantity of ${far} units, the variable cost per unit is ${gbp(Math.max(50, e.vc[5] - g.int(2, 8) * 10))}.`,
        `The company manufactured ${e.qty[q]} units last month.`,
      ][k];
      return S("exp", "cannot say", text, "C", { t: "cs", why: ["price", "qty", "volume"][k], qty: far },
        ["The chart shows costs only, not selling prices.", `The chart stops at 600 units; ${far} is not shown.`, "The chart shows costs at each quantity, not how many units were made."][k]);
    } },
  ],

  hours: [
    { id: "hours-same-agreed", kind: "comparison", f(g, P, want) {
      const h = P.hours, pairs = [];
      for (let i = 0; i < 6; i++) for (let j = 0; j < 6; j++) if (i !== j && (h.agreed[i] === h.agreed[j]) === (want === "T")) pairs.push([i, j]);
      if (!pairs.length) return null;
      const [i, j] = g.pick(pairs), [ti, ni] = h.staff[i], [tj, nj] = h.staff[j];
      return S("hours", "comparison", `${ti} ${ni} has the same amount of agreed working hours as ${tj} ${nj} in ${h.month}.`, h.agreed[i] === h.agreed[j] ? "T" : "F",
        { t: "cmp", emp: i, emp2: j, month: h.month, l: [T(["hours", "agreed", i])], op: "==", r: [T(["hours", "agreed", j])] },
        `Agreed hours: ${ni} ${h.agreed[i]}, ${nj} ${h.agreed[j]}.`);
    } },
    { id: "hours-less-than-normal", kind: "comparison", f(g, P, want) {
      const h = P.hours, opts = [0, 1, 2, 3, 4, 5].filter(i => (h.actual[i] < h.agreed[i]) === (want === "T"));
      if (!opts.length) return null;
      const i = g.pick(opts), [t, n] = h.staff[i];
      return S("hours", "comparison", `${t} ${n} worked less than ${poss(t)} normal working hours in ${h.month}.`, h.actual[i] < h.agreed[i] ? "T" : "F",
        { t: "cmp", emp: i, month: h.month, l: [T(["hours", "actual", i])], op: "<", r: [T(["hours", "agreed", i])] },
        `${n}: actual ${h.actual[i]} vs agreed ${h.agreed[i]}.`);
    } },
    { id: "hours-overtime", kind: "two-step", f(g, P, want) {
      const h = P.hours, over = [0, 1, 2, 3, 4, 5].filter(i => h.actual[i] > h.agreed[i]);
      if (!over.length) return null;
      let i, x;
      if (want === "T") { i = g.pick(over); x = h.actual[i] - h.agreed[i]; }
      else if (g.chance(0.5)) { i = g.pick(over); x = falseVal(g, h.actual[i] - h.agreed[i], [], [1, 2, 3, 5]); }
      else { const short = [0, 1, 2, 3, 4, 5].filter(k => h.actual[k] < h.agreed[k]); if (!short.length) return null; i = g.pick(short); x = h.agreed[i] - h.actual[i]; }
      const [t, n] = h.staff[i], v = h.actual[i] - h.agreed[i];
      return S("hours", "two-step", `${t} ${n} worked ${x} hours of overtime in ${h.month}.`, v === x ? "T" : "F",
        { t: "cmp", emp: i, month: h.month, l: [T(["hours", "actual", i]), T(["hours", "agreed", i], -1)], op: "==", r: x, fmt: "int" },
        `Overtime = actual − agreed = ${h.actual[i]} − ${h.agreed[i]} = ${v}${v < 0 ? " (that is a shortfall, not overtime)" : ""}.`);
    } },
    { id: "hours-total-overtime", kind: "three-step", f(g, P, want) {
      const h = P.hours, idx = [0, 1, 2, 3, 4, 5].filter(i => h.actual[i] > h.agreed[i]);
      const v = idx.reduce((a, i) => a + h.actual[i] - h.agreed[i], 0);
      const net = h.actual.reduce((a, x, i) => a + x - h.agreed[i], 0);
      const x = want === "T" ? v : falseVal(g, v, [net, v + 1], [2, 3, 5]);
      return S("hours", "three-step", `In ${h.month}, the employees in the table worked ${x} hours of overtime in total.`, x === v ? "T" : "F",
        { t: "overtimeSum", month: h.month, r: x, fmt: "int" },
        `Add only the people above their agreed hours: ${idx.map(i => `${h.staff[i][1]} ${h.actual[i] - h.agreed[i]}`).join(" + ")} = ${v}.`);
    } },
    { id: "hours-cs", kind: "cannot say", cs: true, f(g, P) {
      const h = P.hours, i = g.int(0, 5), [t, n] = h.staff[i], om = otherMonth(g, h.month), k = g.int(0, 1);
      const text = [
        `${t} ${n} had more agreed working hours in ${om} than in ${h.month}.`,
        `${t} ${n} was paid extra for ${poss(t)} hours in ${h.month}.`,
      ][k];
      return S("hours", "cannot say", text, "C", { t: "cs", why: k === 0 ? "month" : "pay", month: om },
        k === 0 ? `The table only covers ${h.month}.` : "The table says nothing about pay.");
    } },
  ],

  emp: [
    { id: "emp-more-than", kind: "lookup", f(g, P, want) {
      const e = P.emp, c = g.int(0, 2), y = g.int(0, 3), v = e.cats[c][y], more = g.chance(0.5);
      // "more than N" is true when N < v; "fewer than N" is true when N > v. Never use N === v.
      const below = v - g.int(1, Math.min(4, v)), above = v + g.int(1, 4);
      const N = (want === "T") === more ? below : above;
      if (N < 1) return null;
      const ok = more ? v > N : v < N;
      return S("emp", "lookup", `In financial year ${e.years[y]}, there were ${more ? "more" : "fewer"} than ${N} ${CATS[c].noun}.`, ok ? "T" : "F",
        { t: "cmp", cat: c, year: e.years[y], l: [T(["emp", c, y])], op: more ? ">" : "<", r: N, fmt: "int" },
        `${CATS[c].label}, year ${e.years[y]}: ${v}.`);
    } },
    { id: "emp-two-cats", kind: "two-step", f(g, P, want) {
      const e = P.emp, [a, b] = g.shuffle([0, 1, 2]).slice(0, 2), y = g.int(0, 3), v = e.cats[a][y] + e.cats[b][y];
      const x = want === "T" ? v : falseVal(g, v, [e.total[y], e.cats[a][(y + 1) % 4] + e.cats[b][(y + 1) % 4]], [1, 2, 3]);
      return S("emp", "two-step", `In financial year ${e.years[y]}, ${x} employees in total were ${CATS[a].noun} or ${CATS[b].noun}.`, x === v ? "T" : "F",
        { t: "cmp", cat: a, cat2: b, year: e.years[y], l: [T(["emp", a, y]), T(["emp", b, y])], op: "==", r: x, fmt: "int" },
        `${e.cats[a][y]} + ${e.cats[b][y]} = ${v}.`);
    } },
    { id: "emp-half", kind: "comparison", f(g, P, want) {
      const e = P.emp, opts = [];
      for (let c = 0; c < 3; c++) for (let i = 0; i < 4; i++) for (let j = 0; j < 4; j++) if (i !== j && (2 * e.cats[c][i] === e.cats[c][j]) === (want === "T") && e.cats[c][i] < e.cats[c][j]) opts.push([c, i, j]);
      if (!opts.length) return null;
      const [c, i, j] = g.pick(opts), ok = 2 * e.cats[c][i] === e.cats[c][j];
      return S("emp", "comparison", `In financial year ${e.years[i]}, there were exactly half as many ${CATS[c].noun} as in financial year ${e.years[j]}.`, ok ? "T" : "F",
        { t: "cmp", cat: c, year: e.years[i], year2: e.years[j], l: [T(["emp", c, i], 2)], op: "==", r: [T(["emp", c, j])] },
        `${e.cats[c][i]} vs ${e.cats[c][j]}: half of ${e.cats[c][j]} is ${e.cats[c][j] / 2}.`);
    } },
    { id: "emp-rose-every-year", kind: "comparison", f(g, P, want) {
      const e = P.emp, opts = [0, 1, 2].filter(c => e.cats[c].every((v, i) => i === 0 || v > e.cats[c][i - 1]) === (want === "T"));
      if (!opts.length) return null;
      const c = g.pick(opts), ok = e.cats[c].every((v, i) => i === 0 || v > e.cats[c][i - 1]);
      return S("emp", "comparison", `The number of ${CATS[c].noun} rose every year from financial year ${e.years[0]} to financial year ${e.years[3]}.`, ok ? "T" : "F",
        { t: "rise", cat: c },
        `${CATS[c].label}: ${e.cats[c].join(", ")}.`);
    } },
    { id: "emp-cs", kind: "cannot say", cs: true, f(g, P) {
      const e = P.emp, c = g.int(0, 2), k = g.int(0, 1), y = k === 0 ? e.years[0] - g.int(1, 2) : e.years[g.int(0, 3)];
      const text = [
        `In financial year ${y}, there were only half as many ${CATS[c].noun} as in financial year ${e.years[g.int(1, 3)]}.`,
        `In financial year ${y}, more than half of the ${CATS[c].noun} worked part-time.`,
      ][k];
      return S("emp", "cannot say", text, "C", { t: "cs", why: k === 0 ? "year" : "parttime", year: y },
        k === 0 ? `The chart starts at financial year ${e.years[0]}.` : "The chart does not show working patterns.");
    } },
  ],
};

const TABS = [
  { key: "mail", title: "Mail order" },
  { key: "profit", title: "Profit" },
  { key: "price", title: "Price list" },
  { key: "exp", title: "Expenses" },
  { key: "hours", title: "Working hours" },
  { key: "emp", title: "Employees" },
];

/* One test: n statements, 3 per tab, mixed order, about 30% Cannot say, the rest split True/False. */
function makeTest(seed, n) {
  n = n || 18;
  const g = Rng(seed), P = makePack(g);
  const nCs = Math.round(n * (0.22 + g.f() * 0.12));
  const nT = Math.round((n - nCs) / 2) + g.pick([-1, 0, 1]), nF = n - nCs - nT;
  const wants = g.shuffle([].concat(Array(nCs).fill("C"), Array(nT).fill("T"), Array(nF).fill("F")));
  const slots = g.shuffle([].concat(...TABS.map(t => Array(Math.ceil(n / TABS.length)).fill(t.key)))).slice(0, n);
  const out = [], seen = new Set(), used = new Map();
  for (let s = 0; s < n; s++) {
    let want = wants[s], made = null;
    for (let attempt = 0; attempt < 200 && !made; attempt++) {
      if (attempt === 120) want = want === "C" ? "T" : want;         // fall back if a tab cannot make the wanted kind
      const pool = TEMPLATES[slots[s]].filter(t => !!t.cs === (want === "C"));
      const lo = Math.min(...pool.map(t => used.get(t.id) || 0));
      const t = g.pick(pool.filter(x => (used.get(x.id) || 0) <= lo + (attempt > 40 ? 1 : 0)));
      const st = t.f(g, P, want);
      if (!st || seen.has(st.text) || (want !== "C" && st.answer !== want)) continue;
      st.template = t.id; made = st;
      used.set(t.id, (used.get(t.id) || 0) + 1);
    }
    if (!made) throw new Error("could not fill slot " + s + " (" + slots[s] + ")");
    seen.add(made.text);
    out.push(made);
  }
  return { seed, pack: P, items: out };
}

const API = { makeTest, makePack, Rng, TEMPLATES, TABS, CATS, gbp, gbpCode, pounds, word };
if (typeof module !== "undefined" && module.exports) module.exports = API; else root.AonGen = API;
})(this);
