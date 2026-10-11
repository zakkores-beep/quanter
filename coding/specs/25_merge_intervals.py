from gentools import grid, ints, nondecreasing, size, tree  # noqa: F401
ID = 25
TITLE = "Merge Trading Sessions"
LEVEL = "medium"
TOPIC = "intervals"
FUNC = "merge_intervals"
SIGNATURE = "def merge_intervals(intervals: list[list[int]]) -> list[list[int]]:"
STATEMENT = """
Each interval `[start, end]` (with `start <= end`) is a closed time range.
Merge all intervals that overlap **or touch** (`[1, 3]` and `[3, 5]` become
`[1, 5]`). Return the merged intervals sorted by start.
"""
CONSTRAINTS = """
- `0 <= len(intervals) <= 10**5`
- `0 <= start <= end <= 10**9`
"""
EXAMPLES = [dict(intervals=[[8, 10], [1, 3], [2, 6], [15, 18]]), dict(intervals=[[1, 3], [3, 5]])]


def edge_cases():
    return [dict(intervals=[]), dict(intervals=[[1, 3]]), dict(intervals=[[5, 6], [1, 2]]),
            dict(intervals=[[1, 10], [2, 3], [4, 5]]), dict(intervals=[[2, 2], [2, 2]]),
            dict(intervals=[[0, 0], [1, 1]]), dict(intervals=[[4, 7], [1, 4]])]


def random_case(rng):
    out = []
    for _ in range(rng.randint(0, 8)):
        s = rng.randint(0, 15)
        out.append([s, s + rng.randint(0, 5)])
    return dict(intervals=out)


def perf_case(rng):
    out = []
    for _ in range(100000):
        s = rng.randint(0, 10**9 - 10**4)
        out.append([s, s + rng.randint(0, 10**4)])
    return dict(intervals=out)


def valid(c):
    """Does this input satisfy the stated constraints?"""
    return size(c['intervals'], 0, 10**5) and all(len(x) == 2 and ints(x, 0, 10**9) and x[0] <= x[1] for x in c['intervals'])
