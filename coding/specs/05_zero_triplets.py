from gentools import grid, ints, nondecreasing, size, tree  # noqa: F401
ID = 5
TITLE = "Zero-Sum Hedge Triplets"
LEVEL = "medium"
TOPIC = "two pointers"
FUNC = "count_zero_triplets"
SIGNATURE = "def count_zero_triplets(nums: list[int]) -> int:"
STATEMENT = """
Count the **distinct value triplets** `(a, b, c)` with `a <= b <= c` and
`a + b + c == 0`, where `a`, `b`, `c` come from three different positions
of `nums`. Triplets with the same values are counted once, no matter how
many index combinations produce them.
"""
CONSTRAINTS = """
- `0 <= len(nums) <= 1500`
- `-10**5 <= nums[i] <= 10**5`
"""
EXAMPLES = [dict(nums=[-1, 0, 1, 2, -1, -4]), dict(nums=[0, 0, 0, 0])]


def edge_cases():
    return [dict(nums=[]), dict(nums=[0, 0]), dict(nums=[0, 0, 0]), dict(nums=[1, 2, 3]), dict(nums=[-2, 1, 1]),
            dict(nums=[-2, 1]), dict(nums=[-4, 2, 2, 2, 2, -4, 8]), dict(nums=[3, -3, 0, 3, -3, 0, 0])]


def random_case(rng):
    n = rng.randint(0, 12)
    return dict(nums=[rng.randint(-6, 6) for _ in range(n)])


def perf_case(rng):
    return dict(nums=[rng.randint(-3000, 3000) for _ in range(1500)])


def valid(c):
    """Does this input satisfy the stated constraints?"""
    return size(c['nums'], 0, 1500) and ints(c['nums'], -10**5, 10**5)
