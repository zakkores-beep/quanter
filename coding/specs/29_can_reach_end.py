from gentools import grid, ints, nondecreasing, size, tree  # noqa: F401
ID = 29
TITLE = "Reach the Last Checkpoint"
LEVEL = "medium"
TOPIC = "greedy"
FUNC = "can_reach_end"
SIGNATURE = "def can_reach_end(jumps: list[int]) -> bool:"
STATEMENT = """
You start at index 0. From index `i` you may move forward by any number of
steps from 0 to `jumps[i]`. Return `True` if you can reach the last index.
"""
CONSTRAINTS = """
- `1 <= len(jumps) <= 2 * 10**5`
- `0 <= jumps[i] <= 10**5`
"""
EXAMPLES = [dict(jumps=[2, 0, 1, 0]), dict(jumps=[2, 1, 0, 3])]


def edge_cases():
    return [dict(jumps=[0]), dict(jumps=[0, 1]), dict(jumps=[1, 0]), dict(jumps=[1, 0, 1]),
            dict(jumps=[3, 0, 0, 0]), dict(jumps=[1, 1, 1, 0, 5]), dict(jumps=[10**5, 0])]


def random_case(rng):
    return dict(jumps=[rng.randint(0, 3) for _ in range(rng.randint(1, 10))])


def perf_case(rng):
    jumps = [rng.randint(1, 1000) for _ in range(200000)]
    for i in range(150000, 150000 + 1500):  # a wall of zeros longer than any jump
        jumps[i] = 0
    return dict(jumps=jumps)


def valid(c):
    """Does this input satisfy the stated constraints?"""
    return size(c['jumps'], 1, 2 * 10**5) and ints(c['jumps'], 0, 10**5)
