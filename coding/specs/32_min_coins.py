from gentools import grid, ints, nondecreasing, size, tree  # noqa: F401
ID = 32
TITLE = "Fewest Lots"
LEVEL = "medium"
TOPIC = "1-D dynamic programming"
FUNC = "min_coins"
SIGNATURE = "def min_coins(lots: list[int], amount: int) -> int:"
STATEMENT = """
You can buy any number of each lot size in `lots`. Return the fewest lots
whose sizes add up to exactly `amount`, or -1 if that is impossible.
`amount = 0` needs 0 lots.

Greedy (always take the biggest lot) is **wrong** in general.
"""
CONSTRAINTS = """
- `1 <= len(lots) <= 12`, sizes distinct
- `1 <= lots[i] <= 10**4`
- `0 <= amount <= 10**4`
"""
EXAMPLES = [dict(lots=[1, 3, 4], amount=6), dict(lots=[2], amount=3)]


def edge_cases():
    return [dict(lots=[1], amount=0), dict(lots=[7], amount=14), dict(lots=[5, 10], amount=1),
            dict(lots=[10**4], amount=10**4), dict(lots=[2, 5], amount=3), dict(lots=[9, 6, 1], amount=12)]


def random_case(rng):
    return dict(lots=rng.sample(range(1, 10), rng.randint(1, 4)), amount=rng.randint(0, 30))


def perf_case(rng):
    return dict(lots=[1, 2, 5] + rng.sample(range(100, 10**4), 9), amount=9999)


def valid(c):
    """Does this input satisfy the stated constraints?"""
    return size(c['lots'], 1, 12) and len(set(c['lots'])) == len(c['lots']) and ints(c['lots'], 1, 10**4) and ints([c['amount']], 0, 10**4)
