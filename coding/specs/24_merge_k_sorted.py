from gentools import grid, ints, nondecreasing, size, tree  # noqa: F401
ID = 24
TITLE = "Merge Sorted Order Feeds"
LEVEL = "medium"
TOPIC = "heaps"
FUNC = "merge_feeds"
SIGNATURE = "def merge_feeds(feeds: list[list[int]]) -> list[int]:"
STATEMENT = """
Each feed is a list of timestamps sorted in non-decreasing order. Merge all
feeds into one sorted list.

Use a heap holding one "next" element per feed: O(N log k) for N total
items and k feeds.
"""
CONSTRAINTS = """
- `0 <= len(feeds) <= 2000`
- total items `N <= 2 * 10**5`
- `-10**9 <= timestamp <= 10**9`
"""
EXAMPLES = [dict(feeds=[[1, 5, 9], [2, 2], [0, 10]]), dict(feeds=[[], [3], []])]


def edge_cases():
    return [dict(feeds=[]), dict(feeds=[[]]), dict(feeds=[[1, 1], [1], [1, 1, 1]]), dict(feeds=[[-5, 0, 5]]),
            dict(feeds=[[10**9], [-10**9]])]


def random_case(rng):
    return dict(feeds=[sorted(rng.randint(-9, 9) for _ in range(rng.randint(0, 5))) for _ in range(rng.randint(0, 5))])


def perf_case(rng):
    return dict(feeds=[sorted(rng.randint(-10**9, 10**9) for _ in range(200)) for _ in range(1000)])


def valid(c):
    """Does this input satisfy the stated constraints?"""
    return size(c['feeds'], 0, 2000) and sum(map(len, c['feeds'])) <= 2 * 10**5 and all(nondecreasing(f) and ints(f, -10**9, 10**9) for f in c['feeds'])
