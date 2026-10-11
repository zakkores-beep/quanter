MOD = 10**9 + 7


def count_paths(grid):
    cols = len(grid[0])
    row = [0] * cols  # row[c] = paths into (current row, c)
    row[0] = 1
    for r, line in enumerate(grid):
        for c in range(cols):
            if line[c] == "#":
                row[c] = 0
            elif c > 0:
                row[c] = (row[c] + row[c - 1]) % MOD
    return row[-1]


def brute(grid):
    """Walk every path explicitly (exponential)."""
    rows, cols = len(grid), len(grid[0])

    def walk(r, c):
        if r >= rows or c >= cols or grid[r][c] == "#":
            return 0
        if (r, c) == (rows - 1, cols - 1):
            return 1
        return walk(r + 1, c) + walk(r, c + 1)

    return walk(0, 0) % MOD
