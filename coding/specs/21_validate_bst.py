from gentools import grid, ints, nondecreasing, size, tree  # noqa: F401
from gentools import random_bst, random_tree
from lib import build_tree, tree_values

ID = 21
TITLE = "Validate a Search Tree"
LEVEL = "medium"
TOPIC = "trees (BFS/DFS)"
FUNC = "is_valid_bst"
IMPORTS = "from typing import Optional\nfrom lib import TreeNode"
SIGNATURE = "def is_valid_bst(root: Optional[TreeNode]) -> bool:"
STATEMENT = """
Return `True` if the tree is a valid binary search tree: for **every** node,
all values in its left subtree are strictly smaller and all values in its
right subtree are strictly larger. An empty tree is valid.
"""
CONSTRAINTS = """
- `0 <= number of nodes <= 10**5`
- `-2**31 <= val <= 2**31 - 1`
"""
EXAMPLES = [dict(root=[2, 1, 3]), dict(root=[10, 5, 15, None, None, 6, 20])]


def to_args(case):
    return dict(root=build_tree(case["root"]))


def edge_cases():
    return [dict(root=[]), dict(root=[1]), dict(root=[2, 2, 2]), dict(root=[1, None, 1]), dict(root=[1, 1]),
            dict(root=[-2**31, None, 2**31 - 1]), dict(root=[5, 3, 8, 1, 6])]


def random_case(rng):
    if rng.random() < 0.3:
        return dict(root=random_tree(rng, rng.randint(0, 8), 0, 9))
    level = random_bst(rng, rng.randint(1, 10), 0, 20)
    if rng.random() < 0.6:
        root = build_tree(level)
        nodes, stack = [], [root]
        while stack:
            n = stack.pop()
            if n:
                nodes.append(n)
                stack += [n.left, n.right]
        rng.choice(nodes).val = rng.randint(0, 20)
        level = tree_values(root)
    return dict(root=level)


def perf_case(rng):
    return dict(root=random_bst(rng, 100000, -2**31, 2**31 - 1))


def valid(c):
    """Does this input satisfy the stated constraints?"""
    return tree(c['root'], 10**5, -2**31, 2**31 - 1)
