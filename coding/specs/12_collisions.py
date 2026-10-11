from gentools import grid, ints, nondecreasing, size, tree  # noqa: F401
ID = 12
TITLE = "Colliding Orders"
LEVEL = "medium"
TOPIC = "stack"
FUNC = "surviving"
SIGNATURE = "def surviving(orders: list[int]) -> list[int]:"
STATEMENT = """
Objects sit on a line in the given order. For `orders[i]`, the absolute value
is its size and the sign is its direction (positive = moving right, negative =
moving left). All move at the same speed.

When two objects meet, the smaller one disappears; if they are the same size,
both disappear. Objects moving in the same direction never meet. Return the
objects that remain, in their original order.
"""
CONSTRAINTS = """
- `0 <= len(orders) <= 2 * 10**5`
- `1 <= abs(orders[i]) <= 1000` (no zeros)
"""
EXAMPLES = [dict(orders=[10, 2, -5]), dict(orders=[-2, 1]), dict(orders=[5, -5])]


def edge_cases():
    return [dict(orders=[]), dict(orders=[3]), dict(orders=[1, -2, -2, -2]), dict(orders=[3, 4, -5, 6]),
            dict(orders=[-1, -2, 3, 4]), dict(orders=[2, 2, -2]), dict(orders=[1000, -999, -1, -1000])]


def random_case(rng):
    n = rng.randint(0, 10)
    return dict(orders=[rng.choice((-1, 1)) * rng.randint(1, 5) for _ in range(n)])


def perf_case(rng):
    right = [rng.randint(1, 1000) for _ in range(100000)]
    left = [-rng.randint(1, 1000) for _ in range(100000)]
    return dict(orders=right + left)


def valid(c):
    """Does this input satisfy the stated constraints?"""
    return size(c['orders'], 0, 2 * 10**5) and ints(c['orders'], -1000, 1000) and 0 not in c['orders']
