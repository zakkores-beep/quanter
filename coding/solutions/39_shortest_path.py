from collections import deque


def shortest_path(grid):
    rows, cols = len(grid), len(grid[0])
    if grid[0][0] == "#" or grid[-1][-1] == "#":
        return -1
    dist = [[-1] * cols for _ in range(rows)]
    dist[0][0] = 0
    queue = deque([(0, 0)])
    while queue:
        y, x = queue.popleft()
        if (y, x) == (rows - 1, cols - 1):
            return dist[y][x]
        for ny, nx in ((y + 1, x), (y - 1, x), (y, x + 1), (y, x - 1)):
            if 0 <= ny < rows and 0 <= nx < cols and grid[ny][nx] == "." and dist[ny][nx] < 0:
                dist[ny][nx] = dist[y][x] + 1
                queue.append((ny, nx))
    return -1


def brute(grid):
    """Relax every cell from its neighbours until nothing changes."""
    rows, cols = len(grid), len(grid[0])
    inf = float("inf")
    dist = [[inf] * cols for _ in range(rows)]
    if grid[0][0] == ".":
        dist[0][0] = 0
    changed = True
    while changed:
        changed = False
        for y in range(rows):
            for x in range(cols):
                if grid[y][x] != ".":
                    continue
                for ny, nx in ((y + 1, x), (y - 1, x), (y, x + 1), (y, x - 1)):
                    if 0 <= ny < rows and 0 <= nx < cols and dist[ny][nx] + 1 < dist[y][x]:
                        dist[y][x] = dist[ny][nx] + 1
                        changed = True
    d = dist[-1][-1]
    return -1 if d == inf else d
