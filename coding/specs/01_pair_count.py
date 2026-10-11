from gentools import grid, ints, nondecreasing, size, tree  # noqa: F401
ID = 1
TITLE = "Matching Trade Pairs"
LEVEL = "easy"
TOPIC = "arrays & hashing"
FUNC = "count_pairs"
SIGNATURE = "def count_pairs(prices: list[int], target: int) -> int:"
STATEMENT = """
You are given a list of trade prices and a target value. Count the pairs of
indices `(i, j)` with `i < j` such that `prices[i] + prices[j] == target`.

Different index pairs count separately, even if their values are the same.
"""
CONSTRAINTS = """
- `0 <= len(prices) <= 2 * 10**5`
- `-10**9 <= prices[i], target <= 10**9`
"""
EXAMPLES = [dict(prices=[1, 5, 3, 3, 7], target=6), dict(prices=[2, 2, 2], target=4)]


def edge_cases():
    return [dict(prices=[], target=0), dict(prices=[5], target=10), dict(prices=[4, 4, 4, 4], target=8),
            dict(prices=[-3, 3, 0, 0], target=0), dict(prices=[10**9, -10**9], target=0),
            dict(prices=[1, 2, 3], target=100)]


def random_case(rng):
    n = rng.randint(0, 12)
    return dict(prices=[rng.randint(-5, 5) for _ in range(n)], target=rng.randint(-6, 6))


def perf_case(rng):
    return dict(prices=[rng.randint(0, 1000) for _ in range(200000)], target=1000)


def valid(c):
    """Does this input satisfy the stated constraints?"""
    return size(c['prices'], 0, 2 * 10**5) and ints(c['prices'] + [c['target']], -10**9, 10**9)
