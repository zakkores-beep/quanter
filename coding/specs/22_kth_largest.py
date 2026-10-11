from gentools import grid, ints, nondecreasing, size, tree  # noqa: F401
ID = 22
TITLE = "k-th Largest Fill"
LEVEL = "easy"
TOPIC = "heaps"
FUNC = "kth_largest"
SIGNATURE = "def kth_largest(fills: list[int], k: int) -> int:"
STATEMENT = """
Return the `k`-th largest value in `fills` (counting duplicates, so for
`[7, 7, 1]` the 2nd largest is 7).

Try a min-heap of size `k` (`heapq`) instead of sorting everything.
"""
CONSTRAINTS = """
- `1 <= k <= len(fills) <= 2 * 10**5`
- `-10**9 <= fills[i] <= 10**9`
"""
EXAMPLES = [dict(fills=[7, 7, 7, 1], k=2), dict(fills=[3, 1, 4, 1, 5, 9, 2, 6], k=3)]


def edge_cases():
    return [dict(fills=[5], k=1), dict(fills=[1, 2, 3, 4], k=4), dict(fills=[1, 2, 3, 4], k=1),
            dict(fills=[-1, -1, -2], k=3), dict(fills=[10**9, -10**9, 0], k=2)]


def random_case(rng):
    n = rng.randint(1, 12)
    return dict(fills=[rng.randint(-5, 5) for _ in range(n)], k=rng.randint(1, n))


def perf_case(rng):
    return dict(fills=[rng.randint(-10**9, 10**9) for _ in range(200000)], k=100000)


def valid(c):
    """Does this input satisfy the stated constraints?"""
    return 1 <= c['k'] <= len(c['fills']) <= 2 * 10**5 and ints(c['fills'], -10**9, 10**9)
