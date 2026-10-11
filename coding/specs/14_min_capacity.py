from gentools import grid, ints, nondecreasing, size, tree  # noqa: F401
ID = 14
TITLE = "Minimum Settlement Capacity"
LEVEL = "medium"
TOPIC = "binary search"
FUNC = "min_capacity"
SIGNATURE = "def min_capacity(weights: list[int], days: int) -> int:"
STATEMENT = """
Trades with sizes `weights` must be settled **in the given order** over at
most `days` days. Each day you settle a contiguous block of the remaining
trades whose total size is at most the daily capacity `C`. A trade cannot
be split.

Return the smallest capacity `C` that settles everything within `days` days.
"""
CONSTRAINTS = """
- `1 <= days <= len(weights) <= 5 * 10**4`
- `1 <= weights[i] <= 500`
"""
EXAMPLES = [dict(weights=[3, 2, 2, 4, 1, 4], days=3), dict(weights=[1, 2, 3, 4, 5], days=1)]


def edge_cases():
    return [dict(weights=[7], days=1), dict(weights=[1, 2, 3, 4, 5], days=5), dict(weights=[10, 1, 1, 1], days=2),
            dict(weights=[500] * 4, days=2), dict(weights=[1, 1, 1, 1, 500], days=2),
            dict(weights=[5, 5, 5, 5], days=3)]


def random_case(rng):
    n = rng.randint(1, 10)
    return dict(weights=[rng.randint(1, 10) for _ in range(n)], days=rng.randint(1, n))


def perf_case(rng):
    return dict(weights=[rng.randint(1, 500) for _ in range(50000)], days=7)


def valid(c):
    """Does this input satisfy the stated constraints?"""
    return 1 <= c['days'] <= len(c['weights']) <= 5 * 10**4 and ints(c['weights'], 1, 500)
