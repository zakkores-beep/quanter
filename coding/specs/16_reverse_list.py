from gentools import grid, ints, nondecreasing, size, tree  # noqa: F401
from lib import build_list, list_values

ID = 16
TITLE = "Reverse a Linked List"
LEVEL = "easy"
TOPIC = "linked lists"
FUNC = "reverse_list"
IMPORTS = "from typing import Optional\nfrom lib import ListNode"
SIGNATURE = "def reverse_list(head: Optional[ListNode]) -> Optional[ListNode]:"
STATEMENT = """
Reverse a singly linked list and return the new head.

`ListNode` has fields `val` and `next` (see `lib.py`). The examples show
lists as Python lists; the judge builds the nodes for you.
"""
CONSTRAINTS = """
- `0 <= number of nodes <= 10**5`
- `-10**9 <= val <= 10**9`
- Python's default recursion limit is 1000, so a recursive solution fails on long lists.
"""
EXAMPLES = [dict(head=[1, 2, 3, 4]), dict(head=[])]


def to_args(case):
    return dict(head=build_list(case["head"]))


def from_result(res):
    return list_values(res)


def edge_cases():
    return [dict(head=[]), dict(head=[1]), dict(head=[1, 2]), dict(head=[5, 5, 5]), dict(head=[-10**9, 10**9])]


def random_case(rng):
    return dict(head=[rng.randint(-9, 9) for _ in range(rng.randint(0, 10))])


def perf_case(rng):
    return dict(head=[rng.randint(-10**9, 10**9) for _ in range(100000)])


def valid(c):
    """Does this input satisfy the stated constraints?"""
    return size(c['head'], 0, 10**5) and ints(c['head'], -10**9, 10**9)
