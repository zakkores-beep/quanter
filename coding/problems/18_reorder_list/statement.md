# 18. Interleave a Linked List

**Difficulty:** medium · **Topic:** linked lists

Given the list `L0 -> L1 -> ... -> Ln`, rearrange the nodes into
`L0 -> Ln -> L1 -> Ln-1 -> L2 -> Ln-2 -> ...` and return the head.

Relink the nodes; do not just change values. Aim for O(1) extra space
(find the middle, reverse the second half, merge).

## Function

```python
def reorder(head: Optional[ListNode]) -> Optional[ListNode]:
```

## Constraints

- `0 <= number of nodes <= 10**5`
- `-10**9 <= val <= 10**9`

## Examples

**Example 1**

```
Input:  head = [1, 2, 3, 4]
Output: [1, 4, 2, 3]
```

**Example 2**

```
Input:  head = [1, 2, 3, 4, 5]
Output: [1, 5, 2, 4, 3]
```

## Run

```
python judge.py 18
```
