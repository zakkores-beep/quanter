from gentools import grid, ints, nondecreasing, size, tree  # noqa: F401
ID = 40
TITLE = "Cheapest Currency Route"
TIME_LIMIT = 6.0
LEVEL = "medium"
TOPIC = "graphs"
FUNC = "cheapest_route"
SIGNATURE = "def cheapest_route(n: int, fees: list[list[int]], src: int, dst: int) -> int:"
STATEMENT = """
There are `n` currencies labelled `0 .. n-1`. Each `[u, v, f]` in `fees` is
a one-way conversion from `u` to `v` costing fee `f >= 0`. Return the lowest
total fee to get from `src` to `dst`, or -1 if `dst` is unreachable.
Converting `src` to itself costs 0.
"""
CONSTRAINTS = """
- `1 <= n <= 10**5`
- `0 <= len(fees) <= 2 * 10**5`
- `0 <= f <= 1000`; parallel conversions may exist
"""
EXAMPLES = [dict(n=3, fees=[[0, 1, 5], [1, 2, 5], [0, 2, 20]], src=0, dst=2), dict(n=2, fees=[[1, 0, 3]], src=0, dst=1)]


def edge_cases():
    return [dict(n=1, fees=[], src=0, dst=0), dict(n=2, fees=[], src=0, dst=1),
            dict(n=3, fees=[[0, 1, 0], [1, 2, 0]], src=0, dst=2), dict(n=2, fees=[[0, 1, 9], [0, 1, 4]], src=0, dst=1),
            dict(n=4, fees=[[0, 1, 1], [1, 0, 1], [2, 3, 1]], src=0, dst=3),
            dict(n=4, fees=[[0, 1, 1], [0, 2, 5], [1, 2, 1], [2, 3, 1], [1, 3, 10]], src=0, dst=3)]


def random_case(rng):
    n = rng.randint(1, 6)
    fees = [[rng.randrange(n), rng.randrange(n), rng.randint(0, 9)] for _ in range(rng.randint(0, 10))]
    return dict(n=n, fees=fees, src=rng.randrange(n), dst=rng.randrange(n))


def perf_case(rng):
    n = 100000
    fees = [[i, i + 1, rng.randint(500, 1000)] for i in range(n - 1)]
    fees += [[rng.randrange(n), rng.randrange(n), rng.randint(0, 1000)] for _ in range(100001)]
    rng.shuffle(fees)
    return dict(n=n, fees=fees, src=0, dst=n - 1)


def valid(c):
    """Does this input satisfy the stated constraints?"""
    return 1 <= c['n'] <= 10**5 and size(c['fees'], 0, 2 * 10**5) and all(len(e) == 3 and ints(e[:2], 0, c['n'] - 1) and ints(e[2:], 0, 1000) for e in c['fees']) and ints([c['src'], c['dst']], 0, c['n'] - 1)
