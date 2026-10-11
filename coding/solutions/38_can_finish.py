from collections import deque
from itertools import permutations


def can_finish(n, deps):
    out = [[] for _ in range(n)]
    indeg = [0] * n
    for a, b in deps:
        out[b].append(a)
        indeg[a] += 1
    queue = deque(i for i in range(n) if indeg[i] == 0)
    done = 0
    while queue:
        x = queue.popleft()
        done += 1
        for y in out[x]:
            indeg[y] -= 1
            if indeg[y] == 0:
                queue.append(y)
    return done == n


def brute(n, deps):
    """Try every ordering of the jobs."""
    for perm in permutations(range(n)):
        pos = {job: i for i, job in enumerate(perm)}
        if all(pos[b] < pos[a] for a, b in deps):
            return True
    return False
