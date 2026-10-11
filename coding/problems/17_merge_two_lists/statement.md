# 17. Merge Two Sorted Lists

**Difficulty:** easy · **Topic:** linked lists

`a` and `b` are linked lists sorted in non-decreasing order. Merge them into
one sorted list by relinking the existing nodes, and return its head.

## Function

```python
def merge_lists(a: Optional[ListNode], b: Optional[ListNode]) -> Optional[ListNode]:
```

## Constraints

- `0 <= nodes in each list <= 5 * 10**4`
- `-10**9 <= val <= 10**9`
- Python's default recursion limit is 1000.

## Examples

**Example 1**

```
Input:  a = [1, 5, 9], b = [2, 2, 10]
Output: [1, 2, 2, 5, 9, 10]
```

**Example 2**

```
Input:  a = [], b = [0]
Output: [0]
```

## Run

```
python judge.py 17
```
