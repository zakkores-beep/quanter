from gentools import grid, ints, nondecreasing, size, tree  # noqa: F401
ID = 38
TITLE = "Dependency Order"
TIME_LIMIT = 4.0
LEVEL = "medium"
TOPIC = "graphs"
FUNC = "can_finish"
SIGNATURE = "def can_finish(n: int, deps: list[list[int]]) -> bool:"
STATEMENT = """
There are `n` jobs labelled `0 .. n-1`. Each pair `[a, b]` in `deps` means
job `b` must run before job `a`. Return `True` if all jobs can be run in
some order, i.e. the dependencies contain no cycle. (`[a, a]` is a cycle.)
"""
CONSTRAINTS = """
- `1 <= n <= 10**5`
- `0 <= len(deps) <= 2 * 10**5`
- `0 <= a, b < n`; duplicate pairs may appear
"""
EXAMPLES = [dict(n=2, deps=[[1, 0]]), dict(n=3, deps=[[1, 0], [2, 1], [0, 2]])]


def edge_cases():
    return [dict(n=1, deps=[]), dict(n=1, deps=[[0, 0]]), dict(n=2, deps=[[1, 0], [0, 1]]),
            dict(n=2, deps=[[1, 0], [1, 0]]), dict(n=4, deps=[[1, 0], [2, 0], [3, 1], [3, 2]]),
            dict(n=5, deps=[[1, 0], [2, 1], [3, 4], [4, 3]])]


def random_case(rng):
    n = rng.randint(1, 6)
    deps = [[rng.randrange(n), rng.randrange(n)] for _ in range(rng.randint(0, 7))]
    deps = [d for d in deps if d[0] != d[1] or rng.random() < 0.1]
    return dict(n=n, deps=deps)


def perf_case(rng):
    n = 100000
    order = list(range(n))
    rng.shuffle(order)  # order[i] must come before order[j] when i < j
    deps = [[order[i + 1], order[i]] for i in range(n - 1)]  # one long chain
    for _ in range(100001):
        i, j = sorted(rng.sample(range(n), 2))
        deps.append([order[j], order[i]])
    rng.shuffle(deps)
    return dict(n=n, deps=deps)


def valid(c):
    """Does this input satisfy the stated constraints?"""
    return 1 <= c['n'] <= 10**5 and size(c['deps'], 0, 2 * 10**5) and all(len(d) == 2 and ints(d, 0, c['n'] - 1) for d in c['deps'])
