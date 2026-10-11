# 20. Level-by-Level Report

**Difficulty:** medium · **Topic:** trees (BFS/DFS)

Return the node values level by level, from top to bottom, each level read
left to right. An empty tree gives `[]`.

## Function

```python
def level_order(root: Optional[TreeNode]) -> list[list[int]]:
```

## Constraints

- `0 <= number of nodes <= 10**5`

## Examples

**Example 1**

```
Input:  root = [3, 9, 20, None, None, 15, 7]
Output: [[3], [9, 20], [15, 7]]
```

**Example 2**

```
Input:  root = [1, 2, None, 3]
Output: [[1], [2], [3]]
```

## Run

```
python judge.py 20
```
