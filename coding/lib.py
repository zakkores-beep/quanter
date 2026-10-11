"""ListNode / TreeNode used by the linked-list and tree problems.

Your solution can `from lib import ListNode, TreeNode`. In statements and
--show output, lists are written as Python lists ([1, 2, 3]) and trees in
level order with None for a missing child: [3, 9, 20, None, None, 15, 7].
"""
from collections import deque


class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

    def __repr__(self):
        return "ListNode(%r)" % (self.val,)


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

    def __repr__(self):
        return "TreeNode(%r)" % (self.val,)


def build_list(values):
    dummy = tail = ListNode()
    for v in values:
        tail.next = ListNode(v)
        tail = tail.next
    return dummy.next


def list_values(head, limit=10**6):
    out = []
    while head is not None:
        if not isinstance(head, ListNode):
            raise TypeError("expected a ListNode, got %s" % type(head).__name__)
        out.append(head.val)
        if len(out) > limit:
            raise ValueError("returned list is too long - does it contain a cycle?")
        head = head.next
    return out


def build_tree(level):
    if not level or level[0] is None:
        return None
    root = TreeNode(level[0])
    queue = deque([root])
    i = 1
    while queue and i < len(level):
        node = queue.popleft()
        for side in ("left", "right"):
            if i < len(level) and level[i] is not None:
                child = TreeNode(level[i])
                setattr(node, side, child)
                queue.append(child)
            i += 1
    return root


def tree_values(root):
    out = []
    queue = deque([root])
    while queue:
        node = queue.popleft()
        if node is None:
            out.append(None)
        else:
            out.append(node.val)
            queue.append(node.left)
            queue.append(node.right)
    while out and out[-1] is None:
        out.pop()
    return out
