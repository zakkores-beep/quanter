from gentools import grid, ints, nondecreasing, size, tree  # noqa: F401
ID = 15
TITLE = "Integer Square Roots"
LEVEL = "easy"
TOPIC = "binary search"
FUNC = "isqrt_all"
SIGNATURE = "def isqrt_all(nums: list[int]) -> list[int]:"
STATEMENT = """
For each `x` in `nums`, return the largest integer `r` with `r * r <= x`.

Do **not** use `math.sqrt`, `math.isqrt` or `** 0.5`: use binary search on
integers. (Floating point gives wrong answers near `10**18` - try it.)
"""
CONSTRAINTS = """
- `1 <= len(nums) <= 10**4`
- `0 <= nums[i] <= 10**18`
"""
EXAMPLES = [dict(nums=[0, 1, 8, 9, 10, 99])]


def edge_cases():
    return [dict(nums=[0]), dict(nums=[1, 2, 3, 4]), dict(nums=[15, 16, 17]), dict(nums=[10**18]),
            dict(nums=[10**18 - 1]), dict(nums=[999999999999999999, 999999998000000001, 999999998000000000]),
            dict(nums=[2**59, 2**59 - 1])]


def random_case(rng):
    nums = []
    for _ in range(rng.randint(1, 8)):
        r = rng.random()
        if r < 0.4:
            nums.append(rng.randint(0, 200))
        else:
            k = rng.randint(0, 10**9)
            nums.append(max(0, min(10**18, k * k + rng.randint(-1, 1))))
    return dict(nums=nums)


def perf_case(rng):
    return dict(nums=[rng.randint(0, 10**18) for _ in range(10000)])


def valid(c):
    """Does this input satisfy the stated constraints?"""
    return size(c['nums'], 1, 10**4) and ints(c['nums'], 0, 10**18)
