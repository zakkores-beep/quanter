from collections import deque


def level_order(root):
    out = []
    level = deque([root] if root else [])
    while level:
        row = []
        for _ in range(len(level)):
            node = level.popleft()
            row.append(node.val)
            if node.left:
                level.append(node.left)
            if node.right:
                level.append(node.right)
        out.append(row)
    return out


def brute(root):
    """Pre-order DFS visits each level left to right, so bucket by depth."""
    rows = []

    def visit(node, d):
        if node is None:
            return
        if d == len(rows):
            rows.append([])
        rows[d].append(node.val)
        visit(node.left, d + 1)
        visit(node.right, d + 1)

    visit(root, 0)
    return rows
