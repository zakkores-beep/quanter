"""Random generators shared by several specs (not needed for solving)."""
from lib import TreeNode, tree_values


def random_tree(rng, n, lo, hi):
    """Random binary tree with n nodes and values in [lo, hi], as a level-order list."""
    if n == 0:
        return []
    root = TreeNode(rng.randint(lo, hi))
    slots = [(root, "left"), (root, "right")]
    for _ in range(n - 1):
        i = rng.randrange(len(slots))
        slots[i], slots[-1] = slots[-1], slots[i]
        parent, side = slots.pop()
        child = TreeNode(rng.randint(lo, hi))
        setattr(parent, side, child)
        slots += [(child, "left"), (child, "right")]
    return tree_values(root)


def bst_from_sorted(rng, values):
    """Random-shaped BST containing the sorted values, as a level-order list."""
    if not values:
        return []
    holder = TreeNode()
    stack = [(0, len(values) - 1, holder, "left")]
    while stack:
        lo, hi, parent, side = stack.pop()
        if lo > hi:
            continue
        mid = rng.randint(lo, hi)
        node = TreeNode(values[mid])
        setattr(parent, side, node)
        stack.append((lo, mid - 1, node, "left"))
        stack.append((mid + 1, hi, node, "right"))
    return tree_values(holder.left)


def random_bst(rng, n, lo, hi):
    return bst_from_sorted(rng, sorted(rng.sample(range(lo, hi + 1), n)))


# ---- constraint checks used by each spec's valid() ----

def ints(xs, lo, hi):
    return all(type(x) is int and lo <= x <= hi for x in xs)


def size(xs, lo, hi):
    return lo <= len(xs) <= hi


def grid(g, max_side, chars):
    return (size(g, 1, max_side) and 1 <= len(g[0]) <= max_side and all(len(r) == len(g[0]) for r in g)
            and all(set(r) <= set(chars) for r in g))


def tree(level, max_nodes, lo, hi):
    vals = [v for v in level if v is not None]
    return (not level or level[0] is not None) and len(vals) <= max_nodes and ints(vals, lo, hi)


def nondecreasing(xs):
    return all(a <= b for a, b in zip(xs, xs[1:]))
