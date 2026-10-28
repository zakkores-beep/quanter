# Aon Sprint (Aon-style numerical and verbal practice)

Live page: https://claude.ai/artifact/E8nbR9Vrx9pp6fRmgzXn5p

The page has two sections, both modelled on the Fidelity / Aon mocks (18 True / False / Cannot say statements, 6 tabs, 6 minutes).

Numerical:
- six data tabs: mail order, profit donut, price list, expenses line chart, working hours, employees bar chart
- 18 True / False / Cannot say statements in 6 minutes
- fresh data on every attempt

Files:
- `gen.js`: numerical data and statement generator (pure logic, money in integer pence)
- `verbal.js`: verbal generator. Builds a fictional bank as structured facts, writes the six text tabs from them, and builds every statement from labelled claims (atoms)
- `verify-verbal.js`: independent verbal checker. Re-derives each answer from the facts and the printed tab text, confirms every Cannot-say detail (including the regions of any named country) is absent from all six tabs, and checks the mix. `MUTATE=1` proves it catches wrong answers.
- `index.src.html`: page template; `node build.js` inlines gen.js and verbal.js into `index.html`
- `verify.js`: independent checker. `node verify.js 20000` checks 20,000 tests, and `MUTATE=1 node verify.js 500` proves it catches flipped answers.

For each statement the verifier:
- recomputes the answer from the raw data with its own code
- checks the text names the same cells, weight band, service, period and number
- checks Cannot-say statements point at information no tab holds
- checks a/an grammar

It also checks each data pack (shares sum to 100, totals add up, bands don't overlap, axes cover the data) and each test's mix (3 statements per tab, 3–7 Cannot say, at least 4 True and 4 False, no duplicates).
