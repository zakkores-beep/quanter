from gentools import grid, ints, nondecreasing, size, tree  # noqa: F401
ID = 3
TITLE = "P&L Windows Hitting Target"
LEVEL = "medium"
TOPIC = "arrays & hashing"
FUNC = "count_subarrays"
SIGNATURE = "def count_subarrays(pnl: list[int], k: int) -> int:"
STATEMENT = """
`pnl[i]` is the profit (possibly negative) on day `i`. Count the contiguous,
non-empty ranges of days whose total profit is exactly `k`.
"""
CONSTRAINTS = """
- `1 <= len(pnl) <= 2 * 10**5`
- `-1000 <= pnl[i] <= 1000`
- `-10**9 <= k <= 10**9`
"""
EXAMPLES = [dict(pnl=[3, 4, 7, -7, 2], k=7), dict(pnl=[1, -1, 1, -1], k=0)]


def edge_cases():
    return [dict(pnl=[0, 0, 0], k=0), dict(pnl=[1], k=1), dict(pnl=[1], k=2), dict(pnl=[-1000] * 5, k=-2000),
            dict(pnl=[5, -5, 5, -5, 5], k=5), dict(pnl=[1, 2, 3], k=10**9)]


def random_case(rng):
    n = rng.randint(1, 12)
    return dict(pnl=[rng.randint(-3, 3) for _ in range(n)], k=rng.randint(-4, 4))


def perf_case(rng):
    return dict(pnl=[rng.randint(-10, 10) for _ in range(200000)], k=5)


def valid(c):
    """Does this input satisfy the stated constraints?"""
    return size(c['pnl'], 1, 2 * 10**5) and ints(c['pnl'], -1000, 1000) and ints([c['k']], -10**9, 10**9)
