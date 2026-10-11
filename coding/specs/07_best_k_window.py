from gentools import grid, ints, nondecreasing, size, tree  # noqa: F401
ID = 7
TITLE = "Best k-Day Window"
LEVEL = "easy"
TOPIC = "sliding window"
FUNC = "best_window"
SIGNATURE = "def best_window(pnl: list[int], k: int) -> int:"
STATEMENT = """
Return the largest total of `k` consecutive values in `pnl`.
"""
CONSTRAINTS = """
- `1 <= k <= len(pnl) <= 2 * 10**5`
- `-10**4 <= pnl[i] <= 10**4`
"""
EXAMPLES = [dict(pnl=[4, -1, 4, -10, 8], k=2), dict(pnl=[-3, -1, -2], k=2)]


def edge_cases():
    return [dict(pnl=[5], k=1), dict(pnl=[1, 2, 3], k=3), dict(pnl=[0, 0, 0, 0], k=2),
            dict(pnl=[-10**4] * 4, k=1), dict(pnl=[1, -5, 1, 1, -5, 1], k=2), dict(pnl=[3, 3, -9, 9], k=3)]


def random_case(rng):
    n = rng.randint(1, 12)
    return dict(pnl=[rng.randint(-10, 10) for _ in range(n)], k=rng.randint(1, n))


def perf_case(rng):
    return dict(pnl=[rng.randint(-10**4, 10**4) for _ in range(200000)], k=100000)


def valid(c):
    """Does this input satisfy the stated constraints?"""
    return 1 <= c['k'] <= len(c['pnl']) <= 2 * 10**5 and ints(c['pnl'], -10**4, 10**4)
