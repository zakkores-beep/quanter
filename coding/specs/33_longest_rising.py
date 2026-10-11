from gentools import grid, ints, nondecreasing, size, tree  # noqa: F401
ID = 33
TITLE = "Longest Rising Subsequence"
LEVEL = "medium"
TOPIC = "1-D dynamic programming"
FUNC = "longest_rising"
SIGNATURE = "def longest_rising(prices: list[int]) -> int:"
STATEMENT = """
Return the length of the longest **strictly increasing** subsequence of
`prices` (elements keep their order but need not be adjacent).

The O(n^2) DP is too slow for the largest test; you need O(n log n).
"""
CONSTRAINTS = """
- `0 <= len(prices) <= 2 * 10**5`
- `-10**9 <= prices[i] <= 10**9`
"""
EXAMPLES = [dict(prices=[0, 8, 4, 12, 2, 10, 6, 14]), dict(prices=[3, 3, 3])]


def edge_cases():
    return [dict(prices=[]), dict(prices=[5]), dict(prices=[1, 2, 3]), dict(prices=[3, 2, 1]),
            dict(prices=[1, 3, 2, 3, 4, 1]), dict(prices=[2, 2, 3, 3, 4, 4])]


def random_case(rng):
    return dict(prices=[rng.randint(0, 8) for _ in range(rng.randint(0, 10))])


def perf_case(rng):
    return dict(prices=[rng.randint(-10**9, 10**9) for _ in range(200000)])


def valid(c):
    """Does this input satisfy the stated constraints?"""
    return size(c['prices'], 0, 2 * 10**5) and ints(c['prices'], -10**9, 10**9)
