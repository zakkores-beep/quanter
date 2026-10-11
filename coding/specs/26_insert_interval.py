from gentools import grid, ints, nondecreasing, size, tree  # noqa: F401
ID = 26
TITLE = "Insert a Blackout Window"
LEVEL = "medium"
TOPIC = "intervals"
FUNC = "insert_interval"
SIGNATURE = "def insert_interval(intervals: list[list[int]], new: list[int]) -> list[list[int]]:"
STATEMENT = """
`intervals` is sorted by start and contains closed intervals that neither
overlap nor touch. Insert the closed interval `new`, merging wherever
intervals overlap **or touch**, and return the sorted result.

Aim for O(n): the input is already sorted.
"""
CONSTRAINTS = """
- `0 <= len(intervals) <= 10**5`
- `0 <= start <= end <= 10**9` for every interval, including `new`
"""
EXAMPLES = [dict(intervals=[[1, 2], [5, 6], [9, 12]], new=[3, 5]), dict(intervals=[], new=[4, 8])]


def edge_cases():
    return [dict(intervals=[[1, 2], [5, 6]], new=[3, 4]), dict(intervals=[[1, 2], [5, 6]], new=[2, 5]),
            dict(intervals=[[1, 5]], new=[2, 3]), dict(intervals=[[3, 4]], new=[0, 1]),
            dict(intervals=[[3, 4]], new=[9, 9]), dict(intervals=[[0, 0], [2, 2], [4, 4]], new=[0, 10**9])]


def _disjoint(rng, count, lo, gap_max, len_max):
    out, pos = [], lo
    for _ in range(count):
        s = pos + rng.randint(1, gap_max)
        e = s + rng.randint(0, len_max)
        out.append([s, e])
        pos = e + 1  # next start >= e + 2, so intervals never touch
    return out


def random_case(rng):
    intervals = _disjoint(rng, rng.randint(0, 6), -1, 4, 3)
    s = rng.randint(0, 30)
    return dict(intervals=intervals, new=[s, s + rng.randint(0, 8)])


def perf_case(rng):
    intervals = _disjoint(rng, 100000, -1, 5000, 4000)
    mid = intervals[50000][0]
    return dict(intervals=intervals, new=[mid, mid + 10**7])


def valid(c):
    """Does this input satisfy the stated constraints?"""
    return size(c['intervals'], 0, 10**5) and all(len(x) == 2 and ints(x, 0, 10**9) and x[0] <= x[1] for x in c['intervals'] + [c['new']]) and all(a[1] < b[0] for a, b in zip(c['intervals'], c['intervals'][1:]))
