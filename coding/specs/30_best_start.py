from gentools import grid, ints, nondecreasing, size, tree  # noqa: F401
ID = 30
TITLE = "Circular Funding Route"
LEVEL = "medium"
TOPIC = "greedy"
FUNC = "best_start"
SIGNATURE = "def best_start(gas: list[int], cost: list[int]) -> int:"
STATEMENT = """
There are `n` stations on a circle. At station `i` you collect `gas[i]`, and
travelling from station `i` to station `(i + 1) % n` uses `cost[i]`. You
start with an empty tank at a station of your choice and must go once round
the whole circle; the tank may never go negative.

Return the **smallest** starting index that works, or -1 if none does.
"""
CONSTRAINTS = """
- `1 <= n == len(gas) == len(cost) <= 2 * 10**5`
- `0 <= gas[i], cost[i] <= 10**4`
"""
EXAMPLES = [dict(gas=[1, 2, 3, 4, 5], cost=[3, 4, 5, 1, 2]), dict(gas=[1, 1], cost=[1, 1])]


def edge_cases():
    return [dict(gas=[1], cost=[1]), dict(gas=[1], cost=[2]), dict(gas=[0, 2], cost=[1, 1]),
            dict(gas=[2, 3, 4], cost=[3, 4, 3]), dict(gas=[0, 0, 0], cost=[0, 0, 0]), dict(gas=[3, 0, 0], cost=[0, 0, 3])]


def random_case(rng):
    n = rng.randint(1, 8)
    return dict(gas=[rng.randint(0, 4) for _ in range(n)], cost=[rng.randint(0, 4) for _ in range(n)])


def perf_case(rng):
    n = 200000
    gas = [rng.randint(0, 10**4) for _ in range(n)]
    cost = [rng.randint(0, 10**4) for _ in range(n)]
    i = 0
    while sum(gas) < sum(cost):  # make a solution exist
        gas[i], cost[i] = 10**4, 0
        i += 1000
    return dict(gas=gas, cost=cost)


def valid(c):
    """Does this input satisfy the stated constraints?"""
    return 1 <= len(c['gas']) == len(c['cost']) <= 2 * 10**5 and ints(c['gas'] + c['cost'], 0, 10**4)
