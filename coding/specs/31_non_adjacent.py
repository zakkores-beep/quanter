from gentools import grid, ints, nondecreasing, size, tree  # noqa: F401
ID = 31
TITLE = "Non-Adjacent Trading Days"
LEVEL = "medium"
TOPIC = "1-D dynamic programming"
FUNC = "max_non_adjacent"
SIGNATURE = "def max_non_adjacent(gains: list[int]) -> int:"
STATEMENT = """
`gains[i] >= 0` is what you earn by trading on day `i`, but you may never
trade on two consecutive days. Return the largest total you can earn.
"""
CONSTRAINTS = """
- `0 <= len(gains) <= 2 * 10**5`
- `0 <= gains[i] <= 10**4`
"""
EXAMPLES = [dict(gains=[4, 1, 1, 4]), dict(gains=[2, 7, 9, 3, 1])]


def edge_cases():
    return [dict(gains=[]), dict(gains=[5]), dict(gains=[2, 1]), dict(gains=[0, 0, 0]), dict(gains=[1, 3, 1, 3, 100]),
            dict(gains=[10**4] * 5)]


def random_case(rng):
    return dict(gains=[rng.randint(0, 10) for _ in range(rng.randint(0, 10))])


def perf_case(rng):
    return dict(gains=[rng.randint(0, 10**4) for _ in range(200000)])


def valid(c):
    """Does this input satisfy the stated constraints?"""
    return size(c['gains'], 0, 2 * 10**5) and ints(c['gains'], 0, 10**4)
