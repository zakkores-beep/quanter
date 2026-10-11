# 19. Depth of a Binary Tree

**Difficulty:** easy · **Topic:** trees (BFS/DFS)

Return the number of nodes on the longest path from the root down to a leaf.
An empty tree has depth 0.

`TreeNode` has fields `val`, `left`, `right` (see `lib.py`). Trees are shown
in level order with `None` for a missing child; the judge builds the nodes.

## Function

```python
def max_depth(root: Optional[TreeNode]) -> int:
```

## Constraints

- `0 <= number of nodes <= 10**5`

## Examples

**Example 1**

```
Input:  root = [3, 9, 20, None, None, 15, 7]
Output: 3
```

**Example 2**

```
Input:  root = [1, None, 2]
Output: 2
```

## Run

```
python judge.py 19
```
