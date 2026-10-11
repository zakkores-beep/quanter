# 21. Validate a Search Tree

**Difficulty:** medium · **Topic:** trees (BFS/DFS)

Return `True` if the tree is a valid binary search tree: for **every** node,
all values in its left subtree are strictly smaller and all values in its
right subtree are strictly larger. An empty tree is valid.

## Function

```python
def is_valid_bst(root: Optional[TreeNode]) -> bool:
```

## Constraints

- `0 <= number of nodes <= 10**5`
- `-2**31 <= val <= 2**31 - 1`

## Examples

**Example 1**

```
Input:  root = [2, 1, 3]
Output: True
```

**Example 2**

```
Input:  root = [10, 5, 15, None, None, 6, 20]
Output: False
```

## Run

```
python judge.py 21
```
