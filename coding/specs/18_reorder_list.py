from gentools import grid, ints, nondecreasing, size, tree  # noqa: F401
from lib import build_list, list_values

ID = 18
TITLE = "Interleave a Linked List"
LEVEL = "medium"
TOPIC = "linked lists"
FUNC = "reorder"
IMPORTS = "from typing import Optional\nfrom lib import ListNode"
SIGNATURE = "def reorder(head: Optional[ListNode]) -> Optional[ListNode]:"
STATEMENT = """
Given the list `L0 -> L1 -> ... -> Ln`, rearrange the nodes into
`L0 -> Ln -> L1 -> Ln-1 -> L2 -> Ln-2 -> ...` and return the head.

Relink the nodes; do not just change values. Aim for O(1) extra space
(find the middle, reverse the second half, merge).
"""
CONSTRAINTS = """
- `0 <= number of nodes <= 10**5`
- `-10**9 <= val <= 10**9`
"""
EXAMPLES = [dict(head=[1, 2, 3, 4]), dict(head=[1, 2, 3, 4, 5])]


def to_args(case):
    return dict(head=build_list(case["head"]))


def from_result(res):
    return list_values(res)


def edge_cases():
    return [dict(head=[]), dict(head=[1]), dict(head=[1, 2]), dict(head=[1, 2, 3]), dict(head=[7, 7, 7, 7, 7, 7])]


def random_case(rng):
    return dict(head=[rng.randint(0, 99) for _ in range(rng.randint(0, 11))])


def perf_case(rng):
    return dict(head=[rng.randint(-10**9, 10**9) for _ in range(100000)])


def valid(c):
    """Does this input satisfy the stated constraints?"""
    return size(c['head'], 0, 10**5) and ints(c['head'], -10**9, 10**9)
