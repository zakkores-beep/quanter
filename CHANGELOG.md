# Changelog

## Phase 0: Research (2026-10-11)
- Added FORMAT.md, which summarises the GS Engineering OA format from the official guide plus candidate reports.
- Defaults chosen:
  - Fundamentals: 2 problems in 30 min (1 easy + 1 medium)
  - Math: 10 MCQs in 22 min
  - Diagnostics: 1 Django bug in 45 min
- Environment where the trainers are built and verified: Python 3.13.16, Node 22.22.0.

## Phase 1: Coding trainer (2026-10-11)
At your request, built this before the math and diagnostics trainers.
- `coding/`: 40 original problems across 13 topics (11 easy, 29 medium), plus:
  - a local judge with per-test process isolation, time limits and `--show`
  - `--mock` mode: 1 easy + 1 medium problem, 30 min, auto-submit
  - progress tracking
- **Verification** (`python verify.py`, Python 3.13): 40/40 problems OK.
  - 15-16 tests per problem; reference passes all of them.
  - Brute force agrees with the reference on 500/500 random inputs per problem (20,000 total).
  - Every input satisfies the stated constraints.
  - Reference uses at most 1/4 of each perf time limit.
  - Brute force fails the perf test in 30/40 problems. In the other 10 the naive approach is already near-linear, so the perf test there only guards against crashes and pathological solutions.
- **Mutation self-test** (`python selftest.py`): 15/15 realistic wrong solutions rejected with the expected verdict (WA / TLE / RE).
- **Cross-version:** identical tests regenerate on Python 3.9, 3.11, 3.12 and 3.13.
- **Bugs fixed during verification:**
  - An edge case in problem 15 (`2**60`) exceeded the stated `10**18` constraint. Replaced it, and added `valid()` constraint checks to every spec.
  - Time limits raised for problems 13, 38 and 40 to keep at least 4x headroom.

## Numerical Sprint: Aon numerical trainer (2026-10-28)
- New page at https://claude.ai/artifact/E8nbR9Vrx9pp6fRmgzXn5p, built from the user's Fidelity numerical mock (6 tabs, 18 statements, 6 minutes). The existing Fidelity Aon Trainer artifact was left untouched.
- **Verification** (`node aon-numerical/verify.js 20000`):
  - 20,000 tests, 360,000 statements, 0 failures, with at least 7,000 checks for each of 30 statement templates.
  - Answer mix: 37% True, 35% False, 28% Cannot say (the mock had 4 of 14 Cannot say).
- **Mutation check:** flipping every answer on 500 tests was caught 9,000 / 9,000 times.
- **Bugs fixed during verification:**
  - "a air filter" and "a 8 / 11 / 18 kilo parcel" became "an …".
  - A verifier gap for "Last year" Cannot-say wording.
  - Chart labels overlapping on the expenses chart.
  - A missing hidden-screen rule.
