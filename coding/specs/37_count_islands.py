from gentools import grid, ints, nondecreasing, size, tree  # noqa: F401
ID = 37
TITLE = "Count the Islands"
LEVEL = "medium"
TOPIC = "graphs"
FUNC = "count_islands"
SIGNATURE = "def count_islands(grid: list[str]) -> int:"
STATEMENT = """
`grid` is a list of equal-length strings of `'1'` (land) and `'0'` (water).
An island is a group of land cells connected up, down, left or right (not
diagonally). Return the number of islands.
"""
CONSTRAINTS = """
- `1 <= rows, cols <= 400`
- Python's default recursion limit is 1000: a recursive DFS can crash on big islands.
"""
EXAMPLES = [dict(grid=["11000", "11000", "00100", "00011"]), dict(grid=["101", "010", "101"])]


def edge_cases():
    return [dict(grid=["0"]), dict(grid=["1"]), dict(grid=["11", "11"]), dict(grid=["1" * 7]),
            dict(grid=["111", "101", "111"]), dict(grid=["10", "01"]), dict(grid=["0", "1", "0", "1"])]


def random_case(rng):
    r, c = rng.randint(1, 6), rng.randint(1, 6)
    return dict(grid=["".join("1" if rng.random() < 0.5 else "0" for _ in range(c)) for _ in range(r)])


def perf_case(rng):
    return dict(grid=["".join("1" if rng.random() < 0.6 else "0" for _ in range(400)) for _ in range(400)])


def valid(c):
    """Does this input satisfy the stated constraints?"""
    return grid(c['grid'], 400, '01')
