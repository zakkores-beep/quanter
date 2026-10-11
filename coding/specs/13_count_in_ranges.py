from gentools import grid, ints, nondecreasing, size, tree  # noqa: F401
ID = 13
TITLE = "Price Range Queries"
TIME_LIMIT = 4.0
LEVEL = "easy"
TOPIC = "binary search"
FUNC = "count_in_ranges"
SIGNATURE = "def count_in_ranges(prices: list[int], queries: list[list[int]]) -> list[int]:"
STATEMENT = """
`prices` is sorted in non-decreasing order. Each query is `[lo, hi]` with
`lo <= hi`. For each query, return how many prices `p` satisfy
`lo <= p <= hi`.

You may use the `bisect` module, but practise writing the binary search
yourself too.
"""
CONSTRAINTS = """
- `0 <= len(prices) <= 10**5`, sorted non-decreasing
- `1 <= len(queries) <= 10**5`
- `-10**9 <= prices[i], lo, hi <= 10**9`
"""
EXAMPLES = [dict(prices=[1, 2, 2, 2, 3, 7], queries=[[2, 2], [1, 3], [4, 6], [0, 100]])]


def edge_cases():
    return [dict(prices=[], queries=[[1, 2]]), dict(prices=[5], queries=[[5, 5], [6, 9], [0, 4]]),
            dict(prices=[-3, -3, 0, 4], queries=[[-3, -3], [-10**9, 10**9], [-2, -1]]),
            dict(prices=[2, 2, 2], queries=[[2, 2], [1, 1], [3, 3]])]


def random_case(rng):
    n = rng.randint(0, 12)
    prices = sorted(rng.randint(-5, 5) for _ in range(n))
    queries = []
    for _ in range(rng.randint(1, 5)):
        a, b = rng.randint(-6, 6), rng.randint(-6, 6)
        queries.append([min(a, b), max(a, b)])
    return dict(prices=prices, queries=queries)


def perf_case(rng):
    prices = sorted(rng.randint(-10**9, 10**9) for _ in range(100000))
    queries = []
    for _ in range(100000):
        a, b = rng.randint(-10**9, 10**9), rng.randint(-10**9, 10**9)
        queries.append([min(a, b), max(a, b)])
    return dict(prices=prices, queries=queries)


def valid(c):
    """Does this input satisfy the stated constraints?"""
    return size(c['prices'], 0, 10**5) and nondecreasing(c['prices']) and ints(c['prices'], -10**9, 10**9) and size(c['queries'], 1, 10**5) and all(len(q) == 2 and q[0] <= q[1] and ints(q, -10**9, 10**9) for q in c['queries'])
