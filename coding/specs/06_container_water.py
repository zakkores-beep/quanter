from gentools import grid, ints, nondecreasing, size, tree  # noqa: F401
ID = 6
TITLE = "Widest Price Channel"
LEVEL = "medium"
TOPIC = "two pointers"
FUNC = "max_area"
SIGNATURE = "def max_area(heights: list[int]) -> int:"
STATEMENT = """
Pick two indices `i < j`. The channel between them has area
`min(heights[i], heights[j]) * (j - i)`. Return the largest possible area.
"""
CONSTRAINTS = """
- `2 <= len(heights) <= 2 * 10**5`
- `0 <= heights[i] <= 10**4`
"""
EXAMPLES = [dict(heights=[3, 1, 2, 4, 5]), dict(heights=[1, 1])]


def edge_cases():
    return [dict(heights=[0, 0]), dict(heights=[5, 5, 5, 5]), dict(heights=[1, 2, 3, 4, 5, 6]),
            dict(heights=[6, 5, 4, 3, 2, 1]), dict(heights=[10000, 0, 10000]), dict(heights=[0, 10000])]


def random_case(rng):
    n = rng.randint(2, 12)
    return dict(heights=[rng.randint(0, 10) for _ in range(n)])


def perf_case(rng):
    return dict(heights=[rng.randint(0, 10**4) for _ in range(200000)])


def valid(c):
    """Does this input satisfy the stated constraints?"""
    return size(c['heights'], 2, 2 * 10**5) and ints(c['heights'], 0, 10**4)
