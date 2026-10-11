from gentools import grid, ints, nondecreasing, size, tree  # noqa: F401
from lib import build_list, list_values

ID = 17
TITLE = "Merge Two Sorted Lists"
LEVEL = "easy"
TOPIC = "linked lists"
FUNC = "merge_lists"
IMPORTS = "from typing import Optional\nfrom lib import ListNode"
SIGNATURE = "def merge_lists(a: Optional[ListNode], b: Optional[ListNode]) -> Optional[ListNode]:"
STATEMENT = """
`a` and `b` are linked lists sorted in non-decreasing order. Merge them into
one sorted list by relinking the existing nodes, and return its head.
"""
CONSTRAINTS = """
- `0 <= nodes in each list <= 5 * 10**4`
- `-10**9 <= val <= 10**9`
- Python's default recursion limit is 1000.
"""
EXAMPLES = [dict(a=[1, 5, 9], b=[2, 2, 10]), dict(a=[], b=[0])]


def to_args(case):
    return dict(a=build_list(case["a"]), b=build_list(case["b"]))


def from_result(res):
    return list_values(res)


def edge_cases():
    return [dict(a=[], b=[]), dict(a=[1], b=[]), dict(a=[5], b=[1, 2, 3]), dict(a=[1, 1], b=[1, 1]),
            dict(a=[-3, 0], b=[-5, 10**9])]


def random_case(rng):
    return dict(a=sorted(rng.randint(-5, 5) for _ in range(rng.randint(0, 8))),
                b=sorted(rng.randint(-5, 5) for _ in range(rng.randint(0, 8))))


def perf_case(rng):
    return dict(a=sorted(rng.randint(-10**9, 10**9) for _ in range(50000)),
                b=sorted(rng.randint(-10**9, 10**9) for _ in range(50000)))


def valid(c):
    """Does this input satisfy the stated constraints?"""
    return all(size(c[k], 0, 5 * 10**4) and nondecreasing(c[k]) and ints(c[k], -10**9, 10**9) for k in ('a', 'b'))
