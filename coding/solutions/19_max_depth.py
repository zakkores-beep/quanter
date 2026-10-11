from collections import deque


def max_depth(root):
    if not root:
        return 0
    depth, level = 0, deque([root])
    while level:
        depth += 1
        for _ in range(len(level)):
            node = level.popleft()
            if node.left:
                level.append(node.left)
            if node.right:
                level.append(node.right)
    return depth


def brute(root):
    if root is None:
        return 0
    return 1 + max(brute(root.left), brute(root.right))
