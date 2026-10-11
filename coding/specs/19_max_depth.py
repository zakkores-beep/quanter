from gentools import grid, ints, nondecreasing, size, tree  # noqa: F401
from gentools import random_tree
from lib import build_tree

ID = 19
TITLE = "Depth of a Binary Tree"
LEVEL = "easy"
TOPIC = "trees (BFS/DFS)"
FUNC = "max_depth"
IMPORTS = "from typing import Optional\nfrom lib import TreeNode"
SIGNATURE = "def max_depth(root: Optional[TreeNode]) -> int:"
STATEMENT = """
Return the number of nodes on the longest path from the root down to a leaf.
An empty tree has depth 0.

`TreeNode` has fields `val`, `left`, `right` (see `lib.py`). Trees are shown
in level order with `None` for a missing child; the judge builds the nodes.
"""
CONSTRAINTS = """
- `0 <= number of nodes <= 10**5`
"""
EXAMPLES = [dict(root=[3, 9, 20, None, None, 15, 7]), dict(root=[1, None, 2])]


def to_args(case):
    return dict(root=build_tree(case["root"]))


def edge_cases():
    return [dict(root=[]), dict(root=[1]), dict(root=[1, 2]), dict(root=[1, None, 2, None, 3, None, 4]),
            dict(root=[1, 2, 3, 4, None, None, 5, 6])]


def random_case(rng):
    return dict(root=random_tree(rng, rng.randint(0, 12), 0, 9))


def perf_case(rng):
    return dict(root=random_tree(rng, 100000, -10**9, 10**9))


def valid(c):
    """Does this input satisfy the stated constraints?"""
    return tree(c['root'], 10**5, -10**9, 10**9)
