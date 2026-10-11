from gentools import grid, ints, nondecreasing, size, tree  # noqa: F401
ID = 9
TITLE = "Shortest Window to Fill an Order"
LEVEL = "medium"
TOPIC = "sliding window"
FUNC = "shortest_window"
SIGNATURE = "def shortest_window(volumes: list[int], target: int) -> int:"
STATEMENT = """
`volumes[i]` is the (positive) volume traded in minute `i`. Return the length
of the shortest run of consecutive minutes whose total volume is **at least**
`target`. Return 0 if no such run exists.
"""
CONSTRAINTS = """
- `1 <= len(volumes) <= 2 * 10**5`
- `1 <= volumes[i] <= 10**4`
- `1 <= target <= 10**9`
"""
EXAMPLES = [dict(volumes=[2, 3, 1, 2, 4, 3], target=7), dict(volumes=[1, 1, 1], target=5)]


def edge_cases():
    return [dict(volumes=[1], target=1), dict(volumes=[1], target=2), dict(volumes=[1, 4, 4], target=4),
            dict(volumes=[1, 1, 1, 1, 1], target=5), dict(volumes=[5, 1, 3, 5, 10, 7, 4, 9, 2, 8], target=15),
            dict(volumes=[10**4] * 3, target=10**9)]


def random_case(rng):
    n = rng.randint(1, 12)
    return dict(volumes=[rng.randint(1, 6) for _ in range(n)], target=rng.randint(1, 30))


def perf_case(rng):
    return dict(volumes=[rng.randint(1, 100) for _ in range(200000)], target=200000)


def valid(c):
    """Does this input satisfy the stated constraints?"""
    return size(c['volumes'], 1, 2 * 10**5) and ints(c['volumes'], 1, 10**4) and ints([c['target']], 1, 10**9)
