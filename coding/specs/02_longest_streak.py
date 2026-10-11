from gentools import grid, ints, nondecreasing, size, tree  # noqa: F401
ID = 2
TITLE = "Longest Active Streak"
LEVEL = "medium"
TOPIC = "arrays & hashing"
FUNC = "longest_streak"
SIGNATURE = "def longest_streak(days: list[int]) -> int:"
STATEMENT = """
`days` holds the (unsorted) day numbers on which an account traded. A day can
appear more than once. Return the length of the longest run of consecutive
integers `x, x+1, ..., x+L-1` that all appear in `days`. Return 0 for an
empty list.

Aim for O(n) time; sorting works but is not the intended solution.
"""
CONSTRAINTS = """
- `0 <= len(days) <= 2 * 10**5`
- `-10**9 <= days[i] <= 10**9`
"""
EXAMPLES = [dict(days=[10, 5, 6, 100, 4, 7]), dict(days=[1, 2, 2, 3, 9])]


def edge_cases():
    return [dict(days=[]), dict(days=[7]), dict(days=[1, 2, 2, 3]), dict(days=[-1, 0, 1]),
            dict(days=[10**9, -10**9]), dict(days=[5, 5, 5, 5]), dict(days=[3, 1, 5, 7])]


def random_case(rng):
    n = rng.randint(0, 12)
    return dict(days=[rng.randint(-8, 8) for _ in range(n)])


def perf_case(rng):
    days = [rng.randint(-10**9, 10**9) for _ in range(150000)] + list(range(500000, 550000))
    rng.shuffle(days)
    return dict(days=days)


def valid(c):
    """Does this input satisfy the stated constraints?"""
    return size(c['days'], 0, 2 * 10**5) and ints(c['days'], -10**9, 10**9)
