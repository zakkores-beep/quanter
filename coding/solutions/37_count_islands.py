from collections import deque


def count_islands(grid):
    rows, cols = len(grid), len(grid[0])
    seen = [[False] * cols for _ in range(rows)]
    count = 0
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == "1" and not seen[r][c]:
                count += 1
                seen[r][c] = True
                queue = deque([(r, c)])
                while queue:
                    y, x = queue.popleft()
                    for ny, nx in ((y + 1, x), (y - 1, x), (y, x + 1), (y, x - 1)):
                        if 0 <= ny < rows and 0 <= nx < cols and grid[ny][nx] == "1" and not seen[ny][nx]:
                            seen[ny][nx] = True
                            queue.append((ny, nx))
    return count


def brute(grid):
    """Union-find over land cells."""
    rows, cols = len(grid), len(grid[0])
    parent = {(r, c): (r, c) for r in range(rows) for c in range(cols) if grid[r][c] == "1"}

    def find(x):
        while parent[x] != x:
            x = parent[x]
        return x

    for (r, c) in list(parent):
        for nb in ((r + 1, c), (r, c + 1)):
            if nb in parent:
                parent[find(nb)] = find((r, c))
    return len({find(x) for x in parent})
