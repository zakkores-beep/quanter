"""Mutation self-test: realistic WRONG solutions must be rejected by the tests.

Each mutant is a typical mistake (off-by-one, greedy where DP is needed,
recursion too deep, quadratic time, ...). The test suite must fail it with
the expected kind of verdict. If a mutant passes, the tests are too weak.

    python selftest.py
"""
import os
import sys
import tempfile

from common import TESTS, resolve
from judge import load_json, run_one

MUTANTS = [
    ("5", "WA", "counts index triplets instead of distinct value triplets", """
from itertools import combinations
def count_zero_triplets(nums):
    return sum(1 for c in combinations(nums, 3) if sum(c) == 0)
"""),
    ("7", "TLE", "re-sums every window: O(n*k)", """
def best_window(pnl, k):
    return max(sum(pnl[i:i + k]) for i in range(len(pnl) - k + 1))
"""),
    ("8", "WA", "moves the window start backwards on 'abba'", """
def longest_unique(s):
    last, start, best = {}, 0, 0
    for i, ch in enumerate(s):
        if ch in last:
            start = last[ch] + 1
        last[ch] = i
        best = max(best, i - start + 1)
    return best
"""),
    ("10", "WA", "only counts brackets per type, ignores order", """
def is_balanced(s):
    return all(s.count(o) == s.count(c) for o, c in ("()", "[]", "{}"))
"""),
    ("15", "WA", "floating-point square root", """
def isqrt_all(nums):
    return [int(x ** 0.5) for x in nums]
"""),
    ("16", "RE", "recursive reversal exceeds the recursion limit", """
def reverse_list(head):
    if head is None or head.next is None:
        return head
    new_head = reverse_list(head.next)
    head.next.next = head
    head.next = None
    return new_head
"""),
    ("21", "WA", "only compares each node with its direct children", """
def is_valid_bst(root):
    if root is None:
        return True
    if root.left and root.left.val >= root.val:
        return False
    if root.right and root.right.val <= root.val:
        return False
    return is_valid_bst(root.left) and is_valid_bst(root.right)
"""),
    ("25", "WA", "does not merge intervals that only touch", """
def merge_intervals(intervals):
    out = []
    for s, e in sorted(intervals):
        if out and s < out[-1][1]:
            out[-1][1] = max(out[-1][1], e)
        else:
            out.append([s, e])
    return out
"""),
    ("27", "WA", "treats meetings as closed intervals", """
import heapq
def min_rooms(meetings):
    ends = []
    for s, e in sorted(meetings):
        if ends and ends[0] < s:
            heapq.heapreplace(ends, e)
        else:
            heapq.heappush(ends, e)
    return len(ends)
"""),
    ("30", "WA", "forgets the total-gas check, never returns -1", """
def best_start(gas, cost):
    start = tank = 0
    for i in range(len(gas)):
        tank += gas[i] - cost[i]
        if tank < 0:
            start, tank = i + 1, 0
    return start % len(gas)
"""),
    ("31", "WA", "takes the better of even days vs odd days", """
def max_non_adjacent(gains):
    return max(sum(gains[0::2]), sum(gains[1::2]))
"""),
    ("32", "WA", "greedy: always the biggest lot", """
def min_coins(lots, amount):
    count = 0
    for c in sorted(lots, reverse=True):
        count += amount // c
        amount %= c
    return count if amount == 0 else -1
"""),
    ("33", "TLE", "O(n^2) DP", """
def longest_rising(prices):
    best = [1] * len(prices)
    for i in range(len(prices)):
        for j in range(i):
            if prices[j] < prices[i]:
                best[i] = max(best[i], best[j] + 1)
    return max(best, default=0)
"""),
    ("37", "RE", "recursive DFS overflows on a big island", """
def count_islands(grid):
    rows, cols = len(grid), len(grid[0])
    seen = set()
    def dfs(r, c):
        if not (0 <= r < rows and 0 <= c < cols) or grid[r][c] != "1" or (r, c) in seen:
            return
        seen.add((r, c))
        dfs(r + 1, c); dfs(r - 1, c); dfs(r, c + 1); dfs(r, c - 1)
    count = 0
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == "1" and (r, c) not in seen:
                dfs(r, c)
                count += 1
    return count
"""),
    ("40", "WA", "BFS by number of hops, ignoring fees", """
from collections import deque
def cheapest_route(n, fees, src, dst):
    adj = [[] for _ in range(n)]
    for u, v, f in fees:
        adj[u].append((v, f))
    cost = {src: 0}
    q = deque([src])
    while q:
        u = q.popleft()
        for v, f in adj[u]:
            if v not in cost:
                cost[v] = cost[u] + f
                q.append(v)
    return cost.get(dst, -1)
"""),
]


def main():
    caught = 0
    with tempfile.TemporaryDirectory() as tmp:
        for prob, want, why, code in MUTANTS:
            key = resolve(prob)
            path = os.path.join(tmp, key + ".py")
            with open(path, "w") as f:
                f.write(code)
            tests = load_json(os.path.join(TESTS, key + ".json"), None)["tests"]
            verdicts = [run_one(path, key, t)["verdict"] for t in tests]
            failed = sum(v != "PASS" for v in verdicts)
            ok = failed > 0 and want in verdicts
            caught += ok
            print("%-4s %-24s %-3s expected, failed %2d/%d tests  %s   (%s)"
                  % ("OK" if ok else "MISS", key, want, failed, len(tests), "" if ok else verdicts, why))
    print("\n%d/%d wrong solutions rejected with the expected verdict." % (caught, len(MUTANTS)))
    sys.exit(0 if caught == len(MUTANTS) else 1)


if __name__ == "__main__":
    main()
