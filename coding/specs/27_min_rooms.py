from gentools import grid, ints, nondecreasing, size, tree  # noqa: F401
ID = 27
TITLE = "Meeting Rooms Needed"
LEVEL = "medium"
TOPIC = "intervals"
FUNC = "min_rooms"
SIGNATURE = "def min_rooms(meetings: list[list[int]]) -> int:"
STATEMENT = """
Each meeting `[start, end]` occupies a room for the half-open time range
`start <= t < end` (a meeting ending at 10 frees its room for one starting
at 10). Return the minimum number of rooms needed to hold all meetings.
"""
CONSTRAINTS = """
- `0 <= len(meetings) <= 10**5`
- `0 <= start < end <= 10**9`
"""
EXAMPLES = [dict(meetings=[[0, 10], [2, 4], [6, 8], [3, 7]]), dict(meetings=[[1, 2], [2, 3]])]


def edge_cases():
    return [dict(meetings=[]), dict(meetings=[[1, 2]]), dict(meetings=[[1, 5], [1, 5], [1, 5]]),
            dict(meetings=[[5, 8], [1, 5], [8, 9]]), dict(meetings=[[0, 10**9], [1, 2], [3, 4]])]


def random_case(rng):
    out = []
    for _ in range(rng.randint(0, 8)):
        s = rng.randint(0, 12)
        out.append([s, s + rng.randint(1, 5)])
    return dict(meetings=out)


def perf_case(rng):
    out = []
    for _ in range(100000):
        s = rng.randint(0, 10**9 - 10**6)
        out.append([s, s + rng.randint(1, 10**6)])
    return dict(meetings=out)


def valid(c):
    """Does this input satisfy the stated constraints?"""
    return size(c['meetings'], 0, 10**5) and all(len(x) == 2 and ints(x, 0, 10**9) and x[0] < x[1] for x in c['meetings'])
