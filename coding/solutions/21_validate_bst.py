def is_valid_bst(root):
    stack = [(root, None, None)]  # node, exclusive lower bound, exclusive upper bound
    while stack:
        node, lo, hi = stack.pop()
        if node is None:
            continue
        if (lo is not None and node.val <= lo) or (hi is not None and node.val >= hi):
            return False
        stack.append((node.left, lo, node.val))
        stack.append((node.right, node.val, hi))
    return True


def brute(root):
    def values(node):
        return [] if node is None else values(node.left) + [node.val] + values(node.right)

    def ok(node):
        if node is None:
            return True
        return (all(v < node.val for v in values(node.left)) and all(v > node.val for v in values(node.right))
                and ok(node.left) and ok(node.right))

    return ok(root)
