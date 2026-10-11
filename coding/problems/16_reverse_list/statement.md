# 16. Reverse a Linked List

**Difficulty:** easy · **Topic:** linked lists

Reverse a singly linked list and return the new head.

`ListNode` has fields `val` and `next` (see `lib.py`). The examples show
lists as Python lists; the judge builds the nodes for you.

## Function

```python
def reverse_list(head: Optional[ListNode]) -> Optional[ListNode]:
```

## Constraints

- `0 <= number of nodes <= 10**5`
- `-10**9 <= val <= 10**9`
- Python's default recursion limit is 1000, so a recursive solution fails on long lists.

## Examples

**Example 1**

```
Input:  head = [1, 2, 3, 4]
Output: [4, 3, 2, 1]
```

**Example 2**

```
Input:  head = []
Output: []
```

## Run

```
python judge.py 16
```
