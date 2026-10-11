from gentools import grid, ints, nondecreasing, size, tree  # noqa: F401
from gentools import random_tree
from lib import build_tree

ID = 20
TITLE = "Level-by-Level Report"
LEVEL = "medium"
TOPIC = "trees (BFS/DFS)"
FUNC = "level_order"
IMPORTS = "from typing import Optional\nfrom lib import TreeNode"
SIGNATURE = "def level_order(root: Optional[TreeNode]) -> list[list[int]]:"
STATEMENT = """
Return the node values level by level, from top to bottom, each level read
left to right. An empty tree gives `[]`.
"""
CONSTRAINTS = """
- `0 <= number of nodes <= 10**5`
"""
EXAMPLES = [dict(root=[3, 9, 20, None, None, 15, 7]), dict(root=[1, 2, None, 3])]


def to_args(case):
    return dict(root=build_tree(case["root"]))


def edge_cases():
    return [dict(root=[]), dict(root=[1]), dict(root=[1, None, 2, None, 3]), dict(root=[5, 5, 5, 5, 5, 5, 5]),
            dict(root=[1, 2, 3, None, 4, 5])]


def random_case(rng):
    return dict(root=random_tree(rng, rng.randint(0, 12), 0, 9))


def perf_case(rng):
    return dict(root=random_tree(rng, 100000, -10**9, 10**9))


def valid(c):
    """Does this input satisfy the stated constraints?"""
    return tree(c['root'], 10**5, -10**9, 10**9)
