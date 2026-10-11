from gentools import grid, ints, nondecreasing, size, tree  # noqa: F401
ID = 39
TITLE = "Shortest Route Across the Floor"
LEVEL = "medium"
TOPIC = "graphs"
FUNC = "shortest_path"
SIGNATURE = "def shortest_path(grid: list[str]) -> int:"
STATEMENT = """
`grid` is a list of equal-length strings; `'.'` is open, `'#'` is a wall.
Moving one cell up, down, left or right costs one step. Return the fewest
steps from the top-left cell to the bottom-right cell, or -1 if it cannot be
reached (including when either cell is a wall).
"""
CONSTRAINTS = """
- `1 <= rows, cols <= 400`
"""
EXAMPLES = [dict(grid=["..#", "#..", "#.."]), dict(grid=[".#", "#."])]


def edge_cases():
    return [dict(grid=["."]), dict(grid=["#"]), dict(grid=["..", ".."]), dict(grid=["..", ".#"]),
            dict(grid=["...", "##.", "...", ".##", "..."]), dict(grid=["....."])]


def random_case(rng):
    r, c = rng.randint(1, 6), rng.randint(1, 6)
    return dict(grid=["".join("#" if rng.random() < 0.3 else "." for _ in range(c)) for _ in range(r)])


def perf_case(rng):
    rows = [["#" if rng.random() < 0.25 else "." for _ in range(400)] for _ in range(400)]
    rows[0][0] = rows[-1][-1] = "."
    return dict(grid=["".join(r) for r in rows])


def valid(c):
    """Does this input satisfy the stated constraints?"""
    return grid(c['grid'], 400, '.#')
