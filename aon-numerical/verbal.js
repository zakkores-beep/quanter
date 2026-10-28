/* Aon-style verbal statements: a fictional bank described in six text tabs, plus True / False / Cannot say statements.
   Every tab is written from a structured "world"; every statement is built from "atoms" (single claims about that world),
   so verify-verbal.js can re-derive each answer from the world without trusting this file.
   Atom rules:  eq  (single-valued fact: match -> True, mismatch -> False)
                has (list membership: present -> True, absent -> Cannot say, because lists are not exhaustive)
                only (claims a list has just one item: list longer -> False)
                cmp (numbers)
                novel (a detail no tab mentions -> Cannot say)
   A statement with several atoms is False if any atom is False, else Cannot say if any is, else True. */
(function (root) {
"use strict";
const Gen = typeof module !== "undefined" && module.exports ? require("./gen.js") : root.AonGen;
const { Rng } = Gen;

const WORDS = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten", "eleven", "twelve"];
const word = n => WORDS[n];
const cap = s => s[0].toUpperCase() + s.slice(1);
const list = a => (a.length === 1 ? a[0] : a.slice(0, -1).join(", ") + " and " + a[a.length - 1]);

const BANKS = ["Albion Bank", "Kestrel Bank", "Northbridge Bank", "Harlow Bank", "Stanmore Bank"];
const DIVS = [
  { code: "IB", name: "Investment Bank", clients: ["private and public institutions", "medium-sized companies", "global companies"], offer: "capital market products" },
  { code: "PBC", name: "Private and Business Clients", clients: ["private clients", "small businesses"], offer: "investment services" },
  { code: "CB", name: "Corporate Banking", clients: ["large corporations", "public-sector bodies"], offer: "loans and cash management" },
  { code: "WM", name: "Wealth Management", clients: ["wealthy private clients", "family offices"], offer: "portfolio management" },
  { code: "EI", name: "Estate Investments", clients: ["institutional investors", "pension funds"], offer: "investments in real estate and industrial holdings" },
];
const PEOPLE = [["Richard", "Henderson", "m"], ["Gerald", "Watson", "m"], ["Susan", "Gaffney", "f"], ["Frank", "Hill", "m"], ["Amira", "Khalid", "f"], ["Thomas", "Brandt", "m"],
  ["Helen", "Marsh", "f"], ["Daniel", "Okoye", "m"], ["Laura", "Fischer", "f"], ["Martin", "Novak", "m"], ["Claire", "Dubois", "f"], ["Victor", "Lindqvist", "m"]];
const QUALS = ["fully qualified lawyer", "trained economist", "chartered accountant"];
const ROLES = ["legal advisor", "senior manager", "risk analyst", "portfolio manager", "credit officer", "financial consultant"];
const PLACES = ["an English investment bank", "a Swiss private bank", "a German savings bank", "a Dutch insurer"];
const CITIES = ["London", "Dublin", "New York", "Zurich", "Hong Kong", "Paris", "Madrid", "Vienna"];
const BRANCH_CITIES = ["Düsseldorf", "Frankfurt", "Cologne", "Munich", "Hamburg", "Stuttgart"];
const SALE_COUNTRIES = ["the USA", "Canada", "Spain", "Italy", "Poland"];
const SALE_SERVICES = ["client advisory", "management of bank accounts", "investments", "foreign exchange", "mortgage lending"];
const COST_LEVERS = ["the restructuring of measures", "the dismissal of employees", "merging back-office functions", "closing regional offices", "renegotiating supplier contracts"];
const RETURN_LEVERS = ["a rearrangement of the risk assets", "a share buyback", "the sale of non-core holdings"];
const ACQ_NATS = ["English", "Scottish", "Swiss", "Irish", "Dutch"];
const ACQ_NAMES = ["BestConsult", "Ashcombe & Co", "Pryor Private", "Thornfield"];
const RIGHTS = ["the acquisition and free sale of shares", "the exercise of voting rights", "the participation in the company's profits", "attendance at the annual general meeting", "access to information about the company"];
const PERIODS = ["financial quarter", "half-year", "month"];
const PC_OFFERS = ["money investments", "provisions for the future", "capital accumulation", "investment in funds", "pension planning", "insurance products"];
const BC_OFFERS = ["international payment transactions", "interest and currency management", "securitisation", "trade finance", "cash pooling"];
const BIG_OFFERS = ["company financing", "outside capital", "leasing", "government support", "export credit"];
const REGIONS = ["Europe", "the USA", "South America", "Asia", "Africa", "the Middle East"];
const AM_COUNTRIES = ["Australia", "Japan", "Singapore", "Brazil", "Canada", "India", "Mexico", "South Africa"];
const STRONG_COUNTRIES = ["Germany", "France", "the Netherlands", "Austria"];
const HQ_CITIES = ["Frankfurt", "London", "Paris", "Amsterdam", "Vienna"];
// Which region a named country belongs to (used to keep "Cannot say" regions truly unmentioned).
const REGION_OF = { Japan: "Asia", Singapore: "Asia", India: "Asia", "Hong Kong": "Asia", Brazil: "South America", Mexico: "South America", Argentina: "South America", Chile: "South America", Peru: "South America", "South Africa": "Africa" };
const impliedRegions = W => Object.keys(REGION_OF).filter(c => W._text.includes(c.toLowerCase())).map(c => REGION_OF[c]);

function makeWorld(g) {
  const bank = g.pick(BANKS);
  const divs = g.shuffle(DIVS).slice(0, 3).map(d => ({ ...d }));
  divs[0].role = "big"; divs[1].role = "normal"; divs[2].role = "small";
  const ppl = g.shuffle(PEOPLE).slice(0, 5).map(([first, last, sex]) => ({ first, last, name: `${first} ${last}`, sex }));
  const extra = ppl[4];
  const board = ppl.slice(0, 4);
  const cities = g.shuffle(CITIES);
  board.forEach((p, i) => {
    p.boardYears = g.int(2, 8);
    p.qual = g.chance(0.6) ? g.pick(QUALS) : null;
    p.mba = !p.qual;
    p.dr = g.chance(0.5);
    p.role = i === 0 ? "chair" : "director";
    if (i > 0) { p.div = divs[i - 1].code; p.dirYears = p.boardYears + g.int(0, 4); }
  });
  // Careers: A (role + place + years + city), B (role + city), C (traineeship + city stint without a role), D (positions at a consultancy)
  const types = g.shuffle(["A", "B", "C", "D"]);
  board.forEach((p, i) => {
    p.career = types[i]; p.city = cities[i];
    if (p.career === "A") { p.prevRole = g.pick(ROLES); p.prevPlace = g.pick(PLACES); p.prevYears = g.int(3, 9); p.dr = true; }
    if (p.career === "B") p.prevRole = g.pick(ROLES);
    if (p.career === "C") p.branch = g.pick(BRANCH_CITIES);
  });
  const [s1, s2] = g.shuffle(COST_LEVERS), [r1, r2] = g.shuffle(RETURN_LEVERS);
  const fo = g.shuffle(["Europe", "the USA", "Asia"]).slice(0, g.int(2, 3));
  const inv = g.shuffle(REGIONS.filter(r => r !== "Europe"));
  return {
    bank, divs, board, extra,
    umbrellaOverlap: "some",
    sale: { country: g.pick(SALE_COUNTRIES), services: g.shuffle(SALE_SERVICES).slice(0, 3), replaced: "some", freesFor: divs[0].code },
    costs: [s1, s2], returns: [r1, r2],
    acq: { nat: g.pick(ACQ_NATS), name: g.pick(ACQ_NAMES) },
    rights: g.shuffle(RIGHTS).slice(0, 3),
    duties: { strategy: "Board of Directors", goals: "Board of Directors", compensation: "Supervisory Board", profits: "Supervisory Board" },
    period: g.pick(PERIODS),
    pc: g.shuffle(PC_OFFERS).slice(0, 4), bc: g.shuffle(BC_OFFERS).slice(0, 3), big: g.shuffle(BIG_OFFERS).slice(0, 2),
    experts: "optionally", projects: ["regional", "national"],
    invMain: "Europe", invOthers: inv.slice(0, 3),
    amCountries: g.shuffle(AM_COUNTRIES).slice(0, 4), amEurope: "private clients",
    foRegions: fo, pcRegions: g.shuffle(["Western Europe", "the USA", "Australia", "Asia", "Scandinavia"]).slice(0, 3),
    strong: g.pick(STRONG_COUNTRIES), hq: g.pick(HQ_CITIES),
  };
}

/* ---------- tab text ---------- */
const he = p => (p.sex === "f" ? "she" : "he"), his = p => (p.sex === "f" ? "her" : "his");
const full = p => (p.dr ? "Dr. " : "") + p.name;
function qualTxt(p) { return p.qual ? ` and ${p.qual}` : " with an MBA"; }
function careerTxt(W, p) {
  if (p.career === "A") return `After completing ${his(p)} PhD, ${he(p)} worked as a ${p.prevRole} for ${p.prevPlace} for ${word(p.prevYears)} years in ${p.city}.`;
  if (p.career === "B") return `${cap(he(p))} started off working as a ${p.prevRole} in ${p.city} before ${he(p)} joined ${W.bank}.`;
  if (p.career === "C") return `After ${his(p)} traineeship in a bank and after spending several years in ${p.city}, ${he(p)} became one of the directors of ${W.bank}'s ${p.branch} branch.`;
  return `${cap(he(p))} held the positions of manager, director, and partner in a big consultancy company in ${p.city} before ${he(p)} joined ${W.bank}.`;
}
function renderTabs(W) {
  const [big, normal, small] = W.divs, B = W.bank;
  const para = (h, t) => ({ h, t });
  return {
    structure: [
      para("Umbrella organisation", `It supports the Board of Directors in managing the entire bank. Some members of the umbrella organisation are simultaneously members of the Board of Directors. ${W.extra.name} is one of the members of the Board of Directors. Subordinated to the umbrella organisation are three divisions:`),
      para(`${big.name} (${big.code})`, `This division is the biggest and most important one of ${B} and serves ${list(big.clients)}. The focus of the client segments is mostly in Europe but is also in other countries of the world.`),
      para(`${normal.name} (${normal.code})`, `Clients are normally ${list(normal.clients)}. Every client has their own contact person. ${normal.code} offers ${normal.offer} on a worldwide basis.`),
      para(`${small.name} (${small.code})`, `${small.code} specialises in ${small.offer}. Although this division is rather insignificant, the group will not withdraw from this sector in the foreseeable future as it is of strategic importance.`),
    ],
    strategy: [
      para("Concentration on the core business", ""),
      para("Sale", `${B} sold branch offices in ${W.sale.country} that offered services like ${list(W.sale.services)}. Some of these services were replaced by online banking. Numerous advisory services were outsourced in order to release resources for the ${W.sale.freesFor} division.`),
      para("Restructuring", `Costs could be decreased by ${W.costs[0]} or ${W.costs[1]}. The return on net assets could be increased by ${W.returns[0]} and ${W.returns[1]}.`),
      para("Acquisitions", `To provide private clients with a more individual advisory service, ${B} acquired the ${W.acq.nat} private bank ${W.acq.name}, which is a leader in this sector and has a wide range of experience in investments for private clients.`),
    ],
    principles: [
      para("Company principles", "All divisions and umbrella organisations as well as investment advisors are obliged to comply with these principles. They include:"),
      para("Shareholders' rights", `Shareholders' rights include ${list(W.rights)}.`),
      para("Duties of the Board of Directors and Supervisory Board", `They are obliged to comply with the interests of ${B}. The Board of Directors decides on the strategy of the company and is in charge of all issues relating to the achievement of ${B}'s goals. Additionally, the Board of Directors has to inform the Supervisory Board about the situation of the group on a regular basis. When the Board of Directors decides on the appropriation of the company's profits, the Supervisory Board must approve it.`),
      para("Compensation", "The compensation of the members of the Board of Directors and of the senior managers of the group will be determined by the Supervisory Board."),
      para("Transparency", `Is ensured if financial reports are provided in a timely manner, optimally every ${W.period}, and also if major decisions relating to the company's strategy are brought before the Supervisory Board in order to be approved.`),
    ],
    products: [
      para("Private clients", `Private clients are offered ${W.pc[0]} and ${W.pc[1]}. In addition to the management of bank accounts, they are also offered services for ${W.pc[2]} and ${W.pc[3]}.`),
      para("Business clients", `${B} supports self-employed people and family businesses in the financing and safeguarding of their companies. ${B} offers the services of ${list(W.bc)}, due to the globalisation of many companies.`),
      para("Big corporations", `For big corporations, ${B} offers programmes for ${W.big[0]} and ${W.big[1]}. Industry experts may carry out credit checks and then optionally accompany repositioning efforts. All products and services are designed either for regional or national projects.`),
      para("Investments", `Investments are enabled mainly by equity and bond funds in Europe but are also offered in ${list(W.invOthers)}. The hedge funds of ${B} offer the chance of high returns in a very short time period.`),
    ],
    locations: [
      para("Asset management", `In Europe, the bank offers its investment services mainly to private clients but also to small businesses. In ${list(W.amCountries)}, they are offered mainly to big corporations.`),
      para("Investment funds/options", `Investment funds and options are offered in ${list(W.foRegions)}. In countries where it offers options, ${B} also offers real estate funds.`),
      para("Private clients", `The regional focuses are in ${list(W.pcRegions)}. Investments are made both in their own products and outside products.`),
      para("Regional focus", `In Europe, especially in ${W.strong}, ${B} has a strong position in all company divisions. If the number of employees is taken as a criterion, the most important branch office of ${B} is ${W.hq}.`),
    ],
    board: W.board.map(p => para(full(p), p.role === "chair"
      ? `Chairman of the Board of Directors${qualTxt(p)}. ${cap(he(p))} has been a member of the Board of Directors for ${word(p.boardYears)} years. ${careerTxt(W, p)}`
      : `Director of the ${p.div} division${qualTxt(p)}. ${careerTxt(W, p)} ${cap(he(p))} has been the director of the ${p.div} division for the past ${word(p.dirYears)} years and has been a member of the Board of Directors for the past ${word(p.boardYears)} years.`)),
  };
}
const VTABS = [
  { key: "structure", title: "Structure" }, { key: "strategy", title: "Strategy" }, { key: "principles", title: "Principles" },
  { key: "products", title: "Products & Services" }, { key: "locations", title: "Locations" }, { key: "board", title: "Board of Directors" },
];

/* ---------- statement helpers ---------- */
// Atoms: {k, path, say, ...}. `path` points into the world; `say` is what the statement claims.
const A = {
  eq: (path, say) => ({ k: "eq", path, say }),
  has: (path, say) => ({ k: "has", path, say }),
  only: (path, say) => ({ k: "only", path, say }),
  cmp: (l, op, r) => ({ k: "cmp", l, op, r }),
  novel: say => ({ k: "novel", say }),
};
function V(tab, kind, text, answer, atoms, expl) { return { tab, kind, text, answer, atoms, expl }; }
const other = (g, a, x) => g.pick(a.filter(v => v !== x));
// A detail for a Cannot-say statement: unused, and not mentioned anywhere in the six tabs ("Africa" is out if a tab says "South Africa").
const fresh = (g, pool, used, W) => { const c = pool.filter(v => !used.includes(v) && !W._text.includes(v.toLowerCase())); return c.length ? g.pick(c) : null; };
const person = (W, i) => W.board[i];

/* Templates: (g, W, want) -> statement or null.  want "T" | "F" | "C". */
const VT = {
  structure: [
    { id: "s-biggest", ans: "TF", f(g, W, want) {
      const d = want === "T" ? W.divs[0] : g.pick(W.divs.slice(1));
      return V("structure", "detail swap", `The ${d.code} division is the biggest and most important division of ${W.bank}.`, d.role === "big" ? "T" : "F",
        [A.eq(["divRole", d.code], "big")], `Structure: ${W.divs[0].code} is "the biggest and most important one". Only one division can be the biggest.`);
    } },
    { id: "s-withdraw", ans: "TF", f(g, W, want) {
      const d = W.divs[2];
      if (want === "T") return V("structure", "paraphrase", `Although the ${d.code} division is rather insignificant, ${W.bank} intends to stay in this sector for the foreseeable future.`, "T",
        [A.eq(["divRole", d.code], "small"), A.eq(["withdraw"], "no")], `Structure: "the group will not withdraw from this sector in the foreseeable future".`);
      return V("structure", "contradiction", `Because the ${d.code} division is rather insignificant, ${W.bank} plans to withdraw from this sector soon.`, "F",
        [A.eq(["divRole", d.code], "small"), A.eq(["withdraw"], "yes")], `The text says the opposite: the group will not withdraw in the foreseeable future.`);
    } },
    { id: "s-umbrella-members", ans: "TF", f(g, W, want) {
      const say = want === "T" ? "some" : "all";
      return V("structure", want === "T" ? "paraphrase" : "absolute word", want === "T" ? `At least some members of the umbrella organisation also sit on the Board of Directors.` : `All members of the umbrella organisation also sit on the Board of Directors.`, say === W.umbrellaOverlap ? "T" : "F",
        [A.eq(["umbrellaOverlap"], say)], `Structure: "Some members of the umbrella organisation are simultaneously members of the Board of Directors."`);
    } },
    { id: "s-clients", ans: "TF", f(g, W, want) {
      const d = W.divs[1];
      if (want === "T") { const c = g.pick(d.clients); return V("structure", "paraphrase", `Among the clients of the ${d.name} division are ${c}, and each client has their own contact person.`, "T",
        [A.has(["divClients", d.code], c), A.eq(["contact", d.code], "yes")], `Structure: clients are normally ${list(d.clients)}; every client has their own contact person.`); }
      const c = g.pick(d.clients);
      return V("structure", "absolute word", `All clients of the ${d.name} division are ${c}.`, d.clients.length > 1 ? "F" : "T",
        [A.only(["divClients", d.code], c)], `Structure lists several client groups for ${d.code}: ${list(d.clients)}.`);
    } },
    { id: "s-cs", ans: "C", f(g, W) {
      const k = g.int(0, 2), [, n, s] = W.divs;
      const text = [`${W.bank}'s umbrella organisation supports the Board of Directors with drawing up the annual report.`,
        `The ${n.code} division employs more staff than the ${s.code} division.`,
        `${W.extra.name} chairs the umbrella organisation.`][k];
      const nv = ["annual report", "staff", "chairs"][k];
      return V("structure", ["invented detail", "unsupported comparison", "invented role"][k], text, "C", [A.novel(nv)],
        ["The umbrella organisation supports the Board in managing the bank; an annual report is never mentioned.", "The text gives no staff numbers for divisions.", `${W.extra.name} is named as a Board member; nothing says who chairs the umbrella organisation.`][k]);
    } },
  ],
  board: [
    { id: "b-chair", ans: "TF", f(g, W, want) {
      const i = want === "T" ? 0 : g.int(1, 3), p = person(W, i);
      return V("board", "detail swap", `${p.name} is the Chairman of the Board of Directors.`, i === 0 ? "T" : "F",
        [A.eq(["chair"], p.name)], `Board of Directors: ${person(W, 0).name} is the Chairman; ${i ? `${p.name} is director of the ${p.div} division.` : ""}`);
    } },
    { id: "b-years", ans: "TF", f(g, W, want) {
      const p = person(W, g.int(0, 3)), n = want === "T" ? p.boardYears : other(g, [2, 3, 4, 5, 6, 7, 8, 9], p.boardYears);
      return V("board", "number", `${p.name} has been a member of the Board of Directors for ${word(n)} years.`, n === p.boardYears ? "T" : "F",
        [A.cmp(["boardYears", p.name], "==", n)], `Board of Directors: ${p.name}, ${word(p.boardYears)} years on the Board.`);
    } },
    { id: "b-longer", ans: "TF", f(g, W, want) {
      for (let k = 0; k < 10; k++) {
        const [a, b] = g.shuffle(W.board).slice(0, 2), ok = a.boardYears > b.boardYears;
        if (ok !== (want === "T")) continue;
        return V("board", "comparison", `${a.name} has been on the Board of Directors for longer than ${b.name}.`, ok ? "T" : "F",
          [A.cmp(["boardYears", a.name], ">", ["boardYears", b.name])], `${a.last}: ${word(a.boardYears)} years; ${b.last}: ${word(b.boardYears)} years.`);
      }
      return null;
    } },
    { id: "b-before-board", ans: "TF", f(g, W, want) {
      const ds = W.board.slice(1).filter(p => p.dirYears > p.boardYears);
      if (!ds.length) return null;
      const p = g.pick(ds), k = p.dirYears - p.boardYears, n = want === "T" ? k : other(g, [1, 2, 3, 4, 5].filter(x => x !== k), k);
      return V("board", "inference", `${p.name} had already been director of the ${p.div} division for ${word(n)} year${n === 1 ? "" : "s"} when ${he(p)} joined the Board of Directors.`, n === k ? "T" : "F",
        [A.cmp(["dirMinusBoard", p.name], "==", n)], `Director for the past ${word(p.dirYears)} years, on the Board for the past ${word(p.boardYears)}: ${p.dirYears} − ${p.boardYears} = ${k}.`);
    } },
    { id: "b-prev-role", ans: "TF", f(g, W, want) {
      const p = W.board.find(x => x.career === "A");
      const role = want === "T" ? p.prevRole : other(g, ROLES, p.prevRole);
      return V("board", want === "T" ? "paraphrase" : "detail swap", `${p.name} worked as a ${role} for ${p.prevPlace}.`, role === p.prevRole ? "T" : "F",
        [A.eq(["prevRole", p.name], role)], `Board of Directors: ${p.last} worked as a ${p.prevRole} for ${p.prevPlace}.`);
    } },
    { id: "b-two-part", ans: "TF", f(g, W, want) {
      const p = W.board.find(x => x.career === "A" || x.career === "B");
      const q = g.pick(W.board.filter(x => x !== p && x.boardYears !== p.boardYears));
      if (!q) return null;
      const longer = p.boardYears > q.boardYears;
      const sayLonger = want === "T" ? longer : g.chance(0.5) ? !longer : longer;
      const city = want === "T" || sayLonger !== longer ? p.city : other(g, CITIES, p.city);
      if (want === "F" && sayLonger === longer && city === p.city) return null;
      const atoms = [A.eq(["prevCity", p.name], city), A.cmp(["boardYears", p.name], sayLonger ? ">" : "<", ["boardYears", q.name])];
      const ans = city === p.city && sayLonger === longer ? "T" : "F";
      return V("board", "two-part", `${p.name} worked in ${city} before joining ${W.bank} and has been on the Board of Directors ${sayLonger ? "longer" : "for less time"} than ${q.name}.`, ans,
        atoms, `Both halves must hold. ${p.last} worked in ${p.city}; Board years: ${p.last} ${p.boardYears}, ${q.last} ${q.boardYears}.`);
    } },
    { id: "b-cs", ans: "C", f(g, W) {
      const c = W.board.find(x => x.career === "C"), k = g.int(0, 1);
      if (k === 0) {
        const role = g.pick(["customer consultant", "currency trader", "branch manager"]);
        return V("board", "invented purpose", `${c.name} went to ${c.city} after ${his(c)} traineeship in order to work as a ${role}.`, "C",
          [A.has(["prevCity", c.name], c.city), A.novel(role)], `${c.last} did spend several years in ${c.city}, but the text never says what ${he(c)} did there.`);
      }
      const p = g.pick(W.board), city = fresh(g, CITIES, W.board.map(x => x.city), W);
      return V("board", "invented detail", `${p.name} completed ${his(p)} studies in ${city}.`, "C", [A.novel(city)], `The Board of Directors tab says nothing about where anyone studied.`);
    } },
  ],
  strategy: [
    { id: "t-only-return", ans: "F", f(g, W) {
      const r = g.pick(W.returns);
      return V("strategy", "absolute word", `The return on net assets could only be increased through ${r}.`, "F",
        [A.only(["returns"], r)], `Strategy names two ways: ${W.returns[0]} and ${W.returns[1]}.`);
    } },
    { id: "t-outsourcing", ans: "T", f(g, W) {
      const k = g.int(0, 1);
      return V("strategy", "paraphrase", k === 0 ? `In line with the focus on the core business, the outsourcing of advisory services should free up resources for another division of ${W.bank}.` : `Advisory services were outsourced so that the ${W.sale.freesFor} division would have more resources.`, "T",
        [A.eq(["freesFor"], W.sale.freesFor)], `Strategy: advisory services were outsourced "in order to release resources for the ${W.sale.freesFor} division".`);
    } },
    { id: "t-replaced", ans: "TF", f(g, W, want) {
      const say = want === "T" ? "some" : "all";
      return V("strategy", want === "T" ? "paraphrase" : "absolute word", `${cap(say)} of the services offered by the branch offices sold in ${W.sale.country} were replaced by online banking.`, say === W.sale.replaced ? "T" : "F",
        [A.eq(["saleCountry"], W.sale.country), A.eq(["replaced"], say)], `Strategy: "Some of these services were replaced by online banking."`);
    } },
    { id: "t-acq-nat", ans: "TF", f(g, W, want) {
      const nat = want === "T" ? W.acq.nat : other(g, ACQ_NATS, W.acq.nat);
      return V("strategy", "detail swap", `${W.bank} acquired the ${nat} private bank ${W.acq.name} to give private clients a more individual advisory service.`, nat === W.acq.nat ? "T" : "F",
        [A.eq(["acqNat"], nat), A.eq(["acqName"], W.acq.name)], `Strategy: ${W.acq.name} is ${/^[AEIOU]/.test(W.acq.nat) ? "an" : "a"} ${W.acq.nat} private bank.`);
    } },
    { id: "t-costs", ans: "TC", f(g, W, want) {
      const lever = want === "T" ? g.pick(W.costs) : fresh(g, COST_LEVERS, W.costs, W);
      if (!lever) return null;
      return V("strategy", want === "T" ? "paraphrase" : "invented detail", `According to the strategy, costs could be reduced by ${lever}.`, W.costs.includes(lever) ? "T" : "C",
        [W.costs.includes(lever) ? A.has(["costs"], lever) : A.novel(lever)], `Strategy names ${W.costs[0]} or ${W.costs[1]}${W.costs.includes(lever) ? "." : "; nothing about " + lever + "."}`);
    } },
    { id: "t-cs", ans: "C", f(g, W) {
      const k = g.int(0, 2);
      const c = fresh(g, SALE_COUNTRIES, [W.sale.country], W);
      if (k === 0 && !c) return null;
      const text = [`${W.bank} also closed branch offices in ${c}.`, `${W.bank} acquired ${W.acq.name} in order to expand into Asia.`, `As a result of the restructuring, the ${W.divs[0].code} division was changed from a line to a matrix organisation.`][k];
      return V("strategy", ["invented detail", "invented purpose", "invented detail"][k], text, "C", [A.novel(["closed", "expand into", "matrix"][k])],
        [`Only the sale of branches in ${W.sale.country} is mentioned.`, "The stated purpose is a more individual advisory service for private clients; expansion into Asia is never mentioned.", "The restructuring section says nothing about the organisation structure."][k]);
    } },
  ],
  principles: [
    { id: "p-strategy-body", ans: "TF", f(g, W, want) {
      const body = want === "T" ? "Board of Directors" : "Supervisory Board", k = g.int(0, 1);
      const text = k === 0 ? `According to the company principles, the ${body} decides on the strategy of the company.` : `According to the company principles, the ${body} is responsible for all issues relating to the achievement of the group's goals.`;
      return V("principles", "detail swap", text, body === W.duties[k === 0 ? "strategy" : "goals"] ? "T" : "F",
        [A.eq(["duty", k === 0 ? "strategy" : "goals"], body)], `Principles: the Board of Directors decides on strategy and is in charge of all issues relating to the goals.`);
    } },
    { id: "p-compensation", ans: "TF", f(g, W, want) {
      const body = want === "T" ? "Supervisory Board" : "Board of Directors";
      return V("principles", "detail swap", `The compensation of the group's senior managers is determined by the ${body}.`, body === W.duties.compensation ? "T" : "F",
        [A.eq(["duty", "compensation"], body)], `Principles: compensation is "determined by the Supervisory Board".`);
    } },
    { id: "p-two-duties", ans: "TF", f(g, W, want) {
      if (want === "T") return V("principles", "two-part", `The Board of Directors must keep the Supervisory Board regularly informed, and major strategic decisions need the Supervisory Board's approval.`, "T",
        [A.eq(["informs"], "regularly"), A.eq(["strategyApproval"], "Supervisory Board")], `Principles: both are stated (Duties and Transparency).`);
      return V("principles", "two-part", `The Board of Directors must keep the Supervisory Board regularly informed, but it can decide on the appropriation of profits without the Supervisory Board's approval.`, "F",
        [A.eq(["informs"], "regularly"), A.eq(["duty", "profits"], "Board of Directors")], `The first half is true, but the Supervisory Board must approve the appropriation of profits.`);
    } },
    { id: "p-rights", ans: "TC", f(g, W, want) {
      if (want === "T") { const [a] = g.shuffle(W.rights); return V("principles", "paraphrase", `Shareholders' rights include, among other things, ${a}.`, "T", [A.has(["rights"], a)], `Principles: shareholders' rights include ${list(W.rights)}.`); }
      const r = fresh(g, RIGHTS, W.rights, W);
      if (!r) return null;
      return V("principles", "invented detail", `Shareholders' rights include, among other things, ${r}.`, "C", [A.novel(r)], `Principles list ${list(W.rights)}; ${r} is not mentioned, and the list does not claim to be complete.`);
    } },
    { id: "p-period", ans: "TF", f(g, W, want) {
      const per = want === "T" ? W.period : other(g, PERIODS, W.period);
      return V("principles", "detail swap", `To ensure transparency, financial reports should optimally be provided every ${per}.`, per === W.period ? "T" : "F",
        [A.eq(["period"], per)], `Principles: "optimally every ${W.period}".`);
    } },
    { id: "p-cs", ans: "C", f(g, W) {
      const n = g.int(3, 6), k = g.int(0, 1);
      const text = k === 0 ? `According to the company principles, the Board of Directors can decide on a change of strategy every ${word(n)} years.` : `Investment advisors who break the company principles are dismissed.`;
      return V("principles", "invented detail", text, "C", [A.novel(k === 0 ? `every ${word(n)} years` : "dismissed")],
        k === 0 ? "The Board decides on strategy, but no time frame is given." : "Advisors must comply with the principles; consequences are never mentioned.");
    } },
  ],
  products: [
    { id: "r-business-clients", ans: "T", f(g, W) {
      return V("products", "paraphrase", `Business clients of ${W.bank} include self-employed people and family businesses.`, "T", [A.eq(["bcWho"], "self-employed people and family businesses")], `Products & Services: "${W.bank} supports self-employed people and family businesses".`);
    } },
    { id: "r-experts", ans: "TF", f(g, W, want) {
      const say = want === "T" ? "optionally" : "always";
      return V("products", want === "T" ? "paraphrase" : "absolute word", want === "T" ? `For big corporations, industry experts may carry out credit checks and can also support repositioning efforts.` : `For big corporations, industry experts always accompany repositioning efforts after a credit check.`, say === W.experts ? "T" : "F",
        [A.eq(["experts"], say)], `Products & Services: experts "may carry out credit checks and then optionally accompany repositioning efforts".`);
    } },
    { id: "r-projects", ans: "TF", f(g, W, want) {
      const say = want === "T" ? "national" : "international";
      return V("products", want === "T" ? "paraphrase" : "detail swap", want === "T" ? `Some of the products for big corporations may be designed for national projects.` : `Products and services for big corporations are designed for international projects.`, W.projects.includes(say) ? "T" : "F",
        [A.eq(["projectsInclude"], say)], `Products & Services: "All products and services are designed either for regional or national projects."`);
    } },
    { id: "r-hedge", ans: "TF", f(g, W, want) {
      const say = want === "T" ? "chance" : "guarantee";
      return V("products", want === "T" ? "paraphrase" : "detail swap", `The hedge funds of ${W.bank} ${want === "T" ? "offer the possibility of" : "guarantee"} high returns within a very short time.`, say === "chance" ? "T" : "F",
        [A.eq(["hedge"], say)], `Products & Services: hedge funds "offer the chance of high returns".`);
    } },
    { id: "r-investment-region", ans: "TC", f(g, W, want) {
      const r = want === "T" ? g.pick(W.invOthers) : fresh(g, REGIONS, ["Europe"].concat(W.invOthers, W.foRegions, impliedRegions(W)), W);
      if (!r) return null;
      return V("products", want === "T" ? "paraphrase" : "invented detail", `${W.bank}'s investments are also offered in ${r}.`, W.invOthers.includes(r) ? "T" : "C",
        [W.invOthers.includes(r) ? A.has(["invOthers"], r) : A.novel(r)], `Products & Services: investments are mainly in Europe but also offered in ${list(W.invOthers)}.`);
    } },
    { id: "r-cs", ans: "C", f(g, W) {
      const k = g.int(0, 3);
      const text = [`${W.bank}'s industry experts can advise business clients, but not big corporations, as consultants during the acquisition of another company.`,
        `The equity funds offered by ${W.bank} are checked regularly for their return on investment.`,
        `Private clients of ${W.bank} pay no fees for the management of their bank accounts.`,
        `Self-employed people receive lower interest rates on financing than big corporations.`][k];
      return V("products", "invented detail", text, "C", [A.novel(["acquisition of another company", "checked regularly", "fees", "interest rates"][k])],
        ["Experts do credit checks and repositioning for big corporations; advice on acquisitions is never mentioned.", "Nothing is said about checking fund returns.", "Account management is offered; fees are never mentioned.", "No interest rates are given for any client group."][k]);
    } },
  ],
  locations: [
    { id: "l-am-segment", ans: "TF", f(g, W, want) {
      const c = g.pick(W.amCountries), seg = want === "T" ? "big corporations" : "private clients";
      return V("locations", "detail swap", `In ${c}, asset management is offered mainly to ${seg}.`, seg === "big corporations" ? "T" : "F",
        [A.eq(["amSegment", c], seg)], `Locations: in ${list(W.amCountries)} it is offered mainly to big corporations (private clients are the focus in Europe).`);
    } },
    { id: "l-real-estate", ans: "TC", f(g, W, want) {
      const r = want === "T" ? g.pick(W.foRegions) : fresh(g, ["Europe", "the USA", "Asia"], W.foRegions.concat(W.invOthers, impliedRegions(W)), W);
      if (!r) return null;
      return V("locations", want === "T" ? "inference" : "reversed rule", want === "T" ? `${W.bank} offers real estate funds in ${r}.` : `${W.bank} offers real estate funds in ${r}.`, W.foRegions.includes(r) ? "T" : "C",
        [A.eq(["realEstateIn", r], "yes")], W.foRegions.includes(r) ? `Options are offered in ${r}, and wherever options are offered, real estate funds are too.` : `Options are offered only in ${list(W.foRegions)}; nothing tells us about real estate funds in ${r}.`);
    } },
    { id: "l-converse", ans: "C", f(g, W) {
      return V("locations", "reversed rule", `In every country where ${W.bank} offers real estate funds, it also offers options.`, "C",
        [A.eq(["converseRule"], "yes")], `The rule only goes one way: options → real estate funds. The reverse is not stated.`);
    } },
    { id: "l-branch", ans: "TFC", f(g, W, want) {
      if (want === "C") return V("locations", "criterion swap", `${W.hq} is ${W.bank}'s most profitable branch office.`, "C", [A.novel("profitable")], `${W.hq} is the most important branch by number of employees; profit is never mentioned.`);
      const city = want === "T" ? W.hq : other(g, HQ_CITIES, W.hq);
      return V("locations", "detail swap", `Measured by the number of employees, ${city} is ${W.bank}'s most important branch office.`, city === W.hq ? "T" : "F",
        [A.eq(["hq"], city)], `Locations: by number of employees, the most important branch is ${W.hq}.`);
    } },
    { id: "l-cs", ans: "C", f(g, W) {
      const c = fresh(g, AM_COUNTRIES.concat(["Argentina", "Chile", "Peru"]), W.amCountries, W);
      return V("locations", "invented detail", `Asset management outside Europe is primarily offered in ${c}.`, "C", [A.novel(c)], `Locations names ${list(W.amCountries)} outside Europe and never ranks them; ${c} is not mentioned.`);
    } },
  ],
};

/* Answer derived from the world (used by the generator only to label; verify-verbal.js re-derives independently). */
function makeVerbalTest(seed, n) {
  n = n || 18;
  const g = Rng(seed ^ 0x5eed), W = makeWorld(g), tabs = renderTabs(W);
  W._text = Object.values(tabs).flat().map(p => p.h + ". " + p.t).join("\n").toLowerCase();
  const nCs = Math.round(n * (0.39 + g.f() * 0.11));
  const nT = Math.round((n - nCs) / 2) + g.pick([-1, 0, 1]), nF = n - nCs - nT;
  const wants = g.shuffle([].concat(Array(nCs).fill("C"), Array(nT).fill("T"), Array(nF).fill("F")));
  const slots = g.shuffle([].concat(...VTABS.map(t => Array(Math.ceil(n / 6)).fill(t.key)))).slice(0, n);
  const out = [], seen = new Set(), used = new Map();
  for (let s = 0; s < n; s++) {
    let made = null, want = wants[s];
    for (let attempt = 0; attempt < 300 && !made; attempt++) {
      if (attempt === 150) { const rest = wants.slice(s + 1); const swap = rest.findIndex(w => VT[slots[s]].some(t => t.ans.includes(w) && !t.ans.includes(want))); if (swap >= 0) { const j = s + 1 + swap; [wants[s], wants[j]] = [wants[j], wants[s]]; want = wants[s]; } }
      const pool = VT[slots[s]].filter(t => t.ans.includes(want));
      if (!pool.length) continue;
      const lo = Math.min(...pool.map(t => used.get(t.id) || 0));
      const slack = attempt > 200 ? Infinity : attempt > 60 ? 1 : 0;      // prefer unused templates, but never starve one
      const t = g.pick(pool.filter(x => (used.get(x.id) || 0) <= lo + slack));
      const st = t.f(g, W, want);
      if (!st || st.answer !== want || seen.has(st.text)) continue;
      st.template = t.id; made = st; used.set(t.id, (used.get(t.id) || 0) + 1);
    }
    if (!made) throw new Error("verbal: could not fill slot " + s + " (" + slots[s] + ", want " + want + ")");
    seen.add(made.text); out.push(made);
  }
  return { seed, world: W, tabs, items: out };
}

const API = { makeVerbalTest, makeWorld, renderTabs, VTABS, VT };
if (typeof module !== "undefined" && module.exports) module.exports = API; else root.AonVerbal = API;
})(this);
