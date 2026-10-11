# Coding trainer: Software Fundamentals (30 min, Python)

40 problems with a local judge. Needs Python 3.9+ and nothing else (no pip installs).

```bash
cd coding
python judge.py --list          # problems + your progress
python judge.py 7               # first run creates work/07_best_k_window.py from the starter
                                # edit it, then run again to judge
python judge.py 7 --show        # reveal failing inputs / expected / your output
python judge.py --mock          # 1 easy + 1 medium, 30-minute timer, auto-submit at 0:00
```

- Read the problem in `problems/<id>_<name>/statement.md` and write your code in `work/`. That folder is git-ignored, and your progress is saved in `work/progress.json`.
- Linked-list and tree problems: `from lib import ListNode, TreeNode` (see `lib.py`).
- **Don't open `solutions/` or `tests/` while practising.**
- Verdicts:
  - `PASS`
  - `WA`: wrong answer
  - `TLE`: too slow
  - `RE`: crash, with the traceback shown
- Each problem has one `perf` test with a large input, so an O(n^2) solution where O(n) is expected fails it.
- Python's default recursion limit (1000) applies, as on HackerRank, so deep recursion crashes. If your laptop is much slower than average, add `--tl-scale 1.5` to give yourself more time.

## Problems

| Topic | Problems (E = easy, M = medium) |
|---|---|
| arrays & hashing | 1 Matching Trade Pairs (E); 2 Longest Active Streak (M); 3 P&L Windows Hitting Target (M) |
| two pointers | 4 Almost a Palindrome (E); 5 Zero-Sum Hedge Triplets (M); 6 Widest Price Channel (M) |
| sliding window | 7 Best k-Day Window (E); 8 Longest Run Without Repeats (M); 9 Shortest Window to Fill an Order (M) |
| stack | 10 Balanced Brackets (E); 11 Days Until a Higher Price (M); 12 Colliding Orders (M) |
| binary search | 13 Price Range Queries (E); 14 Minimum Settlement Capacity (M); 15 Integer Square Roots (E) |
| linked lists | 16 Reverse a Linked List (E); 17 Merge Two Sorted Lists (E); 18 Interleave a Linked List (M) |
| trees (BFS/DFS) | 19 Depth of a Binary Tree (E); 20 Level-by-Level Report (M); 21 Validate a Search Tree (M) |
| heaps | 22 k-th Largest Fill (E); 23 Most Traded Tickers (M); 24 Merge Sorted Order Feeds (M) |
| intervals | 25 Merge Trading Sessions (M); 26 Insert a Blackout Window (M); 27 Meeting Rooms Needed (M) |
| greedy | 28 Unlimited Round Trips (E); 29 Reach the Last Checkpoint (M); 30 Circular Funding Route (M) |
| 1-D dynamic programming | 31 Non-Adjacent Trading Days (M); 32 Fewest Lots (M); 33 Longest Rising Subsequence (M) |
| 2-D dynamic programming | 34 Paths Through a Blocked Grid (M); 35 Ticker Edit Distance (M); 36 Longest Common Subsequence (M) |
| graphs | 37 Count the Islands (M); 38 Dependency Order (M); 39 Shortest Route Across the Floor (M); 40 Cheapest Currency Route (M) |

The statements, examples and tests are written for this trainer; none are copied from leaked assessments. The underlying patterns are the standard ones (sliding window, monotonic stack, Dijkstra, ...), which is exactly what the real test draws on, so many have well-known LeetCode cousins.

## How the answers are verified

`python verify.py` (about 4 min) checks every problem:

1. **Tests and statements regenerate exactly.** `build.py` rebuilds every expected output from the reference solution, and each must also match an independent brute force. Statement examples go through the same check.
2. **Every input satisfies the stated constraints**, checked by `valid()` in each spec. This caught one bad edge case during the build.
3. **Enough tests:** at least 15 per problem, with exactly one perf test.
4. **Varied answers:** the tests have at least 2 distinct answers, and both True and False for yes/no problems.
5. **The reference passes all tests through the real judge**, using at most 1/4 of the perf time limit.
6. **Brute force agrees with the reference** on 500 fresh random inputs.
7. **The starter file runs** without crashing.

`python selftest.py` runs 15 realistic wrong solutions, such as these, and checks that the tests reject every one:
- greedy coin change
- a BST check that only looks at direct children
- float `sqrt`
- recursive DFS
- an O(n^2) longest increasing subsequence

The latest results are in `verify_report.txt`. They were checked on Python 3.9, 3.11, 3.12 and 3.13, which all produce identical tests.

## Layout

```
specs/       problem definitions: statement, constraints, input generators, valid()
solutions/   reference + brute force for each problem   (don't peek)
tests/       generated hidden tests                       (don't peek)
problems/    generated statement.md + starter.py
judge.py  build.py  verify.py  selftest.py  runner.py  common.py  lib.py  gentools.py
```
