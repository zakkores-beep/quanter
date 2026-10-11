from gentools import grid, ints, nondecreasing, size, tree  # noqa: F401
ID = 34
TITLE = "Paths Through a Blocked Grid"
LEVEL = "medium"
TOPIC = "2-D dynamic programming"
FUNC = "count_paths"
SIGNATURE = "def count_paths(grid: list[str]) -> int:"
STATEMENT = """
`grid` is a list of equal-length strings; `'.'` is open and `'#'` is blocked.
Starting at the top-left cell, you may only move **right** or **down**, and
only through open cells. Return the number of different paths to the
bottom-right cell, modulo `10**9 + 7`. If the start or end cell is blocked,
the answer is 0.
"""
CONSTRAINTS = """
- `1 <= rows, cols <= 300`
"""
EXAMPLES = [dict(grid=["...", ".#.", "..."]), dict(grid=[".#", "#."])]


def edge_cases():
    return [dict(grid=["."]), dict(grid=["#"]), dict(grid=["..", ".."]), dict(grid=["..#"]), dict(grid=["#.."]),
            dict(grid=["....."]), dict(grid=[".", ".", "."]), dict(grid=["..", "#.", ".."])]


def random_case(rng):
    r, c = rng.randint(1, 6), rng.randint(1, 6)
    return dict(grid=["".join("#" if rng.random() < 0.2 else "." for _ in range(c)) for _ in range(r)])


def perf_case(rng):
    rows = [["#" if rng.random() < 0.01 else "." for _ in range(300)] for _ in range(300)]
    rows[0][0] = rows[-1][-1] = "."
    return dict(grid=["".join(r) for r in rows])


def valid(c):
    """Does this input satisfy the stated constraints?"""
    return grid(c['grid'], 300, '.#')
